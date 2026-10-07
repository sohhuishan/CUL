# Company-PC mode, session review, and storage decisions

- **Date:** 2026-10-06
- **Status:** Confirmed (decisions and build state); the PC pieces are untested
- **Data used:** none (no real accrual/actual data in this repo)

## Finding
- Daily review now runs on the company PC, with data, reports and findings kept in company OneDrive. GitHub holds code only.
- The cloud email routine (trig_01GwyBFuLszcGgizNtT7uPp9) is switched OFF: it had no Gmail connector and cannot see OneDrive.
- A review of ~165 past sessions was written up and published as a private page. It is not in this repo because it contains company figures.

## Cause
Cloud sessions cannot reach OneDrive or Outlook, and company data should not sit in a possibly-public repo.

## Evidence
- Pipeline run end to end on Linux with redirected folders: dashboard, deck, email summary and findings page all built.
- NOT tested: scripts/run_daily.bat, scripts/send_email.ps1 (Outlook), the Task Scheduler command, the hook on Windows.

## Action / decision
- Set up on the PC per docs/PC_SETUP.md; send any error from daily_review_errors.log.
- Supply real OPUS exports to the data folder; until then outputs are marked SAMPLE DATA.
- Decide: make the repo private, or keep company data out of it entirely (current state).
