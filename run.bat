@echo off
echo Launching File-Copying...
echo.

REM Проверяем Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo Docker is not installed!
    echo Install Docker Desktop: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Testing X-Server
echo Testing...
if not "%DISPLAY%"=="" (
    echo DISPLAY installed: %DISPLAY%
) else (
    echo WARN: DISPLAY is not installed.
    echo For Windows: Install VcXsrv and launch XLaunch
    pause
)

REM Building
echo.
echo Building...
docker build -t file-copy-app .

REM Launching
echo.
echo Launching...
docker run -it --rm ^
    --name file-copy-app ^
    -e DISPLAY=host.docker.internal:0 ^
    -v %USERPROFILE%\Downloads:/home/user/Downloads ^
    file-copy-app

pause