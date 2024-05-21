from shiny import Inputs, Outputs, Session, module


@module.ui
def overview_tab_ui():
    return "Overview"


@module.server
def overview_tab_server(input: Inputs, output: Outputs, session: Session):
    pass
