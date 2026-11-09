@echo off
title STEM Automated Test Harness
cd /d "%~dp0"
python stem_shared_core\tools\run_batch_auto_test.py
pause
