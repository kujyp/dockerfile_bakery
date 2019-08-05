{{ FROM }}

RUN yum install -y \
 wget gcc make \
 && rm -rf /var/cache/yum

RUN yum install -y \
 zlib-devel openssl-devel libffi-devel \
 sqlite-devel readline-devel \
 && rm -rf /var/cache/yum

{{ python }}

CMD python
