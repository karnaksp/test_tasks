from pony.orm.core import db_session
from pony import orm
from pony.orm import Database, Required, Set, select, commit
import json
import os
import sqlite3  # This is another way to work with SQL
from sqlite3.dbapi2 import Error
from datetime import datetime
from PIL import Image
from tokenize import Double
from pony import orm
from pony.orm import Database, Required, Set, Json, PrimaryKey, Optional
from pony.orm.core import db_session
import datetime

db = Database()
db.bind(
    provider="sqlite",
    filename="//data/data/ru.travelfood.simple_ui/databases/Simple_Birds_2",
    create_db=True,
)


class SW_Units(db.Entity):
    name = Required(str)


class SW_Groups(db.Entity):
    name = Required(str)


class SW_Cells(db.Entity):
    name = Required(str)
    barcode = Optional(str)


class SW_Goods(db.Entity):
    name = Required(str)
    product_number = Optional(str)
    barcode = Optional(str)
    group = Optional(str)
    unique = Optional(int)
    unit = Required(str)
    price = Optional(float)
    pictures = Optional(Json)
    created_at = Optional(datetime.datetime, sql_default="CURRENT_TIMESTAMP")


class SW_Account(db.Entity):
    sku = Required(int)
    cell = Required(int)
    qty = Required(float)

    period = Optional(datetime.datetime, sql_default="CURRENT_TIMESTAMP")


class SW_Inventory(db.Entity):
    description = Required(str)
    created_at = Optional(datetime.datetime, sql_default="CURRENT_TIMESTAMP")
    lines = Set("SW_Inventory_line")


class SW_Inventory_line(db.Entity):
    sku = Required(int)
    cell = Required(int)
    qty = Required(float)
    inventory = Required("SW_Inventory")

    date = Optional(datetime.datetime, sql_default="CURRENT_TIMESTAMP")


def init():
    db.generate_mapping(create_tables=True)


unit_id = -1
nom_id = -1
cell_id = -1
cells = {}
cellid = None
found = []
green_size = 0
yellow_size = 0


def init_on_start(hashMap, _files=None, _data=None):
    init()
    return hashMap


def menu_input(hashMap, _files=None, _data=None):
    if hashMap.get("listener") == "menu":
        if hashMap.get("menu") == "Список птиц":
            hashMap.put("ShowScreen", "Список птиц")
        if hashMap.get("menu") == "Карточка птицы":
            hashMap.put("ShowScreen", "Карточка птицы")
        elif hashMap.get("menu") == "Создание новой птицы":
            hashMap.put("ShowScreen", "Создание новой птицы")
    elif hashMap.get("listener") == "ON_BACK_PRESSED":
        hashMap.put("FinishProcess", "")
    return hashMap


def menu_on_start(hashMap, _files=None, _data=None):
    # hashMap.put("getfiles","")
    # hashMap.put("toast","test1")
    return hashMap


# -----------------------------------------Товары
def birds_on_start(hashMap, _files=None, _data=None):
    hashMap.put("mm_local", "")
    hashMap.put("mm_compression", "70")
    hashMap.put("mm_size", "65")

    list = {
        "customcards": {
            "layout": {
                "type": "LinearLayout",
                "orientation": "vertical",
                "height": "match_parent",
                "width": "match_parent",
                "weight": "0",
                "Elements": [
                    {
                        "type": "LinearLayout",
                        "orientation": "horizontal",
                        "height": "wrap_content",
                        "width": "match_parent",
                        "weight": "0",
                        "Elements": [
                            {
                                "type": "Picture",
                                "show_by_condition": "",
                                "Value": "@pic",
                                "NoRefresh": False,
                                "document_type": "",
                                "mask": "",
                                "Variable": "",
                                "TextSize": "16",
                                "TextColor": "#DB7093",
                                "TextBold": True,
                                "TextItalic": False,
                                "BackgroundColor": "",
                                "width": "75",
                                "height": "75",
                                "weight": 0,
                            },
                            {
                                "type": "LinearLayout",
                                "orientation": "vertical",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "1",
                                "Elements": [
                                    {
                                        "type": "TextView",
                                        "show_by_condition": "",
                                        "Value": "@name",
                                        "NoRefresh": False,
                                        "document_type": "",
                                        "mask": "",
                                        "Variable": "",
                                    },
                                    {
                                        "type": "TextView",
                                        "show_by_condition": "",
                                        "Value": "@color_feathers",
                                        "NoRefresh": False,
                                        "document_type": "",
                                        "mask": "",
                                        "Variable": "",
                                    },
                                ],
                            },
                        ],
                    }
                ],
            }
        }
    }

    # _files = json.loads(hashMap.get("_files"))

    query = select(c for c in SW_Birds)
    list["customcards"]["cardsdata"] = []

    for record in query:

        pic = ""
        if "photo" in record.pictures:

            p = record.pictures["photo"]

            if len(p) > 0:

                for jf in _files:  # находим путь к файлу по идентификатору
                    if jf["id"] == p[0]:
                        if os.path.exists(jf["path"]):
                            pic = "~" + jf["path"]
                        break

        list["customcards"]["cardsdata"].append(
            {
                "name": record.name,
                "key": record.id,
                "color_feathers": str(record.color_feathers),
                "pictures": json.dumps(record.pictures),
                "pic": pic,
            }
        )

    hashMap.put("list", json.dumps(list))

    return hashMap


