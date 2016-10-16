FROM python:3-onbuild
MAINTAINER Spencer Julian <helloThere@spencerjulian.com>
EXPOSE 8081
CMD [ "python", "./index.py" ]
