from fastapi.routing import APIRouter

from . import item


router = APIRouter(prefix="/general")
router.include_router(item.router)