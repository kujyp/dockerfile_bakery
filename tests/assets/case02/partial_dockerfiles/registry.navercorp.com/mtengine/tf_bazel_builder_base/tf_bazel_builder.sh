#!/bin/bash -e

yellow="\033[0;33m"
red="\033[0;31m"
nocolor="\033[0m"


### Main
if [[ -z "${OUTPUT_WHEEL_FILENAME}" ]]; then
    echo -e "${red}[ERROR] Environment variable OUTPUT_WHEEL_FILENAME is empty. [${OUTPUT_WHEEL_FILENAME}]${nocolor}"
    exit 1;
fi

if [[ -z "${OUTPUT_C_LIBRARY_FILENAME}" ]]; then
    echo -e "${red}[ERROR] Environment variable OUTPUT_C_LIBRARY_FILENAME is empty. [${OUTPUT_C_LIBRARY_FILENAME}]${nocolor}"
    exit 1;
fi

mkdir -p /build

printenv | grep TF_ >> /build/configures.txt
yes "" | ./configure >> /build/configures.txt
cat /build/configures.txt

bazel build --show_result=0 --config=opt //tensorflow/tools/pip_package:build_pip_package
./bazel-bin/tensorflow/tools/pip_package/build_pip_package build

bazel build --config=opt //tensorflow/tools/lib_package:libtensorflow

mv bazel-bin/tensorflow/tools/lib_package/libtensorflow.tar.gz /build/${OUTPUT_C_LIBRARY_FILENAME}
mv build/tensorflow-*.whl /build/${OUTPUT_WHEEL_FILENAME}
