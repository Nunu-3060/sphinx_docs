import numpy as np


class Sand:
    def __init__(
        self,
        width: int = 128,
        height: int = 128,
        L0: float = 2,
        b: float = 4,
        q: float = 0.1,
        D: float = 0.2,
        seed: int | None = None
    ) -> None:
        rng: np.random.Generator = np.random.default_rng(seed)
        self.height: np.typing.NDArray[np.float64] = rng.random((height, width), np.float64)
        self.L0: float = L0
        self.b: float = b
        self.q: float = q
        self.D: float = D
        return None

    def next(self) -> None:
        height: int
        width: int
        height, width = self.height.shape
        length: np.typing.NDArray[np.int64] = (self.L0 + self.b * self.height).round(0).astype(np.int64)
        dest: np.typing.NDArray[np.int64] = (np.arange(width, dtype=np.int64)[None, :] - length) % width
        d: np.typing.NDArray[np.float64] = np.full(self.height.shape, -self.q)
        rows: np.typing.NDArray[np.int64] = np.repeat(np.arange(height, dtype=np.int64), width)
        np.add.at(d, (rows, dest.ravel()), self.q)
        self.height += d
        # 可読性のために PEP8 に違反した書き方をしている。
        self.height = self.height * (1-self.D) + (
            np.roll(self.height, shift=( 1,  0), axis=(0, 1)) +  # noqa: E201
            np.roll(self.height, shift=(-1,  0), axis=(0, 1)) +  # noqa: E201
            np.roll(self.height, shift=( 0,  1), axis=(0, 1)) +  # noqa: E201
            np.roll(self.height, shift=( 0, -1), axis=(0, 1))    # noqa: E201
        ) * self.D / 6 + (
            np.roll(self.height, shift=( 1,  1), axis=(0, 1)) +  # noqa: E201
            np.roll(self.height, shift=( 1, -1), axis=(0, 1)) +  # noqa: E201
            np.roll(self.height, shift=(-1,  1), axis=(0, 1)) +  # noqa: E201
            np.roll(self.height, shift=(-1, -1), axis=(0, 1))    # noqa: E201
        ) * self.D / 12
        return None
