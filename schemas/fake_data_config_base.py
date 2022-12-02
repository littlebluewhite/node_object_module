from pydantic import BaseModel


class FakeDataConfigBaseBasic(BaseModel):
    faking_frequency: float = 0
    faking_default_value: float = 0
    faking_max: float = 0
    faking_min: float = 0
    faking_extra_info: str | None = None


class FakeDataConfigBase(FakeDataConfigBaseBasic):
    id: int
    faking_frequency: float
    faking_default_value: float
    faking_max: float
    faking_min: float

    class Config:
        orm_mode = True


class FakeDataConfigBaseCreate(FakeDataConfigBaseBasic):
    pass


class FakeDataConfigBaseUpdate(FakeDataConfigBaseBasic):
    faking_frequency: float | None = None
    faking_default_value: float | None = None
    faking_max: float | None = None
    faking_min: float | None = None


class FakeDataConfigBaseMultipleUpdate(FakeDataConfigBaseUpdate):
    id: int
