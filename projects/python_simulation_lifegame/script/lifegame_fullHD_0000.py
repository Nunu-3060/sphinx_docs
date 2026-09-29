from pathlib import Path

import numpy as np
from PIL import Image

from LifeGame import LifeGame
from utility import hsv2rgb


def main() -> None:
    # config
    pixel: int = 4
    n0: int = 256
    n1: int = 256
    width: int = 1920 // pixel
    height: int = 1080 // pixel
    # calculation
    lg: LifeGame = LifeGame(width=width, height=height)
    lattice: np.typing.NDArray[np.int64] = np.zeros_like(lg.lattice)
    for _ in range(n0):
        lg.next()
    for _ in range(n1):
        lg.next()
        lattice += lg.lattice
    # output
    rng: np.random.Generator = np.random.default_rng()
    im: Image.Image = Image.fromarray(hsv2rgb(
        np.full(lattice.shape, rng.random(), np.float64),
        np.full(lattice.shape, 0.875, np.float64),
        lattice.astype(np.float64) / n1,
    )).resize((width*pixel, height*pixel), resample=Image.Resampling.NEAREST)
    im.save(Path(__file__).resolve().with_suffix(".png"))
    return None


if __name__ == "__main__":
    main()
