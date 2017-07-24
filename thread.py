from instructions import Instructions
from players import Players
from gamblers import Gamblers
from rounds import Rounds
from updates import Updates

from misc import file_read, file_write, file_append

class Thread:
    FORMAT = """{instructions}

{rounds}


{gamblers}"""

    def __init__(self):
        self.instructions = Instructions()
        self.players = Players()
        self.gamblers = Gamblers()
        self.rounds = Rounds()
        self.updates = Updates()

        self.gambler = None
        self.round = None
        self.next_update_index = 0

    def __repr__(self):
        return self.FORMAT.format(
            instructions = self.instructions,
            gamblers = self.gamblers,
            rounds = self.rounds
            )



    def group(self, round_name, player_names):
        return self.rounds.get(round_name).group([self.players.get(player_name) for player_name in player_names])

    def bet(self, round_name, gambler_name, winner_name, loser_names, money, winning_score = -1):
        if isinstance(loser_names, str):
            loser_names = [loser_names]

        return self.rounds.get(round_name).bet(self.gamblers.get(gambler_name), self.players.get(winner_name), [self.players.get(loser_name) for loser_name in loser_names], money, winning_score)

    def win(self, round_name, winner_name, loser_names, winning_score):
        if isinstance(loser_names, str):
            loser_names = [loser_names]

        return self.updates.add(self.rounds.get(round_name).win(self.players.get(winner_name), [self.players.get(loser_name) for loser_name in loser_names], winning_score))

    def finish(self, round_name, player_names):
        return self.group(round_name, player_names).finish()


    def interpret(self, arguments):
        if arguments[0] == "thread":
            print self

        elif arguments[0] == "instructions":
            return self.instructions.interpret(arguments[1:])
        elif arguments[0] == "players":
            return self.players.interpret(arguments[1:])
        elif arguments[0] == "gamblers":
            return self.gamblers.interpret(arguments[1:])
        elif arguments[0] == "rounds":
            return self.rounds.interpret(arguments[1:])
        elif arguments[0] == "updates":
            return self.updates.interpret(arguments[1:])

        elif arguments[0] == "gambler":
            if len(arguments) == 1:
                print self.gambler.name
            elif arguments[1] in ["add", "set"]:
                self.gambler = self.gamblers.get(arguments[2])
                return self.gambler
        elif arguments[0] == "round":
            if len(arguments) == 1:
                print self.round.name
            elif arguments[1] in ["add", "set"]:
                self.round = self.rounds.get(arguments[2], " ".join(arguments[3:]))
                return self.round
            elif arguments[1] == "remove":
                pass
        elif arguments[0] == "group":
            return self.group(round_name = self.round.name, player_names = arguments[1:])
        elif arguments[0] == "bet":
            return self.bet(round_name = self.round.name, gambler_name = self.gambler.name, money = float(arguments[1]) * 100, winner_name = arguments[2], winning_score = int(arguments[3]), loser_names = arguments[4:])
        elif arguments[0] == "win":
            return self.win(round_name = self.round.name, winner_name = arguments[1], winning_score = int(arguments[2]), loser_names = arguments[3:])
        elif arguments[0] == "finish":
            return self.finish(round_name = self.round.name, player_names = arguments[1:])

        elif arguments[0] == "commit":
            return self.updates.commit()

        elif arguments[0] == "reload":
            self.__init__()
            self.load()
        elif arguments[0] == "undo":
            return self.undo()



    def load(self):
        for line in file_read("betting_history.txt").split("\n"):
            line = line.rstrip("\r")
            self.interpret(line.split(" "))
        self.save()

    def save(self):
        file_write("thread.txt", repr(self))
        file_write("updates.txt", repr(self.updates))

    def undo(self):
        lines = file_read("betting_history.txt").rstrip("\n").split("\n")
        print "Undo command: '{}'".format(lines[-1])
        file_write("betting_history.txt", "\n".join(lines[:-1]) + "\n")
        self.__init__()
        self.load()
