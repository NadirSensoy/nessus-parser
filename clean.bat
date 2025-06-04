<<<<<<< HEAD
@echo off
REM raw, output, raw-comparison, output-comparison klasörlerini siler, input.txt dosyasının içeriğini temizler

echo Klasörler siliniyor...

REM raw klasörünü sil
IF EXIST raw (
    rmdir /s /q raw
    echo raw klasörü silindi.
) ELSE (
    echo raw klasörü bulunamadı.
)

REM output klasörünü sil
IF EXIST output (
    rmdir /s /q output
    echo output klasörü silindi.
) ELSE (
    echo output klasörü bulunamadı.
)

REM raw-comparison klasörünü sil
IF EXIST raw-comparison (
    rmdir /s /q raw-comparison
    echo raw-comparison klasörü silindi.
) ELSE (
    echo raw-comparison klasörü bulunamadı.
)

REM output-comparison klasörünü sil
IF EXIST output-comparison (
    rmdir /s /q output-comparison
    echo output-comparison klasörü silindi.
) ELSE (
    echo output-comparison klasörü bulunamadı.
)

echo.

REM input.txt dosyasının içeriğini temizle (dosya kalır)
IF EXIST input.txt (
    type nul > input.txt
    echo input.txt dosyasının içeriği temizlendi.
) ELSE (
    echo input.txt dosyası bulunamadı.
)

=======
@echo off
REM raw, output, raw-comparison, output-comparison klasörlerini siler, input.txt dosyasının içeriğini temizler

echo Klasörler siliniyor...

REM raw klasörünü sil
IF EXIST raw (
    rmdir /s /q raw
    echo raw klasörü silindi.
) ELSE (
    echo raw klasörü bulunamadı.
)

REM output klasörünü sil
IF EXIST output (
    rmdir /s /q output
    echo output klasörü silindi.
) ELSE (
    echo output klasörü bulunamadı.
)

REM raw-comparison klasörünü sil
IF EXIST raw-comparison (
    rmdir /s /q raw-comparison
    echo raw-comparison klasörü silindi.
) ELSE (
    echo raw-comparison klasörü bulunamadı.
)

REM output-comparison klasörünü sil
IF EXIST output-comparison (
    rmdir /s /q output-comparison
    echo output-comparison klasörü silindi.
) ELSE (
    echo output-comparison klasörü bulunamadı.
)

echo.

REM input.txt dosyasının içeriğini temizle (dosya kalır)
IF EXIST input.txt (
    type nul > input.txt
    echo input.txt dosyasının içeriği temizlendi.
) ELSE (
    echo input.txt dosyası bulunamadı.
)

>>>>>>> f2cb617c794372eaa48498d769c99ed44e0a6321
