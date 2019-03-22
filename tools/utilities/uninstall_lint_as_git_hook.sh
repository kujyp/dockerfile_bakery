#!/bin/bash

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

is_git_directory() {
  git status 1> /dev/null 2>&1
}


### Main
(
cd_into_script_path

if ! is_git_directory
then
  echo -e "${red}[ERROR] [$PWD] is not git directory.${nocolor}"
  exit 1;
fi

topdir=$(git rev-parse --show-toplevel)
echo -e "${yellow}[INFO] [$ rm ${topdir}/.git/hooks/pre-commit] ...${nocolor}"
rm "${topdir}/.git/hooks/pre-commit"

echo -e "${yellow}[INFO] [${BASH_SOURCE[0]}] Done.${nocolor}"
)
