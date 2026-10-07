# Run the daily cost review on the company PC

Everything stays in your company OneDrive. GitHub (if used at all) holds only the code.

1. **Get the code** onto the PC: `git clone https://github.com/sohhuishan/CUL` (or download the ZIP of branch `claude/cost-control-setup`). Put it anywhere, e.g. `C:\CUL`.
2. **Install once:** `pip install python-pptx pandas`
3. **Point it at OneDrive:** copy `config.example.json` to `config.local.json` (git-ignored) and edit the four paths:
   - `CUL_DATA_DIR`: folder for your OPUS CSV exports (columns in `data\README.md`)
   - `CUL_REPORTS_DIR`: where the dashboard, deck and findings page are written
   - `CUL_FINDINGS_DIR`: where findings notes are saved (no git, no push when this is set)
   - `CUL_EMAIL_TO`: where the daily email goes
4. **Test:** double-click `scripts\run_daily.bat`. Outlook must be open and signed in. You should get the email with the deck attached, and the files appear in the reports folder.
5. **Schedule (weekdays 17:52):**
   `schtasks /Create /SC WEEKLY /D MON,TUE,WED,THU,FRI /ST 17:52 /TN "CUL Daily Review" /TR "C:\CUL\scripts\run_daily.bat"`
   The PC must be on and you signed in at that time. Failures are written to `daily_review_errors.log`.
6. **Claude findings log on the PC:** the Stop hook in `.claude/settings.json` uses `python3`; on Windows change it to `python` if needed.

If `CUL_DATA_DIR` has no CSVs, the reports use synthetic sample data and say SAMPLE DATA.
