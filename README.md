# NFL Predictions

This a repository based on the one created to accompany [FiveThirtyEight's NFL Forecasting model and repositories](https://github.com/fivethirtyeight/nfl-elo-game).

## Evaluating historical forecasts

`eval.py` is the only runnable script, and does the following:

1. Reads in the CSV of historical games. Each row includes a `elo_prob1` field, which is the probability that `team1` will win the game according to the Elo model.
2. Fills in a `my_prob1` field for every game using code in `forecast.py`. By default, these are filled in using the exact same Elo model.
3. ~~Evaluates the probabilities stored in `my_prob1` against the ones in `elo_prob1`, and shows how those forecasts would have done in our game for every season since 1920.~~
4. Provides the resulting elo values for recently played games so that the `nfl-elo-game.csv` file can be updated for the next week of games.
5. Lists probabilities, spreads, and decimal odds for upcoming games.

Simply run `python eval.py`.