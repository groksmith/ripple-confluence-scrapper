#!/usr/bin/env bash

if [ $(which "git" 2>/dev/null | grep -v "not found" | wc -l) -eq 0 ] ; then
    echo "git is not installed"
else
    echo "Updating..."
    git pull
fi

if [ $(which "virtualenv" 2>/dev/null | grep -v "not found" | wc -l) -eq 0 ] ; then
    echo "Installing `virtualenv`..."
    pip3 install virtualenv
fi

if [ ! -d "venv" ]; then
    echo "Creating `virtual environment`..."
    virtualenv -p python3 venv
fi

. venv/bin/activate

pip install --no-use-wheel --upgrade setuptools
pip install --editable .