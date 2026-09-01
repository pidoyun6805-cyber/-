#!/usr/bin/env python3
# 볼트의 학교/과목/*.md 를 읽어 강의 알림 메시지를 생성한다.
# 사용: python school_check.py <볼트경로> [기준날짜 YYYY-MM-DD]
import sys, re, glob, os
from datetime import date, datetime, timedelta

vault = sys.argv[1]
today = datetime.strptime(sys.argv[2], "%Y-%m-%d").date() if len(sys.argv) > 2 else date.today()

# 주차 진행도 줄 패턴:
#  - [ ] 2주차 (09/07~09/27) 발음 기제 ... 📅 2026-09-27
LINE = re.compile(r"^\s*-\s*\[( |x|X)\]\s*(\d+)주차\s*\(([\d/]+)~([\d/]+)\)\s*(.*?)(?:📅\s*(\d{4}-\d{2}-\d{2}))?\s*$")

def mmdd(s, year):
    m, d = s.split("/"); return date(year, int(m), int(d))

new_open, due_soon = [], []
for path in sorted(glob.glob(os.path.join(vault, "학교", "과목", "*.md"))):
    txt = open(path, encoding="utf-8").read()
    # 과목명 (frontmatter)
    mo = re.search(r"^과목명:\s*(.+)$", txt, re.M)
    subj = mo.group(1).strip() if mo else os.path.basename(path)[:-3]
    # 인강만 대상
    if "방식: 인강" not in txt and "방식: 인강\r" not in txt:
        continue
    for ln in txt.splitlines():
        m = LINE.match(ln)
        if not m: continue
        done = m.group(1).lower() == "x"
        wk = int(m.group(2))
        try:
            open_d = mmdd(m.group(3), today.year)
            close_d = mmdd(m.group(4), today.year)
        except Exception:
            continue
        topic = re.sub(r"\s*—.*$", "", m.group(5)).strip()
        # ① 이번 주(최근 7일 내)에 새로 열린 강의 & 아직 미수강
        if not done and 0 <= (today - open_d).days <= 6:
            new_open.append((subj, wk, topic, close_d))
        # ② 마감 D-3 이내인데 미수강
        if not done:
            dleft = (close_d - today).days
            if 0 <= dleft <= 3:
                due_soon.append((subj, wk, topic, close_d, dleft))

lines = []
if due_soon:
    lines.append("🚨 <b>마감 임박 — 아직 안 들은 강의</b>")
    for subj, wk, topic, close_d, dleft in sorted(due_soon, key=lambda x: x[4]):
        dd = "오늘 마감!" if dleft == 0 else f"D-{dleft}"
        lines.append(f"▪ [{dd}] {subj} {wk}주차 — {topic} (마감 {close_d.strftime('%m/%d')})")
    lines.append("")
if new_open:
    lines.append("🆕 <b>이번 주 새로 열린 강의</b>")
    for subj, wk, topic, close_d in new_open:
        lines.append(f"▪ {subj} {wk}주차 — {topic} (마감 {close_d.strftime('%m/%d')})")
    lines.append("")

if not lines:
    print("")  # 알릴 것 없음 → 빈 출력 (전송 스킵)
else:
    header = f"🎓 <b>학교 강의 알림</b> · {today.strftime('%m/%d')}\n"
    tail = "\n강의 들으면 옵시디언 과목노트에서 체크 ✅ (누적 30분+학습종료 잊지 말기)"
    print(header + "\n".join(lines).rstrip() + tail)
