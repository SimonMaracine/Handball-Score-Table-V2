import tkinter as tk
from src.timer import PlayerTimer


class Player:
    """Class representing a player"""

    def __init__(self, name: str, number: int, team, timer_on_finish):
        self.name = name
        self.number = number
        self.team = team
        self.scores = 0
        self.suspended = False
        self.disqualified = False
        self.yellow_cards = 0
        self.red_cards = 0
        self.timer = None
        self._suspend_text_var = tk.StringVar(value="{} | 00:00".format(self.number))
        self._timer_on_finish = timer_on_finish
        self._text_var = tk.StringVar()

    def __repr__(self):
        return "Player {} [{}] - {}".format(self.name, self.number, self.team)

    def score_up(self):
        """Increment player's scores and his/hers team's score"""
        self.scores += 1
        self.team.change_score(1)

    def score_down(self):
        """Decrement player's scores and his/hers team's score"""
        if self.scores >= 1:
            self.scores -= 1
            self.team.change_score(-1)

    def give_card(self, color: str):
        """Give player a yellow or red card

        A player can have a maximum of 2 yellow cards and 1 red card.
        If a card cannot be given, this method does nothing.

        Args:
            color (str): The type of card to give

        """
        if color == "red":
            if self.red_cards < 1:
                self.red_cards += 1
        else:
            if self.yellow_cards < 2:
                self.yellow_cards += 1

    def take_card(self, color: str):
        """Take from player a yellow or red card

        A player cannot have negative value cards.
        This method does nothing, if the player has 0 cards.

        Args:
            color (str): The type of card to give

        """
        if color == "red":
            if self.red_cards >= 1:
                self.red_cards -= 1
        else:
            if self.yellow_cards >= 1:
                self.yellow_cards -= 1

    def suspend(self, start=True):
        """Suspend a player

        This method does nothing, if the player is already suspended.

        Args:
            start (bool): Whether or not to start the timer immediately

        """
        if not self.suspended:
            self.timer = PlayerTimer(self._suspend_text_var, self._timer_on_finish, self, 120)
            if start:
                self.timer.start()
            self.suspended = True
        else:
            print("Player already suspended")

    def release(self):
        """Release a player

        This method does nothing, if the player is not suspended.

        """
        if self.suspended:
            self.suspended = False
            self.timer.stop()
        else:
            print("Player is not suspended")

    def can_suspend(self) -> bool:
        """Check if a player is not suspended

        Returns:
            bool: True if the player is not suspended, False otherwise

        """
        if not self.suspended:
            return True
        else:
            return False

    def can_release(self) -> bool:
        """Check if a player is suspended

        Returns:
            bool: True if the player is suspended, False otherwise

        """
        if self.suspended:
            return True
        else:
            return False

    def disqualify(self):
        pass
