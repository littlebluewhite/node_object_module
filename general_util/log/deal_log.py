import time
import grpc
import requests
from fastapi import Request
from fastapi.responses import JSONResponse
from .data import url_module_mapping, status_code_rules
from .system_log_schema import Log
from .proto import system_log_pb2, system_log_pb2_grpc


class DealSystemLog:
    def __init__(self, request: Request, response: JSONResponse, url_mapping:dict=None, code_rules=None):
        self.request = request
        self.response = response
        self.url_mapping = url_module_mapping
        self.code_rules = status_code_rules
        if url_mapping is not None:
            self.url_mapping = url_mapping
        if code_rules is not None:
            self.code_rules = code_rules

    async def deal(self, system_log_g_server):
        log = self.__create_system_log()
        print("write log: ", self.__write_log_g(log, system_log_g_server))

    async def deal_r(self, system_log_r_server):
        log = self.__create_system_log()
        print("write log: ", self.__write_log_r(log, system_log_r_server))


    def __create_system_log(self):
        response_headers: dict = dict(self.response.headers)
        request_headers: dict  = dict(self.request.headers)
        module, submodule, item = self.__get_module_submodule_item()
        response_headers["check_header"] = "check_value"
        self.response.init_headers(response_headers)
        message, message_code = self.__get_message(response_headers)
        t = time.time()
        return Log(
            timestamp= t,
            module=module,
            submodule=submodule,
            item=item,
            method=self.request.method,
            status_code=f"{self.response.status_code}",
            message_code=message_code,
            message=message,
            response_size=response_headers.get("content-length", ""),
            account=request_headers.get("account", ""),
            ip=self.request.client.host,
            api_url=self.request.url.path,
            query_params=self.request.url.query,
            web_path=request_headers.get("web-path", "")
        )

    def __get_module_submodule_item(self):
        if self.url_mapping.get(self.request.url.path, None) is not None:
            return self.url_mapping.get(self.request.url.path)
        else:
            url_path = self.request.url.path.split("/")
            if len(url_path) < 5:
                return "error", "error", "error"
            else:
                return url_path[2], url_path[3], url_path[4]

    def __get_message(self, headers):
        status_code = str(self.response.status_code)
        message = ""
        message_code = ""
        if status_code in self.code_rules:
            message = str(self.code_rules[status_code]["message"])
            message_code = str(self.code_rules[status_code]["message_code"])
        # 以headers為主
        h_message = headers.get("message", None)
        if h_message is not None:
            message = h_message
        h_message_code = headers.get("message_code", None)
        if h_message_code is not None:
            message_code = h_message_code
        return message, message_code

    @staticmethod
    def __write_log_g(log, system_log_g_server):
        with grpc.insecure_channel(f"{system_log_g_server}") as channel:
            stub = system_log_pb2_grpc.SystemLogServiceStub(channel)
            request = system_log_pb2.LogRequest(
                timestamp=log.timestamp,
                module=log.module,
                submodule=log.submodule,
                item=log.item,
                method=log.method,
                status_code=log.status_code,
                message_code=log.message_code,
                message=log.message,
                response_size=log.response_size,
                account=log.account,
                ip=log.ip,
                api_url=log.api_url,
                query_params=log.query_params,
                web_path=log.web_path
            )
            return stub.WriteLog(request)

    @staticmethod
    def __write_log_r(log, system_log_r_server):
        body = {
            "timestamp": log.timestamp,
            "module": log.module,
            "submodule": log.submodule,
            "item": log.item,
            "method": log.method,
            "status_code": log.status_code,
            "message_code": log.message_code,
            "message": log.message,
            "response_size": log.response_size,
            "account": log.account,
            "ip": log.ip,
            "api_url": log.api_url,
            "query_params": log.query_params,
            "web_path": log.web_path
        }
        url = f'{system_log_r_server}/api/log/'
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=body, headers=headers)
        return response

