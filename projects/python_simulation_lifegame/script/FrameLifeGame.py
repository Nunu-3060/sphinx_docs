import tkinter as tk
from tkinter import ttk

from PIL import ImageTk

from LifeGameImage import LifeGameImage


class FrameLifeGame(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc | None = None,
        lifegameimage: LifeGameImage | None = None,
        interval: int = 10,
    ) -> None:
        super().__init__(master)
        if lifegameimage is None:
            lifegameimage = LifeGameImage()
        self.lifegameimage: LifeGameImage = lifegameimage
        self.image: ImageTk.PhotoImage = self.lifegameimage.image_tk()
        self.label: ttk.Label = ttk.Label(self, image=self.image)
        self.label.pack()
        self.interval: int = interval

        self._after_id: str | None = None
        self.bind("<Destroy>", self._on_destroy)
        self._after_id = self.after(self.interval, self.next)
        return None

    def _on_destroy(self, event: tk.Event) -> None:
        if event.widget is self and self._after_id is not None:
            self.after_cancel(self._after_id)
            self._after_id = None
        return None

    def next(self) -> None:
        self.lifegameimage.next()
        self.image = self.lifegameimage.image_tk()
        self.label.configure(image=self.image)
        self._after_id = self.after(self.interval, self.next)
        return None
