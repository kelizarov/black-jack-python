from Types import ModeState
from InputHandler import InputHandler


class Player:

    def __init__(self, name, score = 0):
        self.input = InputHandler(False)
        self.wants_to_leave = False

        self.name = name
        self.score = score
        self.points = 0
        self.bid = 0
        self.pocket = 500
        self.number_of_cards = 0

        self.commands = {
            "quit": self.quit,
            "place_bid": self.place_bid
        }

    def add_score(self, score):
        self.score += score

    def set_score(self, score):
        self.score = score

    def set_points(self, points):
        self.points = points

    def give_card(self, card):
        self.points += card
        self.number_of_cards += 1

    def reset_cards(self):
        self.points = 0
        self.number_of_cards = 0

    def get_name(self):
        return self.name

    def think(self, state):
        line = input().rstrip()
        if line == "quit":
            self.quit()
            return
        if state == ModeState.BIDDING:
            if int(line):
                self.place_bid(int(line))
        elif state == ModeState.ROUND:
            pass

        # self.input.execute_command(line, self.commands, False)

    def quit(self):
        self.wants_to_leave = True
        return "{0} decided to quit".format(self.name)

    def place_bid(self, bid_amount):
        if bid_amount > 0 and self.pocket >= bid_amount:
            self.bid += bid_amount

    def notify(self, msg):
        print(msg)

    def __repr__(self):
        return "Name: {0} Score: {1} Cards: {2} Pocket: {3}".format(self.name, self.score, self.points, self.pocket)