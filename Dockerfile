FROM python:3.11.0-alpine

WORKDIR /app

ENV db_host 127.0.0.1
ENV redis_host 127.0.0.1
ENV influx_host 127.0.0.1

EXPOSE 9330

COPY . .

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

CMD python3.11 node_object_main.py --db_host=$db_host --redis_host=$redis_host --influx_host=$influx_host