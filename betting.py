# -*- coding: cp1252 -*-

def str_money(money):
    cents = int(abs(money) % 100)
    return "{sign}${dollars}.{cents}".format(
        sign = "-" if money < 0 else "",
        dollars = abs(int(money / 100.)),
        cents = ("0" if cents < 10 else "") + str(cents)
        )

def str_list(list_):
    return list_[0] if len(list_) == 1 else (", ".join(list_[:-1]) + " & " + list_[-1])

def file_read(file_name):
    file_ = open(file_name, "r")
    contents = file_.read()
    file_.close()
    return contents

def file_write(file_name, string):
    file_ = open(file_name, "w")
    file_.write(string)
    file_.close()

def file_append(file_name, string):
    file_ = open(file_name, "a")
    file_.write(string)
    file_.close()



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
            if arguments[1] in ["add", "set"]:
                self.gambler = self.gamblers.get(arguments[2])
                return self.gambler
        elif arguments[0] == "round":
            if arguments[1] in ["add", "set"]:
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
            
        elif arguments[0] == "commit":
            return self.updates.commit()



    def load(self):
        for line in file_read("betting_history.txt").split("\n"):
            self.interpret(line.split(" "))
    
    def save(self):
        file_write("thread.txt", repr(self))
        file_write("updates.txt", repr(self.updates))
        
class Instructions:
    FORMAT = file_read("instructions.txt")

    def __init__(self):
        pass

    def __repr__(self):
        return self.FORMAT

    def interpret(self, arguments):
        if len(arguments) == 0:
            print self

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

class Gamblers:
    FORMAT = """[b][size=5]Standings[/size][/b]


[table]
[tr] [td][b]Player[/b][/td] [td][b]Net $[/b][/td] [td][b]Predictions Correct[/b][/td] [td][b]Correct %[/b][/td] [/tr]
{gamblers}
[tr] [td]––––––––––––[/td] [td]––––––––––––[/td] [td]––––––––––––––––––––[/td] [td]––––––––[/td]
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
        self.gamblers = sorted(sorted(self.gamblers, key = lambda gambler: gambler.name), key = lambda gambler: -gambler.money)
        return self.FORMAT.format(gamblers = "\n".join([repr(gambler) for gambler in self.gamblers if gambler.predictions_made > 0]))

    def interpret(self, arguments):
        if len(arguments) == 0:
            print self
        elif arguments[0] == "get":
            print self.get(" ".join(arguments[1:]))

class Rounds:
    FORMAT = "{rounds}"

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
        return self.FORMAT.format(rounds = "\n\n\n".join([repr(round) for round in self.rounds]))

    def interpret(self, arguments):
        if len(arguments) == 0:
            print self
        elif arguments[0] == "get":
            print self.get(" ".join(arguments[1:]))

class Updates:
    FORMAT = "{updates}"

    def __init__(self):
        self.updates = []

        self.next_update_index = 0

    def __repr__(self):
        return self.FORMAT.format(updates = "\n\n".join([repr(update) for update in self.updates[self.next_update_index:]]))

    def add(self, update):
        self.updates.append(update)
        return update

    def commit(self):
        self.next_update_index = len(self.updates)
        return self.next_update_index

    def interpret(self, arguments):
        print self



class Player:
    FORMAT = "{name}"
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.FORMAT.format(name = self.name)

class Gambler:
    FORMAT = "[tr] [td]{player}[/td] [td]{money}[/td] [td]{correct}/{total}[/td] [td]{percentage}%[/td] [/tr]"
    
    def __init__(self, name):
        self.name = name
        self.money = 0
        self.predictions_made = 0
        self.predictions_correct = 0

    def __repr__(self):
        return self.FORMAT.format(
            player = self.name,
            money = str_money(self.money),
            correct = self.predictions_correct,
            total = self.predictions_made,
            percentage = int(round(self.predictions_correct * 100.0 / self.predictions_made)) if self.predictions_made > 0 else ""
            )

class Round:
    FORMAT = """[b][size=5]{display_name}[/size][/b]


[table]
[tr] [td][b]Match[/b][/td] [td][b]Pool[/b][/td] [td][b]Betting odds[/b][/td] [td][b]Winner[/b][/td] [/tr]
{groups}
[tr] [td]––––––––––––––––––––––––[/td] [td]––––––––––––[/td] [td]––––––––––––––––––––––––––––[/td] [td]––––––––––––––––[/td] [/tr]
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

class Group:
    FORMAT = "[tr] [td][color=#{color}]{player1} vs. {player2}[/color][/td] [td][color=#{color}]{pool}[/color][/td] [td][color=#{color}]{odds1}, {odds2}[/color][/td] [td][color=#{color}]{winner} {score}[/color][/td] [/tr]"
    
    def __init__(self, round, players, initial_pool = 50000):
        self.round, self.players, self.initial_pool = round, players, initial_pool
        
        self.is_finished = False
        self.winner = None
        self.winning_score = 0
        
        self.bets = []

    def __repr__(self):
        if len(self.players) == 2:
            odds = self.odds()
            return self.FORMAT.format(
                player1 = self.players[0],
                player2 = self.players[1],
                pool = str_money(self.pool()),
                odds1 = odds[0],
                odds2 = odds[1],
                winner = self.winner if self.is_finished else "",
                score = self.score(),
                color = "AAAAAA" if self.is_finished else "666666"
                )
        else:
            pass # TODO

    def bet(self, gambler, winner, money, winning_score):
        for bet in self.bets:
            if bet.gambler == gambler:
                self.bets.remove(bet)

        bet = Bet(gambler, winner, money, winning_score)
        self.bets.append(bet)
        self.bets = sorted(self.bets, key = lambda bet: -bet.money)
        return bet

    def contains(self, players):
        for player in players:
            if player not in self.players:
                return False
        return True

    def pool(self):
        return self.initial_pool + sum(bet.money for bet in self.bets)

    def odds(self):
        pool = self.pool() + 0.0
        odds = []
        for player in self.players:
            player_totalbet = 0
            for bet in self.bets:
                if bet.winner == player:
                    player_totalbet += bet.money
            proportion = player_totalbet / pool
            odds.append(Odds(player, proportion))

        return sorted(odds, key = lambda o: -o.proportion)

    def score(self):
        return "{}-{}".format(self.winning_score, 5 - self.winning_score) if self.is_finished else ""

    def win(self, winner, winning_score):
        self.winner = winner
        self.winning_score = winning_score
        self.is_finished = True

        return Update(self, winner, winning_score)

