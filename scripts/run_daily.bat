@echo off
rem Daily cost review on the company PC. Scheduled via Task Scheduler (see docs\PC_SETUP.md).
cd /d "%~dp0"
python build_dashboard.py || goto :fail
python build_ppt.py || goto :fail
python build_email.py || goto :fail
python findings.py build || goto :fail
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0send_email.ps1" || goto :fail
exit /b 0
:fail
echo Daily review failed >> "%~dp0..\daily_review_errors.log"
exit /b 1
