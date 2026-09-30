# Duplicate Files Report

## Executive Summary
The Worksheet Wonder repository was scanned for duplicate, redundant, and multiple version files. All duplicate or obsolete versions were identified and archived into the `Archive/` directory to enforce single sources of truth without data loss.

## Duplicate Files Inventory

| Original File Path | Secondary / Canonical Target | Description | Action Taken |
| :--- | :--- | :--- | :---: |
| `/MASTER_*.xlsx` (9 files) | `/database/MASTER_*.xlsx` | Duplicate copies of database master spreadsheets | ARCHIVED |
| `/index - backup.html` | `/index.html` | Backup copy of homepage | ARCHIVED |
| `/flagship_letter_a.html` | `/worksheets/alphabet/letter-a-worksheet.html` | Superseded v1 flagship worksheet | ARCHIVED |
| `/flagship_letter_a_v2.html` | `/worksheets/alphabet/letter-a-worksheet.html` | Superseded v2 flagship worksheet | ARCHIVED |
| `/data/worksheets.json` | `/database/data/worksheets.json` | Old duplicate database directory | ARCHIVED |
