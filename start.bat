@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

cd /d "%~dp0"

title gobang-python 一键启动

echo ========================================
echo gobang-python 一键启动
echo ========================================
echo.

:: 检查是否已有虚拟环境
if exist ".venv\Scripts\python.exe" (
    set "PYCMD=.venv\Scripts\python.exe"
    echo [1/5] 已找到 Python 虚拟环境。
) else (
    :: 尝试多种方式找 Python
    set "PYCMD="

    :: 方式1：py 启动器
    where py >nul 2>nul
    if not errorlevel 1 (
        set "PYCMD=py"
        echo [找到] py 启动器。
    )

    :: 方式2：直接 python
    if not defined PYCMD (
        where python >nul 2>nul
        if not errorlevel 1 (
            set "PYCMD=python"
            echo [找到] python 命令。
        )
    )

    :: 方式3：conda
    if not defined PYCMD (
        where conda >nul 2>nul
        if not errorlevel 1 (
            echo [找到] conda，正在检测 Python 环境...
            conda run -n base python --version >nul 2>nul
            if not errorlevel 1 (
                set "PYCMD=conda run -n base python"
                echo [找到] conda base Python。
            ) else (
                echo [警告] conda 已安装但未找到可用 Python 环境。
                echo 请先创建 conda 环境：
                echo   conda create -n gobang python=3.12
                pause
                exit /b 1
            )
        )
    )

    if not defined PYCMD (
        echo [错误] 未找到 Python 3.12 或 3.13。
        echo 请先安装 Python：https://www.python.org/downloads/
        echo 或安装 Anaconda：https://www.anaconda.com/download
        echo.
        pause
        exit /b 1
    )

    echo [1/5] 正在创建 Python 虚拟环境...
    !PYCMD! -m venv .venv
    if errorlevel 1 (
        echo [错误] 创建虚拟环境失败。
        echo.
        pause
        exit /b 1
    )
    set "PYCMD=.venv\Scripts\python.exe"
)

echo [2/5] 正在安装或检查 Python 依赖...
".venv\Scripts\python.exe" -m pip install -r backend\requirements.lock.txt
if errorlevel 1 (
    echo [错误] 安装 Python 依赖失败。
    echo 请检查网络连接后重新双击本文件。
    echo.
    pause
    exit /b 1
)

where npm >nul 2>nul
if errorlevel 1 (
    echo [错误] 没有找到 npm。
    echo 请先安装 Node.js，然后重新双击本文件。
    echo.
    pause
    exit /b 1
)

where node >nul 2>nul
if errorlevel 1 (
    echo [错误] 没有找到 Node.js。
    echo 请先安装 Node.js 20.19 或 22.12 以上版本，然后重新双击本文件。
    echo.
    pause
    exit /b 1
)

node -e "const [major,minor]=process.versions.node.split('.').map(Number); if(!((major===20&&minor>=19)||major>20)){process.exit(1)}"
if errorlevel 1 (
    echo [错误] 当前 Node.js 版本不满足 Vite 要求。
    node --version
    echo 请安装 Node.js 20.19 或 22.12 以上版本。
    echo.
    pause
    exit /b 1
)

echo [3/6] 正在安装或检查前端依赖...
npm install
if errorlevel 1 (
    echo [错误] 安装前端依赖失败。
    echo 请检查网络连接后重新双击本文件。
    echo.
    pause
    exit /b 1
)

echo [4/6] 正在启动后端服务：http://127.0.0.1:8000
start "gobang backend" cmd /k "cd /d "%~dp0" && ".venv\Scripts\python.exe" -m backend.dev_server --host 127.0.0.1 --port 8000"

echo [5/6] 正在等待后端就绪...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ok=$false; for($i=0; $i -lt 30; $i++){ try { $r=Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/health' -TimeoutSec 1; if($r.status -eq 'ok'){ $ok=$true; break } } catch { Start-Sleep -Seconds 1 } }; if(-not $ok){ exit 1 }"
if errorlevel 1 (
    echo [错误] 后端服务没有正常启动。
    echo 请查看新打开的 gobang backend 窗口里的错误信息。
    echo.
    pause
    exit /b 1
)

echo [6/6] 正在启动前端页面：http://127.0.0.1:4173/?apiBase=http://127.0.0.1:8000
start "gobang frontend" cmd /k "cd /d "%~dp0" && npm run dev:frontend -- --host 127.0.0.1 --port 4173"
start "" "http://127.0.0.1:4173/?apiBase=http://127.0.0.1:8000"

echo.
echo 启动完成！
echo.
echo 浏览器地址：
echo http://127.0.0.1:4173/?apiBase=http://127.0.0.1:8000
echo.
echo 后端接口文档：
echo http://127.0.0.1:8000/docs
echo.
echo 如果要关闭项目，请关闭 gobang backend 和 gobang frontend 两个黑色窗口。
echo.
pause
