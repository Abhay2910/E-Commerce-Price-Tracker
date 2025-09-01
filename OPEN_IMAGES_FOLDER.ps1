# PowerShell script to open the Pricely images folder
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    PRICELY IMAGES FOLDER OPENER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get the current script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$imagesFolder = Join-Path $scriptPath "static\images"

Write-Host "Current location: $scriptPath" -ForegroundColor Yellow
Write-Host "Looking for images folder: $imagesFolder" -ForegroundColor Yellow
Write-Host ""

if (Test-Path $imagesFolder) {
    Write-Host "✓ Images folder found!" -ForegroundColor Green
    Write-Host "Opening folder..." -ForegroundColor Yellow
    
    try {
        # Method 1: Try to open with explorer
        Start-Process "explorer.exe" -ArgumentList $imagesFolder
        Write-Host "✓ Folder opened successfully!" -ForegroundColor Green
    }
    catch {
        Write-Host "✗ Error opening with explorer: $($_.Exception.Message)" -ForegroundColor Red
        
        # Method 2: Try to open with default file manager
        try {
            Invoke-Item $imagesFolder
            Write-Host "✓ Folder opened with default file manager!" -ForegroundColor Green
        }
        catch {
            Write-Host "✗ Error opening folder: $($_.Exception.Message)" -ForegroundColor Red
            Write-Host ""
            Write-Host "Manual instructions:" -ForegroundColor Yellow
            Write-Host "1. Open File Explorer manually" -ForegroundColor White
            Write-Host "2. Navigate to: $imagesFolder" -ForegroundColor White
            Write-Host "3. Add your profile pictures there" -ForegroundColor White
        }
    }
}
else {
    Write-Host "✗ Images folder not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please make sure you're running this from the main project folder." -ForegroundColor Yellow
    Write-Host "Expected location: $imagesFolder" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Required profile picture files:" -ForegroundColor Cyan
Write-Host "• gyaneshwar_pardhi.jpg (Founder & CEO)" -ForegroundColor White
Write-Host "• gayatri_bopche.jpg (Co-Founder)" -ForegroundColor White
Write-Host "• abhay_rahangdale.jpg (Lead Engineer)" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
