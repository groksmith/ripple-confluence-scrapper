# -*- coding: utf-8 -*-


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
