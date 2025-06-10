# filepath: tools/reqs.bat
@echo off
title Smart Thermostat Requirements Tool

REM Launch the Streamlit app
echo Starting Streamlit app...
start "" /B python -m streamlit run reqs-tool.py

REM Give the app time to start
timeout /t 3 >nul

echo.
echo ======================================
echo   Streamlit app should be running at:
echo   http://localhost:8501
echo ======================================
echo.

pause

REM Try to gracefully terminate the streamlit process
echo Closing Streamlit app...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8501') do (
    taskkill /PID %%a /F >nul 2>&1
)

echo Done.
