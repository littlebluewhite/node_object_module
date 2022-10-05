class APIObjectFunction:
    @staticmethod
    def format_api_object(obj: dict):
        object_groups = []
        for item in obj["object_groups"]:
            object_groups.append(item["id"])
        obj["object_groups"] = object_groups
        return obj
