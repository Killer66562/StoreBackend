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
    birthday: Mapped[datetime] = mapped_column(DateTime, unique=False, index=False, nullable=False)
    level: Mapped[int] = mapped_column(Integer, unique=False, index=False, nullable=False, default=1)
    is_admin: Mapped[bool] = mapped_column(Boolean, unique=False, index=False, nullable=False, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, unique=False, index=False, nullable=False, default=False)

    verification: Mapped["Verification"] = relationship("Verification", primaryjoin="User.id == Verification.user_id", uselist=False, back_populates="user")
    store: Mapped["Store"] = relationship("Store", primaryjoin="User.id == Store.user_id", uselist=False, back_populates="owner")
    orders: Mapped[list["Order"]] = relationship("Order", primaryjoin="User.id == Order.user_id", uselist=True, back_populates="owner")
    cart_items: Mapped[list["CartItem"]] = relationship("CartItem", primaryjoin="User.id == CartItem.user_id", uselist=True, back_populates="owner")
    buy_next_time_items: Mapped[list["BuyNextTimeItem"]] = relationship("BuyNextTimeItem", primaryjoin="User.id == BuyNextTimeItem.user_id", uselist=True, back_populates="owner")


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
    icon: Mapped[str] = mapped_column(String(length=100), unique=False, index=False, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), unique=True, index=True, nullable=False)
    district_id: Mapped[int] = mapped_column(ForeignKey("districts.id", ondelete="RESTRICT", onupdate="CASCADE"), unique=False, index=False, nullable=False)

    owner: Mapped["User"] = relationship("User", primaryjoin="User.id == Store.user_id", uselist=False, back_populates="store")
    district: Mapped["District"] = relationship("District", primaryjoin="District.id == Store.district_id", uselist=False, back_populates="stores")
    items: Mapped[list["Item"]] = relationship("Item", primaryjoin="Store.id == Item.store_id", uselist=True, back_populates="store")


class Item(Base):
    __tablename__ = "items"
    name: Mapped[str] = mapped_column(String(length=50), unique=False, index=False, nullable=False)
    introduction: Mapped[str] = mapped_column(String(length=500), unique=False, index=False, nullable=False)
    icon: Mapped[str] = mapped_column(String(length=100), unique=False, index=False, nullable=True)
    count: Mapped[int] = mapped_column(Integer, unique=False, index=False, nullable=False, default=0)
    price: Mapped[int] = mapped_column(Integer, unique=False, index=False, nullable=False)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    need_18: Mapped[bool] = mapped_column(Boolean, unique=False, index=False, nullable=False, default=False)

    store: Mapped["Store"] = relationship("Store", primaryjoin="Store.id == Item.store_id", uselist=False, back_populates="items")
    images: Mapped[list["ItemImage"]] = relationship("ItemImage", primaryjoin="ItemImage.item_id == Item.id", uselist=True, back_populates="item", order_by="ItemImage.id")
    comments: Mapped[list["Comment"]] = relationship("Comment", primaryjoin="Comment.item_id == Item.id", uselist=True)

class ItemImage(Base):
    __tablename__ = "item_images"
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=True, nullable=False)
    path: Mapped[str] = mapped_column(String(length=100), unique=False, index=False, nullable=True)

    item: Mapped["Item"] = relationship("Item", primaryjoin="ItemImage.item_id == Item.id", uselist=False, back_populates="images")


class Order(Base):
    __tablename__ = "orders"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id", ondelete="RESTRICT", onupdate="CASCADE"), unique=False, index=False, nullable=False)
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
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id", ondelete="RESTRICT", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    count: Mapped[int] = mapped_column(Integer, unique=False, index=False, nullable=False)

    owner: Mapped["User"] = relationship("User", primaryjoin="User.id == CartItem.user_id", uselist=False, back_populates="cart_items")
    item: Mapped["Item"] = relationship("Item", primaryjoin="Item.id == CartItem.item_id", uselist=False)


class BuyNextTimeItem(Base):
    __tablename__ = "buy_next_time_items"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)

    owner: Mapped["User"] = relationship("User", primaryjoin="User.id == BuyNextTimeItem.user_id", uselist=False, back_populates="buy_next_time_items")
    item: Mapped["Item"] = relationship("Item", primaryjoin="Item.id == BuyNextTimeItem.item_id", uselist=False)


class ItemReport(Base):
    __tablename__ = "item_reports"
    reporter_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    reported_item_id: Mapped[int] = mapped_column(ForeignKey("items.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    reason: Mapped[str] = mapped_column(String(length=500), unique=False, index=False, nullable=False)

    reporter: Mapped["User"] = relationship("User", primaryjoin="User.id == ItemReport.reporter_id", uselist=False)
    reported_item: Mapped["Item"] = relationship("Item", primaryjoin="Item.id == ItemReport.reported_item_id", uselist=False)
    images: Mapped[list["ItemReportImage"]] = relationship("ItemReportImage", primaryjoin="ItemReport.id == ItemReportImage.report_id", uselist=True)


class UserReport(Base):
    __tablename__ = "user_reports"
    reporter_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    reported_user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    reason: Mapped[str] = mapped_column(String(length=500), unique=False, index=False, nullable=False)

    reporter: Mapped["User"] = relationship("User", primaryjoin="User.id == UserReport.reporter_id", uselist=False)
    reported_user: Mapped["User"] = relationship("User", primaryjoin="User.id == UserReport.reported_user_id", uselist=False)
    images: Mapped[list["UserReportImage"]] = relationship("UserReportImage", primaryjoin="UserReport.id == UserReportImage.report_id", uselist=True)


class ItemReportImage(Base):
    __tablename__ = "item_report_images"
    report_id: Mapped[int] = mapped_column(ForeignKey("item_reports.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    path: Mapped[str] = mapped_column(String(length=100), unique=False, index=False, nullable=False)


class UserReportImage(Base):
    __tablename__ = "user_report_images"
    report_id: Mapped[int] = mapped_column(ForeignKey("user_reports.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    path: Mapped[str] = mapped_column(String(length=100), unique=False, index=False, nullable=False)


class Comment(Base):
    __tablename__ = "comments"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)
    content: Mapped[str] = mapped_column(String(length=200), unique=False, index=False, nullable=False)

    user: Mapped["User"] = relationship("User", primaryjoin="Comment.user_id == User.id", uselist=False)