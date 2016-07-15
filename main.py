# -*- coding: utf-8 -*-
import click
import os
from time import sleep
import html2text
import shutil
from past.builtins.misc import unicode
from tqdm import tqdm
import datetime
from colorama import Fore, Back, Style, init
from bs4 import BeautifulSoup, NavigableString

# Init colorama
init()

# Set necessary variables
BASE_DIR = os.path.dirname(os.path.realpath(__file__))


@click.command()
@click.argument('src-dir')
@click.option('--silent', default=False)
@click.option('--keep-tmp', default=False)
def cli(src_dir, silent, keep_tmp):
    session_id = str(datetime.datetime.now())
    src_dir = os.path.join(BASE_DIR, src_dir)
    tmp_dir = os.path.join(BASE_DIR, 'tmp', session_id)
    out_dir = os.path.join(BASE_DIR, 'out', session_id)

    ####################################################################################################################
    # Checking
    ####################################################################################################################

    log("info", "Checking for issues...", silent)

    """Check for possible errors during conversion"""
    if not os.path.isdir(src_dir):
        log("error", "Directory '{}' not found.".format(src_dir), silent)

    if not os.path.isdir(os.path.join(src_dir, 'attachments')):
        log("error", "'attachments' directory is missing from {},".format(src_dir), silent)

    if not os.path.isdir(os.path.join(src_dir, 'images')):
        log("error", "'images' directory is missing from {},".format(src_dir), silent)

    log("success", "Success\n", silent)

    ####################################################################################################################
    # Preparing
    ####################################################################################################################

    log("info", "Preparing content...", silent)

    log("info", "Copying necessary directories", silent)
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    log("info", "Copying necessary files", silent)
    copytree(src=src_dir, dst=tmp_dir, silent=silent)

    log("success", "Success\n", silent)

    ####################################################################################################################
    # Converting
    ####################################################################################################################

    log("info", "Converting...", silent)

    log("info", "Copying necessary directories", silent)
    copytree(src=os.path.join(tmp_dir, 'attachments'), dst=os.path.join(out_dir, 'attachments'), silent=silent)
    copytree(src=os.path.join(tmp_dir, 'images'), dst=os.path.join(out_dir, 'images'), silent=silent)
    log("success", "Success\n", silent)

    log("info", "Convert files to Markdown", silent=silent)
    for file in tqdm(os.listdir(tmp_dir), disable=silent):
        sleep(0.01)
        # file.endswith(".html")
        if file == 'Payment-States_2425830.html':
            f = open(os.path.join(tmp_dir, file), 'r')
            md = convert_content(f.read())
            nf = open(os.path.join(out_dir, file.replace('.html', '.md')), 'w')
            nf.write(md)
    log("success", "Success\n", silent)

    if not keep_tmp:
        log("info", "Removing temporary directory", silent=silent)
        shutil.rmtree(tmp_dir)
        log("success", "Success\n", silent)


def convert_content(content):
    soup = BeautifulSoup(content, "html.parser")

    for td in soup.findAll("td"):
        for code in td.findAll("code"):
            code.unwrap()

        td.string = str(td.text).strip()
        td.string = str(td.text).replace("\n", " ")

    output = html2text.html2text(str(soup), baseurl='', bodywidth=1000000000)
    return output


def copytree(src, dst, silent):
    """
    Copies entire directory content to destination folder.
    :param silent:
    :param src: Source directory
    :param dst: Destination directory
    """
    for item in tqdm(os.listdir(src), disable=silent):
        sleep(0.01)
        s = os.path.join(src, item)
        d = os.path.join(dst, item)

        if os.path.isdir(s):
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)


def log(level, message, silent):
    """
    Logs message with given level. Exits on error.
    :param level:
    :param message:
    :param silent:
    """
    if not silent:
        if level == "error":
            print(Fore.RED + message + Style.RESET_ALL)
            exit()
        if level == "warning":
            print(Back.YELLOW + message + Style.RESET_ALL)
        if level == "info":
            print(Fore.BLUE + message + Style.RESET_ALL)
        if level == "success":
            print(Fore.GREEN + message + Style.RESET_ALL)


def strip_tags(html, invalid_tags):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup.findAll(True):
        if tag.name in invalid_tags:
            s = ""

            for c in tag.contents:
                if not isinstance(c, NavigableString):
                    c = strip_tags(unicode(c), invalid_tags)
                s += unicode(c)

            tag.replaceWith(s)

    return soup
