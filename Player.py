class Player:

    def __init__(self, name, score = 0):
        self.name = name
        self.score = score
        self.cards = 0
        self.wants_to_leave = False
        self.commands = {
            "quit": self.quit
        }

    def add_score(self, score):
        self.score += score

    def set_score(self, score):
        self.score = score

    def give_card(self, card):
        self.cards += card

    def reset_cards(self):
        self.cards = 0

    def get_name(self):
        return self.name

    def think(self):
        # print(">>> %s is thinking"% self.name)
        line = input().rstrip()
        if line == "quit":
            self.quit()

    def quit(self):
        self.wants_to_leave = True

    def __repr__(self):
        return "Name: {0} Score: {1} Cards: {2}".format(self.name, self.score, self.cards)