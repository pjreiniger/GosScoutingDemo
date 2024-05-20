import json

import pandas as pd
from typing import Dict, Any, List
import statbotics


def download_matches(event: str, output_path: str, quals_only=True):
    sb = statbotics.Statbotics()

    elims = False if quals_only else None
    print(elims)
    data = sb.get_matches(event=event, elims=elims)

    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)


def get_alliance_teams_in_match(
    match_data: pd.DataFrame, alliance_color: str, num_teams
) -> List[int]:
    teams = []

    for i in range(num_teams):
        x = match_data[f"{alliance_color}_{i + 1}"].values[0]
        teams.append(x)

    return teams


def get_red_teams_in_match(match_data: pd.DataFrame, num_teams=3) -> List[int]:
    return get_alliance_teams_in_match(match_data, "red", num_teams)


def get_blue_teams_in_match(match_data: pd.DataFrame, num_teams=3) -> List[int]:
    return get_alliance_teams_in_match(match_data, "blue", num_teams)
