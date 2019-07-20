import tkinter as tk
from src.timer import Timer
from src.spectator_window import SpectatorWindow


class ControlWindow:

    def __init__(self, root: tk.Tk):
        self._root = root
        self._root.option_add("*tearOff", False)
        self._root.minsize(width=1400, height=700)
        menu_bar = tk.Menu()
        self._root.config(menu=menu_bar)
        self.content = tk.Frame(self._root)
        self.content.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # File menu
        ###########################################################################################
        file_menu = tk.Menu(menu_bar)
        file_menu.add_command(label="New", state="disabled")
        file_menu.add_command(label="Open Spectator window", command=self.open_spectator_window)
        file_menu.add_command(label="Exit", command=self._root.quit)
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
        container1 = tk.Frame(self.content)
        container2 = tk.Frame(self.content, borderwidth=2, relief="sunken")

        container1.grid(column=0, row=0, rowspan=3)
        container2.grid(column=1, row=2)

        # Team 1
        ###########################################################################################
        team1_name = tk.Frame(container1, borderwidth=5, relief="sunken", width=400, height=100)
        tk.Label(team1_name, text="Home", font="Times, 40").pack(padx=70, pady=20)

        team1_score = tk.Frame(container1, borderwidth=3, relief="sunken")
        score_team1 = tk.IntVar(container1, value=0)
        tk.Label(team1_score, text="{}".format(score_team1.get()), font="Times, 35").pack(padx=30, pady=10)

        team1_players = tk.Frame(container1, borderwidth=3, relief="sunken")
        players1 = tk.Listbox(team1_players, font="Times, 15", height=17)
        for i in range(5):
            players1.insert(i, "Player {}".format(i + 1))

        team1_suspended = tk.Frame(container1, borderwidth=5, relief="sunken")
        players_suspended1 = tk.Listbox(team1_suspended, font="Times, 14", width=14, height=17)
        for i in range(2):
            players_suspended1.insert(i, "I'm suspended")

        players1.pack(padx=2, pady=2)
        players_suspended1.pack(padx=2, pady=2)

        team1_name.grid(column=0, row=0)
        team1_score.grid(column=1, row=0)
        team1_players.grid(column=0, row=1)
        team1_suspended.grid(column=1, row=1)

        # Team 2
        ###########################################################################################
        team2_name = tk.Frame(container1, borderwidth=5, relief="sunken", width=400, height=100)
        tk.Label(team2_name, text="Guest", font="Times, 40").pack(padx=70, pady=20)

        team2_score = tk.Frame(container1, borderwidth=3, relief="sunken")
        score_team2 = tk.IntVar(container1, value=0)
        tk.Label(team2_score, text="{}".format(score_team2.get()), font="Times, 35").pack(padx=30, pady=10)

        team2_players = tk.Frame(container1, borderwidth=3, relief="sunken")
        players2 = tk.Listbox(team2_players, font="Times, 15", height=17)
        players2.bind("<<ListboxSelect>>", self.list_box_select)
        for i in range(5):
            players2.insert(i, "Player {}".format(i + 1))

        team2_suspended = tk.Frame(container1, borderwidth=5, relief="sunken")
        players_suspended2 = tk.Listbox(team2_suspended, font="Times, 14", width=14, height=17)
        for i in range(3):
            players_suspended2.insert(i, "I'm suspended")

        players2.pack(padx=2, pady=2)
        players_suspended2.pack(padx=2, pady=2)

        team2_name.grid(column=3, row=0)
        team2_score.grid(column=2, row=0)
        team2_players.grid(column=3, row=1)
        team2_suspended.grid(column=2, row=1)

        # Main timer
        ###########################################################################################
        self.time_var = tk.StringVar(self.content, value="0")  # time in seconds
        timer = Timer(self.time_var, 3600)
        self.time_var.set(timer.get_time())

        main_timer = tk.Frame(self.content, borderwidth=5, relief="sunken")
        tk.Label(main_timer, textvariable=self.time_var, font="Times, 75").grid(column=0, row=0, columnspan=3)

        main_timer.grid(column=1, row=0)

        # Match round
        ###########################################################################################
        match_round = tk.Frame(self.content, borderwidth=5, relief="sunken")
        self.round_num_var = tk.IntVar(self.content, value=1)
        tk.Label(match_round, text="{}".format(self.round_num_var.get()), font="Times, 55").pack(padx=40, pady=10)

        match_round.grid(column=1, row=1)

        # Timer buttons
        ###########################################################################################
        tk.Button(main_timer, text="Start", command=timer.start).grid(column=0, row=1)
        tk.Button(main_timer, text="Pause", command=timer.pause).grid(column=1, row=1)
        tk.Button(main_timer, text="Stop", command=timer.stop).grid(column=2, row=1)

        # Menu for players
        ###########################################################################################
        self.player_selected = tk.StringVar(container2, value="Player selected: None")
        self.selected_scores = tk.StringVar(container2, value="Score: 0")
        self.selected_cards = tk.StringVar(container2, value="Cards: None")

        tk.Label(container2, textvariable=self.player_selected).grid(column=0, row=0, columnspan=2)
        tk.Label(container2, textvariable=self.selected_scores).grid(column=0, row=1)
        tk.Label(container2, textvariable=self.selected_cards).grid(column=1, row=1)
        tk.Button(container2, text="Score up", command=None).grid(column=0, row=2, columnspan=2)
        tk.Button(container2, text="Score down", command=None).grid(column=0, row=3, columnspan=2)
        tk.Button(container2, text="Suspend", command=None).grid(column=0, row=4, columnspan=2)
        tk.Button(container2, text="Release", command=None).grid(column=0, row=5, columnspan=2)
        tk.Button(container2, text="+ Yellow card", command=None).grid(column=0, row=6, columnspan=2)
        tk.Button(container2, text="- Yellow card", command=None).grid(column=0, row=7, columnspan=2)
        tk.Button(container2, text="+ Red card", command=None).grid(column=0, row=8, columnspan=2)
        tk.Button(container2, text="- Red card", command=None).grid(column=0, row=9, columnspan=2)
        tk.Button(container2, text="Disqualify", command=None).grid(column=0, row=10, columnspan=2)

    def run(self):
        self._root.mainloop()

    @staticmethod
    def say_hello():
        print("Hello")

    def list_box_select(self, event):
        widget = event.widget
        player = widget.get(int(widget.curselection()[0]))
        self.player_selected.set("Player selected: " + player)
        print(player)

    def open_spectator_window(self):
        window = tk.Toplevel()
        SpectatorWindow(window, time_var=self.time_var, round_num_var=self.round_num_var)

    def close_spectator_window(self):
        pass
