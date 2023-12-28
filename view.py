
from dash import dcc, html
#import dash_core_components as dcc
#import dash_html_components as html
from datetime import date

"""
Defining the core view (layout) component for the entire app.

Please do not define any callback logic in this file.
"""


def core_view_html():
    """
    Getting the core view component (layout) for the entire app.
    Contains the nav bar, footer, etc. All view components are either called
    (preferred) or superceded (not preferred) by this function.

    tl;dr: This function makes the html block for what you see when you load
    the webpage!

    Returns:
        core_view (dash_html_components.Div): An html block for the entire site.

    """

    # The nav bar for all apps
    nav = html.Div(id="core-nav-container")

    # The footer for all apps
    footer_interior = footer_html()
    footer_section = html.Div(footer_interior, className="section")
    footer = html.Footer(footer_section, className="footer has-margin-top-50")

    # The container for individual apps
    app_container = html.Div(
        "", id="core-app-container", className="container is-fluid"
    )
    app_expander = html.Div(
        app_container, className="msweb-is-tall has-margin-20"
    )
    app_expander_container = html.Div(
        app_expander,
        className="msweb-is-tall-container msweb-fade-in has-margin-top-50",
    )

    # External stylesheets should be linked here.
    external_stylesheets = html.Link(
        href="https://fonts.googleapis.com/css?family=Ubuntu&display=swap",
        rel="stylesheet",
        className="is-hidden",
    )

    # Location defines the linking for how to change the app.
    location = dcc.Location(id="core-url", refresh=False)

    core_view = html.Div(
        [external_stylesheets, location, nav, app_expander_container, footer],
        className="msweb-background msweb-fade-in",
    )
    return core_view


def nav_html(page="/"):
    """
    Get the plotly html block for the nav bar.

    Returns:
        (dash_html_components.Div): The nav bar.

    """
    common_nav_item_style = "navbar-item has-text-weight-semibold"

    # Styles for the navbar elements, by their texts
    style_ids = ["extract", "about", "search", "info", "journals"]
    styles = {k: common_nav_item_style for k in style_ids}
    styles["info"] = "navbar-link has-text-weight-semibold"

    highlighted_style = " msweb-is-underlined"
    if page in ["/", "/search"]:
        styles["search"] += highlighted_style
    #elif page == "/extract":
    #    styles["extract"] += highlighted_style
    elif page == "/about":
        # styles["about"] += highlighted_style
        styles["info"] += highlighted_style
    elif page == "/journals":
        # styles["journals"] += highlighted_style
        styles["info"] += highlighted_style
    elif page is None:
        pass
    else:
        raise ValueError(f"Invalid page for highlighting: '{page}'")

    search = dcc.Link(
        "Pesquisar Corpus", href="/search", className=styles["search"]
    )
    #extract = dcc.Link(
    #    "Analisar uma Matéria", href="/extract", className=styles["extract"]
    #)
    about = dcc.Link("Sobre", href="/about", className=styles["about"])
    journals = dcc.Link(
        "Matérias", href="/journals", className=styles["journals"]
    )
    dropdown_items = html.Div([about, journals], className="navbar-dropdown")
    dropdown_link = html.Div("Info", className=styles["info"])
    dropdown = html.Div(
        [dropdown_link, dropdown_items],
        className="navbar-item has-dropdown is-hoverable",
    )
    navbar_start = html.Div(
        #[search, extract, dropdown], className="navbar-start"
        [search, dropdown], className="navbar-start"
    )

    log_in = html.A(
        "PUC-SP",
        href="https://pucsp.br",
        className="button is-dark",
    )
    buttons = html.Div(log_in, className="buttons")
    buttons_item = html.Div(buttons, className="navbar-item")
    navbar_end = html.Div(buttons_item, className="navbar-end")

    navbar_menu_id = "core-navbar-menu"
    navbar_menu = html.Div(
        [navbar_start, navbar_end],
        id=navbar_menu_id,
        className="navbar-menu is-active",
    )

    nav_image = html.Img(src="/assets/logo_mao_branca_v02.png", height=400)
    nav_image_container = html.A(
        nav_image,
        className="navbar-item",
        href="https://github.com/zumbi-ML",
    )

    burger = html.Span(**{"aria-hidden": True})
    nav_burger = html.A(
        [burger] * 3,
        id="core-burger-trigger-cs",
        role="button",
        className="navbar-burger is-active",
        **{
            "aria-label": "menu",
            "aria-expanded": False,
            "data-target": navbar_menu_id,
        },
    )
    navbar_brand = html.Div(
        [nav_image_container, nav_burger], className="navbar-brand"
    )

    nav_menu = html.Div(
        [navbar_brand, navbar_menu],
        className="navbar is-link is-fixed-top",
        role="navigation",
        **{"aria-label": "main navigation"},
    )
    nav_with_padding = html.Div(nav_menu, className="has-navbar-fixed-top")
    return nav_with_padding


def footer_html():
    """
    Make the footer for all apps.

    Returns:
        (dash_html_components.Div): The footer as an html block.

    """
    note_div = html.Div(
        [
            html.Span(
                "Nota: Este motor de busca está em estágio ALFA com o propósito de coletar feedback"
            )
        ]
    )

    common_footer_style = "has-text-weight-bold"

    about_zumbi = html.A(
        "Sobre o Zumbi",
        href="#",
        target="_blank",
        className=common_footer_style,
    )

    privacy_policy = html.A(
        "Política de Privacidade",
        href="#",
        target="_blank",
        className=common_footer_style,
    )

    submit_feedback = html.A(
        "Feedback",
        href="#",
        target="_blank",
        className=common_footer_style,
    )

    footer_link_tree = html.Div(
        [
            about_zumbi,
            html.Span(" | "),
            privacy_policy,
            html.Span(" | "),
            submit_feedback,
        ]
    )

    this_year = str(date.today().year)
    footer_copyright = html.Div(
        html.Span(f"Copyright © {this_year} - PUC-SP Intelligence Team")
    )

    footer = html.Div(
        [note_div, footer_link_tree, footer_copyright],
        id="footer_container",
        className="content has-text-centered",
    )

    footer_container = html.Div(footer)
    return footer_container


def outage_html():
    """
    The html to be shown during a power outage.

    Returns:
        (dash_html_components.Div): the html block for the outage.

    """
    common_text_size = "is-size-5"
    central_image = html.Img(
        src="/assets/logo_zumbi_v02.png", style={"height": "100px"}
    )
    img_link = html.A(
        central_image,
        href="#"
    )
    title = html.Div(
        "Zumbi is currently down because of a server outage.",
        className="is-size-3 has-text-weight-bold",
    )
    explanation1 = html.Div(
        "Our primary servers are run at [TODO] "
        "and are currently undergoing extended maintenance.",
        className=common_text_size,
    )
    explanation2 = html.Div(
        "Please be patient while we wait for our servers to come back online!",
        className=common_text_size,
    )
    contact = html.Div(
        "Need to contact us? Please email help@zumbi.com",
        className=common_text_size,
    )

    inner_container = html.Div(
        [img_link, title, explanation1, explanation2, contact],
        className="has-margin-30",
    )

    container = html.Div(inner_container, className="container")
    return container
