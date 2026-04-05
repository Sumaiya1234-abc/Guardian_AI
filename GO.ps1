#!/usr/bin/env batch
:: GuardianAI - PowerShell One Command
powershell -NoProfile -ExecutionPolicy Bypass -Command "& '.\.venv\Scripts\Activate.ps1'; pip install flask -q; echo 'Opening in browser...'; Start-Process 'http://127.0.0.1:5000'; python app_ui.py"
