import tkinter as tk
from typing import Union, Callable

import src.log
from src.alert_window import alert

logger = src.log.get_logger(__name__)
logger.setLevel(10)


class ChangeTimeWindow:

    MIN_TIMER_TIME = 1
    MAX_TIMER_TIME = 90

    def __init__(self, top_level: tk.Toplevel, on_apply: Callable):
        self.top_level = top_level
        self.on_apply = on_apply
        self.top_level.minsize(width=215, height=120)
        self.top_level.title("Change Round Time")
        self.content = tk.Frame(self.top_level)
        self.content.pack(padx=10, pady=10, expand=True)

        self.entry = tk.Entry(self.content, width=3)
        self.entry.grid(column=0, row=0, columnspan=2)

        tk.Label(self.content, text="min").grid(column=1, row=0, columnspan=2)

        tk.Button(self.content, text="Apply", command=self.apply).grid(column=0, row=1, padx=0, pady=14)
        tk.Button(self.content, text="Cancel", command=self.close).grid(column=1, row=1, padx=0, pady=14)

    def apply(self) -> Union[int, None]:
        try:
            entry = int(self.entry.get())
        except ValueError:
            logger.info("Entry must be a number")
            alert(self.top_level, "Entry must be a number.")
            return

        if entry < ChangeTimeWindow.MIN_TIMER_TIME:
            entry = 1
        elif entry > ChangeTimeWindow.MAX_TIMER_TIME:
            entry = 90

        self.on_apply(entry)
        self.close()

    def close(self):
        self.top_level.destroy()
