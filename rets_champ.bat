@echo off
REM Activate the virtual environment
call "\\wsl.localhost\Debian\home\yanirregev\Git\dmap-tools\RETS_Python\venv\Scripts\activate"

REM Run the Python script
python "\\wsl.localhost\Debian\home\yanirregev\Git\dmap-tools\RETS_Python\refindly_rets_v2.py"

REM Pause to keep the terminal open
pause