from shiny import App, ui
from data_container import data_container

from tabs.team_overview import team_tab_ui, team_tab_server
from tabs.match_overview import match_tab_ui, match_tab_server
from tabs.raw_data import raw_data_tab_ui, raw_data_tab_server
from tabs.overview import overview_tab_ui, overview_tab_server


app_ui = ui.page_navbar(
    ui.nav_panel("Overview", overview_tab_ui("overview_tab")),
    ui.nav_panel("Match Summary", match_tab_ui("match_tab")),
    ui.nav_panel("Team Summary", team_tab_ui("team_tab")),
    ui.nav_panel("Raw Data", raw_data_tab_ui("raw_data")),
    title=data_container.event,
)


def server(input, output, session):
    overview_tab_server("overview_tab")
    match_tab_server("match_tab")
    team_tab_server("team_tab")
    raw_data_tab_server("raw_data")


app = App(app_ui, server)
