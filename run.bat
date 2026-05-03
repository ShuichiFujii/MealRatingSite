@echo off

if "%1"=="setup" (
    echo Running setup...
    echo.

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
    echo Next commands:
    echo   run server  - Start the development server
    echo   run test    - Run tests

) else if "%1"=="test" (
    echo Running tests...
    echo.
    python manage.py test

) else if "%1"=="migrate" (
    echo Running migrations...
    echo.
    python manage.py makemigrations
    python manage.py migrate

) else if "%1"=="server" (
    echo Starting development server...
    echo.
    python manage.py runserver

) else (
    echo Usage:
    echo.
    echo   run setup   - Set up the project
    echo   run test    - Run tests
    echo   run migrate - Run migrations
    echo   run server  - Start the development server
)