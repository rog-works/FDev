#!/bin/bash

cwd=$(cd $(dirname $0); pwd)
appdir=${cwd}/../

source ${cwd}/.env.sh

cd ${appdir} && vendor/tranp/bin/transpile.sh -c config.yml $*
