from shiny import Inputs, Outputs, Session, module, render, ui
from data_container import data_container


@module.ui
def raw_data_tab_ui():
    return ui.layout_columns(
        ui.card(
            ui.card_header("Penguin data"),
            ui.output_data_frame("raw_data"),
            full_screen=True,
        ),
    )


@module.server
def raw_data_tab_server(input: Inputs, output: Outputs, session: Session):
    @render.data_frame
    def raw_data():
        cols = data_container.scouted_data.keys()
        return render.DataGrid(data_container.scouted_data[cols], filters=True)
