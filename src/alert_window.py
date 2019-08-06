from tkinter import messagebox


def alert(window, message: str):
    messagebox.showerror(title="Error", message=message, parent=window)


def info(window, message: str):
    messagebox.showinfo(title="Info", message=message, parent=window)


def ask(window, message: str) -> bool:
    response = messagebox.askyesno(title="Confirm", message=message, parent=window)
    return response
