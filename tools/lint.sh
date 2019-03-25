#!/bin/bash -e

yellow="\033[0;33m"
red="\033[0;31m"
nocolor="\033[0m"


cd_into_gitrootdir() {
    local topdir=$(git rev-parse --show-toplevel)
    cd ${topdir}
}

command_exists() {
    command -v "$@" > /dev/null 2>&1
}


### Main
echo -e "${yellow}[INFO] [${BASH_SOURCE[0]}] executed.${nocolor}"

if ! command_exists flake8; then
    echo -e "${red}[ERROR] Install flake8 first. \n\
pip install flake8==3.6.0${nocolor}"
    exit 1;
fi

(
cd_into_gitrootdir

echo -e "${yellow}[INFO] flake8 version: [$(flake8 --version)]${nocolor}"
# E501 - line too long
flake8 --exclude 'venv*,build' --ignore E501
)
echo -e "${yellow}[INFO] [${BASH_SOURCE[0]}] Done.${nocolor}"
