@echo off
title Wordle Solver CLI v1.0.0
echo.
echo Wordle Solver CLI v1.0.0
echo =====================
echo.
echo Usage: run_cli.bat [guess] [feedback]
echo Example: run_cli.bat crane BYGBY
echo.
echo Feedback codes:
echo   B = Gray (letter not in word)
echo   Y = Yellow (letter in word, wrong position)  
echo   G = Green (letter correct and in right position)
echo.

if "%1"=="" (
    echo Please provide a guess and feedback.
    echo Example: run_cli.bat crane BYGBY
    pause
    exit /b 1
)

if "%2"=="" (
    echo Please provide feedback for your guess.
    echo Example: run_cli.bat crane BYGBY
    pause
    exit /b 1
)

echo Running: WordleSolverCLI.exe --guess %1 --feedback %2
echo.
WordleSolverCLI.exe --guess %1 --feedback %2
echo.
pause