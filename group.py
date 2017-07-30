from bet import Bet
from odds import Odds
from updates import Update

from utils.strings import str_money


class Group:
    FORMAT = "[tr] [td][color=#{color}]{player1} vs. {player2}[/color][/td] [td][color=#{color}]{pool}[/color][/td] " \
             "[td][color=#{color}]{odds1}, {odds2}[/color][/td] [td][color=#{color}]{winner} {score}[/color][/td] [/tr]"

    def __init__(self, round, players, initial_pool=50000):
        self.round, self.players, self.initial_pool = round, players, initial_pool

        self.is_finished = False
        self.winner = None
        self.winning_score = None

        self.bets = []

    def __repr__(self):
        if len(self.players) == 2:
            odds = self.odds()
            return self.FORMAT.format(
                player1=self.players[0],
                player2=self.players[1],
                pool=str_money(self.pool()),
                odds1=odds[0],
                odds2=odds[1],
                winner=self.winner if self.winner is not None else "",
                score=self.score(),
                color="AAAAAA" if self.is_finished else "666666"
            )
        else:
            pass  # TODO

    def bet(self, gambler, winner, money, winning_score):
        for bet in self.bets:
            if bet.gambler == gambler:
                self.bets.remove(bet)

        bet = Bet(gambler, winner, money, winning_score)
        self.bets.append(bet)
        self.bets = sorted(self.bets, key=lambda bet: -bet.money)
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

        return sorted(odds, key=lambda o: -o.proportion)

    def score(self):
        return "{}-{}".format(self.winning_score, 5 - self.winning_score) if self.winning_score is not None else ""

    def win(self, winner, winning_score):
        self.winner = winner
        self.winning_score = winning_score
        self.is_finished = True

        return Update(self, winner, winning_score)

    def finish(self):
        self.is_finished = True

        return True
