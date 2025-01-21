import requests
import pprint as pp

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

headers = {
    "User-Agent": user_agent,
}


def get_player_splits(player_id: str) -> dict:
    """
    Get splits for a player.
    Player ID is the ESPN ID for the player.
    """

    try:
        url = f"https://site.web.api.espn.com/apis/common/v3/sports/basketball/nba/athletes/{player_id}/splits"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return {}
    except Exception as err:
        print(f"An error occurred: {err}")
        return {}


def transform_splits(splits: dict) -> dict:
    """
    Transform the splits data into a more usable format.
    """

    # pp.pprint(splits)

    def format_split_dict(split_dict: dict) -> dict:

        # map the display names to the stats
        mapped_stats = {
            display_names[i]: split_dict[i] for i in range(len(display_names))
        }

        # split the 3-Point Field Goals Made-Attempted Per Game into 3-Point Field Goals Made and 3-Point Field Goals Attempted
        mapped_stats["3-Point Field Goals Made Per Game"] = mapped_stats[
            "3-Point Field Goals Made-Attempted Per Game"
        ].split("-")[0]
        mapped_stats["3-Point Field Goals Attempted Per Game"] = mapped_stats[
            "3-Point Field Goals Made-Attempted Per Game"
        ].split("-")[1]

        # remove the 3-Point Field Goals Made-Attempted Per Game key
        del mapped_stats["3-Point Field Goals Made-Attempted Per Game"]

        # split the Field Goals Made-Attempted Per Game into Field Goals Made and Field Goals Attempted
        mapped_stats["Field Goals Made Per Game"] = mapped_stats[
            "Field Goals Made-Attempted Per Game"
        ].split("-")[0]
        mapped_stats["Field Goals Attempted Per Game"] = mapped_stats[
            "Field Goals Made-Attempted Per Game"
        ].split("-")[1]

        # remove the Field Goals Made-Attempted Per Game key
        del mapped_stats["Field Goals Made-Attempted Per Game"]

        # split the Free Throws Made-Attempted Per Game into Free Throws Made and Free Throws Attempted
        mapped_stats["Free Throws Made Per Game"] = mapped_stats[
            "Free Throws Made-Attempted Per Game"
        ].split("-")[0]
        mapped_stats["Free Throws Attempted Per Game"] = mapped_stats[
            "Free Throws Made-Attempted Per Game"
        ].split("-")[1]

        # remove the Free Throws Made-Attempted Per Game key
        del mapped_stats["Free Throws Made-Attempted Per Game"]

        # convert all values to floats
        for key, value in mapped_stats.items():
            mapped_stats[key] = float(value)

        return mapped_stats

    # 'displayNames' is a list of keys
    display_names = splits["displayNames"]

    # get overall splits
    overall_splits = splits["splitCategories"][0]["splits"][0]["stats"]
    overall_splits_dict = format_split_dict(overall_splits)

    # get home splits
    home_splits = splits["splitCategories"][0]["splits"][1]["stats"]
    home_splits_dict = format_split_dict(home_splits)

    # get road splits
    road_splits = splits["splitCategories"][0]["splits"][2]["stats"]
    road_splits_dict = format_split_dict(road_splits)

    output = {
        "Overall": overall_splits_dict,
        "RoadVsHome": {
            "Road": road_splits_dict,
            "Home": home_splits_dict,
        },
        "Month": {},
        "Opponent": {},
    }

    # get splits for for each month
    for month in splits["splitCategories"][1]["splits"]:
        month_splits = month["stats"]
        month_splits_dict = format_split_dict(month_splits)
        output["Month"][month["displayName"]] = month_splits_dict

    # get splits for each opponent
    for opponent in splits["splitCategories"][5]["splits"]:
        opponent_splits = opponent["stats"]
        opponent_splits_dict = format_split_dict(opponent_splits)
        output["Opponent"][opponent["displayName"]] = opponent_splits_dict

    return output


def get_transformed_splits(player_id: str) -> dict:
    """
    Get the transformed splits for a player.
    """

    player_splits = get_player_splits(player_id)

    transformed_splits = transform_splits(player_splits)

    return transformed_splits


if __name__ == "__main__":

    player_id = input("Enter player ID: ")
    transformed_splits = get_transformed_splits(player_id)

    print("--- Transformed Splits ---")
    pp.pprint(transformed_splits)
