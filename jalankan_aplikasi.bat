@echo off
title AbsenGo Server
echo ===========================================
echo    Menjalankan AbsenGo - Port 8080
echo ===========================================
echo.

:: 1. Cek folder venv
if not exist venv (
    echo [+] Membuat folder virtual env (ini hanya sekali)...
    python -m venv venv
)

:: 2. Aktifkan venv dan jalankan
echo [+] Mengaktifkan lingkungan virtual...
call venv\Scripts\activate

echo [+] Memastikan library terinstal...
pip install django pillow

echo [+] Sinkronisasi database...
python manage.py migrate

echo.
echo ===========================================
echo SERVER AKAN DINYALAKAN...
echo Jika jendela ini ditutup, aplikasi akan mati.
echo Buka browser: http://127.0.0.1:8080
echo ===========================================
echo.

python manage.py runserver 8080

:: Jika server mati, jangan langsung tutup jendela agar user bisa baca error
echo.
echo [!] Server terhenti. Silakan baca pesan di atas untuk melihat errornya.
pause
