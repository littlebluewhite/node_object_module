FROM python:3.10

WORKDIR /app

ENV db_host 127.0.0.1
ENV redis_host 127.0.0.1
ENV influx_host 127.0.0.1

COPY . .

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

CMD python3.10 node_object_main.py --db_host=$db_host --redis_host=$redis_host --influx_host=$influx_host