import argparse
from pathlib import Path

import numpy as np

from BMLImage import BMLImage

C0: np.typing.NDArray[np.uint8] = np.array([255, 255, 255], dtype=np.uint8)
C1: np.typing.NDArray[np.uint8] = np.array([49, 99, 206], dtype=np.uint8)
C2: np.typing.NDArray[np.uint8] = np.array([214, 69, 65], dtype=np.uint8)

SCENARIOS: dict[str, float] = {
    "free_flow": 0.2,
    "jam": 0.6,
}


def render(width: int, height: int, probability: float, seed: int, steps: int, pixel: int) -> BMLImage:
    bmli: BMLImage = BMLImage(
        width=width,
        height=height,
        probability=probability,
        seed=seed,
        c0=C0,
        c1=C1,
        c2=C2,
        pixel=pixel,
    )
    for _ in range(steps):
        bmli.next()
    return bmli


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--width", type=int, default=128)
    parser.add_argument("--height", type=int, default=128)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--steps", type=int, default=300)
    parser.add_argument("--pixel", type=int, default=4)
    args: argparse.Namespace = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, probability in SCENARIOS.items():
        bmli: BMLImage = render(args.width, args.height, probability, args.seed, args.steps, args.pixel)
        bmli.image_pil().save(args.output_dir / f"{name}.png")
    return None


if __name__ == "__main__":
    main()
