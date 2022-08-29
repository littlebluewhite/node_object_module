import sys

py_v = sys.version_info
if py_v.major > 3 and py_v.minor > 9:
    from typing import Optional
    l = list
else:
    from typing import Optional, List
    l = List

from fastapi import Query, Depends

from app_node_object.node_object_function import search_function


async def common_search(_range: Optional[l[str]] = Query(None),
                        _value_in: Optional[l[str]] = Query(None),
                        _json_in: Optional[l[str]] = Query(None)):
    if not _range and not _value_in and not _json_in:
        return None
    else:
        result = "where "
        if _range:
            result += search_function.deal_range(_range)
        if _value_in:
            result += search_function.deal_value_in(_value_in)
        if _json_in:
            result += search_function.deal_json_in(_json_in)
        return result[:-5]


class CommonQuery:
    def __init__(self, skip: int = Query(0), limit: int = Query(None), where_command: str = Depends(common_search)):
        if where_command is not None:
            self.pattern = "search"
            self.where_command = where_command
        else:
            self.pattern = "all"
        self.skip = skip
        self.limit = limit
