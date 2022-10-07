import datetime

from pydantic import BaseModel

from node_object_schemes.fake_data_config import FakeDataConfigBasic
from node_object_schemes.fake_data_config_base import FakeDataConfigBaseBasic, FakeDataConfigBaseUpdate
from node_object_schemes.object import ObjectBasic
from node_object_schemes.object_base import ObjectBaseBasic, ObjectBaseUpdate


class APIFdc(FakeDataConfigBasic):
    fake_data_config_base: FakeDataConfigBaseBasic


class APIObject(ObjectBasic):
    id: int

    create_at: datetime.datetime
    update_at: datetime.datetime

    object_base: ObjectBaseBasic
    fake_data_config: APIFdc | None = None
    object_groups: list = list()


class APIObjectCreate(ObjectBasic):
    object_base: ObjectBaseBasic
    fake_data_config: APIFdc | None = None


class APIFdcUpdate(APIFdc):
    fake_data_config_base: FakeDataConfigBaseUpdate | None = None


class APIObjectUpdate(ObjectBasic):
    name: str | None = None
    object_id: str | None = None
    object_base: ObjectBaseUpdate | None = None
    fake_data_config: APIFdcUpdate | None = None


class APIObjectMultipleUpdate(APIObjectUpdate):
    id: int


class InsertValue(BaseModel):
    id: int
    value: str
