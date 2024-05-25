import asyncio

from datetime import datetime

from models import User

from dependencies import get_db, get_password_hash

async def create_admin_user():
    db = await get_db().__anext__()
    admin = User(id=10, username="admin", password=get_password_hash("admin123456"), email="admin@gmail.com", birthday=datetime.now(), is_admin=True, is_verified=True)
    member = User(id=11, username="member", password=get_password_hash("member123456"), email="member@gmail.com", birthday=datetime.now(), is_admin=False, is_verified=True)
    db.add(admin)
    db.add(member)
    db.commit()

asyncio.run(create_admin_user())