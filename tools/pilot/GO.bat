@echo off
chcp 65001 >nul
setlocal
title Pilot Bugcrowd OpenAI

:MENU
cls
echo ============================================
echo   PILOT BUGCROWD OPENAI - double-clic = go
echo ============================================
echo.
echo   1. Lancer Chrome compte A      (port 9222)
echo   2. Lancer Chrome compte B      (port 9223)
echo.
echo   3. Mission EXEMPLE        (A doit etre ouvert et connecte)
echo   4. Mission T-01 partie A  (A ouvert et connecte)
echo   5. Mission T-01 partie B  (B ouvert et connecte, apres la 4)
echo.
echo   6. Mettre a jour depuis GitHub (git pull)
echo   Q. Quitter
echo.
set /p CHOIX= Ton choix puis Entree :

if /i "%CHOIX%"=="Q" goto END
if "%CHOIX%"=="1" goto CHROME_A
if "%CHOIX%"=="2" goto CHROME_B
if "%CHOIX%"=="3" set MISSION=%~dp0missions\exemple-verif-connexion.json& goto RUN
if "%CHOIX%"=="4" set MISSION=%~dp0missions\t01-partie-A.json& goto RUN
if "%CHOIX%"=="5" set MISSION=%~dp0missions\t01-partie-B.json& goto RUN
if "%CHOIX%"=="6" goto UPDATE
goto MENU

:FIND_CHROME
set "CHROME=C:\Program Files\Google\Chrome\Application\chrome.exe"
if not exist "%CHROME%" set "CHROME=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
if not exist "%CHROME%" (
  echo.
  echo [ERREUR] Chrome introuvable aux emplacements habituels.
  echo Dis-le dans le chat, on trouvera son chemin ensemble.
  pause
)
exit /b

:CHROME_A
call :FIND_CHROME
if not exist "%CHROME%" goto MENU
start "" "%CHROME%" --remote-debugging-port=9222 --remote-debugging-address=127.0.0.1 --user-data-dir="%USERPROFILE%\oai-pilot\A" "https://chatgpt.com"
echo Chrome A lance. Connecte-toi avec snwdc@bugcrowdninja.com si besoin.
timeout /t 2 >nul
goto MENU

:CHROME_B
call :FIND_CHROME
if not exist "%CHROME%" goto MENU
start "" "%CHROME%" --remote-debugging-port=9223 --remote-debugging-address=127.0.0.1 --user-data-dir="%USERPROFILE%\oai-pilot\B" "https://chatgpt.com"
echo Chrome B lance. Connecte-toi avec le compte B (adresse email DISTINCTE de A : les alias +b sont fusionnes par OpenAI).
timeout /t 2 >nul
goto MENU

:RUN
echo.
echo === Mission : %MISSION%
echo (Entree = executer chaque etape, q = arreter. Le dossier resultats s'ouvrira tout seul a la fin.)
echo.
py "%~dp0pilot.py" "%MISSION%"
echo.
echo === Termine. Envoie dans le chat : A-MENVOYER.md (ou DERNIER-A-MENVOYER.md) + les .png apres relecture.
pause
goto MENU

:UPDATE
git -C "%~dp0..\.." pull
echo.
pause
goto MENU

:END
endlocal
