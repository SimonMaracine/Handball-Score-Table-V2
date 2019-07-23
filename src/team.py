class Team:

    def __init__(self, name: str, order: int):
        self.name = name
        self.order = order
        self.players = []
        self.score = 0
        self.time_out_requests = 0

    def __str__(self):
        return "Team {}".format(self.name)

    def change_score(self, x: int):
        if x >= 0:
            self.score += 1
        else:
            if self.score >= 1:
                self.score -= 1

    def add_player(self, player):
        self.players.append(player)

    def sort_players(self):
        self.players.sort(key=lambda player: player.name)

    def request_time_out(self):
        self.time_out_requests += 1
