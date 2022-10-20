import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "node_object"
org = "my-org"
token = "my-super-influxdb-auth-token"

url = "http://127.0.0.1:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

write_api = client.write_api(write_options=SYNCHRONOUS)

p = influxdb_client.Point("my_measurement").tag("location", "Prague").tag("station", "AAA").field("temperature", 25.3).field("ph", 7)
write_api.write(bucket=bucket, org=org, record=p)

query_api = client.query_api()
query = '''from(bucket:"node_object")
|> range(start: 2022-10-18T00:00:00Z8:00, stop: now())
|> filter(fn:(r) => r._measurement == "my_measurement")
|> filter(fn:(r) => r.location == "Prague")
|> filter(fn:(r) => r._field == "temperature")'''
result = query_api.query(org=org, query=query)
results = []
for table in result:
    for record in table.records:
        results.append({"timestamp": record.get_time(), "value": record.get_value()})


print(results)
