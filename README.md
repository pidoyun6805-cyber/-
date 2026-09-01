# -
## 학교 강의 알림 (2026-09-01 추가)

옵시디언 볼트(`doyun-vault` 리포)의 `학교/과목/*.md` 진행도 체크박스를 매일 아침 스캔해
① 이번 주 새로 열린 강의 ② 마감 D-3 이내인데 미체크 강의를 텔레그램으로 알린다.

- `.github/scripts/school_check.py <볼트경로> [기준일]` → 알림 텍스트 생성(없으면 빈 출력)
- 클라우드 routine 이 매일 아침 볼트를 clone → 위 스크립트 실행 → 출력 있으면 `school/<날짜>.md` 커밋
- push(school/**) 시 `.github/workflows/school-telegram.yml` 이 `@kdeng_news_bot`(chat_id 7697652808)으로 전송
- 판단 기준 = 옵시디언 체크박스(강의 들으면 과목노트에서 `- [x]` 체크). 실제 KCU/OCU 출석은 클라우드가 못 봄.
