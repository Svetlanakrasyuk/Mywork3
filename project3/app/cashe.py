import json

from .database import decoded_connection
from fastapi.encoders import jsonable_encoder


def get_cash(key_redis):
    redis_data = decoded_connection.get(key_redis)
    if redis_data:
        return json.loads(redis_data)
    return None


def set_cash(postgres_data, key_redis):
    # encode object to json, then json to str
    rescash = json.dumps(jsonable_encoder(postgres_data))
    # set to redis
    decoded_connection.set(key_redis, rescash, 30)


def del_cashe(key_redis):
    decoded_connection.delete(key_redis)


def change_dish_cashe(menu_id, submenu_id, dish_id=""):
    del_cashe("dishes")
    del_cashe("menus")
    del_cashe("submenus")
    del_cashe("menu" + menu_id)
    del_cashe("submenu" + submenu_id)
    del_cashe("dish" + dish_id)


def change_submenu_cashe(menu_id="", submenu_id=""):
    del_cashe("menus")
    del_cashe("submenus")
    del_cashe("menu" + menu_id)
    del_cashe("submenu" + submenu_id)


def change_menu_cashe(menu_id=""):
    del_cashe("menus")
    del_cashe("menu" + menu_id)
