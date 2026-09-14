"""도면 크롭 — 내용 bounding box 로 잘라 도면 고유 비율을 지킨다(임시 구현 · 2026-09-14).

**엔진 경로가 아니다.** 현행 계약은 `figures.render-spec` 으로 1200×675 @2x 를 강제하며(SPEC §6.6
「16:9 피드 안전 크롭」), 그 고정 비율이 세로형 도면을 캔버스 면적의 1/8 로 줄인다는 것이 런 -3 에서
드러났다(도면 7 중 4 가 비율 0.70~0.85). 판정 기준 변경은 재정 사항이므로(규율 11) 이 파일은 **게시본을
손으로 다듬는 데 쓴 도구**를 보존한 것이고, HANDOFF §0-A ⑵ 의 개선 착수점이다.

하는 일 — 행/열 잉크 프로파일로 띠를 나누고, 가장 큰 띠를 도면 본체로 본다. 시트 맨 아래 띠는 페이지
번호이므로 버리고 그 앞 띠(있으면)를 `FIG.` 라벨로 함께 취한다. 공보 머리글은 본체 위라 자연히 빠진다.

    python3 studio/tools/crop_figures.py <입력 디렉터리> <출력 디렉터리> [긴 변 픽셀]
"""

from __future__ import annotations

import glob
import os
import sys

from PIL import Image

INK = 200          # 이 값보다 어두우면 잉크로 본다
SAMPLE = 2         # 가로 표본 간격 — 전수 주사는 불필요하다
PAD_RATIO = 0.04   # 내용 기준 여백
DEFAULT_LONG_EDGE = 2048


def _runs(flags: list[bool], gap: int) -> list[tuple[int, int]]:
    """`gap` 이상 비어 있으면 끊어 [(시작, 끝)] 구간으로 만든다."""
    out: list[tuple[int, int]] = []
    start: int | None = None
    blank = 0
    for i, value in enumerate(flags):
        if value:
            if start is None:
                start = i
            blank = 0
        elif start is not None:
            blank += 1
            if blank >= gap:
                out.append((start, i - blank))
                start, blank = None, 0
    if start is not None:
        out.append((start, len(flags) - 1))
    return out


def content_box(path: str) -> tuple[int, int, int, int]:
    grey = Image.open(path).convert("L")
    width, height = grey.size
    pixels = grey.load()

    row_ink = [False] * height
    for y in range(height):
        for x in range(0, width, SAMPLE):
            if pixels[x, y] < INK:
                row_ink[y] = True
                break
    rows = [r for r in _runs(row_ink, int(height * 0.03)) if r[1] - r[0] > 4]
    if not rows:
        return (0, 0, width, height)

    main = max(rows, key=lambda r: r[1] - r[0])
    below = [r for r in rows if r[0] > main[1]]
    labels = below[:-1] if below else []      # 마지막 띠 = 시트 하단 페이지 번호
    if labels:
        main = (main[0], labels[-1][1])
    body_height = main[1] - main[0]

    col_ink = [False] * width
    for y in range(main[0], main[1] + 1):
        for x in range(0, width, SAMPLE):
            if pixels[x, y] < INK:
                col_ink[x] = True
    cols = [c for c in _runs(col_ink, int(width * 0.05)) if c[1] - c[0] > 4]
    left, right = cols[0][0], cols[-1][1]

    pad = int(max(body_height, right - left) * PAD_RATIO)
    return (max(0, left - pad), max(0, main[0] - pad),
            min(width, right + pad + 2), min(height, main[1] + pad + 1))


def crop_one(path: str, out_dir: str, long_edge: int) -> tuple[int, int]:
    box = content_box(path)
    image = Image.open(path).convert("RGB").crop(box)
    w, h = image.size
    scale = long_edge / max(w, h)
    image = image.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    os.makedirs(out_dir, exist_ok=True)
    image.save(os.path.join(out_dir, os.path.basename(path)), optimize=True)
    return image.size


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__)
        return 2
    src, dst = argv[1], argv[2]
    long_edge = int(argv[3]) if len(argv) > 3 else DEFAULT_LONG_EDGE
    found = sorted(glob.glob(os.path.join(src, "*.png")))
    if not found:
        print(f"PNG 가 없다: {src}")
        return 1
    for path in found:
        w, h = crop_one(path, dst, long_edge)
        print(f"{os.path.basename(path):14s} {w}x{h}  비율 {w / h:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
