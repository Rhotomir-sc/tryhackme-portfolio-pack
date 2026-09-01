# 08 - Threat Intelligence & IOC Analysis

| Information | Details |
|---|---|
| Difficulty | Beginner |
| Category | Threat Intelligence & Malware Analysis |
| Platform | TryHackMe |
| Practice Room | File and Hash Threat Intel |
| Analysis Tool | TryDetectThis |

---

## Overview

In this lab, I practiced analysing suspicious Windows files by using file hashes and threat intelligence data.

Instead of relying only on filenames, I generated SHA-256 hashes for suspicious files and used them as indicators to search for additional intelligence.

I analysed two different samples:

- `payroll.pdf.exe`
- `bl0gger.exe`

The investigation included file reputation, malware classification, network indicators, sandbox behaviour and MITRE ATT&CK technique mapping.

---

## Learning Goal

My main goal was to understand how a file hash can be used as a starting IOC and how an investigation can move from one indicator to related technical information.

I also wanted to practice separating direct evidence from assumptions while reviewing threat intelligence reports.

---

# Sample 1 - payroll.pdf.exe

## Initial Observation

One of the files on the system was named:

`payroll.pdf.exe`

The double extension made the file suspicious because it could appear to a user as a payroll-related PDF while actually being a Windows executable.

Before checking its reputation, I generated its SHA-256 hash locally.

```text
d202ed020ed8e36bd8a0f5b571a19d386c12abecb2a28c989d50bbf92c78f54e
