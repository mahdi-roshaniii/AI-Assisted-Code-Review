@echo off
REM ============================================
REM AI Programming Tutor - Windows Launcher
REM ============================================

REM Check if venv exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found.
    echo Creating new virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Check if requirements.txt exists
if exist "requirements.txt" (
    echo Installing/updating dependencies...
    pip install -r requirements.txt --upgrade
)

echo Starting AI Programming Tutor...
echo ============================================
echo Open your browser and go to: http://localhost:8501
echo Press Ctrl+C to stop the server
echo ============================================

REM Run the Streamlit app
streamlit run app.py --server.port 8501 --server.headless true

pause