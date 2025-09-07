@echo off
REM File: /media/gaurav8077/New Volume/projects/activate_env.bat
echo Activating weather application environment...
call weather_env\Scripts\activate.bat
echo Environment activated! You can now run:
echo   python main.py
echo   python app.py
echo.
echo To deactivate, run: deactivate
