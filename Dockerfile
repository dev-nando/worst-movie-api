FROM python:3.10
ENV PYTHONUNBUFFERED 1

RUN mkdir var/data
COPY ./data /var/data

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ./backend ./
EXPOSE 8000