from fastapi.routing import APIRouter

from . import district, item, city, store, item_report


router = APIRouter(prefix="/general", tags=["General"])
router.include_router(item.router)
router.include_router(city.router)
router.include_router(district.router)
router.include_router(store.router)
router.include_router(item_report.router)