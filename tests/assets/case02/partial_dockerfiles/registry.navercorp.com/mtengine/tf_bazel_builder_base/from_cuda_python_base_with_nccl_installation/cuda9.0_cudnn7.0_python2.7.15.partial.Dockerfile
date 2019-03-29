FROM registry.navercorp.com/mtengine/cuda_python_base:cuda9.0_cudnn7.0_python2.7.15

RUN yum install -y \
 cuda-command-line-tools-9-0 \
 cuda-cufft-dev-9-0.x86_64 cuda-cublas-dev-9-0.x86_64 \
 cuda-curand-dev-9-0.x86_64 cuda-cusolver-dev-9-0.x86_64 \
 cuda-cusparse-dev-9-0.x86_64 \
 && rm -rf /var/cache/yum

RUN cd /usr/local \
 && wget http://mtdependency.navercorp.com/static/packages/nccl_2.2.13-1+cuda9.0_x86_64.txz \
 && tar xvf nccl_2.2.13-1+cuda9.0_x86_64.txz \
 && rm -f nccl_2.2.13-1+cuda9.0_x86_64.txz
RUN mkdir /usr/local/cuda-9.0/lib \
 && ln -s /usr/local/nccl_2.2.13-1+cuda9.0_x86_64/lib/libnccl.so.2 /usr/local/cuda/lib/libnccl.so.2 \
 && ln -s /usr/local/nccl_2.2.13-1+cuda9.0_x86_64/include/nccl.h /usr/local/cuda/include/nccl.h

ENV TF_CUDA_VERSION=9.0
ENV TF_CUDNN_VERSION=7.0
ENV PYTHON_LIB_PATH=/usr/include/python2.7

ENV OUTPUT_WHEELNAME_PYTHON_VERSION=cp27-cp27mu
