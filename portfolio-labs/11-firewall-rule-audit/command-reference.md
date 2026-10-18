# Commands and queries

Extracted from the existing report for review. These are reference snippets, not a new execution record. Use the original lab context; results depend on its dataset and environment.

## Snippet 1

```powershell
cd C:\Users\Administrator\Desktop\tools\utils
.\fw-summary.ps1 | Tee-Object -FilePath fw-rules.txt
```

## Snippet 2

```powershell
Get-NetFirewallProfile |
Format-Table Name,Enabled,DefaultInboundAction,DefaultOutboundAction -AutoSize
```

## Snippet 3

```powershell
Get-NetFirewallRule |
Where-Object { $_.DisplayName -match "AnyDesk|LMV" } |
Select-Object DisplayName,Enabled,Direction,Action |
Format-Table -AutoSize
```

## Snippet 4

```powershell
$rule = Get-NetFirewallRule -DisplayName "LMV-ADM-EMRG"

$rule |
Select-Object DisplayName,Enabled,Direction,Action |
Format-Table -AutoSize

$rule | Get-NetFirewallPortFilter |
Format-Table Protocol,LocalPort,RemotePort -AutoSize

$rule | Get-NetFirewallAddressFilter |
Format-Table LocalAddress,RemoteAddress -AutoSize

$rule | Get-NetFirewallApplicationFilter |
Format-Table Program -AutoSize
```

[Investigation](README.md)
