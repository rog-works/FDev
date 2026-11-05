#!/bin/bash

set -eux

cwd=$(cd $(dirname $0); pwd)
appdir=${cwd}/../

if [ "$1" == "-d" ]; then
	rm -fr ${appdir}/.cache/master
	rm -fr ${appdir}/.cache/tranp
fi
