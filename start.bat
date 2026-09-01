@echo off
echo ===================================================
echo  Starting Fake Certificate Detection Server...
echo ===================================================
start http://localhost:3000
node server/server.js
pause
