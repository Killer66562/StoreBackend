from fastapi.routing import APIRouter

from . import district, city, user_report, item_report, users, ad


router = APIRouter(prefix="/admin", tags=["Admin"])

router.include_router(district.router)
router.include_router(city.router)
router.include_router(user_report.router)
router.include_router(item_report.router)
router.include_router(users.router)
router.include_router(ad.router)