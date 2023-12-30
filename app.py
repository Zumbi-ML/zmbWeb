# -*- coding: utf-8 -*-
# Main Dash Application for 'Zumbi' Platform
# This script initializes and configures the Dash web application for 'Zumbi'.
# It includes setup for routing, layout, and callbacks across different modules.

import dash
from dash.dependencies import ClientsideFunction, Input, Output
from flask_caching import Cache

# Import views for different sections of the application
import about.view as bv
import extract.logic as el
import extract.view as av
import journals.view as jv

# Import utility functions and constants
from common import common_404_html
from constants import outage
from view import core_view_html, nav_html, outage_html
from search.util import get_search_field_callback_args
import search.logic as sl
import search.view as sv

################################################################################
# Initialization of Dash App
################################################################################
external_scripts = ["https://www.googletagmanager.com/gtag/js?id=UA-149443072-1"]
app = dash.Dash(__name__, external_scripts=external_scripts)
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True
app.title = "Zumbi - A medida da discriminação racial"

# Layout Configuration
app.layout = outage_html() if outage else core_view_html()
cache = Cache(app.server, config={"CACHE_TYPE": "simple"})

################################################################################
# Callbacks for Routing and Navigation
################################################################################

@app.callback(Output("core-app-container", "children"), [Input("core-url", "pathname")])
def display_app_html(path):
    """
    Determines which application view to display based on the URL path.
    Returns the appropriate HTML for the requested section of the application.
    """
    if path in ["/", "/search"] or not path:
        return sv.app_view_html()
    elif path == "/extract":
        return av.app_view_html()
    elif path == "/about":
        return bv.app_view_html()
    elif path == "/journals":
        return jv.app_view_html()
    else:
        return common_404_html()

@app.callback(Output("core-nav-container", "children"), [Input("core-url", "pathname")])
def update_nav_bar_highlight(path):
    """
    Updates the navigation bar to highlight the current page.
    """
    return nav_html(path)

# Clientside callback for animating the burger menu on mobile devices
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="animateBurgerOnClickClientsideFunction"),
    Output("core-burger-trigger-cs", "value"),
    [Input("core-navbar-menu", "id"), Input("core-burger-trigger-cs", "n_clicks")]
)

################################################################################
# Registration of Additional Callbacks
################################################################################

# Import and register callbacks for different sections of the application
from callbacks.callbacks_search import register_search_callbacks
from callbacks.callbacks_extract import register_extract_callbacks
from callbacks.callbacks_about import register_about_callbacks

register_search_callbacks(app)
register_extract_callbacks(app)
register_about_callbacks(app)
