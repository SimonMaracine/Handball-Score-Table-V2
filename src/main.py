import tkinter as tk
from src.control_window import ControlWindow


class MainApplication:

    def __init__(self):
        pass


def main():
    root = tk.Tk()
    ControlWindow(root).run()
