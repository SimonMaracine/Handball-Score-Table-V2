import tkinter as tk
from typing import Tuple, Optional
from dataclasses import dataclass

from PIL import Image, ImageTk

import src.log
from src.settings import get_settings

logger = src.log.get_logger(__name__)
logger.setLevel(10)

SCL = 1.0


@dataclass
class SpecWinPointer:
    window: Optional[tk.Toplevel]


class SpectatorWindow:

    def __init__(self, top_level: tk.Toplevel, x: int, y: int, **kwargs):
        global SCL
        SCL, _ = get_settings()

        self.top_level = top_level
        self.top_level.minsize(width=int(1000 * SCL), height=int(670 * SCL))
        self.top_level.title("Handball Score Table")
        self.top_level.protocol("WM_DELETE_WINDOW", self.close)

        if x != 0 and y != 0:
            self.top_level.geometry(f"+{x}+{y}")

        self.content = tk.Frame(self.top_level)
        self.content.pack(expand=True, padx=int(6 * SCL), pady=int(6 * SCL))
        for key, value in kwargs.items():
            self.__setattr__(key, value)

        # Team logos
        ###########################################################################################
        logo1 = Image.open(self.logo1)
        logo1 = logo1.resize((int(118 * SCL), int(88 * SCL)), Image.ANTIALIAS)
        self.team1_logo = ImageTk.PhotoImage(logo1)

        logo2 = Image.open(self.logo2)
        logo2 = logo2.resize((int(118 * SCL), int(88 * SCL)), Image.ANTIALIAS)
        self.team2_logo = ImageTk.PhotoImage(logo2)

        # Team 1
        ###########################################################################################
        team1_name = tk.Frame(self.content, borderwidth=int(4 * SCL), relief="sunken", width=int(400 * SCL), height=int(100 * SCL))
        tk.Label(team1_name, textvariable=self.name_team1_var, font=f"Times, {int(34 * SCL)}").pack(padx=int(8 * SCL), pady=int(20 * SCL))

        team1_score = tk.Frame(self.content, borderwidth=int(3 * SCL), relief="sunken")
        tk.Label(team1_score, textvariable=self.score_team1_var, font=f"Times, {int(35 * SCL)}").pack(padx=int(26 * SCL), pady=int(8 * SCL))

        team1_players = tk.Frame(self.content, borderwidth=int(3 * SCL), relief="sunken", width=int(290 * SCL), height=int(425 * SCL))
        team1_players.pack_propagate(False)

        self.team1_suspended = tk.Frame(self.content, borderwidth=int(4 * SCL), relief="sunken", width=int(160 * SCL), height=int(420 * SCL))
        self.team1_suspended.pack_propagate(False)

        team1_logo = tk.Label(self.content, image=self.team1_logo)

        team1_name.grid(column=0, row=0, columnspan=2)
        team1_score.grid(column=1, row=1)
        team1_players.grid(column=0, row=2, columnspan=2)
        self.team1_suspended.grid(column=2, row=2)
        team1_logo.grid(column=0, row=1)

        if self.logo1.endswith("__logo.png"):
            team1_logo.destroy()

        # Team 2
        ###########################################################################################
        team2_name = tk.Frame(self.content, borderwidth=int(4 * SCL), relief="sunken", width=int(400 * SCL), height=int(100 * SCL))
        tk.Label(team2_name, textvariable=self.name_team2_var, font=f"Times, {int(34 * SCL)}").pack(padx=int(8 * SCL), pady=int(20 * SCL))

        team2_score = tk.Frame(self.content, borderwidth=int(3 * SCL), relief="sunken")
        tk.Label(team2_score, textvariable=self.score_team2_var, font=f"Times, {int(35 * SCL)}").pack(padx=int(26 * SCL), pady=int(8 * SCL))

        team2_players = tk.Frame(self.content, borderwidth=int(3 * SCL), relief="sunken", width=int(290 * SCL), height=int(425 * SCL))
        team2_players.pack_propagate(False)

        self.team2_suspended = tk.Frame(self.content, borderwidth=int(4 * SCL), relief="sunken", width=int(160 * SCL), height=int(420 * SCL))
        self.team2_suspended.pack_propagate(False)

        team2_logo = tk.Label(self.content, image=self.team2_logo)

        team2_name.grid(column=4, row=0, columnspan=2)
        team2_score.grid(column=4, row=1)
        team2_players.grid(column=4, row=2, columnspan=2)
        self.team2_suspended.grid(column=3, row=2)
        team2_logo.grid(column=5, row=1)

        if self.logo2.endswith("__logo.png"):
            team2_logo.destroy()

        # Init players
        ###########################################################################################
        for i, player in enumerate(self.players1):
            player.text_var = tk.StringVar(team1_players, value="{} [{:02d}]    {}".format(player.name, player.number, player.scores))
            tk.Label(team1_players, textvariable=player.text_var, font=f"Times, {int(13 * SCL)}").pack(padx=int(26 * SCL), pady=0)

        for i, player in enumerate(self.players2):
            player.text_var = tk.StringVar(team2_players,
                                           value="{} [{:02d}]    {}".format(player.name, player.number, player.scores))
            tk.Label(team2_players, textvariable=player.text_var, font=f"Times, {int(13 * SCL)}").pack(padx=int(26 * SCL), pady=0)

        # Main timer
        ###########################################################################################
        main_timer = tk.Frame(self.content, borderwidth=int(4 * SCL), relief="sunken")
        self.timer_text = tk.Label(main_timer, textvariable=self.time_var, font=f"Times, {int(74 * SCL)}")
        self.timer_text.grid(padx=int(16 * SCL), pady=int(4 * SCL))

        main_timer.grid(column=2, row=0, columnspan=2)

        # Match round
        ###########################################################################################
        match_round = tk.Frame(self.content, borderwidth=int(4 * SCL), relief="sunken")
        tk.Label(match_round, textvariable=self.round_num_var, font=f"Times, {int(53 * SCL)}").pack(padx=int(32 * SCL), pady=0)

        match_round.grid(column=2, row=1, columnspan=2)

        # Timeout timer
        ###########################################################################################
        self.time_out_timer_text = tk.Label(main_timer, textvariable=self.time_out_var, font=f"Times, {int(74 * SCL)}",
                                            foreground="darkred")
        self.time_out_timer_text.grid(padx=int(16 * SCL), pady=int(4 * SCL))
        self.time_out_timer_text.grid_remove()

        # Give some variables
        ###########################################################################################
        self.to_give_back(spec_time_out=lambda: self.time_out(),
                          spec_back_to_game=lambda: self.back_to_game(),
                          spec_team1_suspended=self.team1_suspended,
                          spec_team2_suspended=self.team2_suspended,
                          spec_close=lambda: self.close())

    def time_out(self):
        self.timer_text.grid_remove()
        self.time_out_timer_text.grid()

    def back_to_game(self):
        self.time_out_timer_text.grid_remove()
        self.timer_text.grid()

    def close(self) -> Tuple[int, int]:
        x = self.top_level.winfo_x()
        y = self.top_level.winfo_y()

        self.spectator_window.window = None
        self.top_level.destroy()
        return x, y
