@echo off
echo =======================================================
echo VERCEL FRONTEND AUTOMATIC DEPLOYMENT
echo =======================================================
echo.
echo Khouya, l-pc ghadi yttelecharger Vercel CLI rasso...
echo Ghadi i-dirlek page f l-motsaffih dyalk (Chrome) bash dir Login,
echo ghir cliki "Continue with Github".
echo.
cd frontend
call npx vercel --prod
echo.
echo =======================================================
echo DEPLOYMENT HAS FINISHED! (Chouf l-Link lfoq)
echo =======================================================
pause
