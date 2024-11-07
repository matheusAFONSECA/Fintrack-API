from fastapi import APIRouter
from src.fintrack_api.routes.add_router import add_router
from src.fintrack_api.routes.user_router import user_router
from src.fintrack_api.routes.update_router import update_router
from src.fintrack_api.routes.delete_router import delete_router
from src.fintrack_api.routes.visualization_router import visualization_router

router = APIRouter()

# -------------------- INCLUDE ROUTERS -------------------- #

router.include_router(update_router)
router.include_router(delete_router)
router.include_router(user_router)
router.include_router(add_router)
router.include_router(visualization_router)