class Odds:
    FORMAT = "{player} {odds}"
    STR_ODDS = ['1:0', '100:1', '50:1', '32:1', '25:1', '20:1', '15:1', '13:1', '11:1', '10:1',
        '9:1', '8:1', '7:1', '7:1', '6:1', '6:1', '5:1', '5:1', '4:1', '4:1',
        '4:1', '4:1', '7:2', '7:2', '3:1', '3:1', '3:1', '8:3', '5:2', '7:3',
        '7:3', '7:3', '2:1', '2:1', '2:1', '2:1', '5:3', '5:3', '5:3', '3:2',
        '3:2', '3:2', '4:3', '4:3', '5:4', '5:4', '6:5', '6:5', '1:1', '1:1',
        '1:1', '1:1', '1:1', '5:6', '5:6', '4:5', '4:5', '3:4', '3:4', '2:3',
        '2:3', '2:3', '3:5', '3:5', '3:5', '1:2', '1:2', '1:2', '1:2', '3:7',
        '3:7', '3:7', '2:5', '3:8', '1:3', '1:3', '1:3', '2:7', '2:7', '1:4',
        '1:4', '1:4', '1:4', '1:5', '1:5', '1:6', '1:6', '1:7', '1:7', '1:8',
        '1:9', '1:10', '1:11', '1:13', '1:15', '1:20', '1:25', '1:32', '1:50', '1:100', '0:1']
    
    def __init__(self, player, proportion):
        self.player, self.proportion = player, proportion

    def __repr__(self):
        return self.FORMAT.format(
            player = self.player.name,
            odds = self.STR_ODDS[int(round(self.proportion * 100))]
            )

class Bet:
    def __init__(self, gambler, winner, money, winning_score = -1):
        self.gambler, self.winner, self.money, self.winning_score = gambler, winner, money, winning_score

class Update:
    FORMAT = """{winner} {score} {loser}

{payouts}"""
    
    def __init__(self, group, winner, winning_score):
        self.group = group
        self.winner = winner
        self.winning_score = winning_score

        self.payouts = []

        self.update()

    def update(self):
        payouts = []
        
        sum_winning_bets = sum([bet.money for bet in self.group.bets if bet.winner == self.winner])

        for bet in self.group.bets:
            bet.gambler.predictions_made += 1
            net = -bet.money

            if bet.winner == self.winner:
                bet.gambler.predictions_correct += 1
                net += bet.money * self.group.pool() / sum_winning_bets

            payouts.append(Payout([bet], net))

        sum_net_gains = sum([payout.net for payout in payouts if payout.net >= 0])

        for payout in payouts:
            if payout.net > 0 and payout.bets[0].winning_score == self.winning_score:
                payout.net *= 1.5

        new_sum_net_gains = sum([payout.net for payout in payouts if payout.net >= 0])

        for payout in payouts:
            if payout.net > 0:
                payout.net *= sum_net_gains / (new_sum_net_gains + 0.0)

        for payout in payouts:
            self.payout(payout.bets[0], payout.net)

        for payout in self.payouts:
            for bet in payout.bets:
                bet.gambler.money += payout.net

    def __repr__(self):
        return self.FORMAT.format(
            winner = self.winner,
            loser = self.losers()[0],
            score = self.group.score(),
            payouts = "\n".join([repr(payout) for payout in self.payouts])
            )

    def losers(self):
        return [player for player in self.group.players if player != self.winner]

    def payout(self, bet, net):
        for payout in self.payouts:
            if payout.net == net:
                payout.bets.append(bet)
                payout.bets = sorted(payout.bets, key = lambda bet: bet.gambler.name)
                return payout

        payout = Payout([bet], net)
        self.payouts.append(payout)
        self.payouts = sorted(self.payouts, key = lambda payout: -payout.net)
        return payout

class Payout:
    FORMAT = "{gamblers}: {sign}{money}"
    
    def __init__(self, bets, net):
        self.bets, self.net = bets, net

    def __repr__(self):
        return self.FORMAT.format(
            gamblers = str_list([bet.gambler.name for bet in self.bets]),
            sign = "+" if self.net > 0 else "",
            money = str_money(self.net)
            )

def run():
    thread = Thread()
    thread.load()

    while True:
        line = raw_input("> ")
        if line == "exit":
            return
        
        if thread.interpret(line.split(" ")) != None:
            file_append("betting_history.txt", line + "\n")
            thread.save()

if __name__ == "__main__":
    run()
