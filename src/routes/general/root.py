from fastapi.routing import APIRouter

from . import district, item, city, store


router = APIRouter(prefix="/general", tags=["General"])
router.include_router(item.router)
router.include_router(city.router)
router.include_router(district.router)
router.include_router(store.router)