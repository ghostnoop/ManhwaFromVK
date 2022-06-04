from tortoise.models import Model
from tortoise import fields, Tortoise


class VKGroup(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=200, unique=True)


class Post(Model):
    id = fields.IntField(pk=True)
    post_id = fields.IntField()
    group = fields.ForeignKeyField("VKGroup", on_delete=fields.CASCADE)
    text = fields.TextField()
    photo = fields.TextField()
    is_sent = fields.BooleanField(default=False)
    created_at = fields.DatetimeField()


async def db_init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['bot.models.main']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()
