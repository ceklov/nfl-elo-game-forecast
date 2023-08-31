import csv

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
    def evaluate_forecasts(games):

        upcoming_games = [g for g in games if g['result1'] == None and 'my_prob1' in g]

        if len(upcoming_games) > 0:
            print("\n----------------------------------------------------------------------------\n")
            print("Forecasts for upcoming games:\n")
            print("\t\tTeams\t\tProbA\tSpreadA\t\tDecA\t\tDecB\n")
            for game in upcoming_games:
                spread = round(-1*(float(game['elo2'])-float(game['elo1']))/25.0*2)/2 # (x*2)/2 rounds to the nearest 0.5
                
                print("%s\t%s vs. %s\t%s%%\t%.1f\t\t%.2f\t\t%.2f" % (game['date'], game['team1'], game['team2'], int(round(100*game['elo_prob1'])), spread, 1/game['elo_prob1'], 1/(1-game['elo_prob1'])))
