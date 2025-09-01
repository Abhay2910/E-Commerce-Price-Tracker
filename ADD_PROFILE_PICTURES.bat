@echo off
echo ========================================
echo    PRICELY PROFILE PICTURE SETUP
echo ========================================
echo.
echo This will help you add profile pictures to your About Us page.
echo.
echo Required files to add:
echo 1. gyaneshwar_pardhi.jpg (Founder & CEO)
echo 2. gayatri_bopche.jpg (Co-Founder)
echo 3. abhay_rahangdale.jpg (Lead Engineer)
echo.
echo Instructions:
echo 1. Save your profile pictures as JPG files
echo 2. Use the exact filenames shown above
echo 3. Place them in the static/images folder
echo 4. Refresh your browser after adding images
echo.
echo Press any key to open the images folder...
pause >nul

echo.
echo Opening images folder...
cd /d "%~dp0"
if exist "static\images" (
    start explorer "static\images"
    echo Images folder opened successfully!
) else (
    echo ERROR: Images folder not found!
    echo Current directory: %CD%
    echo Looking for: static\images
    echo.
    echo Please make sure you're running this from the main project folder.
    pause
    exit /b 1
)

echo.
echo Images folder opened! 
echo Add your profile pictures there, then refresh your About Us page.
echo.
pause
