import json
import logging
import tkinter as tk
from os.path import join

import src.log
from src.alert_window import alert
from src.settings import get_settings
import src.timer

logger = src.log.get_logger(__name__)
logger.setLevel(logging.DEBUG)


class PreferencesWindow:

    def __init__(self, top_level: tk.Toplevel):
        self.top_level = top_level
        self.top_level.minsize(width=270, height=200)
        self.top_level.title("Preferences")
        self.content = tk.Frame(self.top_level)
        self.content.pack(padx=10, pady=10, expand=True)

        # Containers
        ###########################################################################################
        container1 = tk.Frame(self.content)
        container2 = tk.Frame(self.content)

        container1.grid(column=0, row=0, pady=12)
        container2.grid(column=0, row=1, pady=20)

        # Settings
        ###########################################################################################
        scale, sounds = get_settings()

        self.scale = tk.StringVar(container1, value=scale)
        spectator_scale = tk.Spinbox(container1, from_=0.8, to=2.4, increment=0.2, textvariable=self.scale, width=4)
        spectator_scale.grid(column=1, row=0)

        self.sounds = tk.BooleanVar(container1, value=sounds)
        enable_sounds = tk.Checkbutton(container1, variable=self.sounds)
        enable_sounds.grid(column=1, row=1)

        tk.Label(container1, text="Spectator window scale").grid(column=0, row=0)
        tk.Label(container1, text="Enable sounds").grid(column=0, row=1)

        # Buttons
        ###########################################################################################
        tk.Button(container2, text="Save", command=self.save_preferences).grid(column=0, row=0, padx=5)
        tk.Button(container2, text="Cancel", command=self.top_level.destroy).grid(column=1, row=0, padx=5)

    def save_preferences(self):
        config = {
            "spectator_scale": float,
            "enable_sounds": bool
        }

        try:
            scale = float(self.scale.get())
        except ValueError:
            logger.info("Scale must be a number")
            alert(self.top_level, "Scale must be a number.")
            return

        if scale < 0.8:
            scale = 0.8
        elif scale > 2.4:
            scale = 2.4

        sounds = self.sounds.get()

        config["spectator_scale"] = scale
        config["enable_sounds"] = sounds

        with open(join("data", "settings.json"), "w") as file:
            json.dump(config, file, sort_keys=True, indent=2)

        self.top_level.destroy()
        src.timer.TimeOutTimer.update()
