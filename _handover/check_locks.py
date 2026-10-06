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
SKIP_DIRS = {".git", ".agents", "_handover", "node_modules", "__pycache__",
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

# 검색 결과가 0건이어야 하는 표현.
# (정규식, 사람이 읽을 설명) — 설명은 대외 공개돼도 무방한 수준으로만 적는다.
FORBIDDEN = [
    (r"pslabedu@gmail\.com",            "구 이메일. 공식 이메일은 daehyunkoh@pslabedu.kr 하나"),
    (r"[A-Za-z0-9._%+-]+@khu\.ac\.kr",  "학교 개인 이메일. 공개면에는 회사 이메일만 쓴다"),
    (r"[A-Za-z0-9._%+-]+@naver\.com",   "개인 이메일. 공개면에는 회사 이메일만 쓴다"),
    (r"AKfycbylKX",                     "폐기된 접수 폼 URL"),
    (r"AKfycbyUGP",                     "폐기된 접수 폼 URL"),
    (r"무제한",                          "확정 스펙에 없는 표현"),
    (r"30\s*%\s*환급",                   "현재 공개 문구에 없는 표현"),
    (r"합격\s*시\s*[^<>\n]{0,6}환급",      "현재 공개 문구에 없는 표현"),
    (r"선연락",                          "확정 스펙에 없는 표현"),
    (r"장학금\s*(우선|혜택)",             "확정 스펙에 없는 표현"),
    (r"채용\s*우선",                     "확정 스펙에 없는 표현"),
    (r"Director\s*Plan",                "폐기된 상품명"),
    (r"Architect\s*Plan",               "폐기된 상품명"),
    (r"스탠다드\s*기획",                  "폐기된 상품명. 현재 라인업은 Compass·Navigation·Pilot"),
    (r"프리미엄\s*밀착",                  "폐기된 상품명. 현재 라인업은 Compass·Navigation·Pilot"),
    (r"29\s*인",                        "멘토 총원은 28인"),
    (r"재추천\s*(율\s*)?70",             "재추천율은 80%"),
    (r"고려대(학교)?\s*선정",             "확인되지 않은 선정 표기"),
    (r"경희대(학교)?\s*선정",             "확인되지 않은 선정 표기"),
    (r"전동훈[^<>\n]{0,20}CTO",          "전동훈 직책은 CPO"),
    (r"CTO[^<>\n]{0,20}전동훈",          "전동훈 직책은 CPO"),
    (r"(?i)<\s*input[^>]*type\s*=\s*[\"']?file",  "파일 업로드 입력칸. 생기부 업로드 UI는 구현 금지"),
    (r"(?i)(tosspayments|iamport|portone|nicepay|kcp\.co\.kr|stripe\.com/v3)", "결제/PG 연동. 이번 범위 아님"),
    (r"(?i)(AIza[0-9A-Za-z_\-]{30,}|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{30,})", "API 키로 보이는 문자열"),
    (r"01[016789][-.\s]?\d{3,4}[-.\s]?\d{4}", "휴대폰 번호. 공개면에 전화번호는 노출하지 않는다"),
    (r"\d{6}[-\s]?[1-4]\d{6}",          "주민등록번호 형태의 숫자"),
    (r"9월 면접 컨설팅",        "지난 시즌 문구. 면접 팝업은 '피에스랩 면접 컨설팅 / 현재 접수 중'"),
    (r"사전예약 오픈",          "지난 시즌 문구. 현재는 접수 중 상태"),
    (r"정식 런칭을 진행합니다",  "런칭 전 문구. 이미 운영 중"),
    (r"런칭 기념 혜택가",       "런칭 전 문구. 가격은 플랜&가격 참조로 대체"),
    (r"무료 신청이란 무엇인가요", "구 FAQ 문구. 현재는 '상담 신청이란 무엇인가요'"),
]

# 검사에 걸리지만 의도적으로 남겨둔 것. (찾은 문자열, 파일경로) 가 여기 있으면 BLOCK 하지 않고
# 맨 아래에 '허용됨'으로만 표시한다.
#
# 왜 지우지 않고 예외로 두나: 규칙을 통째로 빼버리면 같은 번호가 엉뚱한 페이지에 새로 생겨도
# 아무도 모른다. 파일을 못 박아두면 '여기까지는 의도, 그 밖은 사고'가 구분된다.
# 예외를 새로 넣을 때는 왜 허용하는지 옆에 한 줄 적을 것.
ALLOWED = {
    # 학원 원장 대상 B2B 페이지의 직통 연락처. 공개 노출을 감수하기로 판단함.
    ("010-5435-2019", "b2b_partnership_proposal.html"),
    ("010-5435-2019", "songpa_b2b_partnership_proposal.html"),
}

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
