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
    def write_games(games, file):
        fields = ['date', 'season', 'neutral', 'playoff', 'team1', 'team2', 'score1', 'score2', 'elo1', 'elo2', 'elo_prob1', 'result1']

        with open(file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames = fields)
            writer.writeheader()
            writer.writerows(games)