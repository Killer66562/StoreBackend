import asyncio

from datetime import datetime

from app.models.models import User
from app.dependencies.base import get_db, get_password_hash

from app.settings.base import settings


async def create_admin():
    db = await get_db().__anext__()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin = User(username=settings.admin_username, password=get_password_hash(settings.admin_password), email=settings.admin_email, birthday=datetime.now(), is_admin=True, is_verified=True)
        db.add(admin)
        db.commit()


def main():
    asyncio.run(main=create_admin())

if __name__ == "__main__":
    main()