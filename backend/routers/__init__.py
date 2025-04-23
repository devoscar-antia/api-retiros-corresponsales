from .auth_router import router as auth_router
from .usuario_router import router as usuario_router
from .retiro_router import router as retiro_router
from .corresponsal_router import router as corresponsal_router

routers = [auth_router, usuario_router, retiro_router, corresponsal_router]

__all__ = ["auth_router", "usuario_router", "retiro_router", "corresponsal_router"] 