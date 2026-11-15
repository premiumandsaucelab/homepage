#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PS:LAB 홈페이지 — 잠금 검사기 (check_locks.py)

용도
  1) snapshot : 넘기기 직전 상태를 baseline.json 에 기록한다. (전동훈이 실행)
  2) check    : 지금 폴더가 baseline 에서 무엇이 달라졌는지, 금지 표현이 되살아났는지 검사한다.
                (CEO 쪽에서 반환 직전 / 전동훈이 회수 직후, 양쪽 다 실행)

실행
  python _handover/check_locks.py snapshot
  python _handover/check_locks.py check

git 없이도 돌아간다. 표준 라이브러리만 쓴다. Python 3.8 이상.
"""

import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASELINE = os.path.join(ROOT, "_handover", "baseline.json")

# 검사에서 통째로 건너뛸 경로.
# 배포에 안 들어가는 작업용 폴더가 생기면 여기 이름을 추가한다.
SKIP_DIRS = {".git", ".agents", "_handover", "_local", "node_modules", "__pycache__",
             ".vscode", ".idea", "Claude outputs"}

# 본문 스캔 대상 확장자
TEXT_EXT = {".html", ".htm", ".js", ".css", ".json", ".txt", ".xml", ".md"}

# 금지 표현을 '설명하기 위해' 담고 있는 문서들. 변경 감시는 하되 본문 스캔에서는 뺀다.
SKIP_SCAN = {"AGENTS.md", "CLAUDE.md", "GEMINI.md", "0_먼저_읽어주세요.md"}

# 바이트 단위로 고정. 한 글자라도 바뀌면 BLOCK.
# 법률 검토를 거쳤거나, 바뀌면 배포/도메인이 깨지는 파일들.
BYTE_LOCKED = [
    "privacy.html",
    "terms.html",
    "CNAME",
    ".nojekyll",
]

# 금지 표현 목록과 예외 목록은 공개 저장소에 두지 않는다.
# 로컬 전용 파일 _local/forbidden.json (.gitignore 대상) 에서 읽는다.
#   forbidden: [{"pattern": 정규식, "why": 설명}, ...]  — 검색 결과가 0건이어야 하는 표현
#   allowed:   [{"text": 찾은 문자열, "file": 파일경로, "reason": 이유}, ...]  — 의도적으로 허용한 것
LOCAL_LIST = os.path.join(ROOT, "_local", "forbidden.json")


def load_local_list():
    """(FORBIDDEN, ALLOWED) 를 돌려준다. 파일이 없으면 None."""
    if not os.path.exists(LOCAL_LIST):
        return None
    with open(LOCAL_LIST, encoding="utf-8") as f:
        data = json.load(f)
    forbidden = [(item["pattern"], item["why"]) for item in data["forbidden"]]
    allowed = {(item["text"], item["file"]) for item in data.get("allowed", [])}
    return forbidden, allowed


KST = timezone(timedelta(hours=9))


def walk_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT).replace("\\", "/")
            yield rel, full


def sha256(path):
    """텍스트 파일은 줄바꿈(CRLF/LF)을 통일한 뒤 해시한다.

    이게 없으면 Windows에서 체크아웃한 파일과 ZIP에서 푼 파일의 해시가 전부 달라져서
    아무것도 안 고쳤는데 모든 파일이 '변경'으로 뜬다."""
    with open(path, "rb") as f:
        raw = f.read()
    if os.path.splitext(path)[1].lower() in TEXT_EXT:
        raw = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(raw).hexdigest()


def read_text(path):
    with open(path, "rb") as f:
        raw = f.read()
    for enc in ("utf-8", "cp949", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return ""


def cmd_snapshot():
    files = {}
    for rel, full in walk_files():
        files[rel] = sha256(full)
    data = {
        "created_kst": datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S"),
        "commit": os.environ.get("PSLAB_BASE_COMMIT", ""),
        "file_count": len(files),
        "files": files,
    }
    os.makedirs(os.path.dirname(BASELINE), exist_ok=True)
    with open(BASELINE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1, sort_keys=True)
    print("[OK] baseline 기록 완료: %d개 파일" % len(files))
    print("     %s" % BASELINE)
    if not data["commit"]:
        print("[안내] 커밋 해시를 같이 박으려면 먼저:")
        print("       $env:PSLAB_BASE_COMMIT = (git rev-parse --short HEAD)")
    return 0


def cmd_check():
    problems = 0

    loaded = load_local_list()
    if loaded is None:
        print("로컬 금지 목록 파일 없음, 대표 PC에서 실행하세요")
        print("     (찾은 위치: %s)" % LOCAL_LIST)
        print()
        print("결과: 실패.")
        return 1
    FORBIDDEN, ALLOWED = loaded

    # 1) 금지 표현 — 같은 표현은 한 덩어리로 묶어서 보고한다.
    #    한 줄에 두 번 나오는 경우(mailto 링크 + 화면 표시)가 흔해서
    #    건별로 찍으면 줄 수만 불어나고 무엇을 고쳐야 하는지가 안 보인다.
    groups = {}   # (why, 찾은문자열) -> {파일: [줄번호]}
    allowed_hits = {}
    total = 0
    for rel, full in walk_files():
        if os.path.splitext(rel)[1].lower() not in TEXT_EXT:
            continue
        if os.path.basename(rel) in SKIP_SCAN:
            continue
        text = read_text(full)
        if not text:
            continue
        for pat, why in FORBIDDEN:
            for m in re.finditer(pat, text):
                line = text.count("\n", 0, m.start()) + 1
                frag = m.group(0)[:60].replace("\n", " ")
                if (frag, rel) in ALLOWED:
                    allowed_hits.setdefault((frag, rel), []).append(line)
                    continue
                groups.setdefault((why, frag), {}).setdefault(rel, []).append(line)
                total += 1

    print("=" * 64)
    print("1. 금지 표현 검사")
    print("=" * 64)
    if not groups:
        print("[OK] 0건")
    else:
        problems += len(groups)
        for (why, frag), byfile in sorted(groups.items()):
            print("[BLOCK] %s" % why)
            hit_count = sum(len(v) for v in byfile.values())
            print('        "%s"  —  %d곳 / %d개 파일' % (frag, hit_count, len(byfile)))
            for rel in sorted(byfile):
                lines = ",".join(str(x) for x in sorted(set(byfile[rel])))
                print("        %s:%s" % (rel, lines))
            print()
        print("고쳐야 할 종류: %d가지 (총 %d곳)" % (len(groups), total))

    if allowed_hits:
        print()
        for (frag, rel), lines in sorted(allowed_hits.items()):
            ln = ",".join(str(x) for x in sorted(set(lines)))
            print('[허용됨] "%s"  %s:%s  — ALLOWED 에 등록된 의도적 노출' % (frag, rel, ln))

    # 2) baseline 대조
    print()
    print("=" * 64)
    print("2. baseline 대조")
    print("=" * 64)
    if not os.path.exists(BASELINE):
        print("[SKIP] baseline.json 이 없다. 먼저 snapshot 을 돌려야 대조가 된다.")
        print()
        return 1 if problems else 0

    with open(BASELINE, encoding="utf-8") as f:
        base = json.load(f)
    old = base["files"]
    new = {rel: sha256(full) for rel, full in walk_files()}

    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    changed = sorted(p for p in (set(old) & set(new)) if old[p] != new[p])

    print("기준: %s  커밋 %s" % (base.get("created_kst", "?"), base.get("commit") or "(미기록)"))
    print()

    locked_broken = [p for p in changed + removed if p in BYTE_LOCKED]
    if locked_broken:
        problems += len(locked_broken)
        for p in locked_broken:
            print("[BLOCK] 잠긴 파일이 바뀌었다: %s" % p)
        print()

    if not (added or removed or changed):
        print("[OK] 변경 없음. baseline 과 동일하다.")
    else:
        for p in changed:
            mark = "BLOCK" if p in BYTE_LOCKED else "변경"
            print("[%s] %s" % (mark, p))
        for p in added:
            print("[추가] %s" % p)
        for p in removed:
            mark = "BLOCK" if p in BYTE_LOCKED else "삭제"
            print("[%s] %s" % (mark, p))
        print()
        print("-> 위 목록만 검토하면 된다. 나머지 파일은 손대지 않았다.")

    print()
    print("=" * 64)
    if problems:
        print("결과: BLOCK %d건. 이 상태로 반환/배포하지 말 것." % problems)
        return 1
    print("결과: 통과.")
    return 0


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        if arg == "snapshot":
            return cmd_snapshot()
        if arg == "check":
            return cmd_check()
        print(__doc__)
        return 2
    except BrokenPipeError:
        # 출력을 head 같은 데로 넘겼을 때 나는 것. 검사 실패가 아니다.
        try:
            sys.stdout.close()
        except Exception:
            pass
        return 0


if __name__ == "__main__":
    sys.exit(main())
