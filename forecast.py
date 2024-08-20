import csv
import math

HFA = 57.5      # Home field advantage -- originally 60.0
K = 19.9        # The speed at which Elo ratings change -- originally 20.0
REVERT = 1/2.97 # Between seasons, a team retains about 2/3 of its previous season's rating -- originally 1/3.0

REVERSIONS = {'CBD1925': 1502.032, 'RAC1926': 1403.384, 'LOU1926': 1307.201, 'CIB1927': 1362.919, 'MNN1929': 1306.702, # Some between-season reversions of unknown origin
              'BFF1929': 1331.943, 'LAR1944': 1373.977, 'PHI1944': 1497.988, 'ARI1945': 1353.939, 'PIT1945': 1353.939, 'CLE1999': 1300.0}

class Forecast:

    @staticmethod
    def get_team_elo(team_name, teams):
        if team_name in teams:
            return teams[team_name]['elo']
        return None

    @staticmethod
    def forecast(games):
        # Generates win probabilities in the elo_prob1 field for each game based on Elo model

        # Initialize team objects to maintain ratings
        teams = {}
        for row in [item for item in csv.DictReader(open("data/initial_elos.csv"))]:
            teams[row['team']] = {
                'name': row['team'],
                'season': None,
                'date': None,
                'elo': float(row['elo'])
            }

        for game in games:
            team1, team2 = teams[game['team1']], teams[game['team2']]

            # Revert teams at the start of seasons
            for team in [team1, team2]:
                if team['season'] and game['season'] != team['season']:
                    k = "%s%s" % (team['name'], game['season'])
                    if k in REVERSIONS:
                        team['elo'] = REVERSIONS[k]
                    else:
                        team['elo'] = 1505.0 * REVERT + team['elo'] * (1 - REVERT)
                team['season'] = game['season']
                team['date'] = game['date']

            # Elo difference includes home field advantage
            elo_diff = team1['elo'] - team2['elo'] + (0 if game['neutral'] == 1 else HFA)

            # This is the most important piece, where we set elo_prob1 to our forecasted probability
            if game['elo_prob1'] != None:
                game['elo_prob1'] = 1.0 / (math.pow(10.0, (-elo_diff / 400.0)) + 1.0)

            # If game was played, maintain team Elo ratings
            if game['score1'] != None:

                # Margin of victory is used as a K multiplier
                pd = abs(game['score1'] - game['score2'])
                mult = math.log(max(pd, 1) + 1.0) * (2.2 / (1.0 if game['result1'] == 0.5 else ((elo_diff if game['result1'] == 1.0 else -elo_diff) * 0.001 + 2.2)))

                # Elo shift based on K and the margin of victory multiplier
                shift = (K * mult) * (game['result1'] - game['elo_prob1'])

                # Apply shift
                team1['elo'] += shift
                team2['elo'] -= shift
  
        # Set new elo for recent games based on actual outcomes
        for game in games:
            if game['elo1'] in [0, ''] or game['elo2'] in [0, '']:
                if not game['elo1']:
                    team1 = game['team1']
                    elo1 = Forecast.get_team_elo(team1, teams)
                    if elo1 is not None:
                        game['elo1'] = elo1

                if not game['elo2']:
                    team2 = game['team2']
                    elo2 = Forecast.get_team_elo(team2, teams)
                    if elo2 is not None:
                        game['elo2'] = elo2

    @staticmethod
    def forecast_betting_odds(games):
        # Calculate forecasts for upcoming games that have elo values but no results
        game_odds = {}

        for game in games:
            if game['result1'] == None and game['elo1'] != '' and game['elo2'] != '':
                elo_diff = float(game['elo1']) - float(game['elo2']) + (0 if game['neutral'] == 1 else HFA)
                game['elo_prob1'] = 1.0 / (math.pow(10.0, (-elo_diff / 400.0)) + 1.0)
                spread = round(-1 * elo_diff / 25.0 * 2) / 2

                percentage1 = game['elo_prob1']
                percentage2 = 1 - percentage1
                decimal1 = 1 / percentage1
                decimal2 = 1 / percentage2

                if percentage1 >= 0.5:
                    american1 = f"-{(-100 / (1 - decimal1)):.0f}"
                    american2 = f"+{((decimal2 - 1) * 100):.0f}"
                else:
                    american1 = f"+{((decimal1 - 1) * 100):.0f}"
                    american2 = f"-{(-100 / (1 - decimal2)):.0f}"

                if spread == 0.0:
                    spread1 = "0.0"
                    spread2 = "0.0"
                else:
                    spread1 = f"{spread:+.1f}"
                    spread2 = f"{-spread:+.1f}"

                game_odds[f"{game['team1']}-{game['team2']}"] = {
                    'date': game['date'],
                    'team1': game['team1'],
                    'percentage1': f"{percentage1:.2%}",
                    'american1': american1,
                    'decimal1': decimal1,
                    'spread1': spread1,
                    'elo1': f"{float(game['elo1']):.4f}",
                    'team2': game['team2'],
                    'percentage2': f"{percentage2:.2%}",
                    'american2': american2,
                    'decimal2': decimal2,
                    'spread2': spread2,
                    'elo2': f"{float(game['elo2']):.4f}"
                }

        return game_odds, games