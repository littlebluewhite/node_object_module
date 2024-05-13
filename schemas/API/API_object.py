import datetime

from pydantic import BaseModel

from schemas.fake_data_config import FakeDataConfigBasic
from schemas.fake_data_config_base import FakeDataConfigBaseBasic, FakeDataConfigBaseUpdate
from schemas.object import ObjectBasic
from schemas.object_base import ObjectBaseBasic, ObjectBaseUpdate


class APIFdc(FakeDataConfigBasic):
    fake_data_config_base: FakeDataConfigBaseBasic


class APIObject(ObjectBasic):
    id: int

    created_at: datetime.datetime
    updated_at: datetime.datetime

    object_base: ObjectBaseBasic
    fake_data_config: APIFdc | None = None
    object_groups: list = list()


class APIObjectSimple(BaseModel):
    id: int
    uid: str | None
    name: str | None


class APIObjectCreate(ObjectBasic):
    object_base: ObjectBaseBasic
    fake_data_config: APIFdc | None = None
    object_groups: list = list()


class APIFdcUpdate(APIFdc):
    fake_data_config_base: FakeDataConfigBaseUpdate | None = None


class APIObjectUpdate(ObjectBasic):
    name: str | None = None
    uid: str | None = None
    source_id: str | None = None
    node_id: int | str | None = None
    object_base: ObjectBaseUpdate | None = None
    fake_data_config: APIFdcUpdate | None = None
    control_href_group_id: int | str | None = None
    object_groups: list = list()


class APIObjectMultipleUpdate(APIObjectUpdate):
    id: int


class InsertValue(BaseModel):
    id: int
    value: str
    timestamp: float = None

class GetValue(BaseModel):
    id: int
    uid: str
    value: str
    timestamp: float

class InsertValueModify(BaseModel):
    uid: str
    value: str
    timestamp: float = None