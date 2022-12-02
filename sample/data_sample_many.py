# import data.object
# import data.node
# import schemas.object_group
# from SQL import models
#
# name = "object_group"
# redis_tables = [
#     {"name": name, "key": "id"},
# ]
# sql_model = models.DeviceInfo
# main_schemas = schemas.object_group.ObjectGroup
# create_schemas = schemas.object_group.ObjectGroupCreate
# update_schemas = schemas.object_group.ObjectGroupUpdate
# multiple_update_schemas = schemas.object_group.ObjectGroupMultipleUpdate
#
# reload_related_redis_tables = {
#     "self_field":
#         [
#         ],
#     "outside_field":
#         [
#         ],
#     "many2many":
#         [
#             {
#                 "self_id_field": "object_group_id",
#                 "other_id_field": "object_id",
#                 "ref_table": "object_object_group",
#                 "module": data.object
#             }
#         ]
# }
