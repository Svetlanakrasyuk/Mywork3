from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import models, schemas, cashe


def get_menu(db: Session, menu_id: str):
    # Get data from redis
    redis_data = cashe.get_cash("menu" + menu_id)
    if redis_data:
        return redis_data
    else:
        # Get data from postgres
        my_db = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
        if my_db:
            res = jsonable_encoder(my_db)
            res["submenus_count"] = (len(my_db.submenus))
            dishes = 0
            for d in my_db.submenus:
                dishes += len(d.dishes)
            res["dishes_count"] = dishes
            # Set data to redis
            cashe.set_cash(res, "menu" + menu_id)
            return res
        cashe.set_cash(my_db, "menu" + menu_id)
        return my_db


def get_menu_by_title(db: Session, title: str):
    if db.query(models.Menu).filter(models.Menu.title == title).first():
        raise HTTPException(status_code=400, detail="Menu already exist")


def get_menus(db: Session):
    # Get data from redis
    redis_data = cashe.get_cash("menus")
    if redis_data:
        return redis_data
    else:
        my_db = db.query(models.Menu).all()
        if my_db:
            res = []
            for instance in my_db:
                menu_dict = jsonable_encoder(instance)
                menu_dict["submenus_count"] = (len(instance.submenus))
                dishes = 0
                for d in instance.submenus:
                    dishes += len(d.dishes)
                menu_dict["dishes_count"] = dishes
                res.append(menu_dict)
            cashe.set_cash(res, "menus")
            return res
        cashe.set_cash(my_db, "menus")
        return my_db


def create_menu(db: Session, menu: schemas.MenuCreate):
    db_menu = models.Menu(title=menu.title, description=menu.description)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    cashe.del_cashe("menus")
    cashe.change_menu_cashe()
    return db_menu


def update_menu(db: Session, menu: schemas.MenuBase, api_test_menu_id):
    db.query(models.Menu).filter(models.Menu.id == api_test_menu_id).update(
        {models.Menu.title: menu.title, models.Menu.description: menu.description},
    )
    db.commit()
    cashe.change_menu_cashe(api_test_menu_id)
    db_menu = get_menu(db=db, menu_id=api_test_menu_id)
    return db_menu


def delete_menu(db: Session, menu_id: str):
    my_db = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    db.delete(my_db)
    db.commit()
    result = {"status": True, "message": "The menu has been deleted"}
    cashe.change_menu_cashe(menu_id)
    return result


def get_submenu(db: Session, submenu_id: str):
    # Get data from redis
    redis_data = cashe.get_cash("submenu" + submenu_id)
    if redis_data:
        return redis_data
    else:
        my_db = db.query(models.Submenu).filter(
            models.Submenu.id == submenu_id,
        ).first()
        if my_db:
            res = jsonable_encoder(my_db)
            res["dishes_count"] = len(my_db.dishes)
            cashe.set_cash(res, "submenu" + submenu_id)
            return res
        cashe.set_cash(my_db, "submenu" + submenu_id)
        return my_db


def get_submenus(db: Session, skip: int = 0, limit: int = 100):
    redis_data = cashe.get_cash("submenus")
    if redis_data:
        return redis_data
    else:
        # Get data from postgres
        db = db.query(models.Submenu).offset(skip).limit(limit).all()
        print(db)
        res = []
        if db:
            for instance in db:
                submenu_dict = jsonable_encoder(instance)
                submenu_dict["dishes_count"] = len(instance.dishes)
                res.append(submenu_dict)
    cashe.set_cash(res, "submenus")
    return res


def create_submenu(db: Session, submenu: schemas.SubmenuCreate, main_menu_id: str):
    db_submenu = models.Submenu(**submenu.dict(), main_menu_id=main_menu_id)
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    cashe.change_submenu_cashe(main_menu_id)
    return db_submenu


def update_submenu(db: Session, submenu: schemas.SubmenuBase, api_test_submenu_id):
    db.query(models.Submenu).filter(models.Submenu.id == api_test_submenu_id).update(
        {
            models.Submenu.title: submenu.title,
            models.Submenu.description: submenu.description,
        },
    )
    db.commit()
    cashe.change_submenu_cashe("", api_test_submenu_id)
    db_submenu = get_submenu(db=db, submenu_id=api_test_submenu_id)
    return db_submenu


def delete_submenu(db: Session, submenu_id: str, menu_id: str):
    my_db = db.query(models.Submenu).filter(
        models.Submenu.id == submenu_id,
    ).first()
    db.delete(my_db)
    db.commit()
    result = {"status": True, "message": "The submenu has been deleted"}
    cashe.change_submenu_cashe(menu_id, submenu_id)
    return result


def get_dishes(db: Session, skip: int = 0, limit: int = 100):
    redis_data = cashe.get_cash("dishes")
    if redis_data:
        return redis_data
    else:
        # Get data from postgres
        res = db.query(models.Dish).offset(skip).limit(limit).all()
    cashe.set_cash(res, "dishes")
    return res


def create_dish(db: Session, dish: schemas.DishCreate, submenu_id: str, menu_id: str):
    db_dish = models.Dish(**dish.dict(), submenu_id=submenu_id)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    cashe.change_dish_cashe(menu_id, submenu_id)
    return db_dish


def get_dish(db: Session, dish_id: str):
    redis_data = cashe.get_cash("dish" + dish_id)
    if redis_data:
        return redis_data
    else:
        # Get data from postgres
        res = db.query(models.Dish).filter(models.Dish.id == dish_id).first()
        cashe.set_cash(res, "dish" + dish_id)
        res = jsonable_encoder(res)
        return res


def update_dish(db: Session, dish: schemas.DishBase, api_test_dish_id: str, api_test_submenu_id: str, api_test_menu_id: str):
    db.query(models.Dish).filter(models.Dish.id == api_test_dish_id).update(
        {
            models.Dish.title: dish.title, models.Dish.description: dish.description,
            models.Dish.price: dish.price,
        },
    )
    db.commit()
    cashe.change_dish_cashe(
        api_test_menu_id, api_test_submenu_id, api_test_dish_id,
    )
    db_dish = get_dish(db=db, dish_id=api_test_dish_id)
    return db_dish


def delete_dish(db: Session, dish_id: str, api_test_submenu_id: str, api_test_menu_id: str):
    my_db = db.query(models.Dish).filter(models.Dish.id == dish_id).first()
    db.delete(my_db)
    db.commit()
    result = {"status": True, "message": "The dish has been deleted"}
    cashe.change_dish_cashe(api_test_menu_id, api_test_submenu_id, dish_id)
    return result
