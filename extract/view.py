# -*- coding: utf-8 -*-

import copy
import json
import urllib

from dash import dcc, html
#import dash_core_components as dcc
#import dash_html_components as html

from resters import ZumbiRestError
from common import (
    common_null_warning_html,
    common_rester_error_html,
    common_warning_html,
    logo_html,
)
from constants import entity_color_map, rester

RESTER_ERROR_TEXT = (
    "Nosso servidor não está conseguindo atender a esta solicitação "
    "Provavelmente estamos em manutenção."
    "Por favor, volte novamente mais tarde."
)

"""
View html blocks for the extract app.

Please do not define callback logic in this file.
"""

# An extension to the global entity color map to include extra entities.
entitiy_color_map_extension = {
    "property value": "aqua",
    "property unit": "yellow",
    "other": None,
}
entity_color_map_extended = copy.deepcopy(entity_color_map)
entity_color_map_extended.update(entitiy_color_map_extension)


def app_view_html():
    """
    The entire app view (layout) for the extract app.

    Returns:
        (dash_html_components.Div): The entire view for the extract app.
    """

    label = html.Label(
        "Cole o texto da matéria para análise:",
        className="is-size-4",
    )
    label_container = html.Div(
        label, className="has-margin-bottom-20 has-text-centered"
    )

    text_area = dcc.Textarea(
        id="extract-text-area",
        spellCheck=True,
        placeholder="Cole o texto da matéria aqui para extrair as entidades nomeadas.",
        className="input is-info is-medium has-min-height-250",
    )
    text_area_div = html.Div(text_area, className="has-margin-5")

    convert_synonyms = dcc.Dropdown(
        id="extract-dropdown-normalize",
        options=[
            {"label": "Não", "value": "no"},
            {"label": "Sim", "value": "yes"},
        ],
        value="no",
        clearable=False,
    )

    convert_synonyms_text = html.Div(
        "Converter sinônimos?", className="is-size-6"
    )
    convert_synonyms_container = html.Div(
        [convert_synonyms_text, convert_synonyms],
        className="is-pulled-right has-margin-5",
    )

    common_button_styling = "button is-size-4 has-margin-5"
    extract_button = html.Button(
        "Extrair entidades",
        id="extract-button",
        className=f"{common_button_styling} is-link",
    )

    suggest_button = html.Button(
        "Sugerir mídias (beta)",
        id="extract-suggest-button",
        className=f"{common_button_styling} is-info",
    )

    random_abstract_button = html.Button(
        "Exemplo",
        id="extract-random",
        className=f"{common_button_styling} is-light",
    )

    loading = dcc.Loading(
        id="loading-extract",
        children=[html.Div(id="extract-results")],
        type="cube",
        color="#21ff0d",
        className="msweb-fade-in",
    )

    loading_container = html.Div(loading)

    logo = logo_html()

    main_app_column = html.Div(
        [
            label_container,
            text_area_div,
            convert_synonyms_container,
            extract_button,
            suggest_button,
            random_abstract_button,
            loading_container,
        ],
        className="column is-three-quarters",
    )

    main_app_columns = html.Div(
        [main_app_column], className="columns is-centered"
    )

    layout = html.Div(
        [logo, main_app_columns], className="container has-margin-top-50"
    )
    return layout


def journal_suggestions_html(text):
    """
    Get an html block of the results for a journal suggestion.

    Args:
        text (the abstract text)

    Returns:
        (dash_html_components.Div): The html block for the journal suggestion
            results.

    """
    try:
        results = rester.get_journal_suggestion(text)
    except ZumbiRestError:
        rester_error_txt = RESTER_ERROR_TEXT

        return common_rester_error_html(rester_error_txt)
    label = html.Label("Suggested journals (Top 10 shown)")
    label_container = html.Div(label, className="is-size-4")
    explanation = html.Div(
        "Your abstract is most similar to abstracts found in the following journals.",
        className="is-size-6",
    )
    beta_label = html.Div(
        "Journal suggestion is a beta feature of Matscholar. Please stay tuned for improvements.",
        className="is-size-6",
    )
    label_and_explanation = html.Div(
        [label_container, explanation, beta_label],
        className="has-margin-top-30 has-margin-bottom-20",
    )

    common_size = "is-size-5"
    header_jname = html.Th("Journal Name", className=common_size)
    header_confidence = html.Th("Score", className=common_size)

    header = html.Tr([header_jname, header_confidence])
    n_results = len(results)

    rows = [None] * n_results
    for i in range(n_results):
        result = results[i]
        journal = result[0]
        confidence = "{0:.1f}%".format(result[1] * 100)
        rows[i] = html.Tr(
            [
                html.Td(
                    journal, className=common_size + " msweb-clicker-green"
                ),
                html.Td(
                    confidence, className=common_size + " msweb-clicker-green"
                ),
            ]
        )

    table = html.Table(
        [header] + rows,
        className="table is-fullwidth is-bordered is-hoverable is-narrow is-striped",
    )

    return html.Div([label_and_explanation, table])


