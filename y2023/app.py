from shiny import App, reactive, render, ui
from shinywidgets import output_widget, render_widget
from data_container import DataContainer
import plotly.express as px


data_container = DataContainer("2023ohmv")


def teams_tab():
    return [
        ui.page_sidebar(
            ui.sidebar(
                ui.input_select(
                    "team_select",
                    "Team",
                    {
                        str(team_number): str(team_number)
                        for team_number in data_container.team_numbers
                    },
                    selected="3504",
                ),
                title="Filter Team",
            ),
            ui.layout_column_wrap(
                ui.value_box(
                    "Avg. Total Auto Pieces",
                    ui.output_text("team_total_auto_pieces"),
                ),
                ui.value_box(
                    "Avg. Auto Points",
                    ui.output_text("team_avg_auto_points"),
                ),
                ui.value_box(
                    "Avg. Total Teleop Pieces",
                    ui.output_text("team_total_tele_pieces"),
                ),
                ui.value_box(
                    "Avg. Teleop Points",
                    ui.output_text("team_avg_tele_points"),
                ),
                fill=False,
            ),
            ui.layout_columns(
                ui.card(
                    ui.card_header("Bill length and depth"),
                    output_widget("team_piece_summary"),
                    full_screen=True,
                ),
                ui.card(
                    ui.card_header("Team Data"),
                    ui.output_data_frame("team_summary_data"),
                    full_screen=True,
                ),
            ),
        )
    ]


def matches_tab():
    return [
        ui.page_sidebar(
            ui.sidebar(
                ui.input_select(
                    "match_select",
                    "Match",
                    {
                        str(match_number): str(match_number)
                        for match_number in data_container.match_numbers
                    },
                ),
                title="Filter Team",
            ),
        #     ui.layout_column_wrap(
        #         ui.value_box(
        #             "Avg. Total Auto Pieces",
        #             ui.output_text("team_total_auto_pieces"),
        #         ),
        #         ui.value_box(
        #             "Avg. Auto Points",
        #             ui.output_text("team_avg_auto_points"),
        #         ),
        #         ui.value_box(
        #             "Avg. Total Teleop Pieces",
        #             ui.output_text("team_total_tele_pieces"),
        #         ),
        #         ui.value_box(
        #             "Avg. Teleop Points",
        #             ui.output_text("team_avg_tele_points"),
        #         ),
        #         fill=False,
        #     ),
            ui.layout_column_wrap(
                ui.value_box(
                    "Red 1",
                    ui.output_text("match_red_1_team"),
                ),
                ui.value_box(
                    "Red 1",
                    ui.output_text("match_red_2_team"),
                ),
                ui.value_box(
                    "Red 3",
                    ui.output_text("match_red_3_team"),
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
    ]


def raw_data_tab():
    return [
        ui.layout_columns(
            ui.card(
                ui.card_header("Penguin data"),
                ui.output_data_frame("raw_data"),
                full_screen=True,
            ),
        ),
    ]


app_ui = ui.page_navbar(
    ui.nav_panel("Raw Data", *raw_data_tab()),
    ui.nav_panel("Matches", *matches_tab()),
    ui.nav_panel("Teams", *teams_tab()),
    title=data_container.event,
)


def server(input, output, session):

    @render.data_frame
    def raw_data():
        cols = data_container.scouted_data.keys()
        return render.DataGrid(data_container.scouted_data[cols], filters=True)

    ###########################
    # Team Page
    ###########################
    @reactive.calc
    def filter_by_team():
        team_number = int(input.team_select())
        return data_container.scouted_data[data_container.scouted_data["Team Number"] == team_number]

    @render_widget
    def team_piece_summary():
        team_data = filter_by_team()
        print(team_data)
        return px.bar(
            team_data,
            x="Match Number",
            y=[
                "autoConesHigh",
                "autoConesMid",
                "autoConesLow",
                "autoCubesHigh",
                "autoCubesMid",
                "autoCubesLow",
                "teleopConesHigh",
                "teleopConesMid",
                "teleopConesLow",
                "teleopCubesHigh",
                "teleopCubesMid",
                "teleopCubesLow",
            ],
        )

    @render.data_frame
    def team_summary_data():
        team_data = filter_by_team()
        cols = team_data.keys()
        return render.DataGrid(team_data[cols], filters=True)

    @render.text
    def team_total_auto_pieces():
        team_data = filter_by_team()
        return f"{team_data['totalAutoPieces'].mean():.1f}"

    @render.text
    def team_avg_auto_points():
        team_data = filter_by_team()
        return f"{team_data['totalAutoPoints'].mean():.1f}"

    @render.text
    def team_total_tele_pieces():
        team_data = filter_by_team()
        return f"{team_data['totalTeleopPieces'].mean():.1f}"

    @render.text
    def team_avg_tele_points():
        team_data = filter_by_team()
        return f"{team_data['totalTeleopPoints'].mean():.1f}"

    ###########################
    # Match Page
    ###########################
    @reactive.calc
    def filter_by_match():
        match_number = int(input.match_select())
        return data_container.scouted_data[data_container.scouted_data["Match Number"] == match_number]


    @render_widget
    def match_red_preview():
        match_data = filter_by_match()
        print(match_data)

    @render_widget
    def match_blue_preview():
        match_data = filter_by_match()
        print(match_data)


app = App(app_ui, server)
