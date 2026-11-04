#!/bin/bash

cwd=$(cd $(dirname $0); pwd)
appdir=${cwd}/../

source ${cwd}/.env.sh

cd ${appdir} && python script/bin/app/master/master.py $*
