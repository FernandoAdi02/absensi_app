@echo off
echo ========================================
echo    Mencoba Menjalankan Absensi
echo ========================================
echo.

:: Cek python dengan berbagai nama
set PY_CMD=python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    set PY_CMD=py
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        set PY_CMD=python3
    )
)

echo [+] Menggunakan: %PY_CMD%
echo.

echo 1. Sinkronisasi Database...
%PY_CMD% manage.py migrate
echo.

echo 2. Menyalakan Server di Port 8080...
echo Buka browser ke: http://127.0.0.1:8080
echo.
%PY_CMD% manage.py runserver 8080

echo.
echo [!] Jika Anda melihat pesan ini, berarti ada error di atas.
pause
