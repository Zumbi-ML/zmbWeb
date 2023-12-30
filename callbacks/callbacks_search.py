#import dash
from dash.dependencies import ClientsideFunction, Input, Output, State
import search.logic as sl
from search.util import get_search_field_callback_args

def register_search_callbacks(app):
    ################################################################################
    # Search app callbacks
    ################################################################################

    @app.callback(
        Output("search-main-bar-input", "value"),
        [Input("search-example-button", "n_clicks")]
        + get_search_field_callback_args(
            as_type="input", return_component="value"
        ),
    )
    def search_bar_live_display(example_search_n_clicks, *ent_txts):
        """
        Update the main search bar text live from the example search button and the
        entity fields being typed in.

        Args:
            example_search_n_clicks (int): The number of times the example search
                button was clicked.
            *ent_txts (strs): The strings for each guided search field.

        Returns:
            (str): The text to be shown in the search bar via live update.

        """
        return sl.search_bar_live_display(example_search_n_clicks, *ent_txts)


    @app.callback(
        Output("search-example-button", "n_clicks"),
        get_search_field_callback_args(as_type="input"),
    )
    def void_example_search_n_clicks_on_live_search(*ent_txts):
        """
        Reset the number of example search button clicks when any search is changed
        via the guided search fields.

        Args:
            *ent_txts: The entity texts, though it does not matter what they
                actually are.
        Returns:
            (int): The number of clicks to set the example search button n_clicks
                to.
        """
        return 0


    @app.callback(
        Output("search-go-button", "n_clicks"),
        [Input("search-main-bar-input", "n_submit")]
        + get_search_field_callback_args(
            as_type="input", return_component="n_submit"
        ),
        [State("search-go-button", "n_clicks")],
    )
    def sum_all_fields_and_buttons_n_submits(*all_n_clicks):
        """
        Sum the guided search fields and main search field and "Go" button n_submits
        and n_clicks to a single n_clicks number for the Go button. Thus the user
        can hit enter on any guided search field or the main box and the app will
        act like you are hitting the go button.

        Args:
            *all_n_clicks (ints): Integers representing the number of times each
                guided search field or main search bar or Go button was
                clicked/entered.

        Returns:
            n_times_searched (int): The total number of times a search was executed.
                If this is voided correctly in another callback, it will be either
                0 or 1.
        """
        return sl.sum_all_fields_and_buttons_n_submits(*all_n_clicks)


    @app.callback(
        Output("search-results-container", "children"),
        [Input("search-go-button", "n_clicks")],
        [
            State("search-main-bar-input", "value"),
        ],
    )
    def show_search_results(go_button_n_clicks, search_text):
        """
        Determine what kind of results to show from the search text, search type,
        and number of clicks of the search button. Cache if necessary using flask.

        Args:
            go_button_n_clicks (int): The number of clicks of the "Go" button.
            dropdown_value (str): The type of search to execute.
            search_text (str): The raw search text as entered in the search field.

        Returns:
            (dash_html_components.Div): The correct html block for the search type
                and customized according to search results from the search text.
        """

        if search_text:
            # Prevent from caching on n_clicks if the results aren't empty
            @cache.memoize(timeout=cache_timeout)
            def memoize_wrapper(search_text):
                return sl.show_search_results(
                    go_button_n_clicks, search_text
                )

            return memoize_wrapper(search_text)
        else:
            return sl.show_search_results(
                go_button_n_clicks,search_text
            )

    # Animates the count up for the search bar
    # See count.js and clientside.js for more details
    app.clientside_callback(
        ClientsideFunction(
            namespace="clientside", function_name="countSearchClientsideFunction"
        ),
        Output("search-count-abstracts-cs", "children"),
        [
            Input("core-url", "pathname"),
            Input("search-count-abstracts-cs", "id"),
            Input("search-count-abstracts-hidden-ref-cs", "id"),
        ],
    )

    # Rotates example searches through the search bar
    # See example_searches.js and clientside.js for more details
    app.clientside_callback(
        ClientsideFunction(
            namespace="clientside",
            function_name="cycleExampleSearchesClientsideFunction",
        ),
        Output("search-main-bar-input", "children"),
        [
            Input("core-url", "pathname"),
            Input("search-main-bar-input", "id"),
            Input("search-examples-hidden-ref-cs", "id"),
        ],
    )