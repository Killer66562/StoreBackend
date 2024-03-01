from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import ForeignKey, String, Integer, Boolean, DateTime

from datetime import datetime

from typing import Literal

from enums import OrderStatus


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, index=True, nullable=False, autoincrement=True)
    created_at: Mapped[int] = mapped_column(DateTime, nullable=False, default=datetime.now())


class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(length=20), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(length=100), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(length=100), unique=False, index=False, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, unique=False, index=False, nullable=False, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, unique=False, index=False, nullable=False, default=False)

    verification: Mapped["Verification"] = relationship("Verification", primaryjoin="User.id == Verification.user_id", uselist=False)


class Verification(Base):
    __tablename__ = "verifications"
    code: Mapped[str] = mapped_column(String(length=5), unique=False, index=False, nullable=False)
    last_request: Mapped[datetime] = mapped_column(DateTime, unique=False, index=False, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), unique=True, index=True, nullable=False)


class City(Base):
    __tablename__ = "cities"
    name: Mapped[str] = mapped_column(String(length=10), unique=False, index=False, nullable=False)

    districts: Mapped[list["District"]] = relationship("District", primaryjoin="City.id == District.city_id", uselist=True, back_populates="city")


class District(Base):
    __tablename__ = "districts"
    name: Mapped[str] = mapped_column(String(length=10), unique=False, index=False, nullable=False)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id", ondelete="RESTRICT", onupdate="CASCADE"), unique=False, index=False, nullable=False)

    city: Mapped["City"] = relationship("City", primaryjoin="City.id == District.city_id", uselist=False, back_populates="districts")


class Store(Base):
    __tablename__ = "stores"
    name: Mapped[str] = mapped_column(String(length=20), unique=True, index=True, nullable=False)
    introduction: Mapped[str] = mapped_column(String(length=500), unique=False, index=False, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), unique=True, index=True, nullable=False)
    district_id: Mapped[int] = mapped_column(ForeignKey("districts.id", ondelete="RESTRICT", onupdate="CASCADE"), unique=False, index=False, nullable=False)

    owner: Mapped["User"] = relationship("User", primaryjoin="User.id == Store.user_id", uselist=False)
    district: Mapped["District"] = relationship("District", primaryjoin="District.id == Store.district_id", uselist=False)
    items: Mapped[list["Item"]] = relationship("Item", primaryjoin="Store.id == Item.store_id", uselist=False)


class Item(Base):
    __tablename__ = "items"
    name: Mapped[str] = mapped_column(String(length=50), unique=False, index=False, nullable=False)
    introduction: Mapped[str] = mapped_column(String(length=500), unique=False, index=False, nullable=False)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)

    store: Mapped["Store"] = relationship("Store", primaryjoin="Store.id == Item.store_id", uselist=False)
    option_titles: Mapped[list["ItemOptionTitle"]] = relationship("ItemOptionTitle", primaryjoin="Item.id == ItemOptionTitle.item_id", uselist=True)


class ItemOptionTitle(Base):
    __tablename__ = "item_option_titles"
    name: Mapped[str] = mapped_column(String(length=20), unique=False, index=False, nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)

    options: Mapped[list["ItemOption"]] = relationship("ItemOption", primaryjoin="ItemOptionTitle.id == ItemOption.item_option_title_id", uselist=True)


class ItemOption(Base):
    __tablename__ = "item_options"
    name: Mapped[str] = mapped_column(String(length=20), unique=False, index=False, nullable=False)
    item_option_title_id: Mapped[int] = mapped_column(ForeignKey("item_option_titles.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    remaining: Mapped[int] = mapped_column(Integer, unique=False, index=False, nullable=False, default=0)
    price: Mapped[int] = mapped_column(Integer, unique=False, index=False, nullable=False)


class Order(Base):
    __tablename__ = "orders"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    item_option_id: Mapped[int] = mapped_column(ForeignKey("item_options.id", ondelete="RESTRICT", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    count: Mapped[int] = mapped_column(Integer, unique=False, index=False, nullable=False)
    status: Mapped[
        Literal[
            OrderStatus.NOT_DELIVERED, 
            OrderStatus.DELIVERED, 
            OrderStatus.PROCESSING, 
            OrderStatus.ARRIVED, 
            OrderStatus.DONE
        ]
    ] = mapped_column(Integer, unique=False, index=False, nullable=False, default=OrderStatus.NOT_DELIVERED.value)


class CartItem(Base):
    __tablename__ = "cart_items"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    item_option_id: Mapped[int] = mapped_column(ForeignKey("item_options.id", ondelete="RESTRICT", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    count: Mapped[int] = mapped_column(Integer, unique=False, index=False, nullable=False)


class Comment(Base):
    __tablename__ = "comments"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    content: Mapped[str] = mapped_column(String(length=200), unique=False, index=False, nullable=False)