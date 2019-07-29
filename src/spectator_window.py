import tkinter as tk

SCL = 1


class SpectatorWindow:

    def __init__(self, top_level: tk.Toplevel, **kwargs):
        self.top_level = top_level
        self.top_level.minsize(width=int(1000 * SCL), height=int(660 * SCL))
        self.content = tk.Frame(self.top_level)
        self.content.pack(expand=True, padx=int(6 * SCL), pady=int(6 * SCL))
        for key, value in kwargs.items():
            self.__setattr__(key, value)
        self.to_give_back(spec_time_out=lambda: self.time_out(), spec_back_to_game=lambda: self.back_to_game())

        # Team 1
        ###########################################################################################
        team1_name = tk.Frame(self.content, borderwidth=int(4 * SCL), relief="sunken", width=int(400 * SCL), height=int(100 * SCL))
        tk.Label(team1_name, textvariable=self.name_team1_var, font=f"Times, {int(34 * SCL)}").pack(padx=int(8 * SCL), pady=int(20 * SCL))

        team1_score = tk.Frame(self.content, borderwidth=int(3 * SCL), relief="sunken")
        tk.Label(team1_score, textvariable=self.score_team1_var, font=f"Times, {int(35 * SCL)}").pack(padx=int(26 * SCL), pady=int(8 * SCL))

        team1_players = tk.Frame(self.content, borderwidth=int(3 * SCL), relief="sunken", width=int(290 * SCL), height=int(415 * SCL))
        team1_players.pack_propagate(False)

        team1_suspended = tk.Frame(self.content, borderwidth=int(4 * SCL), relief="sunken", width=int(160 * SCL), height=int(405 * SCL))
        team1_suspended.grid_propagate(False)

        team1_name.grid(column=0, row=0)
        team1_score.grid(column=0, row=1)
        team1_players.grid(column=0, row=3)
        team1_suspended.grid(column=1, row=3)

        # Team 2
        ###########################################################################################
        team2_name = tk.Frame(self.content, borderwidth=int(4 * SCL), relief="sunken", width=int(400 * SCL), height=int(100 * SCL))
        tk.Label(team2_name, textvariable=self.name_team2_var, font=f"Times, {int(34 * SCL)}").pack(padx=int(8 * SCL), pady=int(20 * SCL))

        team2_score = tk.Frame(self.content, borderwidth=int(3 * SCL), relief="sunken")
        tk.Label(team2_score, textvariable=self.score_team2_var, font=f"Times, {int(35 * SCL)}").pack(padx=int(26 * SCL), pady=int(8 * SCL))

        team2_players = tk.Frame(self.content, borderwidth=int(3 * SCL), relief="sunken", width=int(290 * SCL), height=int(415 * SCL))
        team2_players.pack_propagate(False)

        team2_suspended = tk.Frame(self.content, borderwidth=int(4 * SCL), relief="sunken", width=int(160 * SCL), height=int(405 * SCL))
        team2_suspended.grid_propagate(False)

        team2_name.grid(column=3, row=0)
        team2_score.grid(column=3, row=1)
        team2_players.grid(column=3, row=3)
        team2_suspended.grid(column=2, row=3)

        # Init players
        ###########################################################################################
        for i, player in enumerate(self.players1):
            suspended = tk.Label(team1_suspended, textvariable=player.suspend_text_var, font=f"Times, {int(13 * SCL)}")
            suspended.grid(row=i, padx=int(24 * SCL), pady=0)
            # suspended.grid_remove()

            player.text_var = tk.StringVar(team1_players, value="{} [{:02d}]    {}".format(player.name, player.number, player.scores))
            tk.Label(team1_players, textvariable=player.text_var, font=f"Times, {int(13 * SCL)}").pack(padx=int(26 * SCL), pady=0)

        for i, player in enumerate(self.players2):
            suspended = tk.Label(team2_suspended, textvariable=player.suspend_text_var, font=f"Times, {int(13 * SCL)}")
            suspended.grid(row=i, padx=int(24 * SCL), pady=0)
            # suspended.grid_remove()

            player.text_var = tk.StringVar(team2_players,
                                           value="{} [{:02d}]    {}".format(player.name, player.number, player.scores))
            tk.Label(team2_players, textvariable=player.text_var, font=f"Times, {int(13 * SCL)}").pack(padx=int(26 * SCL), pady=0)

        # Main timer
        ###########################################################################################
        main_timer = tk.Frame(self.content, borderwidth=int(4 * SCL), relief="sunken")
        self.timer_text = tk.Label(main_timer, textvariable=self.time_var, font=f"Times, {int(74 * SCL)}")
        self.timer_text.grid(padx=int(16 * SCL), pady=int(4 * SCL))

        main_timer.grid(column=1, row=0, columnspan=2)

        # Match round
        ###########################################################################################
        match_round = tk.Frame(self.content, borderwidth=int(4 * SCL), relief="sunken")
        tk.Label(match_round, textvariable=self.round_num_var, font=f"Times, {int(53 * SCL)}").pack(padx=int(32 * SCL), pady=0)

        match_round.grid(column=1, row=1, columnspan=2)

        # Timeout timer
        ###########################################################################################
        self.time_out_timer_text = tk.Label(main_timer, textvariable=self.time_out_var, font=f"Times, {int(74 * SCL)}",
                                            foreground="darkred")
        self.time_out_timer_text.grid(padx=int(16 * SCL), pady=int(4 * SCL))
        self.time_out_timer_text.grid_remove()

    def time_out(self):
        self.timer_text.grid_remove()
        self.time_out_timer_text.grid()

    def back_to_game(self):
        self.time_out_timer_text.grid_remove()
        self.timer_text.grid()
