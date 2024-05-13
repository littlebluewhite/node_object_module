from schemas.object_group import ObjectGroupBasic
import datetime


class APIObjectGroupMain(ObjectGroupBasic):
    id: int
    updated_at: datetime.datetime
    objects: list[int]

class APIObjectGroupCreate(ObjectGroupBasic):
    objects: list[int] = list()

class APIObjectGroupUpdate(ObjectGroupBasic):
    objects: list[int] = list()
    
class APIObjectGroupMultipleUpdate(APIObjectGroupUpdate):
    id: int