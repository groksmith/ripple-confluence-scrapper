# -*- coding: utf-8 -*-
import datetime
import os


class Config(object):
    def __init__(self):
        self.session_id = str(datetime.datetime.now())
        self.base_dir = os.path.dirname(os.path.realpath(__file__))
