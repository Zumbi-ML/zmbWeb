#import dash
from dash.dependencies import Input, Output, State
import extract.logic as el

def register_extract_callbacks(app):
    ################################################################################
    # Extract app callbacks
    ################################################################################
    @app.callback(
        Output("extract-results", "children"),
        [
            Input("extract-button", "n_clicks"),
            Input("extract-suggest-button", "n_clicks"),
        ],
        [
            State("extract-text-area", "value"),
            State("extract-dropdown-normalize", "value"),
        ],
    )
    def extracted_results(
        extract_button_n_clicks, suggest_button_n_clicks, text, normalize
    ):
        """
        Get the extracted entities or the journal suggestion results from the
        extract app via clicks and the entered text, along with the
        normalize dropdown.

        Args:
            extract_button_n_clicks (int): The number of clicks of the extract
                button.
            suggest_button_n_clicks (int): the number of clicks of the suggest
                button
            text (str): The text entered in the text box, to extract.
            normalize (bool): The normalize string to pass to the rester.

        Returns:
            (dash_html_components, str): The extracted results html block.
        """
        # if text:
        #     # Prevent from caching on n_clicks if the search isn"t empty
        #     @cache.memoize(timeout=cache_timeout)
        #     def memoize_wrapper(text, normalize):
        #         return el.extracted_results(
        #             extract_button_n_clicks, text, normalize
        #         )
        #
        #     return memoize_wrapper(text, normalize)
        # else:
        #     return el.extracted_results(extract_button_n_clicks, text, normalize)
        return el.extracted_results(
            extract_button_n_clicks, suggest_button_n_clicks, text, normalize
        )


    @app.callback(
        Output("extract-button", "n_clicks"),
        [Input("extract-suggest-button", "n_clicks")],
    )
    def void_extract_button_on_suggest(suggest_button_n_clicks):
        """
        Void the number of clicks of the extract button when the suggest button
        gets hit. This is so that you can keep clicking the extract and suggest
        button alternating and have it still pull up the correct info.

        Args:
            suggest_button_n_clicks (int): The number of clicks of the suggest
                button.

        Returns:
            (int): The number of clicks of the extract button.

        """
        return 0


    @app.callback(
        Output("extract-text-area", "value"), [Input("extract-random", "n_clicks")]
    )
    def get_random_abstract(random_button_n_clicks):
        """
        Get a random abstract for the random button.

        Args:
            random_button_n_clicks (int): The number of clicks of the random button.

        Returns:
            (str): The text of a random abstract.
        """
        return el.get_random_abstract(random_button_n_clicks)