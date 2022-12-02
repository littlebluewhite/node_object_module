import redis


class NodeRedis:
    def __init__(self, redis_config):
        self.host = redis_config["host"]
        self.port = redis_config["port"]
        self.db = redis_config["db"]

    def new_redis(self):
        cn = redis.ConnectionPool(host=self.host,
                                  port=self.port,
                                  db=self.db)
        return redis.Redis(connection_pool=cn)


if __name__ == "__main__":
    pass
