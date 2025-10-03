from fastapi import Depends
from fastapi.routing import APIRouter

from app.routes.admin import district, city, user_report, item_report, users, ad

from app.dependencies.base import get_current_admin_user


router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(get_current_admin_user)])

router.include_router(district.router)
router.include_router(city.router)
router.include_router(user_report.router)
router.include_router(item_report.router)
router.include_router(users.router)
router.include_router(ad.router)