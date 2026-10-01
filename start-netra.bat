@echo off
setlocal

echo ===================================================
echo               NETRA STARTUP SYSTEM
echo ===================================================

:: ====================================================================
::                        CONFIGURATION
:: Evaluators: Please update the two paths below to match your machine!
:: ====================================================================

:: 1. Path to your local llama-server executable (WSL path)
set LLAMA_SERVER_BIN=/usr/bin/llama-server

:: 2. Path to your GGUF model file (WSL path)
set LLM_MODEL_PATH=/mnt/c/Models/Qwen_Qwen3-4B-Instruct-2507-Q4_K_M.gguf

:: ====================================================================

:: Dynamically get the directory where this script is located
set "PROJECT_ROOT=%~dp0"
:: Remove trailing backslash for cleaner paths
if "%PROJECT_ROOT:~-1%"=="\" set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

echo.
echo Project Root Detected: %PROJECT_ROOT%
echo.

:: 1. START LLAMA SERVER (WSL)
echo [1/4] Starting Llama Server on port 8081 (via WSL)...
start "Llama AI Server" wsl bash -ic "%LLAMA_SERVER_BIN% --port 8081 -m %LLM_MODEL_PATH% --jinja -ngl 99 -fa -c 8192; exec bash"

timeout /t 3 /nobreak >nul

:: 2. START PYTHON AI SERVICE (WSL)
echo [2/4] Starting Python AI Service in WSL...
:: Convert Windows path to WSL path format for the cd command
for /f "delims=" %%i in ('wsl wslpath -u "%PROJECT_ROOT%/ai-service"') do set "WSL_AI_PATH=%%i"
start "Python FastAPI" wsl --cd "%WSL_AI_PATH%" bash -ic "uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload; exec bash"

timeout /t 2 /nobreak >nul

:: 3. START SPRING BOOT
echo [3/4] Starting Spring Boot Gateway...
start "Spring Boot" powershell -NoExit -Command "Set-Location -Path '%PROJECT_ROOT%\backend'; .\mvnw.cmd spring-boot:run"

timeout /t 6 /nobreak >nul

:: 4. START REACT FRONTEND
echo [4/4] Starting React Frontend...
start "React UI" powershell -NoExit -Command "Set-Location -Path '%PROJECT_ROOT%\frontend'; npm run dev"

echo.
echo ===================================================
echo All services are launching in their correct environments!
echo ===================================================
pause
