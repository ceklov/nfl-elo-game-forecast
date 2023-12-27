import csv
import math
import datetime
from datetime import date
from datetime import timedelta

HFA = 57.5      # Home field advantage -- originally 60.0
K = 19.9        # The speed at which Elo ratings change -- originally 20.0
REVERT = 1/2.97 # Between seasons, a team retains about 2/3 of its previous season's rating -- originally 1/3.0

REVERSIONS = {'CBD1925': 1502.032, 'RAC1926': 1403.384, 'LOU1926': 1307.201, 'CIB1927': 1362.919, 'MNN1929': 1306.702, # Some between-season reversions of unknown origin
              'BFF1929': 1331.943, 'LAR1944': 1373.977, 'PHI1944': 1497.988, 'ARI1945': 1353.939, 'PIT1945': 1353.939, 'CLE1999': 1300.0}

class Forecast:

    @staticmethod
    def forecast(games):
        """ Generates win probabilities in the my_prob1 field for each game based on Elo model """

        # Initialize team objects to maintain ratings
        d = date.today() + timedelta(days=-6)
        recent_date = datetime.datetime(d.year, d.month, d.day)
                
        teams = {}
        for row in [item for item in csv.DictReader(open("data/initial_elos.csv"))]:
            teams[row['team']] = {
                'name': row['team'],
                'season': None,
                'elo': float(row['elo'])
            }

        first_recent_game = True
        for game in games:
            team1, team2 = teams[game['team1']], teams[game['team2']]

            # Revert teams at the start of seasons
            for team in [team1, team2]:
                if team['season'] and game['season'] != team['season']:
                    k = "%s%s" % (team['name'], game['season'])
                    if k in REVERSIONS:
                        team['elo'] = REVERSIONS[k]
                    else:
                        team['elo'] = 1505.0*REVERT + team['elo']*(1-REVERT)
                team['season'] = game['season']

            # Elo difference includes home field advantage
            elo_diff = team1['elo'] - team2['elo'] + (0 if game['neutral'] == 1 else HFA)

            # This is the most important piece, where we set my_prob1 to our forecasted probability
            if game['elo_prob1'] != None:
                game['my_prob1'] = 1.0 / (math.pow(10.0, (-elo_diff/400.0)) + 1.0)

            # If game was played, maintain team Elo ratings
            if game['score1'] != None:

                # Margin of victory is used as a K multiplier
                pd = abs(game['score1'] - game['score2'])
                mult = math.log(max(pd, 1) + 1.0) * (2.2 / (1.0 if game['result1'] == 0.5 else ((elo_diff if game['result1'] == 1.0 else -elo_diff) * 0.001 + 2.2)))

                # Elo shift based on K and the margin of victory multiplier
                shift = (K * mult) * (game['result1'] - game['my_prob1'])

                # Apply shift
                team1['elo'] += shift
                team2['elo'] -= shift
                
                # Print out new elo for recent games based on actual outcomes
                game_date = datetime.datetime.strptime(game['date'], "%Y-%m-%d")
                if game_date > recent_date:
                    if first_recent_game:
                        print("\n----------------------------------------------------------------------------\n")
                        print("New Elo values for recent games:\n")
                        first_recent_game = False
                    print("%s\t%s:\t%.11f\t%s:\t%.11f" % (game['date'], team1['name'], float(team1['elo']), team2['name'], float(team2['elo'])))

        upcoming_games = [g for g in games if g['result1'] == None and g['elo1'] != '' and g['elo2'] != '']

        if len(upcoming_games) > 0:
            print("\n----------------------------------------------------------------------------\n")
            print("Forecasts for upcoming games:\n")
            print("\t\tTeams\t\tProbA\t\t\tSpreadA\t\tDecA\t\tDecB\n")
            for game in upcoming_games:
                elo_diff = float(game['elo1']) - float(game['elo2']) + (0 if game['neutral'] == 1 else HFA)
                spread = round(-1*elo_diff/25.0*2)/2
                elo_prob = 1.0 / (math.pow(10.0, (-elo_diff/400.0)) + 1.0)
                print("%s\t%s vs. %s\t%s\t%.1f\t\t%.2f\t\t%.2f" % (game['date'], game['team1'], game['team2'], elo_prob, spread, 1/elo_prob, 1/(1-elo_prob)))
                   