@echo off
start  "22" "C:\Windows\System32\cmd.exe" 
reg add HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v MyMemoApp /t reg_sz /d "%~dp0memo.exe" 
taskkill /f /im cmd.exe
pause