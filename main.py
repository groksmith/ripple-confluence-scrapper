# -*- coding: utf-8 -*-
import click
import os
from config import Config
from converter import Converter

pass_config = click.make_pass_decorator(Config, ensure=True)


@click.command()
@click.argument('src-dir')
@pass_config
def cli(config, src_dir):
    """This cli tool converts confluence html to markdown"""
    src_dir = os.path.join(config.base_dir, src_dir)

    converter = Converter(config=config, src_dir=src_dir)
    converter.convert()
