# -*- coding: utf-8 -*-

import logging

logging.basicConfig(filename='app.log', format='%(levelname)s %(asctime)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Confluence(object):
    def __init__(self, username, password, base_url):
        """
        Class to interact with Confluence API
        :param username:
        :param password:
        :param base_url:
        """
        self.username = username
        self.password = password
        self.base_url = base_url if base_url.endswith('/') else base_url + "/"

    def get_content(self):
        # response = requests.get(url=self.base_url, auth=(self.username, self.password))
        # return response.json()
        pass

    @staticmethod
    def _send_request(request_type, url, params):
        pass
