@echo off
chcp 65001 >nul
echo.
echo ╔══════════════════════════════════════╗
echo ║       GitHub Repo Erstellen          ║
echo ╚══════════════════════════════════════╝
echo.

:: ── Eingaben ──────────────────────────────
set /p USERNAME=GitHub Benutzername: 
set /p TOKEN=GitHub Token (ghp_...): 
set /p REPONAME=Repo Name (kein Leerzeichen): 
set /p BESCHREIBUNG=Beschreibung (optional, Enter=leer): 

echo.
set /p PRIVAT=Soll das Repo privat sein? (j/n): 
if /i "%PRIVAT%"=="j" (set PRIVATE=true) else (set PRIVATE=false)

:: ── Repo auf GitHub erstellen (via API) ───
echo.
echo Erstelle Repo auf GitHub...

curl -s -X POST ^
  -H "Authorization: token %TOKEN%" ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"%REPONAME%\",\"description\":\"%BESCHREIBUNG%\",\"private\":%PRIVATE%}" ^
  https://api.github.com/user/repos -o _gh_response.json

:: Pruefen ob erfolgreich
findstr /c:"\"full_name\"" _gh_response.json >nul 2>&1
if errorlevel 1 (
    echo.
    echo FEHLER: Repo konnte nicht erstellt werden!
    echo Antwort von GitHub:
    type _gh_response.json
    del _gh_response.json
    echo.
    pause
    exit /b
)
del _gh_response.json

echo [OK] Repo "%REPONAME%" auf GitHub erstellt!

:: ── Lokales Git Setup ──────────────────────
echo.
echo Initialisiere lokales Git Repo...

if not exist ".git" (
    git init
    echo [OK] git init
) else (
    echo [OK] .git existiert bereits, uebersprungen
)

:: README erstellen falls nicht vorhanden
if not exist "README.md" (
    echo # %REPONAME% > README.md
    echo. >> README.md
    echo %BESCHREIBUNG% >> README.md
    echo [OK] README.md erstellt
)

:: Alles stagen und committen
git add .
git commit -m "Initial commit"

:: Branch auf main setzen
git branch -M main

:: Remote hinzufuegen
git remote remove origin >nul 2>&1
git remote add origin https://github.com/%USERNAME%/%REPONAME%.git
echo [OK] Remote gesetzt

:: Pushen
echo.
echo Pushe zu GitHub...
git push -u origin main

if errorlevel 1 (
    echo.
    echo FEHLER beim Pushen! Pruefe deinen Token und Benutzernamen.
    pause
    exit /b
)

echo.
echo ╔══════════════════════════════════════╗
echo ║            Fertig!                   ║
echo ╠══════════════════════════════════════╣
echo ║  Repo live unter:                    ║
echo ║  https://github.com/%USERNAME%/%REPONAME%
echo ╚══════════════════════════════════════╝
echo.
pause