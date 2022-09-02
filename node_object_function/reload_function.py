from dispatch_SQL import sql_operate
from dispatch_SQL.database import SessionLocal
from dispatch_redis import redis_operate


def initial_reload_data_from_sql(redis_tables: list, sql_model, schemas_model):
    db = SessionLocal()
    # sql 取資料
    sql_data = sql_operate.get_all_sql_data(db, sql_model)
    for table in redis_tables:
        # 清除redis表
        redis_operate.clean_redis_by_name(table["name"])
        # 將sql資料寫入redis表
        redis_operate.write_sql_data_to_redis(table["name"], sql_data, schemas_model, table["key"])
    db.close()


# reload 只需要更新主表
def reload_redis_from_sql(
        db, sql_model, main_schemas, redis_tables: list, data_id_set: set):
    sql_data_list: list = sql_operate.get_sql_data(db, data_id_set, sql_model)
    for table in redis_tables[:1]:
        redis_operate.write_sql_data_to_redis(
            table["name"], sql_data_list, main_schemas, table["key"])
    return sql_data_list


def reload_redis_table(db, reload_related_redis_tables, sql_data_list, origin_id_dict=None):
    if origin_id_dict is None:
        origin_id_dict = dict()
    if reload_related_redis_tables:
        for table in reload_related_redis_tables:
            id_set = {getattr(i, table["field"]) for i in sql_data_list}
            # 取得需要更新的id交集
            origin_id_set: set = origin_id_dict.get(table["field"], None)
            if origin_id_set:
                id_set = id_set.union(origin_id_set)
            # print("id_set: ", id_set)
            sql_data_list2 = reload_redis_from_sql(
                db, table["module"].sql_model, table["module"].main_schemas,
                table["module"].redis_tables, id_set
            )
            reload_redis_table(db, table["module"].reload_related_redis_tables, sql_data_list2)
