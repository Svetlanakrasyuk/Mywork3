from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/api/v1/menus",
    response_model=schemas.Menu,
    status_code=status.HTTP_201_CREATED,
    summary="Create a menu",
    description="Create an menu with all the information, title, description",
)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    # Проверка уникальности меню
    crud.get_menu_by_title(db, title=menu.title)
    return crud.create_menu(db=db, menu=menu)


@app.get(
    "/api/v1/menus",
    response_model=list[schemas.Menu],
    summary="Get all menus",
    description="You can look all of the menus",
)
def read_menus(db: Session = Depends(get_db)):
    menus = crud.get_menus(db)
    return menus


@app.get(
    "/api/v1/menus/{api_test_menu_id}",
    response_model=schemas.Menu,
    summary="Get one menu",
    description="You can look at the menu",
)
def read_menu(api_test_menu_id: str, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db, menu_id=api_test_menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return db_menu


@app.patch(
    "/api/v1/menus/{api_test_menu_id}",
    response_model=schemas.Menu,
    summary="Get one menu for update",
    description="You can update the menu with all the information, title, description",
)
async def update_menu(api_test_menu_id: str, menu: schemas.MenuBase, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db, menu_id=api_test_menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return crud.update_menu(db=db, menu=menu, api_test_menu_id=api_test_menu_id)


@app.delete(
    "/api/v1/menus/{api_test_menu_id}",
    summary="Get one menu for delete",
    description="You can delete the menu with all submenus and dishes",
)
def delete_menu(api_test_menu_id: str, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db, menu_id=api_test_menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return crud.delete_menu(db=db, menu_id=api_test_menu_id)


@app.post(
    "/api/v1/menus/{api_test_menu_id}/submenus/", response_model=schemas.Submenu,
    status_code=status.HTTP_201_CREATED,
    summary="Create a submenu",
    description="Create an submenu with all the information, title, description",
)
def create_submenu(
    api_test_menu_id: str, submenu: schemas.SubmenuCreate, db: Session = Depends(get_db),
):
    return crud.create_submenu(db=db, submenu=submenu, main_menu_id=api_test_menu_id)


@app.get(
    "/api/v1/menus/{api_test_menu_id}/submenus/",
    response_model=list[schemas.Submenu],
    summary="Get all submenus",
    description="You can look all information about the submenus",
)
def read_submenus(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    submenus = crud.get_submenus(db, skip=skip, limit=limit)
    return submenus


@app.get(
    "/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}",
    response_model=schemas.Submenu,
    summary="Get one submenu",
    description="You can look information about the submenu",
)
def read_submenu(api_test_submenu_id: str, db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu(db, submenu_id=api_test_submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    return db_submenu


@app.patch(
    "/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}",
    response_model=schemas.Submenu,
    summary="Get one submenu for update",
    description="You can update the submenu with all the information, title, description",
)
async def update_submenu(api_test_submenu_id: str, submenu: schemas.SubmenuBase, db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu(db, submenu_id=api_test_submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    return crud.update_submenu(
        db=db,
        submenu=submenu,
        api_test_submenu_id=api_test_submenu_id,
    )


@app.delete(
    "/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}",
    summary="Delete one submenu",
    description="You can delete the menu with all dishes",
)
def delete_submenu(api_test_submenu_id: str, api_test_menu_id: str, db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu(db, submenu_id=api_test_submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    return crud.delete_submenu(db=db, submenu_id=api_test_submenu_id, menu_id=api_test_menu_id)


@app.post(
    "/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes",
    response_model=schemas.Dish, status_code=status.HTTP_201_CREATED,
    summary="Create a dish",
    description="Create a dish with all the information, title, description, price",
)
def create_dish(api_test_submenu_id: str, api_test_menu_id: str, dish: schemas.DishCreate, db: Session = Depends(get_db)):
    return crud.create_dish(db=db, dish=dish, submenu_id=api_test_submenu_id, menu_id=api_test_menu_id)


# @app.get("/items/", response_model=list[schemas.Item])
@app.get(
    "/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes",
    response_model=list[schemas.Dish],
    summary="Get all dishes",
    description="You can look all information about the dishes",
)
def read_dishes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    dishes = crud.get_dishes(db, skip=skip, limit=limit)
    return dishes


@app.get(
    "/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}",
    response_model=schemas.Dish,
    summary="Get one dish",
    description="You can look all information about the dish",
)
def read_dish(api_test_dish_id: str, db: Session = Depends(get_db)):
    db_dish = crud.get_dish(db, dish_id=api_test_dish_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return db_dish


@app.patch(
    "/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}",
    response_model=schemas.DishBase,
    summary="Get one dish for update",
    description="You can update the dish with all the information, title, description, price",
)
async def update_dish(api_test_dish_id: str, api_test_submenu_id: str, api_test_menu_id: str, dish: schemas.DishBase, db: Session = Depends(get_db)):
    db_dish = crud.get_dish(db, dish_id=api_test_dish_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return crud.update_dish(db=db, dish=dish, api_test_dish_id=api_test_dish_id, api_test_submenu_id=api_test_submenu_id, api_test_menu_id=api_test_menu_id)


@app.delete(
    "/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}",
    summary="Delete one dish",
    description="You can delete the dish",
)
def delete_dish(api_test_dish_id: str, api_test_submenu_id: str, api_test_menu_id: str, db: Session = Depends(get_db)):
    db_dish = crud.get_dish(db, dish_id=api_test_dish_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return crud.delete_dish(db=db, dish_id=api_test_dish_id, api_test_submenu_id=api_test_submenu_id, api_test_menu_id=api_test_menu_id)
