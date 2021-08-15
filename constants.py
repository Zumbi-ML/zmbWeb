# -*- coding: utf-8 -*-

import copy
import os

from zumbi import Rester
from util import load_static_data_file

"""
Load the static files for the dash app once, and not on import of


Also define all constants which are used across all apps.
"""

# All static files
db_stats = load_static_data_file("db_statistics.json")
example_searches = load_static_data_file("example_searches.json")
sample_abstracts = load_static_data_file("sample_abstracts.json")

ZMB_ENDPOINT = "http://0.0.0.0:8081"
ZMB_API_KEY = "not_a_real_api_key"

# The API endpoint URL defines the Rester
endpoint = os.environ.get("ZUMBI_ENDPOINT", ZMB_ENDPOINT)
api_key = os.environ.get("ZUMBI_API_KEY", ZMB_API_KEY)
rester = Rester(endpoint=endpoint, api_key=api_key)


# Artifacts for elastic testing
fake_elastic_credential = "not_a_real_elastic_credential"

# Elasticsearch credentials
elastic_host = os.environ.get("ELASTIC_HOST", fake_elastic_credential)
elastic_user = os.environ.get("ELASTIC_USER", fake_elastic_credential)
elastic_pass = os.environ.get("ELASTIC_PASS", fake_elastic_credential)

# The mapping of entity type to shortcode
entity_shortcode_map = {
    "pes": "PER",
    "mid": "MED",
    "educ": "EDU",
    "com": "ORG",
    "gov": "GOV",
    "cid": "CITY",
    "pais": "CTRY",
    "pol": "POL",
    "obra": "WRK",
    "mov": "MOV"
}

# The mapping of entity type to color
entity_color_map = {
    "pes": "blue",
    "mid": "purple",
    "educ": "orange",
    "com": "turq",
    "gov": "pink",
    "cid": "red",
    "pais": "green",
    "pol": "blue",
    "obra": "purple",
    "mov": "orange"
}

# The mapping of all search filters
search_filter_color_map = copy.deepcopy(entity_color_map)
search_filter_color_map["texto"] = "grey"

# The valid entity types
valid_entity_filters = list(entity_shortcode_map.keys())

# All valid search filter keys
valid_search_filters = valid_entity_filters + ["texto"]

# How long before the Flask cache times out and is voided.
cache_timeout = 60

# whether there is an outage or not
outage = bool(int(os.environ.get("ZUMBI_OUTAGE", 0)))