def open_nom(hashMap, nom_id, key):
    jlist = json.loads(hashMap.get("list"))
    birdsarray = jlist["customcards"]["cardsdata"]

    jrecord = next(item for item in birdsarray if str(item["key"]) == key)

    nom_id = jrecord["key"]
    hashMap.put("name", jrecord["name"])
    hashMap.put("color_feathers", jrecord["color_feathers"])

    if jrecord["unique"] == 1:
        hashMap.put("unique", "true")
    else:
        hashMap.put("unique", "false")

    jg = json.loads(jrecord["pictures"])
    if "photo" in jg:
        hashMap.put("photoGallery", json.dumps(jg["photo"]))
    else:
        hashMap.put("photoGallery", json.dumps([]))

    hashMap.put("ShowScreen", "ПтицыЗапись")

    return hashMap, nom_id


def birds_input(hashMap, _files=None, _data=None):
    global nom_id

    if hashMap.get("listener") == "btn_add":
        hashMap.put("name", "")
        hashMap.put("color_feathers", "")
        hashMap.put("photoGallery", json.dumps([]))
        nom_id = -1
        hashMap.put("ShowScreen", "ПтицыЗапись")

    elif hashMap.get("listener") == "CardsClick":
        hashMap, nom_id = open_nom(hashMap, nom_id, hashMap.get("selected_card_key"))
    elif hashMap.get("listener") == "color_feathers":
        nom = SW_Birds.get(color_feathers=hashMap.get("color_feathers_search"))
        if nom == None:
            hashMap.put("toast", "Птица не найдена")
        else:
            hashMap, nom_id = open_nom(hashMap, nom_id, str(nom.id))

            hashMap.put("speak", nom.name)

    elif hashMap.get("listener") == "vision":
        nom = SW_Birds.get(id=int(hashMap.get("nom_id")))
        if nom == None:
            hashMap.put("toast", "Птица не найдена")
        else:
            hashMap, nom_id = open_nom(hashMap, nom_id, str(nom.id))
            hashMap.put("speak", nom.name)
    elif hashMap.get("listener") == "ON_BACK_PRESSED":
        hashMap.put("ShowScreen", "Меню НСИ")

    return hashMap


def birds_record_on_start(hashMap, _files=None, _data=None):
    hashMap.put("mm_local", "")
    hashMap.put("mm_compression", "70")
    hashMap.put("mm_size", "65")

    hashMap.put(
        "fill_name",
        json.dumps({"hint": "Наименование", "default_text": hashMap.get("name")}),
    )
    hashMap.put(
        "fill_color_feathers",
        json.dumps(
            {"hint": "Цвет перьев", "default_text": hashMap.get("color_feathers")}
        ),
    )

    return hashMap


def get_if_exist(hashMap, field):
    if hashMap.containsKey(field):
        res = hashMap.get(field)
    else:
        res = ""
    return res


def getboolean_if_exist(hashMap, field):
    if not hashMap.containsKey(field):
        res = 0
    else:
        if hashMap.get(field) == "true":
            res = 1
        else:
            res = 0

    return res


def getfloat_if_exist(hashMap, field):
    if not hashMap.containsKey(field):
        res = 0
    else:
        try:
            res = float(hashMap.get(field))

        except:
            return 0
    return res


def save_nom(hashMap):
    global nom_id
    if not hashMap.containsKey("name"):
        hashMap.put("toast", "Не указано наименование")
        return hashMap, False
    else:
        if len(hashMap.get("name")) == 0:
            hashMap.put("toast", "Не указано наименование")
            return hashMap, False

    if nom_id < 0:

        with db_session:
            r = SW_Birds(
                name=get_if_exist(hashMap, "name"),
                color_feathers=get_if_exist(hashMap, "color_feathers"),
                unique=getboolean_if_exist(hashMap, "unique"),
            )
            nom_id = r.id
            commit()
    else:
        with db_session:

            r = SW_Birds[nom_id]
            r.name = get_if_exist(hashMap, "name")
            r.color_feathers = get_if_exist(hashMap, "color_feathers")
            r.unique = getboolean_if_exist(hashMap, "unique")

            j = {}

            j["photo"] = json.loads(hashMap.get("photoGallery"))
            r.pictures = j

            commit()
    return hashMap, True


def birds_record_input(hashMap, _files=None, _data=None):
    global nom_id
    if hashMap.get("listener") == "btn_save":
        # hashMap.put("toast",str(hashMap.get("unique")))

        hashMap, success = save_nom(hashMap)
        if success:
            hashMap.put("ShowScreen", "Птицы")

    elif hashMap.get("listener") == "color_feathers":
        hashMap.put("color_feathers", hashMap.get("color_feathers_nom"))

    elif hashMap.get("listener") == "CardsClick":
        hashMap.put("toast", str(hashMap.get("selected_card_key")))

    elif hashMap.get("listener") == "ON_BACK_PRESSED":
        hashMap.put("ShowScreen", "Птицы")

    elif hashMap.get("listener") == "menu_del":
        with db_session:
            r = SW_Birds[nom_id]
            r.delete()
        hashMap.put("ShowScreen", "Птицы")
        hashMap.put("toast", "Удалено...")

    elif hashMap.get("listener") == "photo":

        image_file = str(hashMap.get("photo_path"))
        image = Image.open(image_file)
        im = image.resize((500, 500))
        im.save(image_file)

        jphotoarr = json.loads(hashMap.get("photoGallery"))
        hashMap.put("photoGallery", json.dumps(jphotoarr))
    elif hashMap.get("listener") == "gallery_change":

        if hashMap.containsKey("photoGallery"):
            jphotoarr = json.loads(hashMap.get("photoGallery"))
            hashMap.put("photoGallery", json.dumps(jphotoarr))

    return hashMap
