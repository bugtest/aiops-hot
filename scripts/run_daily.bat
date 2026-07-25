@echo off
chcp 65001 >nul
echo ====================================
echo  智能运维前线 — 每日自动更新
echo ====================================
echo.

REM 设置工作目录（请将此行改为你实际存放 aiops-hot 的路径）
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM 设置 Python 环境（适配 QClaw 便携 Python）
set "PYTHON_HOME=C:\Program Files\QClaw\v0.2.34.621\resources\python"
set "PATH=%PYTHON_HOME%;%PYTHON_HOME%\Scripts;%PATH%"

echo [%date% %time%] 开始抓取数据...
python "%SCRIPT_DIR%fetch.py"

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] 数据抓取失败，退出码: %errorlevel%
    pause
    exit /b %errorlevel%
)

echo.
echo [%date% %time%] 开始构建 Hugo 站点...
cd /d "%SCRIPT_DIR%site"
call hugo --quiet

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Hugo 构建失败，退出码: %errorlevel%
    pause
    exit /b %errorlevel%
)

echo.
echo [%date% %time%] ✅ 全部完成！站点已更新到 public 目录
echo.
echo [INFO] 站点构建产物: %SCRIPT_DIR%site\public
echo [INFO] 本地预览: hugo server (在 site 目录下运行)
echo.
pause
