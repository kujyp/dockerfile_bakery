#!/bin/bash -e

yellow="\033[0;33m"
red="\033[0;31m"
nocolor="\033[0m"

get_script_path() {
    local _src="${BASH_SOURCE[0]}"
    while [[ -h "${_src}" ]]; do
        local _dir="$(cd -P "$( dirname "${_src}" )" && pwd)"
        local _src="$(readlink "${_src}")"
        if [[ "${_src}" != /* ]]; then _src="$_dir/$_src"; fi
    done
    echo $(cd -P "$(dirname "$_src")" && pwd)
}

cd_into_script_path() {
    local script_path=$(get_script_path)
    cd ${script_path}
}

command_exists() {
    command -v "$@" > /dev/null 2>&1
}


### Main
echo -e "${yellow}[INFO] [${BASH_SOURCE[0]}] executed.${nocolor}"

if ! command_exists pytest; then
    echo -e "${red}[ERROR] Install pytest first. \n\
pip install pytest${nocolor}"
    exit 1;
fi

(
cd_into_script_path
cd ..

PYTHONPATH='.' pytest tests/
)
echo -e "${yellow}[INFO] [${BASH_SOURCE[0]}] Done.${nocolor}"
