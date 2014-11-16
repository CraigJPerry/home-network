# BoxStarter install script for s3 Server (Dell Precision T5400)
#
# Open this URL in Internet Explorer on a freshly installed machine:
#
# http://boxstarter.org/package/url?https://raw.github.com/CraigJPerry/home-network/windows/s3.ps1
#

Update-ExecutionPolicy Unrestricted

Disable-InternetExplorerESC
Enable-RemoteDesktop

Install-WindowsUpdate -AcceptEula
Enable-MicrosoftUpdate

Set-StartScreenOptions -EnableBootToDesktop -EnableShowAppsViewOnStartScreen -EnableListDesktopAppsFirst
Set-WindowsExplorerOptions -EnableShowHiddenFilesFoldersDrives -EnableShowFileExtensions

cinst Gow
cinst sysinternals

cinst 7zip
cinst greenshot
cinst ant-renamer
cinst windirstat

cinst vim

cinst putty
cinst winscp

cinst networkmonitor

cinst python2

