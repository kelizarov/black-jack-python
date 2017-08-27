from Types import Cards

from Player import Player


class AI(Player):

    def __init__(self, name, score = 0):
        super().__init__(name, score)

    def give_card(self, card):
        self.points += Cards.cards[card]
        self.number_of_cards += 1

    def think(self, state):
        pass