# Commands and queries

Extracted from the existing report for review. These are reference snippets, not a new execution record. Use the original lab context; results depend on its dataset and environment.

## Snippet 1

```powershell
Set-Service -Name "TermService" -StartupType Disabled
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name "fDenyTSConnections" -Value 1
reg save HKLM\SYSTEM C:\Windows\Temp\system.bak /y
Remove-Item C:\Windows\Temp\system.bak -Force
Get-Service TermService | Select-Object Name, Status, StartType
Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Services\TermService" | Select-Object Start
Stop-Service -Name "TermService" -Force
```

[Investigation](README.md)
