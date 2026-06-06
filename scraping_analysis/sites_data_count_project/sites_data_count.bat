@echo off

REM ===== Local settings =====
setlocal

REM ===== Anaconda install path =====
set "CONDA_ROOT=%USERPROFILE%\anaconda3"

REM ===== Optional flags: remove REM to enable =====
REM set f_display_ui=True
REM set f_ng_word=True
REM set f_use_db=True
REM set f_csv2db=True
REM set f_add_dic=True

REM ===== Temporary PATH setup =====
set "PATH=%CONDA_ROOT%;%CONDA_ROOT%\Scripts;%CONDA_ROOT%\Library\bin;%PATH%"

REM ===== Initialize conda =====
call "%CONDA_ROOT%\Scripts\activate.bat"

REM ===== Activate environment =====
call conda activate jugyo2

REM ===== Run Python script =====
cd /d "%~dp0"
python ".\01_src\sites_data_count.py"

REM ===== Keep window open after completion =====
pause
