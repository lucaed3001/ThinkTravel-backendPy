cd ..
py -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
deactivate
echo First start complete. You can now run the program using "start.bat".
REM This batch file is used to set up the virtual environment and install the required packages.
REM It should be run only once, when the program is first set up.
REM After that, you can use "start.bat" to run the program.
REM The "start.bat" file will activate the virtual environment and run the program.