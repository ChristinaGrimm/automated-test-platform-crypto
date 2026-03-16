import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.routers import api_router
from app.database import engine, Base

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="密码学组件设计与分析系统API",
    description="提供密码学组件构造、分析和管理的后端API",
    version="1.0.0"
)

# 挂载静态目录
app.mount(
    "/result",  # 暴露给前端的路径前缀
    StaticFiles(directory="app/utils/analysis/result"),  # 本地真实目录
    name="result"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8000"],  # 前端地址
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "密码学组件设计与分析系统API"}

@app.on_event("startup")
async def startup_event():
    logger.info("应用程序启动")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("应用程序关闭")



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)