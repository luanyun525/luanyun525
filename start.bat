@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo   AI 学习伴侣 - 快速启动
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 检查 Python...
python --version
if errorlevel 1 (
    echo 未找到 Python！请安装 Python 3.8+
    pause
    exit /b 1
)
echo.

echo [2/3] 安装依赖...
pip install -r requirements.txt
echo.

echo [3/3] 启动服务...
echo.
echo ========================================
echo   服务已启动！
echo   访问地址: http://localhost:5000
echo   按 Ctrl+C 停止服务
echo ========================================
echo.

cd agent
python app.py

pause
