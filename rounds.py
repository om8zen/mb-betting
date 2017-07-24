from group import Group

class Rounds:
    FORMAT = """{rounds_in_progress}

[spoiler]
{finished_rounds}
[/spoiler]"""

    def __init__(self):
        self.rounds = []

    def get(self, name, display_name = None):
        for round in self.rounds:
            if round.name == name:
                return round

        round = Round(name, display_name)
        self.rounds.append(round)
        return round

    def __repr__(self):
        return self.FORMAT.format(
            rounds_in_progress = "\n\n\n".join([repr(round) for round in self.rounds if not round.is_finished()]),
            finished_rounds = "\n\n\n".join([repr(round) for round in self.rounds if round.is_finished()])
            )

    def interpret(self, arguments):
        if len(arguments) == 0:
            print self
        elif arguments[0] == "get":
            print self.get(" ".join(arguments[1:]))

class Round:
    FORMAT = """[b][size=5]{display_name}[/size][/b]


[table]
[tr] [td][b]Match[/b][/td] [td][b]Pool[/b][/td] [td][b]Betting odds[/b][/td] [td][b]Winner[/b][/td] [/tr]
{groups}
[tr] [td]________________________[/td] [td]____________[/td] [td]________________________________[/td] [td]________________[/td] [/tr]
[/table]"""

    def __init__(self, name, display_name):
        self.name, self.display_name = name, display_name

        self.groups = []

    def __repr__(self):
        return self.FORMAT.format(
            display_name = self.display_name,
            groups = "\n".join([repr(group) for group in self.groups])
        )

    def group(self, players):
        for group in self.groups:
            if group.contains(players):
                return group

        group = Group(self, players)
        self.groups.append(group)
        return group

    def bet(self, gambler, winner, losers, money, winning_score = -1):
        return self.group([winner] + losers).bet(gambler, winner, money, winning_score)

    def win(self, winner, losers, winning_score):
        return self.group([winner] + losers).win(winner, winning_score)

    def is_finished(self):
        return len([group for group in self.groups if not group.is_finished]) == 0
