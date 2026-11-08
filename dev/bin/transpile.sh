#!/bin/bash

cwd=$(cd $(dirname $0); pwd)
appdir=${cwd}/../

source ${cwd}/.env.sh

cd ${appdir} && vendor/bin/tranp.exe -c config.yml $*
