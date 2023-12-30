# -*- coding: utf-8 -*-

"""
This module defines constants used across the application. It includes configurations for 
API endpoints, database statistics, and other shared resources. Environment variables are 
used for sensitive or environment-specific settings to enhance security and flexibility.
"""

import os
import copy
from resters import Rester
from util import load_static_data_file

# Load static files only once at the start to improve performance
db_stats = load_static_data_file("db_statistics.json")
example_searches = load_static_data_file("example_searches.json")
sample_abstracts = load_static_data_file("sample_abstracts.json")

# API Configuration: Fetches settings from environment variables
endpoint = os.environ.get("ZUMBI_ENDPOINT", "default_endpoint")  # Default value as an example
api_version = os.environ.get("ZUMBI_API_VERSION", "v1")  # Default API version
api_key = os.environ.get("ZUMBI_API_KEY")
if not api_key:
    raise EnvironmentError("API key not set in environment variables")
api_base_path = f"{endpoint}{api_version}"
rester = Rester(endpoint=api_base_path, api_key=api_key)

# Elasticsearch Credentials: Utilize environment variables for security
# Replace 'not_a_real_elastic_credential' with a secure default or error handling
elastic_host = os.environ.get("ELASTIC_HOST", "default_host")
elastic_user = os.environ.get("ELASTIC_USER", "default_user")
elastic_pass = os.environ.get("ELASTIC_PASS", "default_pass")

# Cache Configuration: Time in seconds before the cache expires
cache_timeout = 60  # Cache timeout in seconds

# Service Outage Flag: Determines if there is an ongoing outage (0 for no, 1 for yes)
outage = bool(int(os.environ.get("ZUMBI_OUTAGE", 0)))

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

# Search Filter Color Map: Extends entity color map with additional filters
search_filter_color_map = copy.deepcopy(entity_color_map)
search_filter_color_map["texto"] = "grey"

# Valid Entity Filters: List of all valid entity types for filtering
valid_entity_filters = list(entity_shortcode_map.keys())

# Valid Search Filters: Includes entity filters and additional text filter
valid_search_filters = valid_entity_filters + ["texto"]

# Ensure essential configurations are set
if not endpoint or not api_version:
    raise ValueError("Essential API configurations are missing")

# Add additional checks, documentation, or configurations as needed