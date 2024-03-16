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

    verification: Mapped["Verification"] = relationship("Verification", primaryjoin="User.id == Verification.user_id", uselist=False, back_populates="user")
    store: Mapped["Store"] = relationship("Store", primaryjoin="User.id == Store.user_id", uselist=False, back_populates="owner")
    orders: Mapped[list["Order"]] = relationship("Order", primaryjoin="User.id == Order.user_id", uselist=True, back_populates="owner")
    cart_items: Mapped[list["CartItem"]] = relationship("CartItem", primaryjoin="User.id == CartItem.user_id", uselist=True, back_populates="owner")


class Verification(Base):
    __tablename__ = "verifications"
    code: Mapped[str] = mapped_column(String(length=5), unique=False, index=False, nullable=False)
    last_request: Mapped[datetime] = mapped_column(DateTime, unique=False, index=False, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), unique=True, index=True, nullable=False)

    user: Mapped["User"] = relationship("User", primaryjoin="User.id == Verification.user_id", uselist=False, back_populates="verification")


class City(Base):
    __tablename__ = "cities"
    name: Mapped[str] = mapped_column(String(length=10), unique=False, index=False, nullable=False)

    districts: Mapped[list["District"]] = relationship("District", primaryjoin="City.id == District.city_id", uselist=True, back_populates="city")


class District(Base):
    __tablename__ = "districts"
    name: Mapped[str] = mapped_column(String(length=10), unique=False, index=False, nullable=False)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id", ondelete="RESTRICT", onupdate="CASCADE"), unique=False, index=False, nullable=False)

    city: Mapped["City"] = relationship("City", primaryjoin="City.id == District.city_id", uselist=False, back_populates="districts")
    stores: Mapped[list["Store"]] = relationship("Store", primaryjoin="Store.district_id == District.id", uselist=True, back_populates="district")


class Store(Base):
    __tablename__ = "stores"
    name: Mapped[str] = mapped_column(String(length=20), unique=True, index=True, nullable=False)
    introduction: Mapped[str] = mapped_column(String(length=500), unique=False, index=False, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), unique=True, index=True, nullable=False)
    district_id: Mapped[int] = mapped_column(ForeignKey("districts.id", ondelete="RESTRICT", onupdate="CASCADE"), unique=False, index=False, nullable=False)

    owner: Mapped["User"] = relationship("User", primaryjoin="User.id == Store.user_id", uselist=False, back_populates="store")
    district: Mapped["District"] = relationship("District", primaryjoin="District.id == Store.district_id", uselist=False, back_populates="stores")
    items: Mapped[list["Item"]] = relationship("Item", primaryjoin="Store.id == Item.store_id", uselist=True, back_populates="store")


class Item(Base):
    __tablename__ = "items"
    name: Mapped[str] = mapped_column(String(length=50), unique=False, index=False, nullable=False)
    introduction: Mapped[str] = mapped_column(String(length=500), unique=False, index=False, nullable=False)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)

    store: Mapped["Store"] = relationship("Store", primaryjoin="Store.id == Item.store_id", uselist=False, back_populates="items")
    option_titles: Mapped[list["ItemOptionTitle"]] = relationship("ItemOptionTitle", primaryjoin="Item.id == ItemOptionTitle.item_id", uselist=True, back_populates="item")


class ItemOptionTitle(Base):
    __tablename__ = "item_option_titles"
    name: Mapped[str] = mapped_column(String(length=20), unique=False, index=False, nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    item: Mapped["Item"] = relationship("Item", primaryjoin="Item.id == ItemOptionTitle.item_id", uselist=False, back_populates="option_titles")
    options: Mapped[list["ItemOption"]] = relationship("ItemOption", primaryjoin="ItemOptionTitle.id == ItemOption.item_option_title_id", uselist=True)


class ItemOption(Base):
    __tablename__ = "item_options"
    name: Mapped[str] = mapped_column(String(length=20), unique=False, index=False, nullable=False)
    item_option_title_id: Mapped[int] = mapped_column(ForeignKey("item_option_titles.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)

    option_title: Mapped["ItemOptionTitle"] = relationship("ItemOptionTitle", primaryjoin="ItemOptionTitle.id == ItemOption.item_option_title_id", uselist=False, back_populates="options")


class ItemOptionClosure(Base):
    __tablename__ = "item_option_closures"
    path: Mapped[str] = mapped_column(String(length=1000), unique=True, index=False, nullable=False)
    remaining: Mapped[int] = mapped_column(Integer, unique=False, index=False, nullable=False, default=0)
    price: Mapped[int] = mapped_column(Integer, unique=False, index=False, nullable=False, default=0)


class Order(Base):
    __tablename__ = "orders"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    item_option_closure_id: Mapped[int] = mapped_column(ForeignKey("item_option_closures.id", ondelete="RESTRICT", onupdate="CASCADE"), unique=False, index=False, nullable=False)
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

    owner: Mapped["User"] = relationship("User", primaryjoin="User.id == Order.user_id", uselist=False, back_populates="orders")


class CartItem(Base):
    __tablename__ = "cart_items"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    item_option_id: Mapped[int] = mapped_column(ForeignKey("item_options.id", ondelete="RESTRICT", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    count: Mapped[int] = mapped_column(Integer, unique=False, index=False, nullable=False)

    owner: Mapped["User"] = relationship("User", primaryjoin="User.id == CartItem.user_id", uselist=False, back_populates="cart_items")


class Comment(Base):
    __tablename__ = "comments"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    content: Mapped[str] = mapped_column(String(length=200), unique=False, index=False, nullable=False)