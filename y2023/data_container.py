from pathlib import Path

import pandas as pd
import os
import json


class DataContainer:
    def __init__(self, event):
        self.event = event

        self.scouted_data = self.__load_gos_data(event)
        self.statbotics_matches = self.__load_statbotics_matches(event)

        self.team_numbers = sorted(
            pd.unique(
                pd.concat(
                    [
                        self.statbotics_matches["red_1"],
                        self.statbotics_matches["red_2"],
                        self.statbotics_matches["red_3"],
                        self.statbotics_matches["blue_1"],
                        self.statbotics_matches["blue_2"],
                        self.statbotics_matches["blue_3"],
                    ]
                )
            )
        )

        self.match_numbers = pd.unique(self.statbotics_matches.match_number)

    def __load_statbotics_matches(self, event):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(this_dir, "data", f"{event}_statbotics_matches.json")

        with open(filename, "r") as f:
            json_data = json.load(f)

        return pd.DataFrame(json_data)

    def __load_gos_data(self, event: str) -> pd.DataFrame:
        app_dir = Path(__file__).parent
        filename = os.path.join(app_dir, "data", f"{event}_scouting.csv")

        data_frame = pd.read_csv(filename)
        data_frame = self.__sanitize_gos_field_names(data_frame)

        return data_frame

    def __sanitize_gos_field_names(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        data_frame.rename(
            inplace=True,
            columns={
                "match_number": "Match Number",
                "team_key": "Team Number",
            },
        )

        data_frame["Team Number"] = pd.Series(
            [int(x[3:]) for x in data_frame["Team Number"].values]
        )

        data_frame = data_frame.drop(
            ["org_key", "match_key", "year", "event_key", "time", "alliance"], axis=1
        )

        return data_frame


EVENT = "2023ohmv"
OUR_TEAM_NUMBER = 3504

data_container = DataContainer(EVENT)
