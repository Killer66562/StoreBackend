from fastapi.routing import APIRouter

from . import district


router = APIRouter(prefix="/admin")
router.include_router(district.router)