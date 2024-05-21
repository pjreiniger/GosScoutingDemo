from shiny import Inputs, Outputs, Session, module, reactive, render, ui
from shinywidgets import output_widget, render_widget
from data_container import data_container
import plotly.express as px


@module.ui
def overview_tab_ui():
    return ui.page_fluid(
        ui.card(
            ui.card_header("Team Averages"),
            ui.output_data_frame("overview_data"),
            full_screen=True,
        ),
        ui.layout_columns(
            ui.card(
                ui.card_header("Scoring Plot"),
                output_widget("scoring_plot"),
                full_screen=True,
            ),
            ui.card(
                ui.card_header("Piece Percentages"),
                output_widget("piece_percentage_graph"),
                full_screen=True,
            ),
        ),
    )


@module.server
def overview_tab_server(input: Inputs, output: Outputs, session: Session):
    @reactive.calc
    def average_data():
        avg = data_container.scouted_data.groupby(["Team Number"]).mean(
            numeric_only=True
        )
        avg = avg.reset_index()

        return avg

    @render.data_frame
    def overview_data():
        avg = average_data()
        cols = avg.keys()
        return render.DataGrid(avg[cols].round(2), filters=True)

    @render_widget
    def piece_percentage_graph():
        avg = average_data()

        return px.scatter(
            avg,
            x="totalConesScored",
            y="totalCubesScored",
            text="Team Number",
            color="totalPieces",
            color_continuous_scale="jet",
        )

    @render_widget
    def scoring_plot():
        avg = average_data()

        return px.scatter(
            avg, x="totalTeleopPoints", y="totalAutoPoints", text="Team Number"
        )
