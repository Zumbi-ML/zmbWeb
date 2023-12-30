# -*- coding: utf-8 -*-

from dash import html
from zmb_labels import ZmbLabels
from constants import rester
from search.common import (
    big_label_and_disclaimer_html,
    common_results_container_style,
    no_results_html,
)

# Maximum number of rows shown for each entity table. 10 usually looks good.
MAX_N_ROWS_FOR_EACH_ENTITY_TABLE = 10

# Maximum number of columns to fit on the screen
MAX_N_COLUMNS = 3

big_label_and_disclaimer = big_label_and_disclaimer_html("entities")
entities_no_results_html = no_results_html(pre_label=big_label_and_disclaimer)

def entities_results_query(entity_query, raw_text):
    results = rester.entities_search(
        entity_query, text=raw_text, top_k=MAX_N_ROWS_FOR_EACH_ENTITY_TABLE
    )
    return entities_results_html(results)

def entities_results_summary():
    results = rester.entities_summary(
        None, text=None, top_k=MAX_N_ROWS_FOR_EACH_ENTITY_TABLE
    )
    return entities_results_html(results)

def entities_results_html(results):
    if results_empty(results):
        return entities_no_results_html
    else:
        return construct_results_container(results)

def results_empty(results):
    """
    Check if the results are empty.

    Args:
        results (dict): The result dictionary.

    Returns:
        bool: True if results are empty, False otherwise.
    """
    return results is None or not any(results.values())

def construct_results_container(results):
    """
    Construct the container for displaying results.

    Args:
        results (dict): The result dictionary.

    Returns:
        dash_html_components.Div: The results container HTML block.
    """
    all_tables = all_score_tables_html(results)
    return html.Div(
        children=[big_label_and_disclaimer, all_tables],
        className=common_results_container_style(),
    )

def all_score_tables_html(results_dict):
    columns_classes = "columns is-desktop is-centered"
    div_rows, div_elems = [], []
    k = 0

    for entity_ in ZmbLabels.all_classes():
        if entity_.api() not in results_dict:
            continue

        k += 1
        div_elems.append(
            single_entity_score_table_html(results_dict[entity_.api()], entity_, "is-one-third")
        )

        if should_add_row(k, len(results_dict)):
            div_rows.append(html.Div(div_elems, className=columns_classes))
            div_elems = []

    return html.Div(div_rows)

def should_add_row(k, total_results):
    """
    Determine if a new row should be added to the results layout.

    Args:
        k (int): Current entity type counter.
        total_results (int): Total number of result types.

    Returns:
        bool: True if a new row should be added, False otherwise.
    """
    return k % MAX_N_COLUMNS == 0 or k == total_results

def single_entity_score_table_html(most_common, entity_, width):
    n_results = len(most_common)
    formatted_n_results = min(n_results, MAX_N_ROWS_FOR_EACH_ENTITY_TABLE)
    table_label = create_table_label(formatted_n_results)
    header = create_table_header(entity_, table_label)
    rows = create_table_rows(most_common)

    table = html.Table(
        [header] + rows,
        className="table is-fullwidth is-bordered is-hoverable is-narrow is-striped",
    )
    return html.Div(table, className=f"column {width}")

def create_table_label(n_results):
    """
    Create a label for the entity table.

    Args:
        n_results (int): Number of results in the table.

    Returns:
        str: The label for the table.
    """
    if n_results == MAX_N_ROWS_FOR_EACH_ENTITY_TABLE:
        return f"Top {n_results} entities"
    else:
        return f"All {n_results} entities"

def create_table_header(entity_, table_label):
    """
    Create the header for the entity table.

    Args:
        entity_ (ZmbLabel class): The entity class.
        table_label (str): The label for the table.

    Returns:
        dash_html_components.Tr: The table header.
    """
    color = entity_.color()
    header_entity_type = html.Span(
        f"{entity_.web_label().title()}", className=f"msweb-has-{color}-txt"
    )
    header_table_label = html.Span(f": {table_label}")

    header_entity_type = html.Th([header_entity_type, header_table_label])
    header_score = html.Th("Count")
    return html.Tr([header_entity_type, header_score])

def create_table_rows(most_common):
    """
    Create rows for the entity table.

    Args:
        most_common (list of dicts): Most common entities.

    Returns:
        list of dash_html_components.Tr: The table rows.
    """
    rows = []
    for i, dic in enumerate(most_common):
        if i == MAX_N_ROWS_FOR_EACH_ENTITY_TABLE:
            break
        rows.append(html.Tr([html.Td(dic['name']), html.Td(str(dic['count']))]))
    return rows
