import pprint as pp

from functions import get_transformed_splits


def get_stats_weighted_average(
    stats_data: list, home_or_away: str, opponent: str, month: str
) -> dict:

    # get the overall stats from input
    overall_stats = stats_data["Overall"]

    # --- get Home or Away stats (based on input) ---

    # make sure home_or_away is either "Home" or "Away"
    if home_or_away not in ["Home", "Road"]:
        raise ValueError("Input must be either 'Home' or 'Road'")
    home_or_away_stats = stats_data["RoadVsHome"][home_or_away]

    # --- get the month stats from input ---

    # make sure month is in the list of months
    months = list(stats_data["Month"].keys())
    if month not in months:
        raise ValueError(f"Month must be one of the following: {months}")
    month_stats = stats_data["Month"][month]

    # --- get the opponent stats from input ---

    # make sure opponent is in the list of opponents
    opponents = list(stats_data["Opponent"].keys())
    if opponent not in opponents:
        print(f"Opponent '{opponent}' not found. Ignoring.")
        opponent_stats = None
    else:
        opponent_stats = stats_data["Opponent"][opponent]

    to_calculate = [overall_stats, home_or_away_stats, month_stats]
    if opponent_stats:
        to_calculate.append(opponent_stats)

    # --- calculate the weighted average ---

    def calculate_weighted_average(to_calculate: list) -> dict:
        """
        Calculate the weighted average of stats using 'Games Played' as the weight.
        """

        # Initialize a dictionary to hold the weighted sums and total games played
        weighted_sums = {}
        total_games_played = 0

        # Iterate over each stats dictionary in the list
        for stats in to_calculate:
            games_played = stats.get("Games Played", 0)
            total_games_played += games_played

            # Accumulate weighted sums for each stat
            for key, value in stats.items():
                if key != "Games Played":
                    if key not in weighted_sums:
                        weighted_sums[key] = 0
                    weighted_sums[key] += value * games_played

        # Calculate the weighted average for each stat
        weighted_averages = {
            key: (value / total_games_played) if total_games_played > 0 else 0
            for key, value in weighted_sums.items()
        }

        return weighted_averages

    weighted_average = calculate_weighted_average(to_calculate)

    return weighted_average


if __name__ == "__main__":

    player_id = input("Enter player ID: ")

    stats_data = get_transformed_splits(player_id=player_id)

    input_home_or_away = input("Enter Home or Road: ")

    input_opponent = input("Enter Opponent: ")

    input_month = input("Enter Month: ")

    weighted_average = get_stats_weighted_average(
        stats_data, input_home_or_away, input_opponent, input_month
    )

    print("--- Predicted Stats ---")
    pp.pprint(weighted_average)
