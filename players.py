class Players:
    def __init__(self):
        self.players = []

    def get(self, name):
        for player in self.players:
            if player.name == name:
                return player

        player = Player(name)
        self.players.append(player)
        return player

    def interpret(self, arguments):
        pass

class Player:
    FORMAT = "{name}"

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.FORMAT.format(name = self.name)
