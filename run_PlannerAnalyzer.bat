@echo off
chcp 65001 > nul

set /p start_date=Start date (YYYY-MM-DD): 
set /p end_date=End date (YYYY-MM-DD): 
set /p categories=Categories: 

cd C:\Users\dlgkr\OneDrive\Desktop\code\Projects\ObsidianPlannerAutomation
python PlannerAnalyzer.py ^
  --base-path "C:\Users\dlgkr\OneDrive\문서\Obsidian\Planner" ^
  --start-date %start_date% ^
  --end-date %end_date% ^
  --categories %categories% ^
  --exclude-uncategorized ^
  --font-weight heavy ^
  --show-missing

pause