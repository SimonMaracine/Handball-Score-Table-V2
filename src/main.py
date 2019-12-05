import sys
import time
import tkinter as tk
from os.path import join
from typing import Optional, List
from threading import RLock

import src.log
import src.spectator_window as spec
from gen_report import MatchData, RoundData, generate_report
from src.config_object import Config
from src.timer import Timer, SelfFixTimer, TimeOutTimer
from src.spectator_window import SpectatorWindow
from src.init_window import InitWindow
from src.preferences_window import PreferencesWindow
from src.player import Player
from src.team import Team
from src.alert_window import ask, info
from src.about_window import AboutWindow
from src.change_time_window import ChangeTimeWindow

logger = src.log.get_logger(__name__)
logger.setLevel(10)

if sys.platform == "linux":
    MainTimer = Timer
elif sys.platform == "win32":
    MainTimer = SelfFixTimer


class MainApplication:
    spectator_windows = []

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.option_add("*tearOff", False)
        self.root.minsize(width=1000, height=560)
        self.root.title("Handball Score Table")
        root.protocol("WM_DELETE_WINDOW", self.quit)
        menu_bar = tk.Menu()
        self.root.config(menu=menu_bar)
        self.content = tk.Frame(self.root, padx=8, pady=8)
        self.content.pack(expand=True)

        # File menu
        ###########################################################################################
        file_menu = tk.Menu(menu_bar)
        file_menu.add_command(label="New Match", state="normal", command=self.open_init_window)
        file_menu.add_command(label="Open Spectator Window", command=self.open_spectator_window)
        file_menu.add_command(label="Generate Match Report", command=self.generate_match_report)
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        ###########################################################################################
        edit_menu = tk.Menu(menu_bar)
        edit_menu.add_command(label="Preferences", command=self.open_preferences_window)
        edit_menu.add_command(label="Change Round Time", command=self.change_round_time)
        # edit_menu.add_command(label="Add player", command=None, state="disabled")
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Help menu
        ###########################################################################################
        help_menu = tk.Menu(menu_bar)
        help_menu.add_command(label="About", command=self.about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        # Containers
        ###########################################################################################
        container1 = tk.Frame(self.content)  # players, suspended, scores
        container3 = tk.Frame(self.content)  # right side
        container2 = tk.Frame(container3, borderwidth=2, relief="sunken", pady=6, padx=4)  # menu for players

        container1.grid(column=0, row=0, rowspan=3)
        container2.grid(column=0, row=2)
        container3.grid(column=1, row=1, padx=30)

        # Init teams and players
        ###########################################################################################
        self.team1 = Team("Home", 1)
        self.team2 = Team("Guest", 2)
        self.__selected_player: Optional[Player] = None
        self.suspended_players1: List[Player] = []
        self.suspended_players2: List[Player] = []
        self.is_time_out = False

        self.has_started_match = False
        # self.three_rounds_limit_hit = False

        self.match_data: Optional[MatchData] = None

        # Team 1
        ###########################################################################################
        self.name_team1_var = tk.StringVar(container1, value=self.team1.name)
        team1_name = tk.Frame(container1, borderwidth=4, relief="sunken")
        tk.Label(team1_name, textvariable=self.name_team1_var, font="Times, 18").pack(padx=8, pady=22)

        score1 = tk.Frame(container1)
        team1_score = tk.Frame(score1, borderwidth=3, relief="sunken")
        self.score_team1_var = tk.IntVar(container1, value=0)
        tk.Label(team1_score, textvariable=self.score_team1_var, font="Times, 26").pack(padx=12, pady=4)

        team1_players = tk.Frame(container1, borderwidth=3, relief="sunken")
        self.players1_list = tk.Listbox(team1_players, font="Times, 12", height=18)
        self.players1_list.bind("<<ListboxSelect>>", self.list_box_select)

        self.team1_suspended = tk.Frame(container1, borderwidth=4, relief="sunken", width=130, height=380)
        self.team1_suspended.pack_propagate(False)

        self.players1_list.pack(padx=2, pady=2)
        team1_score.grid(column=0, row=0)

        team1_name.grid(column=0, row=0)
        score1.grid(column=1, row=0)
        team1_players.grid(column=0, row=1)
        self.team1_suspended.grid(column=1, row=1)

        # Team 2
        ###########################################################################################
        self.name_team2_var = tk.StringVar(container1, value=self.team2.name)
        team2_name = tk.Frame(container1, borderwidth=4, relief="sunken")
        tk.Label(team2_name, textvariable=self.name_team2_var, font="Times, 18").pack(padx=8, pady=22)

        score2 = tk.Frame(container1)
        team2_score = tk.Frame(score2, borderwidth=3, relief="sunken")
        self.score_team2_var = tk.IntVar(container1, value=0)
        tk.Label(team2_score, textvariable=self.score_team2_var, font="Times, 26").pack(padx=12, pady=4)

        team2_players = tk.Frame(container1, borderwidth=3, relief="sunken")
        self.players2_list = tk.Listbox(team2_players, font="Times, 12", height=18)
        self.players2_list.bind("<<ListboxSelect>>", self.list_box_select)

        self.team2_suspended = tk.Frame(container1, borderwidth=4, relief="sunken", width=130, height=380, padx=0, pady=0)
        self.team2_suspended.pack_propagate(False)

        self.players2_list.pack(padx=2, pady=2)
        team2_score.grid(column=1, row=0)

        team2_name.grid(column=3, row=0)
        score2.grid(column=2, row=0)
        team2_players.grid(column=3, row=1)
        self.team2_suspended.grid(column=2, row=1)

        # Logos
        ###########################################################################################
        self.logo1 = join("data", "logos", "__logo.png")
        self.logo2 = self.logo1

        # Main timer
        ###########################################################################################
        self.time_var = tk.StringVar(container3, value="00:00")
        self.timer = MainTimer(self.time_var, None, 1200)
        self.time_var.set(self.timer.get_time())

        main_timer = tk.Frame(container3, borderwidth=5, relief="sunken")
        self.timer_text = tk.Label(main_timer, textvariable=self.time_var, font="Times, 67")
        self.timer_text.grid(column=0, row=0, columnspan=3)

        main_timer.grid(column=0, row=0, columnspan=2)

        # Match round
        ###########################################################################################
        match = tk.Frame(container3)
        match_round = tk.Frame(match, borderwidth=5, relief="sunken")
        self.round_num_var = tk.IntVar(container3, value=1)
        tk.Label(match_round, textvariable=self.round_num_var, font="Times, 50").pack(padx=30, pady=5)

        match_round.grid(column=0, row=0, rowspan=2, padx=8)
        match.grid(column=0, row=1, pady=10)

        # Timeout timer
        ###########################################################################################
        self.time_out_var = tk.StringVar(container3, value="00:00")
        self.time_out_timer = TimeOutTimer(self.time_out_var, lambda: self.back_to_game(), 60)
        self.time_out_var.set(self.time_out_timer.get_time())

        self.time_out_timer_text = tk.Label(main_timer, textvariable=self.time_out_var, font="Times, 70",
                                            foreground="darkred")
        self.time_out_timer_text.grid(column=0, row=0, columnspan=3)
        self.time_out_timer_text.grid_remove()

        # Timer buttons
        ###########################################################################################
        tk.Button(main_timer, text="Start", command=self.start).grid(column=0, row=1, pady=3)
        tk.Button(main_timer, text="Pause", command=self.pause).grid(column=1, row=1, pady=3)
        tk.Button(main_timer, text="Stop", command=self.stop).grid(column=2, row=1, pady=3)

        # Round buttons
        ###########################################################################################
        tk.Button(match, text="Advance", command=self.advance_round).grid(column=1, row=0)
        tk.Button(match, text="Reset", command=self.reset_current_round).grid(column=1, row=1)

        # Time out buttons
        ###########################################################################################
        tk.Button(score1, text="T", command=lambda: self.time_out(self.team1)).grid(column=1, row=0, sticky=tk.S, padx=2)
        tk.Button(score2, text="T", command=lambda: self.time_out(self.team2)).grid(column=0, row=0, sticky=tk.S, padx=2)

        # Menu for players
        ###########################################################################################
        self.player_selected_var = tk.StringVar(container2, value="Player selected: None")
        self.selected_scores_var = tk.StringVar(container2, value="Score: n/a")
        self.selected_cards_var = tk.StringVar(container2, value="Cards: n/a")

        tk.Label(container2, textvariable=self.player_selected_var).grid(column=0, row=0, columnspan=2)
        tk.Label(container2, textvariable=self.selected_scores_var).grid(column=0, row=1)
        tk.Label(container2, textvariable=self.selected_cards_var).grid(column=1, row=1)
        tk.Button(container2, text="Score up",
                  command=self.score_up).grid(column=0, row=2, columnspan=1, sticky=tk.W)
        tk.Button(container2, text="Score down",
                  command=self.score_down).grid(column=0, row=3, columnspan=1, sticky=tk.W)
        tk.Button(container2, text="Suspend",
                  command=self.suspend).grid(column=1, row=2, columnspan=1, sticky=tk.E)
        tk.Button(container2, text="Release",
                  command=self.release).grid(column=1, row=3, columnspan=1, sticky=tk.E)
        tk.Button(container2, text="+ Yellow card",
                  command=lambda: self.give_card("yellow")).grid(column=0, row=4, columnspan=1, sticky=tk.W)
        tk.Button(container2, text="- Yellow card",
                  command=lambda: self.take_card("yellow")).grid(column=0, row=5, columnspan=1, sticky=tk.W)
        tk.Button(container2, text="+ Red card",
                  command=lambda: self.give_card("red")).grid(column=1, row=4, columnspan=1, sticky=tk.E)
        tk.Button(container2, text="- Red card",
                  command=lambda: self.take_card("red")).grid(column=1, row=5, columnspan=1, sticky=tk.E)
        tk.Button(container2, text="Disqualify",
                  command=self.disqualify).grid(column=0, row=6, columnspan=2)

        self.lock1 = RLock()
        self.lock2 = RLock()

    def run(self):
        self.root.mainloop()

    def list_box_select(self, event):
        widget = event.widget
        try:
            player_name_number: str = widget.get(int(widget.curselection()[0]))
        except IndexError:
            return

        self.__selected_player = self.get_selected_player_from_widget(player_name_number)
        logger.debug(self.__selected_player)

        self.player_selected_var.set("Player selected: " + self.__selected_player.name)
        self.selected_scores_var.set("Score: " + str(self.__selected_player.scores))
        self.selected_cards_var.set("Cards: " +
                                    "{} yellow, ".format(self.__selected_player.yellow_cards) +
                                    "{} red".format(self.__selected_player.red_cards))

    def get_selected_player_from_widget(self, player_name_number: str) -> Player:
        selected_player: Optional[Player] = None

        for player in self.team1.players + self.team2.players:
            if player_name_number == "{} [{:02d}]".format(player.name, player.number):
                selected_player = player

        assert selected_player is not None, "Could not find player " + player_name_number
        return selected_player

    def score_up(self):
        if self.__selected_player is None:
            return
        if self.__selected_player.disqualified:
            info(self.root, f"{self.__selected_player.name} is disqualified.")
            return
        self.__selected_player.score_up()
        self.selected_scores_var.set("Score: " + str(self.__selected_player.scores))
        self.__selected_player.text_var.set("{} [{:02d}]    {}".format(self.__selected_player.name,
                                                                       self.__selected_player.number,
                                                                       self.__selected_player.scores))
        if self.__selected_player.team.order == 1:
            self.score_team1_var.set(self.__selected_player.team.score)
        else:
            self.score_team2_var.set(self.__selected_player.team.score)

    def score_down(self):
        if self.__selected_player is None:
            return
        if self.__selected_player.disqualified:
            info(self.root, f"{self.__selected_player.name} is disqualified.")
            return
        self.__selected_player.score_down()
        self.selected_scores_var.set("Score: " + str(self.__selected_player.scores))
        self.__selected_player.text_var.set("{} [{:02d}]    {}".format(self.__selected_player.name,
                                                                       self.__selected_player.number,
                                                                       self.__selected_player.scores))
        if self.__selected_player.team.order == 1:
            self.score_team1_var.set(self.__selected_player.team.score)
        else:
            self.score_team2_var.set(self.__selected_player.team.score)

    def give_card(self, color: str):
        if self.__selected_player is None:
            return
        if self.__selected_player.disqualified:
            info(self.root, f"{self.__selected_player.name} is disqualified.")
            return
        self.__selected_player.give_card(color)
        self.selected_cards_var.set("Cards: " +
                                    "{} yellow, ".format(self.__selected_player.yellow_cards) +
                                    "{} red".format(self.__selected_player.red_cards))
        self.__selected_player.text_var.set("{} [{:02d}]    {}".format(self.__selected_player.name,
                                                                       self.__selected_player.number,
                                                                       self.__selected_player.scores))

    def take_card(self, color: str):
        if self.__selected_player is None:
            return
        if self.__selected_player.disqualified:
            info(self.root, f"{self.__selected_player.name} is disqualified.")
            return
        self.__selected_player.take_card(color)
        self.selected_cards_var.set("Cards: " +
                                    "{} yellow, ".format(self.__selected_player.yellow_cards) +
                                    "{} red".format(self.__selected_player.red_cards))
        self.__selected_player.text_var.set("{} [{:02d}]    {}".format(self.__selected_player.name,
                                                                       self.__selected_player.number,
                                                                       self.__selected_player.scores))

    def suspend(self):
        if self.__selected_player is None:
            return
        if self.__selected_player.disqualified:
            info(self.root, f"{self.__selected_player.name} is disqualified.")
            return
        if self.__selected_player.can_suspend():
            if not self.timer.get_going() or self.time_out_timer.get_going():
                self.__selected_player.suspend(start=False)
            else:
                self.__selected_player.suspend()

            if self.__selected_player.team.order == 1:
                self.put_suspended_player_on_main(1)
                self.put_suspended_player_on_spec(1)

                with self.lock1:
                    self.suspended_players1.append(self.__selected_player)
            else:
                self.put_suspended_player_on_main(2)
                self.put_suspended_player_on_spec(2)

                with self.lock2:
                    self.suspended_players2.append(self.__selected_player)

    def put_suspended_player_on_main(self, team: int):
        suspended = tk.Label(self.team1_suspended if team == 1 else self.team2_suspended,
                             textvariable=self.__selected_player.suspend_text_var,
                             font="Times, 12")

        suspended.pack(padx=10, pady=0)

        self.__selected_player.main_label = suspended

    def put_suspended_player_on_spec(self, team: int):
        try:
            spec_suspended = tk.Label(self.spec_team1_suspended if team == 1 else self.spec_team2_suspended,
                                      textvariable=self.__selected_player.suspend_text_var,
                                      font=f"Times, {int(13 * spec.SCL)}")
        except Exception:
            spec_suspended = None

        try:
            spec_suspended.pack(padx=int(24 * spec.SCL), pady=0)
        except AttributeError:
            pass

        self.__selected_player.spec_label = spec_suspended

    def release(self):
        if self.__selected_player is None:
            return
        if self.__selected_player.disqualified:
            info(self.root, f"{self.__selected_player.name} is disqualified.")
            return
        if self.__selected_player.can_release():
            if self.__selected_player.team.order == 1:
                with self.lock1:
                    for player in self.suspended_players1:
                        if int((player.main_label["text"])[0:2]) == self.__selected_player.number:
                            self.__selected_player.release()
                            player.main_label.destroy()
                            try:
                                player.spec_label.destroy()
                            except AttributeError:
                                pass
                            self.suspended_players1.remove(player)
                            break
                    else:
                        logger.info("Could not find " + str(self.__selected_player) + " in suspended players")
            else:
                with self.lock2:
                    for player in self.suspended_players2:
                        if int((player.main_label["text"])[0:2]) == self.__selected_player.number:
                            self.__selected_player.release()
                            player.main_label.destroy()
                            try:
                                player.spec_label.destroy()
                            except AttributeError:
                                pass
                            self.suspended_players2.remove(player)
                            break
                    else:
                        logger.info("Could not find " + str(self.__selected_player) + " in suspended players")

    def release_from_timer(self, player: Player):
        if player.team.order == 1:
            with self.lock1:
                for plr in self.suspended_players1:
                    if int((plr.main_label["text"])[0:2]) == player.number:
                        plr.release()
                        plr.main_label.destroy()
                        try:
                            plr.spec_label.destroy()
                        except AttributeError:
                            pass
                        self.suspended_players1.remove(plr)
                        logger.debug("Released " + plr.name)
                        break
                else:
                    logger.info("Could not find " + str(player) + " in suspended players")
        else:
            with self.lock2:
                for plr in self.suspended_players2:
                    if int((plr.main_label["text"])[0:2]) == player.number:
                        plr.release()
                        plr.main_label.destroy()
                        try:
                            plr.spec_label.destroy()
                        except AttributeError:
                            pass
                        self.suspended_players2.remove(plr)
                        logger.debug("Released " + plr.name)
                        break
                else:
                    logger.info("Could not find " + str(player) + " in suspended players")

    def disqualify(self):
        if self.__selected_player is None:
            return
        if self.__selected_player.disqualified:
            info(self.root, f"{self.__selected_player.name} is already disqualified.")
            return
        if ask(self.root, f"Are you sure you want to disqualify {self.__selected_player.name}?"):
            self.release()
            self.__selected_player.disqualify()

    def advance_round(self):
        if self.round_num_var.get() < 4:
            # Save current round data
            try:
                self.match_data.rounds.append(RoundData(self.team1, self.team2))
            except AttributeError:  # match_data is None
                logger.info("Teams aren't initialized")
            else:
                no_round = self.round_num_var.get()
                self.round_num_var.set(no_round + 1)  # TODO maybe improve this up a little bit

                self.reset_teams(self.team1.name, self.team2.name,
                                 list(map(lambda player: player.name, self.team1.players)),
                                 list(map(lambda player: player.name, self.team2.players)),
                                 list(map(lambda player: str(player.number), self.team1.players)),
                                 list(map(lambda player: str(player.number), self.team2.players)))
        else:
            logger.info("Max 3 rounds are allowed")

    def reset_current_round(self):
        self.reset_teams(self.team1.name, self.team2.name,
                         list(map(lambda player: player.name, self.team1.players)),
                         list(map(lambda player: player.name, self.team2.players)),
                         list(map(lambda player: str(player.number), self.team1.players)),
                         list(map(lambda player: str(player.number), self.team2.players)))

    def start(self):
        if not self.is_time_out:
            self.timer.start()
            self.do_players_timers(0)
        else:
            self.time_out_timer.start()

    def pause(self):
        if not self.is_time_out:
            self.timer.pause()
            self.do_players_timers(2)
        else:
            self.time_out_timer.pause()

    def stop(self):  # TODO rethink what this should do
        if not self.is_time_out:
            self.timer.stop()
            self.do_players_timers(1)
        else:
            self.time_out_timer.stop()
            self.back_to_game()

    def time_out(self, team: Team):
        if not self.is_time_out and self.timer.get_going():
            team.request_time_out()
            self.timer.pause()
            self.do_players_timers(2)
            self.timer_text.grid_remove()

            self.time_out_timer.start()
            self.time_out_timer_text.grid()
            self.is_time_out = True
            try:
                self.spec_time_out()
            except Exception:
                pass

    def back_to_game(self):
        self.time_out_timer_text.grid_remove()
        self.timer_text.grid()
        self.is_time_out = False
        try:
            self.spec_back_to_game()
        except Exception:
            pass

    def do_players_timers(self, todo: int):
        if todo == 0:  # start
            for player in self.team1.players + self.team2.players:
                if player.suspended:
                    player.timer.start()
                    time.sleep(0.014)
        elif todo == 1:  # stop
            for player in self.team1.players + self.team2.players:
                if player.suspended:
                    self.release_from_timer(player)
                    time.sleep(0.014)
        else:  # pause
            for player in self.team1.players + self.team2.players:
                if player.suspended:
                    player.timer.pause()
                    time.sleep(0.014)

    def reset_teams(self, team1_name: str, team2_name: str, players1: List[str], players2: List[str],
                    numbers1: List[str], numbers2: List[str]):
        # Reset these
        self.players1_list.delete(0, tk.END)
        self.players2_list.delete(0, tk.END)
        self.score_team1_var.set("0")
        self.score_team2_var.set("0")
        self.__selected_player = None
        self.player_selected_var.set("Player selected: None")
        self.selected_scores_var.set("Score: n/a")
        self.selected_cards_var.set("Cards: n/a")

        self.team1 = Team(team1_name, 1)
        self.team2 = Team(team2_name, 2)
        self.name_team1_var.set(self.team1.name)
        self.name_team2_var.set(self.team2.name)

        plrs1 = []
        plrs2 = []
        for name, number in zip(players1, numbers1):
            plrs1.append(Player(name, int(number), self.team1, self.release_from_timer))
        for name, number in zip(players2, numbers2):
            plrs2.append(Player(name, int(number), self.team2, self.release_from_timer))

        self.team1.players = plrs1
        self.team1.sort_players()
        for i, player in enumerate(self.team1.players):
            self.players1_list.insert(i, "{} [{:02d}]".format(player.name, player.number))

        self.team2.players = plrs2
        self.team2.sort_players()
        for i, player in enumerate(self.team2.players):
            self.players2_list.insert(i, "{} [{:02d}]".format(player.name, player.number))

    def apply_init_config(self, config: Config):
        # Reset some things
        self.stop()
        self.round_num_var.set("1")
        self.__selected_player = None
        self.player_selected_var.set("Player selected: None")
        self.selected_scores_var.set("Score: n/a")
        self.selected_cards_var.set("Cards: n/a")

        for window in MainApplication.spectator_windows:
            window.destroy()
        MainApplication.spectator_windows.clear()

        # Init suspend timers before init players
        Player.SUS_TIME = int(config.suspend)

        # Init players and teams
        self.reset_teams(config.team1, config.team2, config.players1, config.players2, config.numbers1, config.numbers2)

        # Init main timer
        self.timer = MainTimer(self.time_var, None, int(config.match) * 60)
        self.time_var.set(self.timer.get_time())

        # Init timeout timers
        self.time_out_timer = TimeOutTimer(self.time_out_var, lambda: self.back_to_game(), int(config.timeout))
        self.time_out_var.set(self.time_out_timer.get_time())

        # Init logos
        self.logo1 = config.logo1
        self.logo2 = config.logo2

        # Init the struct to hold the match data
        self.match_data = MatchData()

        self.has_started_match = True

    # def add_another_player(self, player_name: str, number: int, team):
    #     player = Player(player_name, number, team, self.release_from_timer)
    #     team.add_player(player)
    #     team.sort_players()
    #     if team.order == 1:
    #         self.players1_list.insert(tk.LAST, "{} [{:02d}]".format(player.name, player.number))
    #     else:
    #         self.players2_list.insert(tk.LAST, "{} [{:02d}]".format(player.name, player.number))

    def open_spectator_window(self):
        if len(MainApplication.spectator_windows) < 1:
            window = tk.Toplevel()
            MainApplication.spectator_windows.append(window)
            SpectatorWindow(window, players1=self.team1.players, players2=self.team2.players, time_var=self.time_var,
                            round_num_var=self.round_num_var, score_team1_var=self.score_team1_var,
                            score_team2_var=self.score_team2_var, name_team1_var=self.name_team1_var,
                            name_team2_var=self.name_team2_var, time_out_var=self.time_out_var,
                            logo1=self.logo1, logo2=self.logo2,
                            to_give_back=self.take_from_window, spectator_windows=MainApplication.spectator_windows)

            currently_selected_player = self.__selected_player
            with self.lock1:
                with self.lock2:
                    for suspended_player in self.suspended_players1 + self.suspended_players2:
                        self.__selected_player = suspended_player
                        self.put_suspended_player_on_spec(self.__selected_player.team.order)  # TODO might raise exception if selected player is None
            self.__selected_player = currently_selected_player

            if self.is_time_out:
                try:
                    self.spec_time_out()
                except Exception:
                    pass
        else:
            info(self.root, "There can only be one spectator window open.")

    def open_init_window(self):
        window = tk.Toplevel()
        InitWindow(window, self.apply_init_config)

    def take_from_window(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)

    @staticmethod
    def open_preferences_window():
        window = tk.Toplevel()
        PreferencesWindow(window)

    @staticmethod
    def help():
        pass

    @staticmethod
    def about():
        window = tk.Toplevel()
        AboutWindow(window)

    def quit(self):
        if self.has_started_match:
            if ask(self.root, "Are you sure you want to exit?"):
                self.root.quit()
        else:
            self.root.quit()

    def change_round_time(self):
        if self.timer.get_going():
            logger.info("Stop the timer first!")
            return

        def on_apply(seconds: int):
            self.timer = MainTimer(self.time_var, None, seconds * 60)
            self.time_var.set(self.timer.get_time())
            logger.debug("Main timer reset")

        window = tk.Toplevel()
        ChangeTimeWindow(window, on_apply)

    def generate_match_report(self):
        generate_report(self.match_data)


def main():
    root = tk.Tk()
    MainApplication(root).run()
