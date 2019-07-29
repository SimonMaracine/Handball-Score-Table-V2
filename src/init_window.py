import json
import tkinter as tk
from os.path import join
from typing import List

from src.config_object import Config


class InitWindow:
    PATH_TO_CONFIGS = join("data", "configs")

    def __init__(self, top_level: tk.Toplevel, on_apply, **kwargs):
        self.top_level = top_level
        self.on_apply = on_apply
        self.top_level.minsize(width=660, height=420)
        self.content = tk.Frame(self.top_level)
        self.content.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        for key, value in kwargs.items():
            self.__setattr__(key, value)

        # Containers
        ###########################################################################################
        player_entries = tk.Frame(self.content)
        config_entries = tk.Frame(self.content)
        configs = tk.Frame(self.content)
        buttons = tk.Frame(self.content)

        player_entries.grid(column=0, row=0, rowspan=3)
        config_entries.grid(column=1, row=0)
        configs.grid(column=1, row=1)
        buttons.grid(column=1, row=2)

        # Player entries
        ###########################################################################################
        self.team1_players = []
        self.team2_players = []
        self.players1_nums = []
        self.players2_nums = []

        self.team1 = tk.Entry(player_entries, width=21)
        self.team1.grid(column=1, row=0, columnspan=2)
        self.team1.insert(0, "Home")

        for i in range(1, 17):
            ent = tk.Entry(player_entries, width=14)
            ent.grid(column=1, row=i, sticky=tk.W)
            self.team1_players.append(ent)

            ent = tk.Entry(player_entries, width=3)
            ent.grid(column=2, row=i, sticky=tk.W)
            self.players1_nums.append(ent)

        self.team2 = tk.Entry(player_entries, width=21)
        self.team2.grid(column=4, row=0, columnspan=2)
        self.team2.insert(0, "Guest")

        for i in range(1, 17):
            ent = tk.Entry(player_entries, width=14)
            ent.grid(column=4, row=i, sticky=tk.W)
            self.team2_players.append(ent)

            ent = tk.Entry(player_entries, width=3)
            ent.grid(column=5, row=i, sticky=tk.W)
            self.players2_nums.append(ent)

        # Player labels
        ###########################################################################################
        tk.Label(player_entries, text="Team 1").grid(column=0, row=0)
        for i in range(1, 17):
            tk.Label(player_entries, text=f"{i}").grid(column=0, row=i)
        tk.Label(player_entries, text="Team 2").grid(column=3, row=0)
        for i in range(1, 17):
            tk.Label(player_entries, text=f"{i}").grid(column=3, row=i)

        # Config entries
        ###########################################################################################
        self.match = tk.Entry(config_entries, width=5)
        self.match.grid(column=1, row=0, sticky=tk.N)
        self.match.insert(0, "900")
        self.timeout = tk.Entry(config_entries, width=5)
        self.timeout.grid(column=1, row=1, sticky=tk.N)
        self.timeout.insert(0, "60")
        self.suspend = tk.Entry(config_entries, width=5)
        self.suspend.grid(column=1, row=2, sticky=tk.N)
        self.suspend.insert(0, "120")

        self.config_load = tk.Entry(configs, width=10)
        self.config_load.grid(column=0, row=0)
        self.config_save = tk.Entry(configs, width=10)
        self.config_save.grid(column=0, row=1)

        # Config labels
        ###########################################################################################
        tk.Label(config_entries, text="Match time").grid(column=0, row=0, sticky=tk.N)
        tk.Label(config_entries, text="Timeout time").grid(column=0, row=1, sticky=tk.N)
        tk.Label(config_entries, text="Player suspend time").grid(column=0, row=2, sticky=tk.N)

        # Buttons
        ###########################################################################################
        tk.Button(buttons, text="Apply", command=self.apply_new_configuration).pack()
        tk.Button(buttons, text="Discard", command=self.top_level.destroy).pack()
        tk.Button(configs, text="Load config",
                  command=lambda: self.load_configuration(self.config_load.get())).grid(column=1, row=0)
        tk.Button(configs, text="Save config",
                  command=lambda: self.save_configuration(self.config_save.get())).grid(column=1, row=1)

    def get_current_entries(self) -> tuple:
        players1_entries = tuple(filter(lambda entry: entry.get(), self.team1_players))
        nums1 = tuple(map(lambda entry: entry.get(), tuple(filter(lambda entry: entry.get(), self.players1_nums))))
        players2_entries = tuple(filter(lambda entry: entry.get(), self.team2_players))
        nums2 = tuple(map(lambda entry: entry.get(), tuple(filter(lambda entry: entry.get(), self.players2_nums))))

        if len(players1_entries) != len(nums1) or len(players2_entries) != len(nums2):
            print("All players must have a number (or a number must have a name)")
            return
        if len(tuple(filter(lambda num: num.isdigit() and len(num) == 2, nums1))) < len(nums1) or \
                len(tuple(filter(lambda num: num.isdigit() and len(num) == 2, nums2))) < len(nums2):
            print("Players' numbers must be numbers and must be two digits")
            return
        if len(self.team1.get()) > 19 or len(self.team2.get()) > 19:
            print("Teams' names must not exceed 19 characters")
            return
        for name in map(lambda entry: entry.get(), players1_entries + players2_entries):
            if len(name) > 14:
                print("Players' names must not exceed 14 characters")
                return
        if not self.match.get().isdigit() or not self.timeout.get().isdigit() or not self.suspend.get().isdigit():
            print("Timer times must be numbers")
            return

        team1 = self.team1.get()
        team2 = self.team2.get()
        players1 = list(map(lambda entry: entry.get(), tuple(filter(lambda entry: entry.get(), self.team1_players))))
        players2 = list(map(lambda entry: entry.get(), tuple(filter(lambda entry: entry.get(), self.team2_players))))
        nums1 = list(map(lambda entry: entry.get(), tuple(filter(lambda entry: entry.get(), self.players1_nums))))
        nums2 = list(map(lambda entry: entry.get(), tuple(filter(lambda entry: entry.get(), self.players2_nums))))
        match = self.match.get()
        timeout = self.timeout.get()
        suspend = self.suspend.get()
        return team1, team2, players1, players2, nums1, nums2, match, timeout, suspend

    def apply_new_configuration(self):
        try:
            team1, team2, players1, players2, nums1, nums2, match, timeout, suspend = self.get_current_entries()
        except TypeError:  # If returned prematurely, with an error
            return
        self.on_apply(Config(team1, team2, players1, players2, nums1, nums2, match, timeout, suspend))
        self.top_level.destroy()

    def load_configuration(self, json_file: str):
        try:
            with open(join(self.PATH_TO_CONFIGS, json_file + ".json"), "r") as file:
                config_raw = file.read()
                config: dict = json.loads(config_raw)
        except FileNotFoundError:
            print(f'No configuration file "{json_file}" found')
            return

        # Get those values
        team1_object: dict = config["teams"][0]
        team2_object: dict = config["teams"][1]
        players1_list: List[dict] = team1_object["players"]
        players2_list: List[dict] = team2_object["players"]

        team1: str = team1_object["name"]
        team2: str = team2_object["name"]
        players1: List[str] = list(map(lambda player: player["name"], players1_list))
        players2: List[str] = list(map(lambda player: player["name"], players2_list))
        nums1: List[str] = list(map(lambda player: f'{player["number"]:02d}', players1_list))
        nums2: List[str] = list(map(lambda player: f'{player["number"]:02d}', players2_list))
        match = f'{config["match"]:02d}'
        timeout = f'{config["timeout"]:02d}'
        suspend = f'{config["suspend"]:02d}'

        # Erase everything first
        self.team1.delete(0, tk.END)
        self.team2.delete(0, tk.END)
        for entry in self.team1_players + self.team2_players + self.players1_nums + self.players2_nums:
            entry.delete(0, tk.END)
        self.match.delete(0, tk.END)
        self.timeout.delete(0, tk.END)
        self.suspend.delete(0, tk.END)

        # Insert from config file
        self.team1.insert(0, team1)
        self.team2.insert(0, team2)
        for entry, insert in zip(self.team1_players, players1):
            entry.insert(0, insert)
        for entry, insert in zip(self.team2_players, players2):
            entry.insert(0, insert)
        for entry, insert in zip(self.players1_nums, nums1):
            entry.insert(0, insert)
        for entry, insert in zip(self.players2_nums, nums2):
            entry.insert(0, insert)
        self.match.insert(0, match)
        self.timeout.insert(0, timeout)
        self.suspend.insert(0, suspend)

        print("Loaded configuration " + json_file)

    def save_configuration(self, json_file: str):
        config = {
            "teams": [
                {
                    "name": str,
                    "players": List[dict]
                },
                {
                    "name": str,
                    "players": List[dict]
                }
            ],
            "match": int,
            "timeout": int,
            "suspend": int
        }

        # Get config
        try:
            team1, team2, players1, players2, nums1, nums2, match, timeout, suspend = self.get_current_entries()
        except TypeError:  # If returned prematurely, with an error
            return

        config["teams"][0]["name"] = team1
        config["teams"][1]["name"] = team2

        players: List[dict] = []
        for name, number in zip(players1, nums1):
            player = {"name": name, "number": int(number)}
            players.append(player)
        config["teams"][0]["players"] = players
        players: List[dict] = []
        for name, number in zip(players2, nums2):
            player = {"name": name, "number": int(number)}
            players.append(player)
        config["teams"][1]["players"] = players

        config["match"] = int(match)
        config["timeout"] = int(timeout)
        config["suspend"] = int(suspend)

        with open(join(self.PATH_TO_CONFIGS, json_file + ".json"), "w") as file:
            json.dump(config, file)

        print("Saved configuration " + json_file)