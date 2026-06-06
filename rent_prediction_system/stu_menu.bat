call %USERPROFILE%\anaconda3\Scripts\activate.bat
call activate base
cd /d %~dp0
"%USERPROFILE%\anaconda3\python.exe" "%~dp0stu_menu.py"
pause