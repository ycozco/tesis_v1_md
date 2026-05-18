@echo off
REM Script para instalar Pandoc y convertir tesis_v2.md a DOCX

echo === Verificando Pandoc ===
pandoc --version >nul 2>&1
if errorlevel 1 (
    echo Pandoc no encontrado. Descargando e instalando...
    REM Descargar Pandoc (Windows installer)
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/jgm/pandoc/releases/download/3.1.9/pandoc-3.1.9-windows-x86_64.msi' -OutFile 'pandoc-installer.msi'" 2>nul
    if exist pandoc-installer.msi (
        echo Ejecutando instalador...
        msiexec /i pandoc-installer.msi /quiet
        del pandoc-installer.msi
        echo Pandoc instalado. Por favor, reinicia el terminal y ejecuta nuevamente.
        pause
        exit /b
    ) else (
        echo Error descargando Pandoc. Descárgalo manualmente desde:
        echo https://github.com/jgm/pandoc/releases/
        pause
        exit /b 1
    )
)

echo === Pandoc encontrado ===
echo.
echo === Convirtiendo tesis_v2.md a DOCX ===
cd /d D:\tesis_yoset

if not exist "refs.bib" (
    echo Error: refs.bib no encontrado en D:\tesis_yoset
    pause
    exit /b 1
)

if not exist "tesis_v2.md" (
    echo Error: tesis_v2.md no encontrado en D:\tesis_yoset
    pause
    exit /b 1
)

REM Comando de conversión con template y citeproc
pandoc tesis_v2.md -o tesis_integrada.docx ^
    --reference-doc="formato/Plantilla - Tesis de Investigación 2026.docx" ^
    --citeproc ^
    --bibliography=refs.bib ^
    --csl=apa.csl ^
    --toc ^
    --toc-depth=3

if errorlevel 1 (
    echo Error en la conversión. Verifica que refs.bib y apa.csl existan.
    pause
    exit /b 1
)

echo.
echo === Conversión completada ===
echo Archivo generado: D:\tesis_yoset\tesis_integrada.docx
echo.
pause
