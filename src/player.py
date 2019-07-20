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

    def __str__(self):
        return "Player {}[{}] - {}".format(self.name, self.number, self.team)

    def score_up(self):
        self.scores += 1

    def score_down(self):
        if self.scores >= 1:
            self.scores -= 1

    def give_card(self, color: str):
        if color == "red":
            self.red_cards += 1
        else:
            self.yellow_cards += 1

    def take_card(self, color: str):
        if color == "red":
            if self.red_cards >= 1:
                self.red_cards -= 1
        else:
            if self.yellow_cards >= 1:
                self.yellow_cards -= 1

    def suspend(self):
        pass

    def release(self):
        pass
