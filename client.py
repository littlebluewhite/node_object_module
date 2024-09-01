import grpc

from general_util.log.proto import system_log_pb2_grpc, system_log_pb2

if __name__ == "__main__":
    with grpc.insecure_channel(f"192.168.1.194:59360") as channel:
        stub = system_log_pb2_grpc.SystemLogServiceStub(channel)
        l = {'timestamp': 1724901985.7699342,
             'module': 'node_object',
             'submodule': 'object',
             'item': 'all',
             'method': 'GET',
             'status_code': '200',
             'message_code': '',
             'message': '',
             'response_size': '816609',
             'account': 'NADI_Thomas',
             'ip': '127.0.0.1',
             'api_url': '/api/object/all/',
             'query_params': 'skip=0&limit=1500',
             'web_path': '/en'}
        request = system_log_pb2.LogRequest(
            timestamp=l["timestamp"],
            module=l["module"],
            submodule=l["submodule"],
            item=l["item"],
            method=l["method"],
            status_code=l["status_code"],
            message_code=l["message_code"],
            message=l["message"],
            response_size=l["response_size"],
            account=l["account"],
            ip=l["ip"],
            api_url=l["api_url"],
            query_params=l["query_params"],
            web_path=l["web_path"],
        )
        print(stub.WriteLog(request))