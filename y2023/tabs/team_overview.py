from shiny import Inputs, Outputs, Session, module, reactive, render, ui
from shinywidgets import output_widget, render_widget
import plotly.express as px
from data_container import data_container


@module.ui
def team_tab_ui():
    return ui.page_sidebar(
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


@module.server
def team_tab_server(input: Inputs, output: Outputs, session: Session):
    @reactive.calc
    def filter_by_team():
        team_number = int(input.team_select())
        return data_container.scouted_data[
            data_container.scouted_data["Team Number"] == team_number
        ]

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
