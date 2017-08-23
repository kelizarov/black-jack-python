class Player:

    def __init__(self, name, score = 0):
        self.name = name
        self.score = score
        self.cards = 0
        self.commands = {}

    def add_score(self, score):
        self.score = self.score + score
        print(">>> {0} has new score {1}".format(self.name, self.score))

    def set_score(self, score):
        self.score = score
        print(">>> {0} has new score {1}".format(self.name, self.score))

    def give_card(self, card):
        self.cards += card

    def reset_cards(self):
        self.cards = 0

    def get_name(self):
        return self.name

    def think(self):
        print(">>> %s is thinking"% self.name)

    def __repr__(self):
        return "Name: {0} Score: {1} Cards: {2}".format(self.name, self.score, self.cards)