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

install_venv() {
    if [[ -z "${1-}" ]]; then
        echo -e "${red}[ERROR] USAGE: install_venv <venv_path>${nocolor}"
        exit 1;
    fi

    python -m venv $1 || virtualenv $1
}


### Main
echo -e "${yellow}[INFO] [${BASH_SOURCE[0]}] executed.${nocolor}"

(
cd_into_script_path
cd ..

venv_path=venv_sdisttest
echo -e "${yellow}[INFO] Clearing previous builds, venv. [rm -rf dist, ${venv_path}] ...${nocolor}"
rm -rf ${venv_path}
rm -rf dist

echo -e "${yellow}[INFO] Build ... ${nocolor}"
python setup.py sdist

echo -e "${yellow}[INFO] Making virtual environment [$PWD/${venv_path}] ... ${nocolor}"

if ! install_venv ${venv_path}; then
    echo -e "${red}[ERROR] Making virtual environment failed.\n\
Use python3 or Install virtualenv(python2).${nocolor}"
    exit 1;
fi
source ${venv_path}/bin/activate

echo -e "${yellow}[INFO] Install ... ${nocolor}"
pip install dist/*.tar.gz

(
echo -e "${yellow}[INFO] [$ mkdir -p tmp && cd tmp && python -c \"import dockerfile_bakery\"] ${nocolor}"
mkdir -p tmp && cd tmp
python -c "import dockerfile_bakery"
)

deactivate
echo -e "${yellow}[INFO] Clearing [tmp, dist, ${venv_path}] ...${nocolor}"
rm -rf tmp
rm -rf dist
rm -rf ${venv_path}

echo -e "${yellow}[INFO] [${BASH_SOURCE[0]}] Done.${nocolor}"
)
