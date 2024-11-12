# Remove unnecessary package

Get-AppxPackage *3dbuilder* | Remove-AppxPackage
Get-AppxPackage *windowsalarms* | Remove-AppxPackage
Get-AppxPackage *Appconnector* | Remove-AppxPackage
Get-AppxPackage *windowscalculator* | Remove-AppxPackage
Get-AppxPackage *windowscommunicationsapps* | Remove-AppxPackage
Get-AppxPackage *windowscamera* | Remove-AppxPackage
Get-AppxPackage *CandyCrushSaga* | Remove-AppxPackage
Get-AppxPackage *officehub* | Remove-AppxPackage
Get-AppxPackage *skypeapp* | Remove-AppxPackage
Get-AppxPackage *getstarted* | Remove-AppxPackage
Get-AppxPackage *zunemusic* | Remove-AppxPackage
Get-AppxPackage *windowsmaps* | Remove-AppxPackage
Get-AppxPackage *Messaging* | Remove-AppxPackage
Get-AppxPackage *solitairecollection* | Remove-AppxPackage
Get-AppxPackage *ConnectivityStore* | Remove-AppxPackage
Get-AppxPackage *bingfinance* | Remove-AppxPackage
Get-AppxPackage *zunevideo* | Remove-AppxPackage
Get-AppxPackage *bingnews* | Remove-AppxPackage
Get-AppxPackage *onenote* | Remove-AppxPackage
Get-AppxPackage *people* | Remove-AppxPackage
Get-AppxPackage *CommsPhone* | Remove-AppxPackage
Get-AppxPackage *windowsphone* | Remove-AppxPackage
Get-AppxPackage *photos* | Remove-AppxPackage
Get-AppxPackage *WindowsScan* | Remove-AppxPackage
Get-AppxPackage *bingsports* | Remove-AppxPackage
Get-AppxPackage *Office.Sway* | Remove-AppxPackage
Get-AppxPackage *Twitter* | Remove-AppxPackage
Get-AppxPackage *soundrecorder* | Remove-AppxPackage
Get-AppxPackage *bingweather* | Remove-AppxPackage
Get-AppxPackage *xboxapp* | Remove-AppxPackage
Get-AppxPackage *XboxOneSmartGlass* | Remove-AppxPackage
Get-AppxPackage *qq* | Remove-AppxPackage
Get-AppxPackage *Connect* | Remove-AppxPackage
Get-AppxPackage *maps* | Remove-AppxPackage
Get-AppxPackage *people* | Remove-AppxPackage
Get-AppxPackage *phone* | Remove-AppxPackage
Get-AppxPackage *skype* | Remove-AppxPackage

# Install Chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force;
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072;
Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'));
 
# Refresh environment variables (required after installing Chocolatey)
$env:Path += ";$([System.Environment]::GetEnvironmentVariable('ChocolateyInstall'))\bin"

choco install python -y
choco install flutter -y
choco install dotnet -y
choco install gnupg -y
choco install git -y

Write-Output "Verifying installations..." 

# AddTo-Path C:\Python312\
# AddTo-Path C:\'Program Files (x86)'\gnupg\bin\
# AddTo-Path C:\'Program Files (x86)'\dotnet\dotnet
# AddTo-Path C:\tools\flutter\bin\
choco list | Select-String "flutter|python*|dotnet|gnupg" ;
C:\Python312\python --version ;
C:\'Program Files (x86)'\gnupg\bin\gpg --version | Select-String 'gpg' ;
C:\'Program Files (x86)'\dotnet\dotnet --info | Select-String "Version: .*" ;

Write-Output "All requested software has been installed."
