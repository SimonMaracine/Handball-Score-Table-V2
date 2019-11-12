import tkinter as tk


class AboutWindow:

    def __init__(self, top_level: tk.Toplevel):
        self.top_level = top_level
        self.top_level.minsize(width=322, height=160)
        self.top_level.title("About")
        self.content = tk.Frame(self.top_level)
        self.content.pack(padx=10, pady=20, expand=True)

        tk.Label(self.content, text="Handball Score Table-V2", font="Times, 18").grid(column=0, row=0, sticky=tk.N)
        tk.Label(self.content, text="Made by Simon Mărăcine", font="Times, 10").grid(column=0, row=1)

        ok = tk.Frame(self.content)
        ok.grid(column=0, row=2, sticky=tk.S)
        tk.Button(ok, text="Ok", command=self.close).pack(padx=0, pady=14, side="bottom")

    def close(self):
        self.top_level.destroy()
