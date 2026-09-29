import numpy as np


class BML:
    def __init__(
        self,
        width: int = 256,
        height: int = 256,
        probability: float = 0.6,
        seed: int | None = None,
    ) -> None:
        self.lattice: np.typing.NDArray[np.int64] = np.zeros((height, width), dtype=np.int64)
        rng: np.random.Generator = np.random.default_rng(seed)
        p: np.typing.NDArray[np.float64] = rng.random(size=self.lattice.shape)
        self.lattice[p < probability] = 1
        self.lattice[p < probability * 0.5] = 2
        return None

    def next(self) -> None:
        l0: np.typing.NDArray[np.int64] = np.zeros_like(self.lattice)
        south: np.typing.NDArray[np.int64] = np.roll(self.lattice, shift=(-1, 0), axis=(0, 1))
        north: np.typing.NDArray[np.int64] = np.roll(self.lattice, shift=(1, 0), axis=(0, 1))
        l0[((self.lattice == 0) & (south == 1)) | ((self.lattice == 1) & (north != 0))] = 1
        l0[self.lattice == 2] = 2
        east: np.typing.NDArray[np.int64] = np.roll(l0, shift=(0, -1), axis=(0, 1))
        west: np.typing.NDArray[np.int64] = np.roll(l0, shift=(0, 1), axis=(0, 1))
        l1: np.typing.NDArray[np.int64] = np.zeros_like(self.lattice)
        l1[((l0 == 0) & (west == 2)) | ((l0 == 2) & (east != 0))] = 2
        l1[l0 == 1] = 1
        self.lattice = l1
        return None
