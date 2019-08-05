{{ FROM }}

ENV TF_NEED_CUDA=1
ENV CUDA_PATH=/usr/local/cuda
ENV CUDA_TOOLKIT_PATH=/usr/local/cuda

### Region build variables
# These variables are already declared in tf_bazel_builder_base image.
# Explicitly declare Environment variables for "./configure" before the bazel build
ENV TF_CUDA_VERSION=${TF_CUDA_VERSION}
ENV TF_CUDNN_VERSION=${TF_CUDNN_VERSION}
ENV PYTHON_LIB_PATH=${PYTHON_LIB_PATH}
{{ compute_capabilities }}
{{ xla }}
## Region end

ENV OUTPUT_TAG=cuda${TF_CUDA_VERSION}cudnn${TF_CUDNN_VERSION}capability${OUTPUT_CUDA_COMPUTE_CAPABILITIES}${OUTPUT_XLA}
ENV OUTPUT_VERSION_WITH_TAG=${TENSORFLOW_VERSION}.${OUTPUT_TAG}
ENV OUTPUT_WHEEL_FILENAME=tensorflow-${OUTPUT_VERSION_WITH_TAG}-${OUTPUT_WHEELNAME_PYTHON_VERSION}-linux_x86_64.whl
ENV OUTPUT_C_LIBRARY_FILENAME=libtensorflow-${OUTPUT_VERSION_WITH_TAG}.tar.gz

RUN ./tf_bazel_builder.sh

WORKDIR /build

CMD /bin/bash
