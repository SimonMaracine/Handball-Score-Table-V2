import logging
import tkinter as tk
from typing import Optional, Callable

import src.log
from src.timer import PlayerTimer

logger = src.log.get_logger(__name__)
logger.setLevel(logging.DEBUG)


class Player:
    """Class representing a player"""
    SUS_TIME = 120

    def __init__(self, name: str, number: int, team, timer_on_finish: Callable):
        self.name = name
        self.number = number
        self.team = team
        self._timer_on_finish = timer_on_finish

        self.scores = 0
        self.suspended = False
        self.disqualified = False
        self.yellow_cards = 0
        self.red_cards = 0

        self.timer: Optional[PlayerTimer] = None
        self.suspend_text_var = tk.StringVar(value="{:02d} | {}".format(self.number, PlayerTimer.repr(self.SUS_TIME)))
        self.text_var = tk.StringVar()

        self.main_label: Optional[tk.Label] = None
        self.spec_label: Optional[tk.Label] = None

    def __repr__(self):
        return "Player {} [{:02d}] - {}".format(self.name, self.number, self.team)

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
            self.timer = PlayerTimer(self.suspend_text_var, self._timer_on_finish, self, Player.SUS_TIME)
            if start:
                self.timer.start()
            self.suspended = True
        else:
            logger.debug("Player already suspended")

    def release(self):
        """Release a player

        This method does nothing, if the player is not suspended.

        """
        if self.suspended:
            self.suspended = False
            self.timer.stop()
        else:
            logger.debug("Player is not suspended")

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
        self.disqualified = True
