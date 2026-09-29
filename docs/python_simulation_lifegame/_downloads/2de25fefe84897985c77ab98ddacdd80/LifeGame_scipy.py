from collections.abc import Callable

import numpy as np
from scipy.signal import convolve2d


class LifeGame:
    def __init__(
        self,
        rule: list[list[int]] | None = None,
        width: int = 256,
        height: int = 256,
        probability: float = 0.3,
        tb: bool = True,
        lr: bool = True,
    ) -> None:

        if rule is None:
            rule = [[3], [2, 3]]
        self.rule: list[list[int]] = rule

        self.kernel: np.typing.NDArray[np.int64] = np.array([
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1],
        ], dtype=np.int64)

        rng: np.random.Generator = np.random.default_rng()
        self.lattice: np.typing.NDArray[np.int64] = np.zeros((height, width), dtype=np.int64)
        self.lattice[rng.random(size=self.lattice.shape) < probability] = 1

        if not tb:
            def deco(func: Callable[[], None]) -> Callable[[], None]:
                self.lattice[0, :] = 0
                self.lattice[-1, :] = 0

                def tmp() -> None:
                    func()
                    self.lattice[0, :] = 0
                    self.lattice[-1, :] = 0
                    return None
                return tmp
            self.next = deco(self.next)

        if not lr:
            def deco(func: Callable[[], None]) -> Callable[[], None]:
                self.lattice[:, 0] = 0
                self.lattice[:, -1] = 0

                def tmp() -> None:
                    func()
                    self.lattice[:, 0] = 0
                    self.lattice[:, -1] = 0
                    return None
                return tmp
            self.next = deco(self.next)

        return None

    def next(self) -> None:
        neighbour: np.typing.NDArray[np.int64] = convolve2d(
            self.lattice,
            self.kernel,
            mode="same",
            boundary="wrap",
        )
        lattice: np.typing.NDArray[np.int64] = np.zeros_like(self.lattice)
        for i, neighbour_counts in enumerate(self.rule):
            b: np.typing.NDArray[np.bool] = self.lattice == i
            for j in neighbour_counts:
                lattice[b & (neighbour == j)] = 1
        self.lattice = lattice
        return None