def extract_entities_results_html(text, normalize):
    """
    Get an html block of the results for an entity extraction.

    Args:
        text (str): The abstract text to extract entities from.
        normalize (bool): Whether to normalize the entities or not.

    Returns:
        (dash_html_components.Div): The html block for the entity extraction
            results.
    """
    try:
        result = rester.get_ner_tags(
            text, concatenate=True, normalize=normalize
        )
    except ZumbiRestError:
        rester_error_txt = RESTER_ERROR_TEXT
        return common_rester_error_html(rester_error_txt)
    tagged_doc = result["tags"]
    relevance = result["relevance"]
    highlighted = highlight_entities_html(tagged_doc)

    # Add the warning
    if not relevance:
        warning_header_txt = "Warning! Abstract not relevant."
        warning_body_txt = (
            "Our classifier has flagged this document as not relevant to "
            "inorganic materials science. Expect lower than optimum "
            "performance."
        )
        warning = common_warning_html(
            warning_header_txt, warning_body_txt, "is-fullwidth"
        )
    else:
        warning = html.Div("")

    # Update download link
    doc = {"sentences": []}
    for sent in tagged_doc:
        new_sent = []
        for token, tag in sent:
            new_sent.append({"token": token, "tag": tag})
        doc["sentences"].append(new_sent)
    json_string = json.dumps(doc)
    json_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(
        json_string
    )
    download_link = html.A(
        "Fazer Download das entidades como json",
        id="entity-download-link",
        href=json_string,
        download="tagged_docs.json",
        target="_blank",
    )
    download_container = html.Div(
        download_link, className="has-text-size-4 has-margin-top 10"
    )

    label = html.Label("Etiquetas extraídas:")
    label_container = html.Div(label, className="is-size-4 has-margin-top-30")

    highlighted_container = html.Div(highlighted)

    label_label = html.Label("Etiquetas:")
    label_label_container = html.Div(
        label_label, className="is-size-4 has-margin-top-30"
    )

    entity_colormap_key = copy.deepcopy(entity_color_map_extended)
    entities_keys = []
    for e, color in entity_colormap_key.items():
        # don't need the "other" label
        if e == "other":
            continue
        entity_key = html.Div(
            e, className=f"is-size-4 msweb-is-{color}-txt has-text-weight-bold"
        )
        entity_key_container = html.Div(
            entity_key, className="flex-column is-narrow has-margin-5 box"
        )
        entities_keys.append(entity_key_container)

    entity_key_container = html.Div(
        entities_keys, className="columns is-multiline has-margin-5"
    )

    results = html.Div(
        [
            warning,
            label_container,
            highlighted_container,
            label_label_container,
            entity_key_container,
            download_container,
        ]
    )
    return results


def highlight_entities_html(tagged_doc):
    """
    Get the html block for the tagged document returned by the rester.

    Args:
        tagged_doc ([list]): A nested list by sentence - entity nesting

    Returns:
        (dash_html_components.Div): The highlighted entities as an html block.
    """
    tagged_flat1 = [i for sublist in tagged_doc for i in sublist]
    tagged_doc = tagged_flat1

    text_size = "is-size-5"

    entities_containers = [None] * len(tagged_doc)

    # Mapping entity shortcodes returned by the rester to their entity labels
    local_entity_shortcode_map = {
        "PER": "pessoa",
        "MED": "mídia",
        "EDU": "org. educação/pesquisa",
        "ORG": "org. comercial",
        "GOV": "org. governamental",
        "CITY": "cidade",
        "CTRY": "país",
        "POL": "polícia",
        "WRK": "obra",
        "MOV": "movimento",
        "O": "other",
    }

    all_tags = []
    for i, tagged_token in enumerate(tagged_doc):
        token, tag = tagged_token[0], tagged_token[1]

        # todo: remove when backend internal NER is fixed.
        # it is the source of these I-* tags which crash the callback
        if "I-" in tag:
            tag = "O"

        all_tags.append(tag)
        color = entity_color_map_extended[local_entity_shortcode_map[tag]]

        if color is None:
            entity_styled = html.Div(f" {token} ", className=text_size)
            entity_container = html.Div(
                entity_styled,
                className="flex-column is-narrow has-margin-left-5 has-margin-right-5",
            )
        else:
            # the entity is other and we need to not highlight it
            entity_styled = html.Div(
                token, className=f"msweb-is-{color}-txt {text_size}"
            )

            entity_container = html.Div(
                entity_styled,
                className="flex-column is-narrow has-margin-left-5 has-margin-right-5 has-text-weight-bold",
            )
        entities_containers[i] = entity_container
    entities = html.Div(
        entities_containers, className="columns is-multiline has-margin-5"
    )

    if all([t == "O" for t in all_tags]):
        return html.Div("No entities found!", className="is-size-5")

    return entities


def no_abstract_warning_html():
    """
    Get the html block when no abstract is entered.

    Returns:
        (dash_html_components.Div): The warning for no abstract, as an
            html block.

    """
    return common_null_warning_html("Nenhum texto inserido")
