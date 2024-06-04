from tortoise import fields
from tortoise.models import Model


class PoliceStation(Model):
    id = fields.BigIntField(pk=True, index=True)
    email = fields.CharField(max_length=256, unique=True, index=True)
    password = fields.CharField(max_length=300)
    state = fields.CharField(max_length=256)
    district = fields.CharField(max_length=256)
    name = fields.CharField(max_length=256)
    verified = fields.BooleanField(default=False)
    wallet = fields.CharField(max_length=256)
    updated_at = fields.DatetimeField(auto_now=True, alias="updatedAt")

    class Meta:
        table = "police_stations"
        table_description = "Police Station Details"
        ordering = ["state", "district", "name"]

    def __str__(self) -> str:
        return self.name
