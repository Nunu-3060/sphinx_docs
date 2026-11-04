"""CPU バウンドな計算を一括して処理するケーススタディ（ProcessPoolExecutor）。

マンデルブロ集合の画像を行ごとに計算する。行どうしは互いに依存しないため、プロセスに分けて並列に計算できる。
結果は PGM 形式（白黒の画像形式）で mandelbrot.pgm に保存する。
"""

import os
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

WIDTH = 800
HEIGHT = 600
MAX_ITERATIONS = 200


def compute_row(y: int) -> bytes:
    """y 行目の各画素について、発散するまでの反復回数を明るさ（0〜255）に変換して返す。"""
    imaginary = (y / HEIGHT) * 2.4 - 1.2
    row = bytearray(WIDTH)
    for x in range(WIDTH):
        c = complex((x / WIDTH) * 3.2 - 2.2, imaginary)
        z = 0j
        iterations = 0
        while abs(z) <= 2.0 and iterations < MAX_ITERATIONS:
            z = z * z + c
            iterations += 1
        row[x] = 255 - iterations * 255 // MAX_ITERATIONS
    return bytes(row)


def save_pgm(path: Path, rows: list[bytes]) -> None:
    header = f"P5\n{WIDTH} {HEIGHT}\n255\n".encode("ascii")
    path.write_bytes(header + b"".join(rows))


def main() -> None:
    start = time.perf_counter()
    rows = [compute_row(y) for y in range(HEIGHT)]
    print(f"逐次: {time.perf_counter() - start:.2f} 秒")

    start = time.perf_counter()
    with ProcessPoolExecutor() as executor:
        # 1 行ずつ送ると受け渡しの回数が増えるため、chunksize でまとめて送る
        chunksize = max(1, HEIGHT // ((os.cpu_count() or 1) * 4))
        parallel_rows = list(executor.map(compute_row, range(HEIGHT), chunksize=chunksize))
    print(f"プロセス: {time.perf_counter() - start:.2f} 秒 (chunksize={chunksize})")

    assert parallel_rows == rows
    output = Path("mandelbrot.pgm")
    save_pgm(output, parallel_rows)
    print(f"{output.resolve()} に保存した")


if __name__ == "__main__":
    main()
