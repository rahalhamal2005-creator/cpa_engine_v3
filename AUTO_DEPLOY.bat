@echo off
echo ==================================================
echo CPA ENGINE V3 - AUTO DEPLOYMENT PREPARATION SCRIPT
echo ==================================================
echo.
echo 1. Installing Frontend Dependencies...
cd frontend
call npm install

echo.
echo 2. Building Frontend Dashboard...
call npm run build
cd ..

echo.
echo 3. Initializing Git & Committing Project...
git init
git add .
git commit -m "Auto-prepared by Assistant for online deployment"

echo.
echo ==================================================
echo EVERYTHING IS READY FOR ONLINE UPLOAD!
echo The Frontend is built inside the "frontend/dist" folder.
echo The Project is saved locally via Git.
echo ==================================================
pause
