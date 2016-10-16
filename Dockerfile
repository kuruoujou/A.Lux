FROM ubuntu:latest
MAINTAINER Spencer Julian <helloThere@spencerjulian.com>

RUN apt-get update && apt-get upgrade && apt-get install -y nginx uwsgi uwsgi-plugin-python uwsgi-plugin-python3 python3-bottle python3-pip supervisor python3-requests 
 && locale-gen en_US.UTF-8 
 && echo "daemon off;" >> /etc/nginx/nginx.conf

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

COPY uwsgi.ini /etc/uwsgi/apps-enabled/uwsgi.ini
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY nginx.conf /etc/nginx/sites-enabled/default

EXPOSE 80

CMD ["/usr/bin/supervisord", "-n"]
