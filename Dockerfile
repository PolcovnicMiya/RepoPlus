FROM python:3.12.3-slim

ENV PYTHONUNBUFFERED=1

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

COPY . .

EXPOSE 8000

CMD sleep 5 && python -m main


