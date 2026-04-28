@echo off
echo ===========================================
echo    Membuat Akun Admin Otomatis
echo ===========================================
echo.

:: Mencoba menjalankan skrip python
python buat_admin.py
if %errorlevel% neq 0 (
    py buat_admin.py
    if %errorlevel% neq 0 (
        python3 buat_admin.py
    )
)

echo.
echo Jika tidak ada error di atas, akun admin (admin/admin123) sudah siap.
pause
