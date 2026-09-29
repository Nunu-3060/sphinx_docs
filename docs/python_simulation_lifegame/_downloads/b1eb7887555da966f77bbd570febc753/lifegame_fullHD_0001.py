import time

from LifeGame import LifeGame as LGn
from LifeGame_scipy import LifeGame as LGs


def calculation(lg: LGn | LGs) -> float:
    start: float = time.perf_counter()
    for _ in range(256):
        lg.next()
    end: float = time.perf_counter()
    return end - start


def main() -> None:
    print("Processing speed comparison")
    for pixel in [4, 2, 1]:
        width: int = 1920 // pixel
        height: int = 1080 // pixel
        print("\n".join([
            42*"=",
            f"width: {width:>4}, height: {height:>4}",
            42*"=",
        ]))
        for _ in range(4):
            lap_n: float = calculation(LGn(width=width, height=height))
            lap_s: float = calculation(LGs(width=width, height=height))
            result: str = "numpy" if lap_n < lap_s else "scipy"
            print(f"result: {result}, numpy : {lap_n:.2f}, scipy: {lap_s:.2f}")
    return None


if __name__ == "__main__":
    main()
