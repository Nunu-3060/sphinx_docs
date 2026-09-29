import tkinter as tk
from tkinter import ttk

#: Display Size
DISPLAY_SIZE: int = 512


class FrameRadioButton(ttk.Frame):
    def __init__(self, master: tk.Misc | None = None) -> None:
        super().__init__(master)
        self.label: ttk.Label = ttk.Label(self, text="size")
        self.value: tk.IntVar = tk.IntVar(self, value=DISPLAY_SIZE // 2)
        self.radiobutton: dict[int, ttk.Radiobutton] = {
            i: ttk.Radiobutton(self, variable=self.value, value=i, text=str(i))
            for i in [DISPLAY_SIZE // 4, DISPLAY_SIZE // 2, DISPLAY_SIZE]
        }
        self.label.pack()
        for v in self.radiobutton.values():
            v.pack()
        return None

    def get(self) -> int:
        return self.value.get()

    def set(self, value: int = DISPLAY_SIZE // 2) -> None:
        if value in self.radiobutton.keys():
            self.value.set(value)
        return None


class FrameScale(ttk.Frame):
    def __init__(self, master: tk.Misc | None = None, text: str = "") -> None:
        super().__init__(master)
        self.text: str = text
        self.label: ttk.Label = ttk.Label(self, text=self.text)
        self.scale: ttk.Scale = ttk.Scale(self, from_=0.0, to=1.0, value=0.0, orient=tk.HORIZONTAL, command=self.apply)
        self.label.pack(side=tk.TOP, fill=tk.BOTH)
        self.scale.pack(side=tk.TOP, fill=tk.BOTH)
        self.apply()
        return None

    def get(self) -> float:
        return self.scale.get()

    def set(self, p: float = 0) -> None:
        self.scale.set(p)
        return None

    def apply(self, value: str = "") -> None:
        p: float = self.scale.get()
        self.label.configure(text=f"{self.text}: {p:.3f}")
        return None
