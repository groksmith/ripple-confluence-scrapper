Confluence to Markdown converter
================================

Requirements
------
* <a href="https://www.python.org/downloads/" target="_blank">Python +3.4</a>
* <a href="https://virtualenv.pypa.io/en/stable/installation/" target="_blank">Virtualenv</a>

Install these requirements and continue.

Installation
------

* Open **terminal**
* Clone project.
* Change your working directory to cloned project directory.
* Create virtual environment:  `$ virtualenv -p python3 envname`.
* Install package: `$ pip install --editable .`
* Export space from confluence to html(do not export comments).
* Run `$ cnf-convert {CONFLUENCE_EXPORT_DIRECTORY}`.
* pip install --no-use-wheel --upgrade setuptools