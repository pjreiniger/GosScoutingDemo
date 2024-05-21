from shiny import Inputs, Outputs, Session, module, reactive, render, ui
from shinywidgets import output_widget, render_widget
import plotly.express as px
from data_container import data_container
import statbotics_utils


@module.ui
def match_tab_ui():
    return ui.page_sidebar(
        ui.sidebar(
            ui.input_select(
                "match_select",
                "Match",
                {
                    str(match_number): str(match_number)
                    for match_number in data_container.match_numbers
                },
            ),
            title="Select Match",
        ),
        ui.layout_column_wrap(
            ui.value_box(
                "Red 1",
                ui.output_text("match_red_1_team"),
            ),
            ui.value_box(
                "Red 2",
                ui.output_text("match_red_2_team"),
            ),
            ui.value_box(
                "Red 3",
                ui.output_text("match_red_3_team"),
            ),
            fill=False,
        ),
        ui.layout_column_wrap(
            ui.value_box(
                "Blue 1",
                ui.output_text("match_blue_1_team"),
            ),
            ui.value_box(
                "Blue 2",
                ui.output_text("match_blue_2_team"),
            ),
            ui.value_box(
                "Blue 3",
                ui.output_text("match_blue_3_team"),
            ),
            fill=False,
        ),
        ui.layout_columns(
            ui.card(
                ui.card_header("Red Preview"),
                output_widget("match_red_preview"),
                full_screen=True,
            ),
            ui.card(
                ui.card_header("Blue Preview"),
                output_widget("match_blue_preview"),
                full_screen=True,
            ),
        ),
    )


@module.server
def match_tab_server(input: Inputs, output: Outputs, session: Session):

    @reactive.calc
    def filter_by_match():
        match_number = int(input.match_select())
        scouted_data = data_container.scouted_data[
            data_container.scouted_data["Match Number"] == match_number
        ]
        statbotics_data = data_container.statbotics_matches[
            data_container.statbotics_matches.match_number == match_number
        ]

        return scouted_data, statbotics_data

    def _match_preview(alliance_data):
        return px.bar(
            alliance_data,
            y=[
                "totalAutoPieces",
                "totalTeleopPieces",
            ],
        )

    @render_widget
    def match_red_preview():
        scouted_data, statbotics_data = filter_by_match()

        red_teams = statbotics_utils.get_red_teams_in_match(statbotics_data)
        red_data = scouted_data[scouted_data["Team Number"].isin(red_teams)]
        return _match_preview(red_data)

    @render_widget
    def match_blue_preview():
        scouted_data, statbotics_data = filter_by_match()

        blue_teams = statbotics_utils.get_blue_teams_in_match(statbotics_data)
        blue_data = scouted_data[scouted_data["Team Number"].isin(blue_teams)]
        return _match_preview(blue_data)

    @render.text
    def match_red_1_team():
        scouted_data, statbotics_data = filter_by_match()
        return f"{statbotics_data['red_1'].values[0]}"

    @render.text
    def match_red_2_team():
        scouted_data, statbotics_data = filter_by_match()
        return f"{statbotics_data['red_2'].values[0]}"

    @render.text
    def match_red_3_team():
        scouted_data, statbotics_data = filter_by_match()
        return f"{statbotics_data['red_3'].values[0]}"

    @render.text
    def match_blue_1_team():
        scouted_data, statbotics_data = filter_by_match()
        return f"{statbotics_data['blue_1'].values[0]}"

    @render.text
    def match_blue_2_team():
        scouted_data, statbotics_data = filter_by_match()
        return f"{statbotics_data['blue_2'].values[0]}"

    @render.text
    def match_blue_3_team():
        scouted_data, statbotics_data = filter_by_match()
        return f"{statbotics_data['blue_3'].values[0]}"
