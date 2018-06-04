FROM python:3.6.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /docker_web
WORKDIR /docker_web
COPY ./ ./
RUN pip install -r requirements.txt
