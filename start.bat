@echo off
chcp 65001 >nul
setlocal

cd /d "%~dp0"

title gobang-python 一键启动

echo ========================================
echo gobang-python 一键启动
echo ========================================
echo.

where py >nul 2>nul
if errorlevel 1 (
  echo [错误] 没有找到 Python 启动器 py。
  echo 请先安装 Python 3.12 或 3.13，然后重新双击本文件。
  echo.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo [1/5] 正在创建 Python 虚拟环境...
  py -m venv .venv
  if errorlevel 1 (
    echo [错误] 创建虚拟环境失败。
    echo.
    pause
    exit /b 1
  )
) else (
  echo [1/5] 已找到 Python 虚拟环境。
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

echo [3/5] 正在启动后端服务：http://127.0.0.1:8000
start "gobang backend" cmd /k "cd /d "%~dp0" && ".venv\Scripts\python.exe" -m backend.dev_server --host 127.0.0.1 --port 8000"

echo [4/5] 正在等待后端就绪...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ok=$false; for($i=0; $i -lt 30; $i++){ try { $r=Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/health' -TimeoutSec 1; if($r.status -eq 'ok'){ $ok=$true; break } } catch { Start-Sleep -Seconds 1 } }; if(-not $ok){ exit 1 }"
if errorlevel 1 (
  echo [错误] 后端服务没有正常启动。
  echo 请查看新打开的 gobang backend 窗口里的错误信息。
  echo.
  pause
  exit /b 1
)

echo [5/5] 正在启动前端页面：http://127.0.0.1:8765/index.html?apiBase=http://127.0.0.1:8000
start "gobang frontend" cmd /k "cd /d "%~dp0" && ".venv\Scripts\python.exe" -m http.server 8765 --directory frontend"
start "" "http://127.0.0.1:8765/index.html?apiBase=http://127.0.0.1:8000"

echo.
echo 启动完成！
echo.
echo 浏览器地址：
echo http://127.0.0.1:8765/index.html?apiBase=http://127.0.0.1:8000
echo.
echo 后端接口文档：
echo http://127.0.0.1:8000/docs
echo.
echo 如果要关闭项目，请关闭 gobang backend 和 gobang frontend 两个黑色窗口。
echo.
pause
