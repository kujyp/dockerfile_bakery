RUN wget https://www.python.org/ftp/python/3.6.7/Python-3.6.7.tgz -O python.tgz \
 && tar -xvf python.tgz \
 && mv Python-* python \
 && ( \
  cd python \
  && ./configure \
  && make \
  && make install \
 ) \
 && rm -rf python*

RUN curl https://bootstrap.pypa.io/get-pip.py | python

RUN python3 -m venv venv
ENV PATH=/venv/bin:$PATH
