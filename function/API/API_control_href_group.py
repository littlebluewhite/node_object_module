import data.control_href_group
import data.control_href_item
from function.General_operate import GeneralOperate


class APIControlHrefGroupOperate(GeneralOperate):
    def __init__(self, module, redis_db, exc):
        self.exc = exc
        GeneralOperate.__init__(self, module, redis_db, exc)
        self.chg_operate = GeneralOperate(data.control_href_group, redis_db, exc)
        self.chi_operate = GeneralOperate(data.control_href_item, redis_db, exc)