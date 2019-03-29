FROM registry.navercorp.com/mtengine/cuda_python_base:cuda10.0_cudnn7.4_python2.7.15

RUN yum install -y \
 cuda-command-line-tools-10-0 \
 cuda-cufft-dev-10-0.x86_64 cuda-cublas-dev-10-0.x86_64 \
 cuda-curand-dev-10-0.x86_64 cuda-cusolver-dev-10-0.x86_64 \
 cuda-cusparse-dev-10-0.x86_64 \
 && rm -rf /var/cache/yum

RUN wget http://mtdependency.navercorp.com/static/packages/nccl-repo-rhel7-2.3.7-ga-cuda10.0-1-1.x86_64.rpm \
 && rpm -i nccl-repo-rhel7-2.3.7-ga-cuda10.0-1-1.x86_64.rpm \
 && yum install -y \
 libnccl-2.3.7-2+cuda10.0 libnccl-devel-2.3.7-2+cuda10.0 libnccl-static-2.3.7-2+cuda10.0

ENV TF_CUDA_VERSION=10.0
ENV TF_CUDNN_VERSION=7.4
ENV PYTHON_LIB_PATH=/usr/include/python2.7

ENV OUTPUT_WHEELNAME_PYTHON_VERSION=cp27-cp27mu
