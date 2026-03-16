后端运行
1. 安装python3.10及以上版本
2. 进入后端目录(backend), 执行命令进入虚拟环境
   # Linux/MacOS
   wsl -d Ubuntu-22.04
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/MacOS

   # Windows
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   (Get-Command python).Path
3. 安装依赖
   pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple -r requirements.txt
4. 运行后端
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

前端运行
1. 安装nodejs工具, 安装pnpm工具
2. 进入前端目录(frontend), 执行命令
   pnpm i
3. 运行前端
   pnpm run dev