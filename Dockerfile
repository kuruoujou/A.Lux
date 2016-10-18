FROM ubuntu:latest
MAINTAINER Spencer Julian <helloThere@spencerjulian.com>

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

COPY . /alux/

RUN apt-get -y update && \ 
    apt-get -y upgrade && \
    apt-get install -y nginx uwsgi uwsgi-plugin-python uwsgi-plugin-python3 \
                       python3-bottle python3-pip supervisor python3-requests && \
    locale-gen en_US.UTF-8 && \
    echo "daemon off;" >> /etc/nginx/nginx.conf && \
    cp /alux/uwsgi.ini /etc/uwsgi/apps-enabled/uwsgi.ini && \
    cp /alux/supervisord.conf /etc/supervisor/conf.d/supervisord.conf && \
    cp /alux/nginx.conf /etc/nginx/sites-enabled/default

EXPOSE 80

CMD ["/usr/bin/supervisord", "-n"]
