@echo off
REM Python dosyasını çalıştırır

REM Ortamda python yüklü mü kontrol et
where python >nul 2>nul
IF ERRORLEVEL 1 (
    echo Python is not installed or not in PATH.
    pause
    exit /b
)

REM Python scriptini çalıştır
python script.py
