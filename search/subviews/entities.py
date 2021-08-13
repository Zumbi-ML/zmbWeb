# -*- coding: utf-8 -*-

import dash_html_components as html

from constants import entity_color_map, rester
from search.common import (
    big_label_and_disclaimer_html,
    common_results_container_style,
    no_results_html,
)

"""
Functions for defining the results container when entity results are desired.

Please do not define callback logic in this file.
"""

# Maximum number of rows shown for each entity table. 10 usually looks good.
MAX_N_ROWS_FOR_EACH_ENTITY_TABLE = 10

big_label_and_disclaimer = big_label_and_disclaimer_html("entities")
entities_no_results_html = no_results_html(pre_label=big_label_and_disclaimer)


def entities_results_html(entity_query, raw_text):
    """
    Get the html block for entities results from the Rester-compatible
    entity query and text.

    Args:
        entity_query (dict): The entity query, in Rester-compatible format.
        raw_text (str, None): Any raw text to search for.

    Returns:
        (dash_html_components.Div): The entities results html block.

    """
    results = rester.entities_search(
        entity_query, text=raw_text, top_k=MAX_N_ROWS_FOR_EACH_ENTITY_TABLE
    )
    if results is None or not any([v for v in results.values()]):
        return entities_no_results_html
    else:
        all_tables = all_score_tables_html(results)
        all_tables_container = html.Div(
            children=[big_label_and_disclaimer, all_tables],
            className=common_results_container_style(),
        )
        return all_tables_container


def all_score_tables_html(results_dict):
    """
    Get all the score tables for all entity types as an html block.

    Args:
        results_dict (dict): The result dictionary directly from the Rester.

    Returns:
       (dash_html_components.Div): The entity table as an html block.
    """
    columns_classes = "columns is-desktop is-centered"

    half = "is-half"
    third = "is-one-third"

    row1 = html.Div(
        [
            single_entity_score_table_html(
                results_dict["LOC"], "Local", half
            ),
            single_entity_score_table_html(
                results_dict["TIP"], "Tipo", half
            ),
        ],
        className=columns_classes,
    )

    row2 = html.Div(
        [
            single_entity_score_table_html(
                results_dict["PRP"], "Perpetrador", half
            ),
            single_entity_score_table_html(
                results_dict["ORG"], "Organização", half
            ),
        ],
        className=columns_classes,
    )

    row3 = html.Div(
        [
            single_entity_score_table_html(
                results_dict["ACA"], "Ação", third
            ),
            single_entity_score_table_html(
                results_dict["DAT"], "Quando", third
            ),
            single_entity_score_table_html(
                results_dict["VIT"], "Vítima", third
            ),
        ],
        className=columns_classes,
    )
    return html.Div([row1, row2, row3])


def single_entity_score_table_html(most_common, entity_type, width):
    """
    Get the html block for a single entity's score table.

    Args:
        most_common ([str]): The most common entities of this type.
        entity_type (str): The entity type (e.g., "vítima")
        width (the width of the table in terms of the table container). Valid
            widths are specified according to bulma column widths, e.g.,
            "is-half".

    Returns:
        (dash_html_components.Div): A single entity table html block.
    """
    n_results = len(most_common)

    formatted_n_results = min(n_results, MAX_N_ROWS_FOR_EACH_ENTITY_TABLE)
    if formatted_n_results == MAX_N_ROWS_FOR_EACH_ENTITY_TABLE:
        table_label = f"Top {formatted_n_results} entidades"
    else:
        table_label = f"Todas as {formatted_n_results} entidades"

    color = entity_color_map[entity_type.lower()]
    header_entity_type = html.Span(
        f"{entity_type}", className=f"msweb-has-{color}-txt"
    )
    header_table_label = html.Span(f": {table_label}")

    header_entity_type = html.Th([header_entity_type, header_table_label])
    header_score = html.Th("escore")
    header = html.Tr([header_entity_type, header_score])

    rows = [None] * n_results

    row_number = 0
    for dic in most_common:
        ent, count, score = dic['name'], dic['count'], dic['score']
        entity = html.Td(ent, className="has-width-50")
        score = html.Td("{:.2f}".format(score), className="has-width-50")
        rows[row_number] = html.Tr([entity, score])
        row_number += 1
        if row_number == MAX_N_ROWS_FOR_EACH_ENTITY_TABLE - 1:
            break
    table = html.Table(
        [header] + rows,
        className="table is-fullwidth is-bordered is-hoverable is-narrow is-striped",
    )
    return html.Div(table, className=f"column {width}")
