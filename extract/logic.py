# -*- coding: utf-8 -*-

import numpy as np

# Importing constants and specific HTML functions from the application
from constants import sample_abstracts
from extract.view import (
    extract_entities_results_html,
    journal_suggestions_html,
    no_abstract_warning_html,
)

"""
This module handles callbacks for the search functionality in the application.
It processes user actions (button clicks) and entered text to provide relevant
search results, such as entity extraction or journal suggestions.

Note: HTML functions used for rendering results are defined elsewhere and imported here.
Avoid defining HTML blocks directly in this file to maintain a clear separation
between presentation logic and business logic.
"""

def extracted_results(extract_button_n_clicks, suggest_button_n_clicks, text, normalize):
    """
    Processes clicks on extraction and suggestion buttons to provide the appropriate result.
    
    Args:
        extract_button_n_clicks (int): Number of clicks on the extract button.
        suggest_button_n_clicks (int): Number of clicks on the suggest button.
        text (str): Text entered by the user for search.
        normalize (bool): Indicates whether normalization should be applied to the text.

    Returns:
        dash_html_components: HTML block with search results or warning, as appropriate.
    """
    if extract_button_n_clicks is None and suggest_button_n_clicks is None:
        return ""
    
    stripped_text = text.strip() if text else ""
    if not stripped_text:
        # Returns a warning if no text is provided
        return no_abstract_warning_html()
    
    if extract_button_n_clicks and extract_button_n_clicks > 0:
        # Returns entity extraction results if the extract button was clicked
        return extract_entities_results_html(stripped_text, normalize)
    elif suggest_button_n_clicks and suggest_button_n_clicks > 0:
        # Returns journal suggestions if the suggest button was clicked
        return journal_suggestions_html(stripped_text)
    
    return ""


def get_random_abstract(random_button_n_clicks):
    """
    Provides a random abstract when the corresponding button is clicked.

    Args:
        random_button_n_clicks (int): Number of clicks on the random abstract button.

    Returns:
        str: Text of a random abstract or empty string if the button was not clicked.
    """
    if random_button_n_clicks not in [None, 0]:
        # Selects and returns a random abstract if the button was clicked
        return np.random.choice(sample_abstracts)
    return ""
