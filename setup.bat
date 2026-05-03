@echo off

if not exist .venv (
    python -m venv .venv
)

call .venv\Scripts\activate.bat

python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate

echo.
echo Setup complete.
echo.
echo To run the server:
echo   python manage.py runserver
echo.
echo Or on Windows:
echo   run.bat
echo.
echo To run tests:
echo   python manage.py test
echo.
echo Or on Windows:
echo   test.bat