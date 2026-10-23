@echo off
title PSX KSE-100 Institutional Terminal
echo ================================================================
echo  Starting Pakistan Stock Exchange (PSX) KSE-100 Terminal
echo ================================================================
start "" "http://localhost:5000"
python flash_api.py
pause
