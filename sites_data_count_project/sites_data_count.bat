@echo off
setlocal
pushd "%~dp0"

REM Edit this if Anaconda is installed elsewhere.
set "CONDA_ROOT=%USERPROFILE%\anaconda3"

REM Optional flags. Remove REM to enable.
REM set f_display_ui=True
REM set f_ng_word=True
REM set f_use_db=True
REM set f_csv2db=True
REM set f_add_dict=True

REM Add conda commands to PATH for this session.
set "PATH=%CONDA_ROOT%;%CONDA_ROOT%\Scripts;%CONDA_ROOT%\Library\bin;%PATH%"

REM Activate conda.
call "%CONDA_ROOT%\Scripts\activate.bat"

REM Edit the environment name if needed.
call conda activate base

REM Run the program from this project folder.
python ".\01_src\sites_data_count.py"

popd
pause
