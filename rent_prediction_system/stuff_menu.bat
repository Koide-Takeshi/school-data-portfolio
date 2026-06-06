call %USERPROFILE%\anaconda3\Scripts\activate.bat
call activate jugyo2
cd /d %~dp0
python "%~dp0stuff_menu.py"
pause
