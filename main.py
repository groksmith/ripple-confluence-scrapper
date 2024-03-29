# -*- coding: utf-8 -*-
import click
import os
from time import sleep
import html2text
import shutil
from tqdm import tqdm
import datetime
from colorama import Fore, Back, Style, init
from bs4 import BeautifulSoup
import re

# Init colorama
init()

# Set necessary variables
BASE_DIR = os.path.dirname(os.path.realpath(__file__))


@click.command()
@click.argument('src-dir')
@click.option('--silent', default=False, help='Runs in silent mode with not output.')
@click.option('--keep-tmp', default=False, help='If set to true, the temporary folder will not be removed.')
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

    if not os.path.isfile(os.path.join(src_dir, 'index.html')):
        log("error", "'index.html' file is missing from {},".format(src_dir), silent)

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

    names = get_names(src_dir=src_dir, silent=silent)

    ####################################################################################################################
    # Converting
    ####################################################################################################################

    log("info", "Converting...", silent)

    log("info", "Copying necessary directories", silent)

    if os.path.isdir(os.path.join(tmp_dir, 'attachments')):
        copytree(src=os.path.join(tmp_dir, 'attachments'), dst=os.path.join(out_dir, 'attachments'), silent=silent)

    if os.path.isdir(os.path.join(tmp_dir, 'images')):
        copytree(src=os.path.join(tmp_dir, 'images'), dst=os.path.join(out_dir, 'images'), silent=silent)

    log("success", "Success\n", silent)

    log("info", "Convert files to Markdown", silent=silent)
    for file in tqdm(os.listdir(tmp_dir), disable=silent):
        sleep(0.01)

        if file.endswith(".html"):
            f = open(os.path.join(tmp_dir, file), 'r')
            md = convert_content(f.read(), names)
            new_filename = str(names[file]) + ".md" if file in names.keys() else file.replace('.html', '.md')
            nf = open(os.path.join(out_dir, new_filename), 'w')
            nf.write(md)
    log("success", "Success\n", silent)

    if not keep_tmp:
        log("info", "Removing temporary directory", silent=silent)
        shutil.rmtree(tmp_dir)
        log("success", "Success\n", silent)

    log("success", "All files are in '{}' directory\n".format(out_dir), silent)


def convert_content(content, names):
    soup = BeautifulSoup(content, "html.parser")

    for td in soup.findAll("td"):
        for code in td.findAll("code"):
            code.unwrap()

        td.string = str(td.text).strip()
        td.string = str(td.text).replace("\n", " ")

    for td in soup.findAll("th"):
        for p in td.findAll("p"):
            p.unwrap()

    breadcrumbs = soup.findAll('div', id='breadcrumb-section')

    for breadcrumb in breadcrumbs:
        if breadcrumb is not None:
            breadcrumb.extract()

    page_metadatas = soup.findAll('div', {'class': 'page-metadata'})

    for page_metadata in page_metadatas:
        if page_metadata is not None:
            page_metadata.extract()

    footer = soup.find('div', id='footer')

    if footer is not None:
        footer.extract()

    anchors = soup.findAll("a")

    for anchor in anchors:
        if str(anchor['href']).startswith("#"):
            anchor['href'] = "anchor-hash" + anchor['href']

    codes = soup.findAll("code")

    for code in codes:
        anchors = code.findAll("a")
        for anchor in anchors:
            if anchor.parent.name == 'code':
                anchor.parent.unwrap()

    # Convert callouts
    callouts = soup.findAll('div', {'class': 'confluence-information-macro'})

    for callout in callouts:
        output = None
        body = callout.find("div", {"class": "confluence-information-macro-body"})

        if body is not None:
            output = "**Note:** " + str(body)

        if output is not None:
            output = html2text.html2text(output)
            # output = output.replace("\n", "<br/>")
            output = output.replace("**Note:** <br/><br/>", "**Note:** ")
            output = re.sub(' +', ' ', output)
            output = output.replace('\n ', '\n')
            output = output.replace(' \n', '\n')
            output = output.replace(' \n ', '\n')
            output = output.replace('\n\n\n', '')

            output = BeautifulSoup(output, "html.parser")
            callout.replaceWith(output)

    for macro in soup.findAll(True, {'class': [
        'confluence-information-macro',
        'confluence-information-macro-information',
        'conf-macro output-block'
    ]}):
        if macro is not None:
            tmp = html2text.html2text(str(macro))
            tmp = "&nbsp;&nbsp;&nbsp;&nbsp;" + tmp
            tmp = BeautifulSoup(tmp, "html.parser")
            macro.replaceWith(tmp)

    # Indent code samples
    for sample in soup.findAll(True, {'class': [
        'code',
        'panel',
        'pdl',
        'conf-macro',
        'output-block'
    ]}):
        if sample is not None:
            tmp = html2text.html2text(str(sample))
            tmp = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + tmp
            tmp = BeautifulSoup(tmp, "html.parser")
            sample.replaceWith(tmp)

    for li in soup.findAll("li"):
        s = BeautifulSoup(str(li), "html.parser")
        code = s.find("code")
        pre = s.find("pre")
        brs = s.findAll("br")

        if code is not None:
            tmp = "**SPACE****SPACE****SPACE****SPACE****SPACE**" + str(code)
            tmp = BeautifulSoup(tmp, "html.parser")
            code.replaceWith(tmp)

        if pre is not None:
            tmp = "**SPACE****SPACE****SPACE****SPACE****SPACE**" + str(pre)
            tmp = BeautifulSoup(tmp, "html.parser")
            pre.replaceWith(tmp)

        for br in brs:
            tmp = str(br) + '**SPACE****SPACE****SPACE****SPACE****SPACE**'
            tmp = BeautifulSoup(tmp, "html.parser")
            br.replaceWith(tmp)

        li.replaceWith(s)

    pattern = re.compile(r'\b(' + '|'.join(names.keys()) + r')\b')
    result = pattern.sub(lambda x: names[x.group()] + ".html", str(soup))

    output = html2text.html2text(result, baseurl='', bodywidth=1000000000)
    output = output.replace("Documentation :", "")
    output = output.replace("**SPACE**", "&nbsp;")
    output = output.replace("anchor-hash#", "#")

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


def get_names(src_dir, silent):
    log("info", "Getting names for files", silent)
    # pageSection
    names = {}

    soup = BeautifulSoup(open(os.path.join(src_dir, "index.html"), "r"), "html.parser")
    items = soup.findAll("li")

    for item in items:
        links = item.findAll("a")

        for link in links:
            names[link['href']] = slugify(link.text)

    return names


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


def slugify(text):
    """ Simplifies ugly strings into slugyfied ones."""
    text = text.lower()
    for c in [' ', '-', '.', '/']:
        text = text.replace(c, '_')

    text = re.sub('\W', '', text)
    text = text.replace('_', ' ')
    text = re.sub('\s+', ' ', text)
    text = text.strip()
    text = text.replace(' ', '-')

    return text
