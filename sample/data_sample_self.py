# import node_object_data.node
# import node_object_schemes.third_dimension_instance
# from node_object_SQL import models
#
# name = "third_dimension_instance"
# redis_tables = [
#     {"name": name, "key": "id"},
# ]
# sql_model = models.ThirdDimensionInstance
# main_schemas = node_object_schemes.third_dimension_instance.ThirdDimensionInstance
# create_schemas = node_object_schemes.third_dimension_instance.ThirdDimensionInstanceCreate
# update_schemas = node_object_schemes.third_dimension_instance.ThirdDimensionInstanceUpdate
# multiple_update_schemas = node_object_schemes.third_dimension_instance.ThirdDimensionInstanceMultipleUpdate
#
# reload_related_redis_tables = {
#     "outside_field":
#         [
#         ],
#     "self_field":
#         [
#             {"module": node_object_data.node, "field": "node_id"}
#         ]
# }
