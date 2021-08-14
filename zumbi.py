# -*- coding: utf-8 -*-

import requests
import json
import warnings
from os import environ

"""
This module provides classes to interface with the Zumbi REST
API.

To make use of the Zumbi API, you need to obtain an API key by
contacting Jefferson O. Silva at silvajo@pucsp.br.
"""

__author__ = "Jefferson O. Silva"
__credits__ = "All the team"
__copyright__ = "Copyright 2021, PUC-SP Intelligence Team"
__version__ = "0.1"
__maintainer__ = "Jefferson O. Silva"
__email__ = "silvajo@pucsp.br"
__date__ = "January, 1, 2021"

class Rester(object):
    """
    A class to conveniently interface with the Stract REST interface.
    The recommended way to use our StractRester is with the "with" context
    manager to ensure that sessions are properly closed after usage::

        with StractRester("API_KEY") as m:
            do_something

    StractRester uses the "requests" package, which provides for HTTP connection
    pooling. All connections are made via https for security.

    Args:
        api_key (str): A String API key for accessing the Project
            REST interface. Please obtain your API key by emailing
            Jefferson O. Silva at silvajo@pucsp.br. If this is None,
            the code will check if there is a "STRACT_API_KEY" environment variable.
            If so, it will use that environment variable. This makes
            easier for heavy users to simply add this environment variable to
            their setups and MatstractRester can then be called without any arguments.
        endpoint (str): Url of endpoint to access the Zumbi REST
            interface. Defaults to the standard address, but can be changed to other
            urls implementing a similar interface.
    """

    def __init__(self, api_key=None, endpoint=None):
        self.api_key = api_key if api_key else environ.get('ZUMBI_API_KEY', None)
        #if not self.api_key:
        #    raise ZumbiRestError(
        #        "Please specify an API key or request one through the "
        #        "Zumbi team."
        #    )

        if endpoint:
            self.preamble = endpoint
        else:
            self.preamble = environ.get('ZUMBI_ENDPOINT', None)
            if not self.preamble:
                self.preamble = "https://0.0.0.0:8081"

        self.session = requests.Session()
        self.session.headers = {"x-api-key": self.api_key}

    def __enter__(self):
        """
        Support for "with" context.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Support for "with" context.
        """
        self.session.close()

    def _make_request(self, sub_url, payload=None, method="GET"):
        response = None
        data = None
        url = self.preamble + sub_url
        print(url)
        try:
            if method == "POST":
                response = self.session.post(url, json=payload, verify=True)
            else:
                #response = self.session.get(url, params=payload, verify=True)
                response = self.session.get(url)
            #print("response: " + str(response))
            if response.status_code in [200, 400]:
                data = json.loads(response.text)
            #with open('json/file01.json') as f:
            #    text = f.read()
            #    data = json.loads(text)
            #data = data[0]
            #print("data: " + str(data))
            #tdata = type(data)
            #if isinstance(data, dict):
            #    if data.get("warning"):
            #        warnings.warn(data["warning"])
            return data
            #return data
            #else:
            #    raise ZumbiRestError(response)

        except Exception as ex:
            msg = "{}. Content: {}".format(str(ex), response.content) \
                if hasattr(response, "content") else str(ex)
            print(msg)
            raise ZumbiRestError(msg)

    def __search(self, group_by, entities, text=None, elements=None, top_k=10):
        method = "POST"
        sub_url = "/search/"
        query = {'entities': entities, 'group_by': group_by, 'limit': top_k}
        if text:
            query['text'] = text
        if elements:
            query['elements'] = elements

        return self._make_request(sub_url, payload=query, method=method)

    def abstracts_search(self, entities, text=None, elements=None, top_k=10):
        """
        Search for news by entities and text filters.

        Args:

            entities: dict of entity lists (list of str) to filter by. Keys are
              singular snake case for each of the entity types (entity types list)

            text: english text, which gets searched on via Elasticsearch.

            elements: string or list of strings; filter by elements

            top_k: (int or None) if int, specifies the number of matches to
                return; if None, returns all matches.

        Returns:
            List of entries (dictionaries) with abstracts, entities, and metadata.
        """

        method = "POST"
        sub_url = "/entries/"
        query = {'query': {'entities': entities, 'text': text},
                 'limit': top_k}

        return self._make_request(sub_url, payload=query, method=method)

    def entities_search(self, entities, text=None, elements=None, top_k=10):
        method = "GET"
        #sub_url = "/entities/"
        sub_url = "/summary"
        query = {'query': {'entities': entities, 'text': text},
                 'limit': top_k}
        #print(query)
        return self._make_request(sub_url, payload=query, method=method)

    def get_journals(self):
        """
        Get a list of all distinct journals in the db.

        Returns:
            List of distinct journal names
        """

        method = "GET"
        sub_url = "/stats/journals"
        return self._make_request(sub_url, method=method)

    def get_db_stats(self):
        """
         Get the statistics about the Matscholar db.

        Returns:
            dictionary of stats. e.g
              {'abstract_count': 4941666,
               'entities_count': 518026,
               'materials_count': 290952}

        """

        method = "GET"
        sub_url = "/stats/"

        return self._make_request(sub_url, method=method)


class ZumbiRestError(Exception):
    """
    Exception class for Rester.
    Raised when the query has problems, e.g., bad query format.
    """
    pass
