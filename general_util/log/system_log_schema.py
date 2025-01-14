from pydantic import BaseModel


class Log(BaseModel):
    timestamp: float
    module: str
    submodule: str
    item: str
    method: str
    status_code: str
    message_code: str = ""
    message: str = ""
    request_body: str = ""
    response_size: str
    response_body: str = ""
    account: str = ""
    ip: str
    api_url: str
    query_params: str = ""
    web_path: str = ""
