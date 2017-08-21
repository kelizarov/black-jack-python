class Player:

    def __init__(self, name, score = 0):
        self.name = name
        self.score = score
        print(">>> %s has been added" % name)

    def add_score(self, score):
        self.score = self.score + score
        print(">>> %s updated his score" % self.name)
        print(">>> %d new score" % self.score)

    def set_score(self, score):
        self.score = score
        print(">>> %s updated his score" % self.name)
        print(">>> %d new score" % self.score)

    def get_name(self):
        return self.name

    def __think(self):
        print(">>> %s is thinking", self.name)