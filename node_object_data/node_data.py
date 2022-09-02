from node_object_SQL import models

redis_tables = [
    {"name": "node", "key": "id"},
]
sql_model = models.Node
main_schemas = reply_schemas.DispatchReply
multiple_update_schemas = reply_schemas.DispatchReplyMultipleUpdate

reload_related_redis_tables = [
    {"module": task_data, "field": "dispatch_task_id"}
]