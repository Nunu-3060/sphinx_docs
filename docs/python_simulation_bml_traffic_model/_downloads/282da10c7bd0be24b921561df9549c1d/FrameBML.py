import tkinter as tk
from tkinter import ttk

from PIL import ImageTk

from BMLImage import BMLImage


class FrameBML(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc | None = None,
        bmli: BMLImage | None = None,
        interval: int = 10,
    ) -> None:
        super().__init__(master)
        if bmli is None:
            bmli = BMLImage()
        self.bmli: BMLImage = bmli
        self.image: ImageTk.PhotoImage = self.bmli.image_tk()
        self.label: ttk.Label = ttk.Label(self, image=self.image)
        self.label.pack()
        self.interval: int = interval
        self.bind("<Destroy>", self._on_destroy)
        self._after_id: str | None = None
        self._after_id = self.after(self.interval, self.next)
        return None

    def next(self) -> None:
        self.bmli.next()
        self.image = self.bmli.image_tk()
        self.label.configure(image=self.image)
        self._after_id = self.after(self.interval, self.next)
        return None

    def _on_destroy(self, event: tk.Event) -> None:
        if event.widget is self and self._after_id is not None:
            self.after_cancel(self._after_id)
            self._after_id = None
        return None
