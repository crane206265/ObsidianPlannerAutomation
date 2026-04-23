@echo off

set /p start_date=Start date (YYYY-MM-DD): 
set /p end_date=End date (YYYY-MM-DD): 
set /p overwrite=Overwrite? (y/n): 

set overwrite_flag=
if /i "%overwrite%"=="y" set overwrite_flag=--overwrite

cd C:\Users\dlgkr\OneDrive\Desktop\code\Projects\ObsidianPlannerAutomation
python MarkdownGenerator.py ^
  --base-path "C:\Users\dlgkr\OneDrive\문서\Obsidian\Planner" ^
  --start-date %start_date% ^
  --end-date %end_date% ^
  %overwrite_flag%

pause