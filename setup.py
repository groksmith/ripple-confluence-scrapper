# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='Confluence to Markdown converter',
    version='1.0',
    py_modules=['cnf-convert'],
    install_requires=[
        'Click',
        'html2text',
        'colorama',
        'tqdm',
    ],
    entry_points='''
        [console_scripts]
        cnf-convert=main:cli
    '''
)
