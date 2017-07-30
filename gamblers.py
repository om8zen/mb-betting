from utils.strings import str_money


class Gamblers:
    FORMAT = """[b][size=5]Standings[/size][/b]


[table]
[tr] [td][b]Player[/b][/td] [td][b]Net $[/b][/td] [td][b]Predictions Correct[/b][/td] [td][b]Correct %[/b][/td] [/tr]
{gamblers}
[tr] [td]____________[/td] [td]____________[/td] [td]____________________[/td] [td]________[/td]
[/table]"""

    def __init__(self):
        self.gamblers = []

    def get(self, name):
        for gambler in self.gamblers:
            if gambler.name == name:
                return gambler

        gambler = Gambler(name)
        self.gamblers.append(gambler)
        return gambler

    def __repr__(self):
        self.gamblers = sorted(
            sorted(self.gamblers, key=lambda gambler: gambler.name),
            key=lambda gambler: -gambler.money
        )
        return self.FORMAT.format(
            gamblers="\n".join([repr(gambler) for gambler in self.gamblers if gambler.predictions_made > 0])
        )

    def interpret(self, arguments):
        if len(arguments) == 0:
            print(self)
        elif arguments[0] == "get":
            print(self.get(" ".join(arguments[1:])))


class Gambler:
    FORMAT = "[tr] [td]{player}[/td] [td]{money}[/td] [td]{correct}/{total}[/td] [td]{percentage}%[/td] [/tr]"

    def __init__(self, name):
        self.name = name
        self.money = 0
        self.predictions_made = 0
        self.predictions_correct = 0

    def __repr__(self):
        return self.FORMAT.format(
            player=self.name,
            money=str_money(self.money),
            correct=self.predictions_correct,
            total=self.predictions_made,
            percentage=int(
                round(self.predictions_correct * 100.0 / self.predictions_made)
            ) if self.predictions_made > 0 else ""
        )
