from shiny import Inputs, Outputs, Session, module, reactive, render, ui
from shinywidgets import output_widget, render_widget
from data_container import data_container, OUR_TEAM_NUMBER
import plotly.express as px
import statbotics_utils


@module.ui
def match_tab_ui():
    return ui.page_sidebar(
        ui.sidebar(
            ui.input_switch("our_matches_switch", "Filter Our Matches", False),
            ui.output_ui("match_list_combobox"),
            title="Filter Team",
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
        ui.card_header("Preview"),
        ui.layout_column_wrap(
            ui.value_box(
                "Red Prediction",
                ui.output_text("red_statbotics_prediction"),
            ),
            ui.value_box(
                "Predicted Result",
                ui.output_text("statbotics_predicted_result"),
            ),
            ui.value_box(
                "Blue Prediction",
                ui.output_text("blue_statbotics_prediction"),
            ),
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
        ui.card_header("Scouted Data"),
        ui.card(
            ui.card_header("Match Results"),
            ui.output_data_frame("match_results_data"),
            full_screen=True,
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
        alliance_data = (
            alliance_data.groupby("Team Number").mean(numeric_only=True).reset_index()
        )
        return px.bar(
            alliance_data,
            y=[
                "totalAutoPieces",
                "totalTeleopPieces",
            ],
        )

    @render.ui
    def match_list_combobox():
        if input.our_matches_switch():
            team_matches = statbotics_utils.get_matches_for_team(
                data_container.statbotics_matches, OUR_TEAM_NUMBER
            )
            match_numbers = list(team_matches["match_number"])
        else:
            match_numbers = data_container.match_numbers

        return (
            ui.input_select(
                "match_select",
                "Match",
                {
                    str(match_number): str(match_number)
                    for match_number in match_numbers
                },
            ),
        )

    @render_widget
    def match_red_preview():
        scouted_data, statbotics_data = filter_by_match()

        red_teams = statbotics_utils.get_red_teams_in_match(statbotics_data)
        red_data = data_container.scouted_data[
            data_container.scouted_data["Team Number"].isin(red_teams)
        ]
        return _match_preview(red_data)

    @render_widget
    def match_blue_preview():
        scouted_data, statbotics_data = filter_by_match()

        blue_teams = statbotics_utils.get_blue_teams_in_match(statbotics_data)
        blue_data = data_container.scouted_data[
            data_container.scouted_data["Team Number"].isin(blue_teams)
        ]
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

    @render.data_frame
    def match_results_data():
        scouted_data, statbotics_data = filter_by_match()
        return render.DataGrid(scouted_data)

    @render.text
    def red_statbotics_prediction():
        scouted_data, statbotics_data = filter_by_match()
        return f"{statbotics_data['red_epa_sum'].values[0]}"

    @render.text
    def blue_statbotics_prediction():
        scouted_data, statbotics_data = filter_by_match()
        return f"{statbotics_data['blue_epa_sum'].values[0]}"

    @render.text
    def statbotics_predicted_result():
        scouted_data, statbotics_data = filter_by_match()
        winning_alliance = statbotics_data["epa_winner"].values[0]
        win_probability = statbotics_data["epa_win_prob"].values[0]
        if winning_alliance == "blue":
            win_probability = 1 - win_probability
        return f"{winning_alliance} - {100 * win_probability:.2f}%"
