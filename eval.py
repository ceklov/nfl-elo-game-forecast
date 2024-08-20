from util import *
from forecast import *

games = Util.read_games("data/nfl_games.csv")
Forecast.forecast(games)
game_odds, games = Forecast.forecast_betting_odds(games)
Util.write_games(games, "data/nfl_games_updated.csv")
Util.print_betting_odds(game_odds)