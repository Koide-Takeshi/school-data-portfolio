call %USERPROFILE%\anaconda3\Scripts\activate.bat
call activate jugyo2
cd /d %~dp0
python "%~dp0stu_menu.py"
pause