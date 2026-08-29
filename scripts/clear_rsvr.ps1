$downloadsFolder = [Environment]::GetFolderPath('UserProfile')
$downloadsFolder = Join-Path $downloadsFolder 'Downloads'

if (Test-Path $downloadsFolder) {
    Get-ChildItem -Path $downloadsFolder -Filter '*.ics' -File | Remove-Item -Force
    Get-ChildItem -Path $downloadsFolder -Filter 'payment*.pdf' -File | Remove-Item -Force
    Get-ChildItem -Path $downloadsFolder -Filter 'reservations*.pdf' -File | Remove-Item -Force
    Write-Host "Deleted all .ics, payment*.pdf, and reservations*.pdf files from $downloadsFolder"
} else {
    Write-Host "Downloads folder not found: $downloadsFolder"
}
