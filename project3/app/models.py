import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from .database import Base


def generate_uuid():
    return str(uuid.uuid4())


class Menu(Base):
    __tablename__ = "menus"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String, index=True)

    submenus = relationship(
        "Submenu", cascade="all, delete", back_populates="main_menu",
    )


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    main_menu_id = Column(String, ForeignKey("menus.id"))

    main_menu = relationship("Menu", back_populates="submenus")
    dishes = relationship(
        "Dish", cascade="all, delete, delete-orphan", back_populates="relate_sub",
    )


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(String)
    submenu_id = Column(String, ForeignKey("submenus.id"))

    relate_sub = relationship("Submenu", back_populates="dishes")
