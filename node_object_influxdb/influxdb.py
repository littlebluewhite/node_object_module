import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxDB:
    def __init__(self, influx_config):
        self.host = influx_config["host"]
        self.port = influx_config["port"]
        self.org = influx_config["org"]
        self.token = influx_config["token"]
        self.bucket = influx_config["bucket"]
        self.url = f"http://{self.host}:{self.port}"
        self.client = influxdb_client.InfluxDBClient(
            url=self.url,
            token=self.token,
            org=self.org
        )
        self.write = self.client.write_api(write_options=SYNCHRONOUS)
        self.query = self.client.query_api()

    def write_in(self, _id: int, object_id: str, value: str):
        p = influxdb_client.Point(
            "object_value").tag("id", str(_id)) \
            .tag("object_id", object_id) \
            .field("value", value)
        self.write.write(bucket=self.bucket, org=self.org, record=p)

    def query_by_id(self, _id: int, start: int, end: int | None = None):
        if end is None:
            end = "now()"
        query = f'''from(bucket:"node_object")
|> range(start: {start}, stop: {end})
|> filter(fn:(r) => r._measurement == "object_value")
|> filter(fn:(r) => r.id == "{_id}")
|> filter(fn:(r) => r._field == "value")'''
        data = self.query.query(org=self.org, query=query)
        result = []
        for table in data:
            for record in table.records:
                result.append(
                    {
                        "id": _id,
                        "object_id": record.values.get("object_id"),
                        "value": record.get_value(),
                        "timestamp": record.get_time().timestamp(),
                    }
                )
        print(result)
        return result
