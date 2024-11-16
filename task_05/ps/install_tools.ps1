 
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

Write-Output "Refresh environment" 
Import-Module C:\ProgramData\Chocolatey\helpers\chocolateyProfile.psm1; Update-SessionEnvironment

Write-Output "Verifying installations..." 
 
choco list | Select-String "flutter|python*|dotnet|gnupg|git" ;
python --version ;
gpg --version | Select-String 'gpg' ;
dotnet --info | Select-String "Version: .*" ;

Write-Output "All requested software has been installed."

git clone https://github.com/maverick8899/training.git
gpg --import training\task_05\private_key.asc
gpg --decrypt training\task_05\demo.py.gpg  > data