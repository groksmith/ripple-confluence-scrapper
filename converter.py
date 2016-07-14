# -*- coding: utf-8 -*-
import shutil

import os
import html2text


class Converter(object):
    def __init__(self, config, src_dir):
        self.config = config
        self.src_dir = src_dir
        self.html_dir = os.path.join(self.config.base_dir, 'tmp', config.session_id, 'html')
        self.md_dir = os.path.join(self.config.base_dir, 'out', config.session_id, 'md')

    def convert(self):
        self._optimize(self.src_dir)
        self._convert()

    def _convert(self):
        for file in os.listdir(self.html_dir):
            if file.endswith(".html"):
                f = open(os.path.join(self.html_dir, file), 'r')
                md = html2text.html2text(f.read())
                nf = open(os.path.join(self.md_dir, file.replace('.html', '.md')), 'w')
                nf.write(md)

    def _optimize(self, src_dir):
        if not os.path.exists(self.html_dir):
            os.makedirs(self.html_dir)

        if not os.path.exists(self.md_dir):
            os.makedirs(self.md_dir)

        self._copytree(src=src_dir, dst=self.html_dir)

    @staticmethod
    def _copytree(src, dst, symlinks=False, ignore=None):
        """
        Copies entire directory content to destination folder.
        :param src:
        :param dst:
        :param symlinks:
        :param ignore:
        """
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)
