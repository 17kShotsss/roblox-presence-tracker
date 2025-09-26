@echo off
echo Starting..
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Launching..
python jobid.py
pause
