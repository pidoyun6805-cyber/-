# 위스키 브리핑

클라우드 루틴이 매일 아침 `whisky/YYYY-MM-DD.md` 를 커밋하면
`.github/workflows/whisky-telegram.yml` 이 텔레그램(뉴스 개인방)으로 보낸다.
서식 변환은 뉴스 브리핑과 같은 `tg_format.py` 를 쓴다 (표는 라벨 블록으로 펼침).
