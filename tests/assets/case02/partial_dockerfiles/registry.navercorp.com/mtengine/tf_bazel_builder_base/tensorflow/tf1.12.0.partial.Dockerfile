RUN pip --no-cache-dir install \
 keras_applications==1.0.6 \
 keras_preprocessing==1.0.5 \
 matplotlib==2.2.3 \
 mock==2.0.0

# install enum34 https://github.com/tensorflow/tensorflow/issues/23200
RUN pip --no-cache-dir install \
 enum34==1.1.6

ENV TENSORFLOW_VERSION=1.12.0
RUN git clone \
 --branch v${TENSORFLOW_VERSION} \
 --depth 1 \
 https://github.com/tensorflow/tensorflow.git
