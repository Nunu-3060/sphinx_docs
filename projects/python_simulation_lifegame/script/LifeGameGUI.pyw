import random
import tkinter as tk
from tkinter import ttk

from FrameLifeGame import FrameLifeGame
from LifeGameImage import LifeGameImage
from TkWidget import DISPLAY_SIZE, FrameCheckbuttons, FrameHSV, FrameLoop, FrameRadioButton, FrameScale


class LifeGameGUI(ttk.Frame):
    def __init__(self, master: tk.Misc | None = None) -> None:
        super().__init__(master)
        # lifegame window
        self.top: tk.Toplevel | None = None
        # parts
        self.frame: dict[str, ttk.Frame] = {
            "color": ttk.Frame(self),
            "rule": ttk.Frame(self),
            "loop": ttk.Frame(self),
            "button": ttk.Frame(self),
        }
        self.color: dict[str, FrameHSV] = {
            "live": FrameHSV(self.frame["color"], text="live"),
            "dead": FrameHSV(self.frame["color"], text="dead"),
        }
        self.rule: dict[str, FrameCheckbuttons] = {
            "birth": FrameCheckbuttons(self.frame["rule"], text="birth"),
            "survive": FrameCheckbuttons(self.frame["rule"], text="survive"),
        }
        self.loop: FrameLoop = FrameLoop(self.frame["loop"])
        self.size_selector: FrameRadioButton = FrameRadioButton(self.frame["loop"])
        self.scale: FrameScale = FrameScale(self.frame["loop"])
        self.button: dict[str, ttk.Button] = {
            "start": ttk.Button(self.frame["button"], text="start", state=tk.ACTIVE, command=self.start),
            "stop": ttk.Button(self.frame["button"], text="stop", state=tk.DISABLED, command=self.stop),
            "reset": ttk.Button(self.frame["button"], text="reset", state=tk.ACTIVE, command=self.set_rule),
            "color": ttk.Button(self.frame["button"], text="color", state=tk.ACTIVE, command=self.set_color),
        }
        # pack
        for frame in self.frame.values():
            frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        for color in self.color.values():
            color.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        for rule in self.rule.values():
            rule.pack(side=tk.LEFT, fill=tk.BOTH)
        self.loop.pack(side=tk.TOP, fill=tk.BOTH)
        self.size_selector.pack(side=tk.TOP, fill=tk.BOTH)
        self.scale.pack(side=tk.TOP, fill=tk.BOTH)
        for button in self.button.values():
            button.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # set
        self.set_rule()
        self.set_color()
        return None

    def set_rule(self) -> None:
        self.rule["birth"].set([3])
        self.rule["survive"].set([2, 3])
        self.loop.set(tb=True, lr=True)
        self.size_selector.set(DISPLAY_SIZE // 2)
        self.scale.set(0.3)
        return None

    def set_color(self) -> None:
        hue: float = random.random()
        saturation: float = 0.875
        value: float = 0.875
        self.color["live"].set(hue, saturation, value)
        self.color["dead"].set(hue, saturation, 1-value)
        return None

    def start(self) -> None:
        self.button["start"].configure(state=tk.DISABLED)
        self.button["stop"].configure(state=tk.ACTIVE)
        # config
        loop: dict[str, bool] = self.loop.get()
        wh: int = self.size_selector.get()
        pixel: int = DISPLAY_SIZE // wh
        lgi: LifeGameImage = LifeGameImage(
            rule=[self.rule["birth"].get(), self.rule["survive"].get()],
            tb=loop.get("tb", True),
            lr=loop.get("lr", True),
            c0=self.color["dead"].get(),
            c1=self.color["live"].get(),
            width=wh,
            height=wh,
            pixel=pixel,
            probability=self.scale.get(),
        )
        # start
        self.top = tk.Toplevel(self)
        self.top.title("Conway's Game of Life")
        self.top.bind("<Destroy>", self._on_top_destroy)
        flg: FrameLifeGame = FrameLifeGame(self.top, lifegameimage=lgi)
        flg.pack()
        return None

    def _on_top_destroy(self, event: tk.Event) -> None:
        if event.widget is self.top:
            self.button["start"].configure(state=tk.ACTIVE)
            self.button["stop"].configure(state=tk.DISABLED)
        return None

    def stop(self) -> None:
        if self.top is not None and self.top.winfo_exists():
            self.top.destroy()
        return None


def main() -> None:
    root: tk.Tk = tk.Tk()
    root.title("Conway's Game of Life")
    LifeGameGUI(root).pack()
    root.mainloop()
    return None


if __name__ == "__main__":
    main()
