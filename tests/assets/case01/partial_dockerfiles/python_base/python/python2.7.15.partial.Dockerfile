RUN wget https://www.python.org/ftp/python/2.7.15/Python-2.7.15.tgz -O python.tgz \
 && tar -xvf python.tgz \
 && mv Python-* python \
 && ( \
  cd python \
  && ./configure --enable-unicode=ucs4 \
  && make \
  && make install \
 ) \
 && rm -rf python*

RUN wget https://pypi.python.org/packages/source/v/virtualenv/virtualenv-15.0.0.tar.gz \
 && tar -zxvf virtualenv*.tar.gz \
 && cd virtualenv-* \
 && python setup.py install \
 && cd .. \
 && rm -rf virtualenv-*

RUN curl https://bootstrap.pypa.io/get-pip.py | python
