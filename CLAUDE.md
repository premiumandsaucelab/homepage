# CLAUDE.md

작업 규칙은 저장소 루트의 `AGENTS.md` 에 전부 있다. 세션 시작 시 그 파일을 읽고 그대로 따른다.

요약하면: 여기는 pslabedu.kr 의 배포 소스이고 빌드가 없어서 파일이 곧 라이브다.
커밋·푸시하지 않고, `privacy.html` / `terms.html` / `CNAME` / `.nojekyll` 을 건드리지 않고,
요금·멘토 수·문구 같은 확정값은 지시에 없으면 그대로 두고,
끝내기 전에 `python _handover/check_locks.py check` 를 돌린다.
