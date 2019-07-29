import json
import tkinter as tk
from os.path import join


class PreferencesWindow:

    def __init__(self, top_level: tk.Toplevel):
        self.top_level = top_level
        self.top_level.minsize(width=320, height=240)
        self.content = tk.Frame(self.top_level)
        self.content.grid(column=0, row=0, padx=10, pady=10)

        # Containers
        ###########################################################################################
        container1 = tk.Frame(self.content)
        container2 = tk.Frame(self.content)

        container1.grid(column=0, row=0)
        container2.grid(column=0, row=1)

        # Settings
        ###########################################################################################
        try:
            with open(join("data", "settings.json"), "r") as file:
                raw_data = file.read()
                settings: dict = json.loads(raw_data)
                scale = settings["spectator_scale"]
        except FileNotFoundError:
            print("No settings file found")
            scale = 1.0

        self.scale = tk.StringVar(container1, value=scale)
        spectator_scale = tk.Spinbox(container1, from_=0.8, to=3.0, increment=0.2, textvariable=self.scale, width=4)
        spectator_scale.grid(column=1, row=0)

        tk.Label(container1, text="Spectator window scale").grid(column=0, row=0)

        # Buttons
        ###########################################################################################
        tk.Button(container2, text="Save", command=self.save_preferences).grid(column=0, row=0)
        tk.Button(container2, text="Cancel", command=self.top_level.destroy).grid(column=1, row=0)

    def save_preferences(self):
        config = {
            "spectator_scale": float
        }

        config["spectator_scale"] = float(self.scale.get())

        with open(join("data", "settings.json"), "w") as file:
            json.dump(config, file)

        self.top_level.destroy()
