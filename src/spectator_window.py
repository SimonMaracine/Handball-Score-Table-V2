import tkinter as tk


class SpectatorWindow:

    def __init__(self, top_level: tk.Toplevel, **kwargs):
        self.top_level = top_level
        self.top_level.minsize(width=900, height=640)
        self.content = tk.Frame(self.top_level)
        self.content.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        for key, value in kwargs.items():
            self.__setattr__(key, value)

        # Team 1
        ###########################################################################################
        team1_name = tk.Frame(self.content, borderwidth=5, relief="sunken", width=400, height=100)
        tk.Label(team1_name, textvariable=self.name_team1_var, font="Times, 40").pack(padx=10, pady=20)

        team1_score = tk.Frame(self.content, borderwidth=3, relief="sunken")
        tk.Label(team1_score, textvariable=self.score_team1_var, font="Times, 35").pack(padx=24, pady=10)

        team1_players = tk.Frame(self.content, borderwidth=3, relief="sunken", width=290, height=450)
        team1_players.pack_propagate(False)

        team1_suspended = tk.Frame(self.content, borderwidth=5, relief="sunken", width=190, height=430)
        team1_suspended.grid_propagate(False)

        team1_name.grid(column=0, row=0)
        team1_score.grid(column=0, row=1)
        team1_players.grid(column=0, row=3)
        team1_suspended.grid(column=1, row=3)

        # Team 2
        ###########################################################################################
        team2_name = tk.Frame(self.content, borderwidth=5, relief="sunken", width=400, height=100)
        tk.Label(team2_name, textvariable=self.name_team2_var, font="Times, 40").pack(padx=10, pady=20)

        team2_score = tk.Frame(self.content, borderwidth=3, relief="sunken")
        tk.Label(team2_score, textvariable=self.score_team2_var, font="Times, 35").pack(padx=24, pady=10)

        team2_players = tk.Frame(self.content, borderwidth=3, relief="sunken", width=290, height=450)
        team2_players.pack_propagate(False)

        team2_suspended = tk.Frame(self.content, borderwidth=5, relief="sunken", width=190, height=430)
        team2_suspended.grid_propagate(False)

        team2_name.grid(column=3, row=0)
        team2_score.grid(column=3, row=1)
        team2_players.grid(column=3, row=3)
        team2_suspended.grid(column=2, row=3)

        # Init players
        ###########################################################################################
        for i, player in enumerate(self.players1):
            suspended = tk.Label(team1_suspended, textvariable=player.suspend_text_var, font="Times, 15")
            suspended.grid(row=i, padx=24, pady=2)
            # suspended.grid_remove()

            player.text_var = tk.StringVar(team1_players, value="{} [{}]    {}".format(player.name, player.number, player.scores))
            tk.Label(team1_players, textvariable=player.text_var, font="Times, 15").pack(padx=26, pady=2)

        for i, player in enumerate(self.players2):
            suspended = tk.Label(team2_suspended, textvariable=player.suspend_text_var, font="Times, 15")
            suspended.grid(row=i, padx=24, pady=2)
            # suspended.grid_remove()

            player.text_var = tk.StringVar(team2_players,
                                           value="{} [{}]    {}".format(player.name, player.number, player.scores))
            tk.Label(team2_players, textvariable=player.text_var, font="Times, 15").pack(padx=26, pady=2)

        # Main timer
        ###########################################################################################
        main_timer = tk.Frame(self.content, borderwidth=5, relief="sunken")
        tk.Label(main_timer, textvariable=self.time_var, font="Times, 75").pack(padx=40, pady=10)

        main_timer.grid(column=1, row=0, columnspan=2)

        # Match round
        ###########################################################################################
        match_round = tk.Frame(self.content, borderwidth=5, relief="sunken")
        tk.Label(match_round, textvariable=self.round_num_var, font="Times, 52").pack(padx=34, pady=8)

        match_round.grid(column=1, row=1, columnspan=2)
