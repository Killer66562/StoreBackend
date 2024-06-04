import asyncio

from random import choice, choices

from datetime import datetime

from models import Ad, City, District, Store, User, Item

from dependencies import get_db, get_password_hash

def random_name_sm():
    return "".join(choices([chr(_) for _ in range(65, 91)], k=10))

def random_name():
    return "".join(choices([chr(_) for _ in range(65, 91)], k=20))

def random_email():
    return "".join(choices([chr(_) for _ in range(65, 91)], k=40)) + "gmail.com"

async def create_admin_user():
    db = await get_db().__anext__()
    admin_exist = db.query(User).filter(User.username == "admin").first()
    member_exist = db.query(User).filter(User.username == "member").first()
    if not admin_exist:
        admin = User(id=10, username="admin", password=get_password_hash("admin123456"), email="admin@gmail.com", birthday=datetime.now(), is_admin=True, is_verified=True)
        db.add(admin)
    if not member_exist:
        member = User(id=11, username="member", password=get_password_hash("member123456"), email="member@gmail.com", birthday=datetime.now(), is_admin=False, is_verified=True)
        db.add(member)

    cities = [City(name=random_name_sm()) for _ in range(5)]
    db.add_all(cities)
    db.flush()

    districts = [District(name=random_name_sm(), city_id=city.id) for city in cities]
    db.add_all(districts)
    db.flush()

    users = [User(username=random_name(), email=random_email(), birthday=datetime.now(), password=get_password_hash("test")) for _ in range(10)]
    db.add_all(users)
    db.flush()

    stores = [Store(id=user.id, user_id=user.id, name=random_name(), district_id=choice(districts).id, introduction="Fake store") for user in users]
    db.add_all(stores)
    db.flush()

    ads = [Ad(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", icon="midfing.gif") for _ in range(1000)]
    db.add_all(ads)
    db.flush()

    items = []
    for store in stores:
        faked = [Item(name=random_name(), introduction="Fake item", count=1000, price=1000, store_id=store.id, need_18=False) for _ in range(100)]
        items.extend(faked)
    db.add_all(items)
    db.flush()

    db.commit()

asyncio.run(create_admin_user())