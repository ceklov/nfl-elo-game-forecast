from util import *
from forecast import *

games = Util.read_games("data/nfl_games.csv")

Forecast.forecast(games)

Util.write_games(games, "data/nfl_games_updated.csv")