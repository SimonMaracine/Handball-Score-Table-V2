import tkinter as tk
from src.config_object import Config


class InitWindow:

    def __init__(self, top_level: tk.Toplevel, on_apply, **kwargs):
        self.top_level = top_level
        self.on_apply = on_apply
        self.top_level.minsize(width=900, height=640)
        self.content = tk.Frame(self.top_level)
        self.content.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        for key, value in kwargs.items():
            self.__setattr__(key, value)

        # Containers
        ###########################################################################################
        player_entries = tk.Frame(self.content)
        config_entries = tk.Frame(self.content)
        button = tk.Frame(self.content)

        player_entries.grid(column=0, row=0)
        config_entries.grid(column=1, row=0)
        button.grid(column=2, row=0)

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
        tk.Label(player_entries, text="Team 1")
        for i in range(1, 17):
            tk.Label(player_entries, text=f"{i}").grid(column=0, row=i)
        tk.Label(player_entries, text="Team 2")
        for i in range(1, 17):
            tk.Label(player_entries, text=f"{i}").grid(column=3, row=i)

        # Config entries
        ###########################################################################################
        self.match = tk.Entry(config_entries, width=5)
        self.match.grid(column=1, row=0, sticky=tk.N)
        self.match.insert(0, "3600")
        self.timeout = tk.Entry(config_entries, width=5)
        self.timeout.grid(column=1, row=1, sticky=tk.N)
        self.timeout.insert(0, "60")
        self.suspend = tk.Entry(config_entries, width=5)
        self.suspend.grid(column=1, row=2, sticky=tk.N)
        self.suspend.insert(0, "120")

        # Config labels
        ###########################################################################################
        tk.Label(config_entries, text="Match time").grid(column=0, row=0, sticky=tk.N)
        tk.Label(config_entries, text="Timeout time").grid(column=0, row=1, sticky=tk.N)
        tk.Label(config_entries, text="Player suspend time").grid(column=0, row=2, sticky=tk.N)

        # Buttons
        ###########################################################################################
        tk.Button(button, text="Apply", command=self.apply_new_configuration).pack()
        tk.Button(button, text="Discard", command=self.top_level.destroy).pack()

    def apply_new_configuration(self):
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
        if len(self.team1.get()) > 21 or len(self.team2.get()) > 21:
            print("Teams' names must not exceed 21 characters")
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

        self.on_apply(Config(team1, team2, players1, players2, nums1, nums2, match, timeout, suspend))
        self.top_level.destroy()
