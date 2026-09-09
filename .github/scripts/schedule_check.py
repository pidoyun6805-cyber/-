#!/usr/bin/env python3
"""schedule/일정.md 를 읽어 오늘 보낼 일정 알림 메시지를 만든다.

한 줄에 일정 하나. 형식:
    2026-09-15 무역정책론 과제 마감
    2026-09-20 18:00 아버지 생신 저녁
'#' 로 시작하는 줄과 빈 줄은 무시한다.

알림 시점은 D-7, D-1, 당일. 보낼 게 있으면 메시지를 stdout 으로 내고 0,
없으면 아무것도 내지 않고 9 로 끝낸다.
"""
import html
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

KST = timezone(timedelta(hours=9))  # 한국은 서머타임이 없어 고정 오프셋으로 충분하다
SOURCE = Path("schedule/일정.md")
OFFSETS = {0: "오늘", 1: "내일", 7: "일주일 뒤"}
LINE = re.compile(r"^(\d{4}-\d{2}-\d{2})\s+(?:(\d{1,2}:\d{2})\s+)?(.+?)\s*$")


def parse(path):
    events, bad = [], []
    for no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = LINE.match(line)
        if not m:
            bad.append((no, line))
            continue
        day, time, what = m.groups()
        try:
            date = datetime.strptime(day, "%Y-%m-%d").date()
        except ValueError:
            bad.append((no, line))
            continue
        events.append((date, time, what))
    return events, bad


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    if not SOURCE.exists():
        print(f"{SOURCE} 가 없습니다.", file=sys.stderr)
        return 9

    today = datetime.now(KST).date()
    events, bad = parse(SOURCE)
    for no, line in bad:
        print(f"{SOURCE}:{no} 형식을 못 읽었습니다: {line}", file=sys.stderr)

    due = {}
    for date, time, what in events:
        delta = (date - today).days
        if delta in OFFSETS:
            due.setdefault(delta, []).append((date, time, what))

    if not due:
        print(f"오늘({today}) 보낼 일정이 없습니다. 등록된 일정 {len(events)}건.", file=sys.stderr)
        return 9

    out = [f"🗓 <b>일정 알림</b> · {today.month}월 {today.day}일"]
    for delta in sorted(due):
        out.append("")
        out.append(f"<b>{OFFSETS[delta]}</b>")
        for date, time, what in sorted(due[delta], key=lambda e: (e[0], e[1] or "")):
            when = f"{date.month}/{date.day}"
            if time:
                when += f" {time}"
            out.append(f"▪ {when} · {html.escape(what)}")

    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
