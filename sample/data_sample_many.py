# import node_object_data.object
# import node_object_data.node
# import node_object_schemes.object_group
# from node_object_SQL import models
#
# name = "object_group"
# redis_tables = [
#     {"name": name, "key": "id"},
# ]
# sql_model = models.DeviceInfo
# main_schemas = node_object_schemes.object_group.ObjectGroup
# create_schemas = node_object_schemes.object_group.ObjectGroupCreate
# update_schemas = node_object_schemes.object_group.ObjectGroupUpdate
# multiple_update_schemas = node_object_schemes.object_group.ObjectGroupMultipleUpdate
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
#                 "module": node_object_data.object
#             }
#         ]
# }