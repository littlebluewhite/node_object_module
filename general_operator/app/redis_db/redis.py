import redis
from redis.cluster import ClusterNode
from redis.cluster import RedisCluster


class RedisDB:
    def __init__(self, redis_config, decode_responses=False):
        self.host = redis_config["host"]
        self.port = redis_config["port"]
        self.db = redis_config["db"]
        self.username = redis_config["user"]
        self.password = redis_config["password"]
        self.decode_responses = decode_responses
        self.is_cluster = self.__is_redis_cluster()

    def redis_client(self):
        if self.is_cluster:
            return self.__new_cluster()
        else:
            return self.__new_redis()

    def __new_cluster(self):
        nodes = [ClusterNode(self.host, self.port)]
        return RedisCluster(startup_nodes=nodes,
                            username=self.username,
                            password=self.password,
                            decode_responses=self.decode_responses)

    def __new_redis(self):
        return redis.Redis(host=self.host,
                           port=self.port,
                           db=self.db,
                           username=self.username,
                           password=self.password,
                           decode_responses=self.decode_responses)

    def __is_redis_cluster(self):
        try:
            # Create a Redis client
            r = redis.StrictRedis(host=self.host, port=self.port,
                                  username=self.username,
                                  password=self.password)
            cluster_info = r.execute_command('CLUSTER INFO')

            return cluster_info['cluster_state'] == 'ok'
        except redis.exceptions.ResponseError as e:
            # If a ResponseError is raised, it's not in cluster mode
            return False
        except Exception as e:
            # Handle other exceptions (e.g., connection errors)
            print(f"Error: {e}")
            return False

    if __name__ == "__main__":
        pass
