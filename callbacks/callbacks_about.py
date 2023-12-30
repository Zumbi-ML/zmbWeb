from dash.dependencies import ClientsideFunction, Input, Output

def register_about_callbacks(app):
    ################################################################################
    # About app callbacks
    ################################################################################

    # Counts up each stat in the about page introduction section
    # See count.js and clientside.js for more details
    app.clientside_callback(
        ClientsideFunction(
            namespace="clientside", function_name="countStatsClientsideFunction"
        ),
        Output("about-count-materials-cs", "children"),
        [
            Input("core-url", "pathname"),
            Input("about-count-materials-cs", "id"),
            Input("about-count-abstracts-cs", "id"),
            Input("about-count-entities-cs", "id"),
            Input("about-count-materials-hidden-ref-cs", "id"),
            Input("about-count-abstracts-hidden-ref-cs", "id"),
            Input("about-count-entities-hidden-ref-cs", "id"),
        ],
    )
