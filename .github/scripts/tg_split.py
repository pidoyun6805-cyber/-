#!/usr/bin/env python3
# 학교 알림 md 를 3500바이트씩 줄 단위로 잘라 parts/NN.txt 로 저장. 통 수를 stdout 으로 출력.
import sys, os

text = open(sys.argv[1], encoding="utf-8").read().strip()
os.makedirs("parts", exist_ok=True)
buf, n, size = [], 0, 0


def flush():
    global buf, n
    if buf:
        n += 1
        with open(f"parts/{n:02d}.txt", "w", encoding="utf-8") as fp:
            fp.write("\n".join(buf))
        buf = []


for line in text.split("\n"):
    b = len(line.encode("utf-8")) + 1
    if size + b > 3500 and buf:
        flush()
        size = 0
    buf.append(line)
    size += b
flush()
print(n)
