# -*- coding: utf-8 -*-

import os

# Confluence config
CNF_USERNAME = os.environ.get('CNF_USERNAME', None)
CNF_PASSWORD = os.environ.get('CNF_PASSWORD', None)
CNF_BASE_URL = os.environ.get('CNF_BASE_URL', None)

# GitHub config
GH_USERNAME = os.environ.get('GH_USERNAME', None)
GH_PASSWORD = os.environ.get('GH_PASSWORD', None)

if __name__ == '__main__':
    pass
