@echo off
echo ===========================================
echo AI Math Chatbot - Repository Cleanup
echo ===========================================
echo.

echo Cleaning up Python cache files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
echo.

echo Cleaning up Python compiled files...
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul
echo.

echo Cleaning up database files...
del /s /q *.db 2>nul
del /s /q *.sqlite 2>nul
del /s /q *.sqlite3 2>nul
echo.

echo Cleaning up log files...
del /s /q *.log 2>nul
echo.

echo Cleaning up temporary files...
del /s /q *.tmp 2>nul
del /s /q *.temp 2>nul
del /s /q *.bak 2>nul
echo.

echo Cleaning up IDE files...
if exist ".vscode" rd /s /q ".vscode" 2>nul
if exist ".idea" rd /s /q ".idea" 2>nul
if exist ".cursor" rd /s /q ".cursor" 2>nul
echo.

echo Repository cleanup completed!
echo.
echo Next steps:
echo 1. git add .
echo 2. git commit -m "feat: Complete AI Math Chatbot with RAG system"
echo 3. git push origin main
echo.
pause
