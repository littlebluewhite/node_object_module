parser_arguments = [
    ("-rh", "--redis_host", "Redis host", str),
    ("-rp", "--redis_port", "Redis port", str),
    ("-dh", "--db_host", "SQL DB host", str),
    ("-dp", "--db_port", "SQL DB port", str),
    ("-ih", "--influx_host", "InfluxDB host", str),
    ("-ip", "--influx_port", "InfluxDB port", str),
]

check_list = [
    {"arg": "redis_host", "cfg": ["Redis", "host"]},
    {"arg": "redis_port", "cfg": ["Redis", "port"]},
    {"arg": "db_host", "cfg": ["SQLDB", "host"]},
    {"arg": "db_port", "cfg": ["SQLDB", "port"]},
    {"arg": "influx_host", "cfg": ["InfluxDB", "host"]},
    {"arg": "influx_port", "cfg": ["InfluxDB", "port"]},
]