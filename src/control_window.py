import tkinter as tk

from src.timer import Timer
from src.spectator_window import SpectatorWindow
from src.player import Player
from src.team import Team


class ControlWindow:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.option_add("*tearOff", False)
        self.root.minsize(width=1235, height=690)
        menu_bar = tk.Menu()
        self.root.config(menu=menu_bar)
        self.content = tk.Frame(self.root)
        self.content.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # File menu
        ###########################################################################################
        file_menu = tk.Menu(menu_bar)
        file_menu.add_command(label="New", state="disabled")
        file_menu.add_command(label="Open spectator window", command=self.open_spectator_window)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        ###########################################################################################
        edit_menu = tk.Menu(menu_bar)
        edit_menu.add_command(label="Preferences", state="disabled")
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Help menu
        ###########################################################################################
        help_menu = tk.Menu(menu_bar)
        help_menu.add_command(label="About", command=self.say_hello)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        # Containers
        ###########################################################################################
        container1 = tk.Frame(self.content)  # players, suspended, scores
        container2 = tk.Frame(self.content, borderwidth=2, relief="sunken", pady=6, padx=4)  # menu for players

        container1.grid(column=0, row=0, rowspan=3)
        container2.grid(column=1, row=2)

        # Init teams and players
        ###########################################################################################
        self.team1 = Team("The Team", 1)
        self.team2 = Team("Double Power", 2)

        self.__players1 = (Player("Theodore", 16, self.team1),
                           Player("Simon", 17, self.team1),
                           Player("Jane", 18, self.team1))

        self.__players2 = (Player("Paul", 29, self.team2),
                           Player("Andrew", 64, self.team2))

        for player in self.__players1:
            self.team1.add_player(player)
        for player in self.__players2:
            self.team2.add_player(player)

        print(self.team1.players)
        print(self.team2.players)

        self.team1.sort_players()
        self.team2.sort_players()
        print(self.team1.players)
        print(self.team2.players)

        self.__selected_player = None
        self.suspended_players1 = []
        self.suspended_players2 = []

        # Team 1
        ###########################################################################################
        team1_name = tk.Frame(container1, borderwidth=5, relief="sunken")
        if len(self.team2.name) >= 20:
            size = 14
        elif len(self.team2.name) >= 15:
            size = 18
        elif len(self.team2.name) >= 10:
            size = 27
        else:
            size = 28
        tk.Label(team1_name, text=self.team1.name, font="Times, {}".format(size)).pack(padx=10, pady=25)

        team1_score = tk.Frame(container1, borderwidth=3, relief="sunken")
        self.score_team1_var = tk.IntVar(container1, value=0)
        tk.Label(team1_score, textvariable=self.score_team1_var, font="Times, 35").pack(padx=30, pady=10)

        team1_players = tk.Frame(container1, borderwidth=3, relief="sunken")
        players1_list = tk.Listbox(team1_players, font="Times, 15", height=17)
        players1_list.bind("<<ListboxSelect>>", self.list_box_select)
        for i, player in enumerate(self.team1.players):
            players1_list.insert(i, "{} [{}]".format(player.name, player.number))

        self.team1_suspended = tk.Frame(container1, borderwidth=5, relief="sunken", width=185, height=420)
        self.team1_suspended.pack_propagate(False)

        players1_list.pack(padx=2, pady=2)

        team1_name.grid(column=0, row=0)
        team1_score.grid(column=1, row=0)
        team1_players.grid(column=0, row=1)
        self.team1_suspended.grid(column=1, row=1)

        # Team 2
        ###########################################################################################
        team2_name = tk.Frame(container1, borderwidth=5, relief="sunken")
        if len(self.team2.name) >= 20:
            size = 14
        elif len(self.team2.name) >= 15:
            size = 18
        elif len(self.team2.name) >= 10:
            size = 27
        else:
            size = 28
        tk.Label(team2_name, text=self.team2.name, font="Times, {}".format(size)).pack(padx=10, pady=25)

        team2_score = tk.Frame(container1, borderwidth=3, relief="sunken")
        self.score_team2_var = tk.IntVar(container1, value=0)
        tk.Label(team2_score, textvariable=self.score_team2_var, font="Times, 35").pack(padx=30, pady=10)

        team2_players = tk.Frame(container1, borderwidth=3, relief="sunken")
        players2_list = tk.Listbox(team2_players, font="Times, 15", height=17)
        players2_list.bind("<<ListboxSelect>>", self.list_box_select)
        for i, player in enumerate(self.team2.players):
            players2_list.insert(i, "{} [{}]".format(player.name, player.number))

        self.team2_suspended = tk.Frame(container1, borderwidth=5, relief="sunken", width=185, height=420)
        self.team2_suspended.pack_propagate(False)

        players2_list.pack(padx=2, pady=2)

        team2_name.grid(column=3, row=0)
        team2_score.grid(column=2, row=0)
        team2_players.grid(column=3, row=1)
        self.team2_suspended.grid(column=2, row=1)

        # Main timer
        ###########################################################################################
        self.time_var = tk.StringVar(self.content, value="00:00")
        timer = Timer(self.time_var, 3600)
        self.time_var.set(timer.get_time())

        main_timer = tk.Frame(self.content, borderwidth=5, relief="sunken")
        tk.Label(main_timer, textvariable=self.time_var, font="Times, 71").grid(column=0, row=0, columnspan=3)

        main_timer.grid(column=1, row=0)

        # Match round
        ###########################################################################################
        match_round = tk.Frame(self.content, borderwidth=5, relief="sunken")
        self.round_num_var = tk.IntVar(self.content, value=1)
        tk.Label(match_round, textvariable=self.round_num_var, font="Times, 50").pack(padx=30, pady=5)

        match_round.grid(column=1, row=1)

        # Timer buttons
        ###########################################################################################
        tk.Button(main_timer, text="Start", command=timer.start).grid(column=0, row=1)
        tk.Button(main_timer, text="Pause", command=timer.pause).grid(column=1, row=1)
        tk.Button(main_timer, text="Stop", command=timer.stop).grid(column=2, row=1)

        # Round number buttons
        ###########################################################################################
        ...

        # Menu for players
        ###########################################################################################
        self.player_selected_var = tk.StringVar(container2, value="Player selected: None")
        self.selected_scores_var = tk.StringVar(container2, value="Score: n/a")
        self.selected_cards_var = tk.StringVar(container2, value="Cards: None")

        tk.Label(container2, textvariable=self.player_selected_var).grid(column=0, row=0, columnspan=2)
        tk.Label(container2, textvariable=self.selected_scores_var).grid(column=0, row=1)
        tk.Label(container2, textvariable=self.selected_cards_var).grid(column=1, row=1)
        tk.Button(container2, text="Score up",
                  command=self.score_up).grid(column=0, row=2, columnspan=1)
        tk.Button(container2, text="Score down",
                  command=self.score_down).grid(column=0, row=3, columnspan=1)
        tk.Button(container2, text="Suspend",
                  command=self.suspend).grid(column=1, row=2, columnspan=1)
        tk.Button(container2, text="Release",
                  command=self.release).grid(column=1, row=3, columnspan=1)
        tk.Button(container2, text="+ Yellow card",
                  command=lambda: self.give_card("yellow")).grid(column=0, row=4, columnspan=1)
        tk.Button(container2, text="- Yellow card",
                  command=lambda: self.take_card("yellow")).grid(column=0, row=5, columnspan=1)
        tk.Button(container2, text="+ Red card",
                  command=lambda: self.give_card("red")).grid(column=1, row=4, columnspan=1)
        tk.Button(container2, text="- Red card",
                  command=lambda: self.take_card("red")).grid(column=1, row=5, columnspan=1)
        tk.Button(container2, text="Disqualify",
                  command=None).grid(column=0, row=6, columnspan=2)

    def run(self):
        self.root.mainloop()

    @staticmethod
    def say_hello():
        print("Hello")

    def list_box_select(self, event):
        widget = event.widget
        player_name_number: str = widget.get(int(widget.curselection()[0]))
        # print(player_name_number)

        selected_player = None
        for player in self.team1.players + self.team2.players:
            if player_name_number == "{} [{}]".format(player.name, player.number):
                selected_player = player

        assert selected_player is not None, "Could not find player " + player_name_number
        self.__selected_player = selected_player
        print(self.__selected_player)

        self.player_selected_var.set("Player selected: " + self.__selected_player.name)
        self.selected_scores_var.set("Score: " + str(self.__selected_player.scores))
        self.selected_cards_var.set("Cards: " +
                                    "{} yellow, ".format(self.__selected_player.yellow_cards) +
                                    "{} red".format(self.__selected_player.red_cards))

    def score_up(self):
        self.__selected_player.score_up()
        self.selected_scores_var.set("Score: " + str(self.__selected_player.scores))
        if self.__selected_player.team.order == 1:
            self.score_team1_var.set(self.__selected_player.team.score)
        else:
            self.score_team2_var.set(self.__selected_player.team.score)

    def score_down(self):
        self.__selected_player.score_down()
        self.selected_scores_var.set("Score: " + str(self.__selected_player.scores))
        if self.__selected_player.team.order == 1:
            self.score_team1_var.set(self.__selected_player.team.score)
        else:
            self.score_team2_var.set(self.__selected_player.team.score)

    def give_card(self, color: str):
        self.__selected_player.give_card(color)
        self.selected_cards_var.set("Cards: " +
                                    "{} yellow, ".format(self.__selected_player.yellow_cards) +
                                    "{} red".format(self.__selected_player.red_cards))

    def take_card(self, color: str):
        self.__selected_player.take_card(color)
        self.selected_cards_var.set("Cards: " +
                                    "{} yellow, ".format(self.__selected_player.yellow_cards) +
                                    "{} red".format(self.__selected_player.red_cards))

    def suspend(self):
        if self.__selected_player.suspend():
            if self.__selected_player.team.order == 1:
                suspended = tk.Label(self.team1_suspended, textvariable=self.__selected_player.suspend_text_var,
                                     font="Times, 15")
                self.suspended_players1.append(suspended)
            else:
                suspended = tk.Label(self.team2_suspended, textvariable=self.__selected_player.suspend_text_var,
                                     font="Times, 15")
                self.suspended_players2.append(suspended)

            suspended.pack(padx=26, pady=2)

    def release(self):
        if self.__selected_player.can_release():
            if self.__selected_player.team.order == 1:
                for suspended in self.suspended_players1:
                    # print(suspended["text"][0:2])
                    if int((suspended["text"])[0:2]) == self.__selected_player.number:
                        self.__selected_player.release()
                        suspended.destroy()
                        self.suspended_players1.remove(suspended)
                        break
                else:
                    print("Could not find " + str(self.__selected_player) + " in suspended players")
            else:
                for suspended in self.suspended_players2:
                    # print(suspended["text"][0:2])
                    if int((suspended["text"])[0:2]) == self.__selected_player.number:
                        self.__selected_player.release()
                        suspended.destroy()
                        self.suspended_players2.remove(suspended)
                        break
                else:
                    print("Could not find " + str(self.__selected_player) + " in suspended players")

    def open_spectator_window(self):
        window = tk.Toplevel()
        SpectatorWindow(window, time_var=self.time_var, round_num_var=self.round_num_var)

    def close_spectator_window(self):
        pass
