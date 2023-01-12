import data.control_href_group
import data.control_href_item
from function.General_operate import GeneralOperate


class APIChgFunction:

    @staticmethod
    def format_simple_api_chg(chg: dict) -> dict:
        return {
            "id": chg["id"],
            "uid": "",
            "name": chg["name"],
        }


class APIControlHrefGroupOperate(GeneralOperate, APIChgFunction):
    def __init__(self, module, redis_db, exc):
        self.exc = exc
        GeneralOperate.__init__(self, module, redis_db, exc)
        self.chg_operate = GeneralOperate(data.control_href_group, redis_db, exc)
        self.chi_operate = GeneralOperate(data.control_href_item, redis_db, exc)
