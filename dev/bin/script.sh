#!/bin/bash

cwd=$(cd $(dirname $0); pwd)
appdir=${cwd}/../

source ${cwd}/.env.sh

domains=()
force=
verbose=
help=
for arg in "$@"; do
	if [ "${arg}" == "-f" ]; then
		force=-f
	elif [ "${arg}" == "-v" ]; then
		verbose=-v
	elif [ "${arg}" == "-h" ]; then
		help=-h
	else
		domains+=(${arg})
	fi
done

if [ ${#domains[@]} -eq 0 ]; then
	domains=("mfs")
fi

if [ "${help}" == "-h" ]; then
	cat << EOS
# Usage
$ bin/script.sh [mfs]
# Example
$ bin/script.sh mfs
$ bin/script.sh -f -v
$ bin/script.sh -h
EOS
else
	for domain in ${domains[@]}; do
		cd ${appdir} && vendor/bin/tranp.exe -c script/${domain}/${domain}_config.yml ${force} ${verbose}
	done
fi
