@echo off
echo =========================================
echo   ABRINDO GOOGLE CHROME COM DEBUG
echo =========================================
echo.
echo 🔧 Configurando Chrome para monitoramento...
echo.

REM Fechar todas as instâncias do Chrome
taskkill /f /im chrome.exe >nul 2>&1

REM Aguardar um momento
timeout /t 2 >nul

REM Abrir Chrome com debug habilitado
echo 🚀 Abrindo Google Chrome com debug na porta 9222...
start chrome.exe --remote-debugging-port=9222 --user-data-dir="%TEMP%\chrome_debug"

echo.
echo ✅ Chrome aberto com debug habilitado!
echo.
echo 📋 PRÓXIMOS PASSOS:
echo 1. Acesse https://luck.bet.br/live-casino/game/1384453
echo 2. Faça login na Luckbet
echo 3. Entre no Football Studio
echo 4. No sistema, clique em um dos botões de captura
echo.
echo ⚠️  IMPORTANTE: NÃO FECHE ESTA JANELA DO CHROME!
echo.
pause
