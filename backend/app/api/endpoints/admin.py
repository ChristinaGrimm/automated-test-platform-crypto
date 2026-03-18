from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm  # 保留导入，但不再手动实例化

from app.configs.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.dependencies import (
    Token,
    User,
    authenticate_user,
    create_access_token,
    fake_users_db,
    get_current_user,
)

router = APIRouter()


# 用户登录，获取token
# 修改点1：移除多余的 OAuth2PasswordRequestForm 实例化，直接使用 User 模型的参数
@router.post("/login", response_model=Token)
async def get_login_data(user: User):  # 保持你的 User 模型入参不变
    print(user)
    # 删除手动创建 OAuth2PasswordRequestForm 的代码 ↓（这行是报错核心）
    # form_data = OAuth2PasswordRequestForm(
    #     username=user.username, password=user.password
    # )
    
    # 修改点2：直接使用 user.username / user.password，无需 form_data 中转
    auth_user = authenticate_user(fake_users_db, user.username, user.password)
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": auth_user.username}, expires_delta=access_token_expires
    )

    # 修改点3：统一变量名（可选，只是为了避免混淆，不改也能运行）
    return JSONResponse(
        {
            "msg": "ok",
            "code": 0,
            "data": {"username": auth_user.username, "token": access_token},
        }
    )


# 获取用户信息（这部分代码完全没问题，无需修改）
@router.get("/info", response_model=User)
async def get_admin_info(current_user: User = Depends(get_current_user)):
    return JSONResponse(
        {
            "msg": "ok",
            "code": 0,
            "data": {
                "admin_info": {
                    "id": current_user.id,
                    "username": current_user.username,
                    "email": current_user.email,
                }
            },
        }
    )