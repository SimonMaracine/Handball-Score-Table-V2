import tkinter as tk


class SpectatorWindow:

    def __init__(self, top_level: tk.Toplevel, **kwargs):
        self.top_level = top_level
        self.content = tk.Frame(self.top_level)
        self.content.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        for key, value in kwargs.items():
            self.__setattr__(key, value)

        # Team 1
        ###########################################################################################
        team1_name = tk.Frame(self.content, borderwidth=5, relief="sunken", width=400, height=100)
        tk.Label(team1_name, text="Home", font="Times, 40").pack(padx=70, pady=20)

        team1_score = tk.Frame(self.content, borderwidth=3, relief="sunken")
        score_team1 = tk.IntVar(self.content, value=0)
        tk.Label(team1_score, text="{}".format(score_team1.get()), font="Times, 35").pack(padx=30, pady=10)

        team1_players = tk.Frame(self.content, borderwidth=3, relief="sunken")
        players1 = tk.Listbox(team1_players, font="Times, 15", height=17)
        for i in range(5):
            players1.insert(i, "Player {}".format(i + 1))

        team1_suspended = tk.Frame(self.content, borderwidth=5, relief="sunken")
        players_suspended1 = tk.Listbox(team1_suspended, font="Times, 14", width=14, height=17)
        for i in range(2):
            players_suspended1.insert(i, "I'm suspended")

        players1.pack(padx=2, pady=2)
        players_suspended1.pack(padx=2, pady=2)

        team1_name.grid(column=0, row=0)
        team1_score.grid(column=0, row=1)
        team1_players.grid(column=0, row=3)
        team1_suspended.grid(column=1, row=3)

        # Team 2
        ###########################################################################################
        team2_name = tk.Frame(self.content, borderwidth=5, relief="sunken", width=400, height=100)
        tk.Label(team2_name, text="Guest", font="Times, 40").pack(padx=70, pady=20)

        team2_score = tk.Frame(self.content, borderwidth=3, relief="sunken")
        score_team2 = tk.IntVar(self.content, value=0)
        tk.Label(team2_score, text="{}".format(score_team2.get()), font="Times, 35").pack(padx=30, pady=10)

        team2_players = tk.Frame(self.content, borderwidth=3, relief="sunken")
        players2 = tk.Listbox(team2_players, font="Times, 15", height=17)
        for i in range(5):
            players2.insert(i, "Player {}".format(i + 1))

        team2_suspended = tk.Frame(self.content, borderwidth=5, relief="sunken")
        players_suspended2 = tk.Listbox(team2_suspended, font="Times, 14", width=14, height=17)
        for i in range(3):
            players_suspended2.insert(i, "I'm suspended")

        players2.pack(padx=2, pady=2)
        players_suspended2.pack(padx=2, pady=2)

        team2_name.grid(column=3, row=0)
        team2_score.grid(column=3, row=1)
        team2_players.grid(column=3, row=3)
        team2_suspended.grid(column=2, row=3)

        # Main timer
        ###########################################################################################
        main_timer = tk.Frame(self.content, borderwidth=5, relief="sunken")
        tk.Label(main_timer, textvariable=self.time_var, font="Times, 75").pack(padx=40, pady=10)

        main_timer.grid(column=1, row=0, columnspan=2)

        # Match round
        ###########################################################################################
        match_round = tk.Frame(self.content, borderwidth=5, relief="sunken")
        tk.Label(match_round, text="{}".format(self.round_num_var.get()), font="Times, 55").pack(padx=30, pady=10)

        match_round.grid(column=1, row=1, columnspan=2)
