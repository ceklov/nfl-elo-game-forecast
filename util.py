import csv
from forecast import HFA

class Util:

    @staticmethod
    def read_games(file):
        games = [item for item in csv.DictReader(open(file))]

        for game in games:
            game['season'], game['neutral'], game['playoff'] = int(game['season']), int(game['neutral']), int(game['playoff'])
            game['score1'], game['score2'] = int(game['score1']) if game['score1'] != '' else None, int(game['score2']) if game['score2'] != '' else None
            game['elo_prob1'], game['result1'] = float(game['elo_prob1']) if game['elo_prob1'] != '' else None, float(game['result1']) if game['result1'] != '' else None

        return games
    
    @staticmethod
    def write_games(games, file):
        fields = ['date', 'season', 'neutral', 'playoff', 'team1', 'team2', 'elo1', 'elo2', 'score1', 'score2', 'elo_prob1', 'result1']

        with open(file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames = fields)
            writer.writeheader()
            writer.writerows(games)

    @staticmethod
    def print_betting_odds(game_odds):
        print("\n----------------------------------------------------------------------------\n")
        print("Forecasts for upcoming games:\n")
        print("\t\tTeam\t\tElo (Base)\tElo (HFA-Adj.)\tImplied\t\tAmerican\tDecimal\t\tSpread\n")

        for key, game in game_odds.items():
            # follows the convention to print away team before home team that seems prominent
            print(f"{game['date']}\t{game['team2']}\t\t{game['elo2']}\t{game['elo2']}\t{game['percentage2']}\t\t{game['american2']}\t\t{game['decimal2']:.2f}\t\t{game['spread2']}")
            print(f"\t\t@ {game['team1']}\t\t{game['elo1']}\t{float(game['elo1']) + HFA}\t{game['percentage1']}\t\t{game['american1']}\t\t{game['decimal1']:.2f}\t\t{game['spread1']}\n")
