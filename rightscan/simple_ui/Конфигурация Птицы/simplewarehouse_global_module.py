from tokenize import Double
from pony import orm
from pony.orm import Database, Required, Set, Json, PrimaryKey, Optional
from pony.orm.core import db_session
import datetime

db = Database()
db.bind(
    provider="sqlite",
    filename="//data/data/ru.travelfood.simple_ui/databases/SimpleBirds",
    create_db=True,
)


class SW_Birds(db.Entity):
    name = Required(str)
    color_feathers = Optional(str)
    image_path = Optional(str)
