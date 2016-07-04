# -*- coding: utf-8 -*-

import os
from utils.confluence import Confluence

# Confluence config
CNF_USERNAME = os.environ.get('CNF_USERNAME', None)
CNF_PASSWORD = os.environ.get('CNF_PASSWORD', None)
CNF_BASE_URL = os.environ.get('CNF_BASE_URL', 'https://ararat.atlassian.net/rest/api/content')

# GitHub config
GH_USERNAME = os.environ.get('GH_USERNAME', None)
GH_PASSWORD = os.environ.get('GH_PASSWORD', None)

if __name__ == '__main__':
    cnf = Confluence(username=CNF_USERNAME, password=CNF_PASSWORD, base_url=CNF_BASE_URL)
    cnf.get_content()
