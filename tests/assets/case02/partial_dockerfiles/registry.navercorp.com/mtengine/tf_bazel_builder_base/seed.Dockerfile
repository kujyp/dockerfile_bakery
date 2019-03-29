{{ from_cuda_python_base_with_nccl_installation }}

RUN yum install -y \
 which unzip python-devel patch \
 && rm -rf /var/cache/yum

RUN touch /usr/include/stropts.h

{{ tensorflow }}

WORKDIR tensorflow

RUN ./tensorflow/tools/ci_build/install/install_bazel.sh

ADD tf_bazel_builder.sh tf_bazel_builder.sh

CMD /bin/bash
