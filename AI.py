from Player import Player


class AI(Player):

    def __init__(self, name):
        super().__init__(name)

    def take_card(self, card):
        self.points += card
        self.number_of_cards += 1

    def think(self, state):
        pass

    def notify(self, msg):
        pass