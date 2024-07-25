import json
from enum import Enum

import redis
from fastapi.encoders import jsonable_encoder


class OperateFunction:
    @staticmethod
    def write_main_table(sql_data_list: list, schemas_model, set_mapping: dict):
        result = []
        for sql_data in sql_data_list:
            row = schemas_model(**jsonable_encoder(sql_data))
            value = row.json()
            set_mapping[getattr(row, "id")] = value
            result.append(row)
        return result

    @staticmethod
    def write_index_table(sql_data_list: list, schemas_model, set_mapping: dict, key: str,
                          table_name: str, r: redis.Redis):
        result = []
        if len(key.split("__")) > 1:
            result = OperateFunction.write_complex_key(
                sql_data_list, schemas_model, set_mapping, key, table_name, r)
        else:
            result = OperateFunction.write_single_key(
                sql_data_list, schemas_model, set_mapping, key, table_name, r)

        return result

    @staticmethod
    def write_complex_key(sql_data_list: list, schemas_model, set_mapping: dict, key: str,
                          table_name: str, r: redis.Redis):
        result = []
        # 處理complex key
        value_list = []
        key_list = key.split("__")
        for sql_data in sql_data_list:
            row = schemas_model(**jsonable_encoder(sql_data))
            complex_value = ""
            v_list = [getattr(row, key) for key in key_list]
            for v in v_list:
                if isinstance(v, Enum):
                    complex_value += v.value
                else:
                    complex_value += str(v)
            value_list.append(complex_value)
        r_data = r.hmget(table_name, value_list)
        set_mapping.update({x[0]: x[1] for x in zip(value_list, r_data) if x[1] is not None})
        for sql_data in sql_data_list:
            row = schemas_model(**jsonable_encoder(sql_data))
            complex_value = ""
            v_list = [getattr(row, key) for key in key_list]
            for v in v_list:
                if isinstance(v, Enum):
                    complex_value += v.value
                else:
                    complex_value += str(v)
            original_data = set_mapping.get(complex_value, None)
            if original_data:
                ids_list = json.loads(original_data)
                if row.id not in ids_list:
                    ids_list.append(row.id)
                set_mapping[complex_value] = json.dumps(ids_list)
            else:
                set_mapping[complex_value] = json.dumps([row.id])
            result.append(row)
        return result

    @staticmethod
    def write_single_key(sql_data_list: list, schemas_model, set_mapping: dict, key: str,
                         table_name: str, r: redis.Redis):
        result = []
        # 處理single key
        # 取得初始資料
        value_list = [getattr(schemas_model(**jsonable_encoder(sql_data)), key) for sql_data in sql_data_list]
        # key_list = [sql_data[key] for sql_data in sql_data_list]
        r_data = r.hmget(table_name, value_list)
        set_mapping.update({x[0]: x[1] for x in zip(value_list, r_data) if x[1] is not None})
        # sql type 是 json list的情況
        if isinstance(getattr(schemas_model(**jsonable_encoder(sql_data_list[0])), key), list):
            for sql_data in sql_data_list:
                row = schemas_model(**jsonable_encoder(sql_data))
                for item in getattr(row, key):
                    original_data = set_mapping.get(item, None)
                    if original_data:
                        ids_list = json.loads(original_data)
                        if row.id not in ids_list:
                            ids_list.append(row.id)
                        set_mapping[item] = json.dumps(ids_list)
                    else:
                        set_mapping[item] = json.dumps([row.id])
                result.append(row)

        # sql type 是單一值的情況
        else:
            for sql_data in sql_data_list:
                row = schemas_model(**jsonable_encoder(sql_data))
                original_data = set_mapping.get(getattr(row, key), None)
                if original_data:
                    ids_list = json.loads(original_data)
                    if row.id not in ids_list:
                        ids_list.append(row.id)
                    set_mapping[getattr(row, key)] = json.dumps(ids_list)
                else:
                    set_mapping[getattr(row, key)] = json.dumps([row.id])
                result.append(row)
        return result
