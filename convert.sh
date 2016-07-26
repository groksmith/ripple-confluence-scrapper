#!/usr/bin/env bash

INVALID_ENV_MESSAGE="No directory specified."

if [ -z "$1" ]; then
	echo "$INVALID_ENV_MESSAGE"
	exit 1
fi

. venv/bin/activate

cnf-convert $1