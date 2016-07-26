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
* Run `$ sudo chmod a+x install.sh` (this must be done once).
* Run `$ sudo chmod a+x convert.sh` (this must be done once).
* Change your working directory to cloned project directory.
* Run:  `$ ./install.sh`.

Then for converting you can run `$ ./convert {DOCS_DIR}`

Issues
------

* How to save callouts, problem with multline strings.

Suggestions
-----------

* We can setup this project in pypi under private repo. 