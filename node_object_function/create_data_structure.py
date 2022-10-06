def create_update_dict(create: bool = True, update: bool = True, sql: bool = True, temp: bool = False) -> dict:
    result = dict()
    if create:
        result["create_list"] = []
    if update:
        result["update_list"] = []
    if sql:
        result["sql_list"] = []
    if temp:
        result["temp_list"] = []
    return result


def create_delete_dict():
    return {
        "id_set": set(),
        "data_list": []
    }
