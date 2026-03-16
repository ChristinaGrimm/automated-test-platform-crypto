# routers.py
from fastapi import APIRouter
from app.api.endpoints import construction, operate_sql, check, analyze, download, algorithm, admin, file, impl_analyze

# 创建主API路由器
api_router = APIRouter()

# 包含各个子路由 - 添加前缀
api_router.include_router(construction.router, prefix="/construction", tags=["construction"])
api_router.include_router(operate_sql.router, prefix="/operate_sql", tags=["operate_sql"])
api_router.include_router(check.router, prefix="/check", tags=["check"])
api_router.include_router(analyze.router, prefix="/analyze", tags=["analyze"])
api_router.include_router(download.router, prefix="/download", tags=["download"])
api_router.include_router(algorithm.router, prefix="/algorithm", tags=["algorithm"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(file.router, prefix="/file", tags=["file"]) 
api_router.include_router(impl_analyze.router, prefix="/impl_analyze", tags=["impl_analyze"]) 