from shiny import App
from app_ui import app_ui
from app_server import app_server

app = App(app_ui(), app_server)