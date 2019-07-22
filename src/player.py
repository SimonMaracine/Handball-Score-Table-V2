import tkinter as tk
from src.timer import PlayerTimer


class Player:

    def __init__(self, name: str, number: int, team):
        self.name = name
        self.number = number
        self.team = team
        self.scores = 0
        self.suspended = False
        self.disqualified = False
        self.yellow_cards = 0
        self.red_cards = 0
        self.timer = None
        self.suspend_text_var = tk.StringVar(value="{} | 00:00".format(self.number))

    def __repr__(self):
        return "Player {} [{}] - {}".format(self.name, self.number, self.team)

    def score_up(self):
        self.scores += 1
        self.team.change_score(1)

    def score_down(self):
        if self.scores >= 1:
            self.scores -= 1
            self.team.change_score(-1)

    def give_card(self, color: str):
        if color == "red":
            if self.red_cards < 1:
                self.red_cards += 1
        else:
            if self.yellow_cards < 2:
                self.yellow_cards += 1

    def take_card(self, color: str):
        if color == "red":
            if self.red_cards >= 1:
                self.red_cards -= 1
        else:
            if self.yellow_cards >= 1:
                self.yellow_cards -= 1

    def suspend(self) -> bool:
        if not self.suspended:
            self.timer = PlayerTimer(self.suspend_text_var, self.number, 180)
            self.timer.start()
            self.suspended = True
            return True
        else:
            print("Player already suspended")
            return False

    def release(self):
        if self.suspended:
            self.timer.stop()
            self.suspended = False
        else:
            print("Player is not suspended")

    def can_release(self) -> bool:
        if self.suspended:
            return True
        else:
            return False

    def disqualify(self):
        pass
