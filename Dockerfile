FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /django-genba-basic
WORKDIR /django-genba-basic
ADD requirements.txt /django-genba-basic/
RUN pip install -r requirements.txt
ADD . /django-genba-basic/
