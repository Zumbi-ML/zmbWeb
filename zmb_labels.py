# -*- coding: UTF-8 -*-

import pandas as pd

CODES_FILE = 'language/codes_ptBR.tsv'

def get_code_values(label, column):
    df = pd.read_csv(CODES_FILE, sep='\t')
    return df[df.code_id == label][column].values[0]

class ZmbLabels:

    class Source:
        def api():
            return "sources"

        def web_label():
            line = ZmbLabels.Source.api()
            return get_code_values(line, "web_label")

        def examples():
            line = ZmbLabels.Source.api()
            return get_code_values(line, "examples")

        def explanation():
            line = ZmbLabels.Source.api()
            return get_code_values(line, "explanation")

        def color():
            return "purple"

    class People:
        def api():
            return "people"

        def web_label():
            line = ZmbLabels.People.api()
            return get_code_values(line, "web_label")

        def examples():
            line = ZmbLabels.People.api()
            return get_code_values(line, "examples")

        def explanation():
            line = ZmbLabels.People.api()
            return get_code_values(line, "explanation")

        def color():
            return "dark-red"

    class Educational:
        def api():
            return "educational"

        def web_label():
            line = ZmbLabels.Educational.api()
            return get_code_values(line, "web_label")

        def examples():
            line = ZmbLabels.Educational.api()
            return get_code_values(line, "examples")

        def explanation():
            line = ZmbLabels.Educational.api()
            return get_code_values(line, "explanation")

        def color():
            return "orange"


    class Private:
        def api():
            return "private"

        def web_label():
            line = ZmbLabels.Private.api()
            return get_code_values(line, "web_label")

        def examples():
            line = ZmbLabels.Private.api()
            return get_code_values(line, "examples")

        def explanation():
            line = ZmbLabels.Private.api()
            return get_code_values(line, "explanation")

        def color():
            return "turq"


    class Public:
        def api():
            return "public"

        def web_label():
            line = ZmbLabels.Public.api()
            return get_code_values(line, "web_label")

        def examples():
            line = ZmbLabels.Public.api()
            return get_code_values(line, "examples")

        def explanation():
            line = ZmbLabels.Public.api()
            return get_code_values(line, "explanation")

        def color():
            return "pink"

    class City:
        def api():
            return "cities"

        def web_label():
            line = ZmbLabels.City.api()
            return get_code_values(line, "web_label")

        def examples():
            line = ZmbLabels.City.api()
            return get_code_values(line, "examples")

        def explanation():
            line = ZmbLabels.City.api()
            return get_code_values(line, "explanation")

        def color():
            return "red"

    class State:
        def api():
            return "states"

        def web_label():
            line = ZmbLabels.State.api()
            return get_code_values(line, "web_label")

        def examples():
            line = ZmbLabels.State.api()
            return get_code_values(line, "examples")

        def explanation():
            line = ZmbLabels.State.api()
            return get_code_values(line, "explanation")

        def color():
            return "dark-blue"

    class Country:
        def api():
            return "countries"

        def web_label():
            line = ZmbLabels.Country.api()
            return get_code_values(line, "web_label")

        def examples():
            line = ZmbLabels.Country.api()
            return get_code_values(line, "examples")

        def explanation():
            line = ZmbLabels.Country.api()
            return get_code_values(line, "explanation")

        def color():
            return "green"

    class Police:
        def api():
            return "polices"

        def web_label():
            line = ZmbLabels.Police.api()
            return get_code_values(line, "web_label")

        def examples():
            line = ZmbLabels.Police.api()
            return get_code_values(line, "examples")

        def explanation():
            line = ZmbLabels.Police.api()
            return get_code_values(line, "explanation")

        def color():
            return "brown"

    class Work:
        def api():
            return "works"

        def web_label():
            line = ZmbLabels.Work.api()
            return get_code_values(line, "web_label")

        def examples():
            line = ZmbLabels.Work.api()
            return get_code_values(line, "examples")

        def explanation():
            line = ZmbLabels.Work.api()
            return get_code_values(line, "explanation")

        def color():
            return "grey"

    class Movement:
        def api():
            return "movements"

        def web_label():
            line = ZmbLabels.Movement.api()
            return get_code_values(line, "web_label")

        def examples():
            line = ZmbLabels.Movement.api()
            return get_code_values(line, "examples")

        def explanation():
            line = ZmbLabels.Movement.api()
            return get_code_values(line, "explanation")

        def color():
            return "dark-green"

    class Political:
        def api():
            return "political"

        def web_label():
            line = ZmbLabels.Political.api()
            return get_code_values(line, "web_label")

        def examples():
            line = ZmbLabels.Political.api()
            return get_code_values(line, "examples")

        def explanation():
            line = ZmbLabels.Political.api()
            return get_code_values(line, "explanation")

        def color():
            return "black"

    class Law:
        def api():
            return "laws"

        def web_label():
            line = ZmbLabels.Law.api()
            return get_code_values(line, "web_label")

        def examples():
            line = ZmbLabels.Law.api()
            return get_code_values(line, "examples")

        def explanation():
            line = ZmbLabels.Law.api()
            return get_code_values(line, "explanation")

        def color():
            return "blue"

    class Media:
        def api():
            return "media"

        def web_label():
            line = ZmbLabels.Media.api()
            return get_code_values(line, "web_label")

        def examples():
            line = ZmbLabels.Media.api()
            return get_code_values(line, "examples")

        def explanation():
            line = ZmbLabels.Media.api()
            return get_code_values(line, "explanation")

        def color():
            return "light-blue"

    def all_classes():
        """
        Returns the classes of all labels
        """
        return [ \
            ZmbLabels.City,
            ZmbLabels.Country,
            ZmbLabels.State,
            ZmbLabels.Private,
            ZmbLabels.Educational,
            ZmbLabels.Public,
            ZmbLabels.Police,
            ZmbLabels.Law,
            ZmbLabels.People,
            ZmbLabels.Movement,
            ZmbLabels.Political,
            ZmbLabels.Work,
            ZmbLabels.Source,
            #ZmbLabels.Media,
        ]

    def web_lbl_2_api(wlbl):
        for class_ in ZmbLabels.all_classes():
            if (wlbl == class_.web_label()):
                return class_.api()
        return None

    def valid_search_filters():
        return [class_.web_label() for class_ in ZmbLabels.all_classes()]
