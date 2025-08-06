@echo off
echo =========================================
echo   ABRINDO MICROSOFT EDGE COM DEBUG
echo =========================================
echo.
echo 🔧 Configurando Edge para monitoramento...
echo.

REM Fechar todas as instâncias do Edge
taskkill /f /im msedge.exe >nul 2>&1

REM Aguardar um momento
timeout /t 2 >nul

REM Abrir Edge com debug habilitado
echo 🚀 Abrindo Microsoft Edge com debug na porta 9222...
start msedge.exe --remote-debugging-port=9222 --user-data-dir="%TEMP%\edge_debug"

echo.
echo ✅ Edge aberto com debug habilitado!
echo.
echo 📋 PRÓXIMOS PASSOS:
echo 1. Acesse https://luck.bet.br/live-casino/game/1170048?provider=Evolution&from=%2Flive-casino&locale=pt-BR&lang=pt
echo 2. Faça login na Luckbet
echo 3. Entre no Football Studio
echo 4. No sistema, clique em um dos botões de captura
echo.
echo ⚠️  IMPORTANTE: NÃO FECHE ESTA JANELA DO EDGE!
echo.
pause
