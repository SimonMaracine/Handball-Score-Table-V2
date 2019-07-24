import tkinter as tk


class InitWindow:

    def __init__(self, top_level: tk.Toplevel, **kwargs):
        self.top_level = top_level
        self.top_level.minsize(width=900, height=640)
        self.content = tk.Frame(self.top_level)
        self.content.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        for key, value in kwargs.items():
            self.__setattr__(key, value)

        # Rest of the code
