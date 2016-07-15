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
* Export space from confluence to html(do not export comments).
* Copy exported directory to `files` folder.
* Change your working directory to cloned project directory.
* Create virtual environment:  `$ virtualenv -p python3 venv`.
* Activate virtual environment:  `$ source venv/bin/activate`.
* Upgrade setuptools:  `$ pip install --no-use-wheel --upgrade setuptools`.
* Install package: `$ pip install --editable .`
* Run `$ cnf-convert files/{CONFLUENCE_EXPORT_DIRECTORY}`.

Issues
------

* How to save callouts, problem with multline strings.