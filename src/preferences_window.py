import json
import logging
import tkinter as tk
from os.path import join

from src.log import stream_handler
from src.alert_window import alert

logger = logging.getLogger(__name__)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


def create_settings_file():
    with open(join("data", "settings.json"), "w") as file:
        file.write('{"spectator_scale": 1.0}')


class PreferencesWindow:

    def __init__(self, top_level: tk.Toplevel):
        self.top_level = top_level
        self.top_level.minsize(width=320, height=240)
        self.top_level.title("Preferences")
        self.content = tk.Frame(self.top_level)
        self.content.grid(column=0, row=0, padx=10, pady=10)

        # Containers
        ###########################################################################################
        container1 = tk.Frame(self.content)
        container2 = tk.Frame(self.content)

        container1.grid(column=0, row=0, pady=12)
        container2.grid(column=0, row=1)

        # Settings
        ###########################################################################################
        try:
            with open(join("data", "settings.json"), "r") as file:
                raw_data = file.read()
                settings: dict = json.loads(raw_data)
                scale = settings["spectator_scale"]
        except FileNotFoundError:
            logger.info("No settings file found")
            create_settings_file()
            scale = 1.0

        self.scale = tk.StringVar(container1, value=scale)
        spectator_scale = tk.Spinbox(container1, from_=0.8, to=2.4, increment=0.2, textvariable=self.scale, width=4)
        spectator_scale.grid(column=1, row=0)

        tk.Label(container1, text="Spectator window scale").grid(column=0, row=0)

        # Buttons
        ###########################################################################################
        tk.Button(container2, text="Save", command=self.save_preferences).grid(column=0, row=0, padx=5)
        tk.Button(container2, text="Cancel", command=self.top_level.destroy).grid(column=1, row=0, padx=5)

    def save_preferences(self):
        config = {
            "spectator_scale": float
        }

        try:
            scale = float(self.scale.get())
        except ValueError:
            logger.info("Scale must be a number")
            alert(self.top_level, "Scale must be a number")
            return

        if scale < 0.8:
            scale = 0.8
        elif scale > 2.4:
            scale = 2.4

        config["spectator_scale"] = scale

        with open(join("data", "settings.json"), "w") as file:
            json.dump(config, file)

        self.top_level.destroy()
