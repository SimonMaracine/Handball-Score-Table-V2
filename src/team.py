class Team:
    """Class representing a team

    Holds all the players, i.e. all the data.
    """

    def __init__(self, name: str, order: int):
        self.name = name
        self.order = order
        self.players = []
        self.score = 0
        self.time_out_requests = 0

    def __str__(self):
        return "Team {}".format(self.name)

    def change_score(self, x: int):
        """Increment team's score upwards or downwards

        Args:
            x (int): Negative to decrement the score, positive to increment

        """
        if x >= 0:
            self.score += 1
        else:
            if self.score >= 1:
                self.score -= 1

    def add_player(self, player):
        """Adds a player into the players list"""
        self.players.append(player)

    def sort_players(self):
        """Sorts the players alphabetically"""
        self.players.sort(key=lambda player: player.name)

    def request_time_out(self):
        """Increments the time_out_requests variable"""
        self.time_out_requests += 1
