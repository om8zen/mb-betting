from misc import str_money

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
