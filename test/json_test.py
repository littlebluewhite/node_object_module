from fastapi.encoders import jsonable_encoder

from app.SQL import models

a = models.Node(**{"id": 1})
print(jsonable_encoder(a))
