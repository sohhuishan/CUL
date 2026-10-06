# Session log: 2026-10-06 — Phone remote access not working

**Surface:** Claude app on phone (Code tab) + Chrome Remote Desktop to work PC
**Repo:** CUL (no files changed other than this log)

## Question
Why does remote control from the phone keep failing? It works at first, then stops, and Remote Control (RC) has to be turned on again.

## What the screenshots showed
- Phone Code tab: **Devices: none** ("Add device" only).
- Sessions listed: "Recording session findings" (CUL, `claude/cost-control-setup`, cloud) and "Log sessions from AI agent to Obsidian" (6d, crossed-out laptop icon = host PC offline).
- PC (via Chrome Remote Desktop): Claude Desktop, local session "JO Creation Status report", with a follow-up checklist visible.
- The local PC session did not appear on the phone, so the PC was not connected as a remote device.

## Findings
RC is a live connection from a running session on the PC to Claude's servers. It is not a permanent pairing, so it can drop while the session stays open on the PC.

Likely causes, most likely first (not confirmed; PC logs were not checked):
1. PC went idle: Windows sleep, screen lock or a Wi-Fi change cut the link, and it often does not reconnect by itself.
2. RC is per session: a new session or an app restart starts with RC off.
3. Ending Chrome Remote Desktop can lock or sleep the PC, which triggers cause 1.
4. Company network / VPN cutting long-lived connections.

## Recommended fixes
- Windows: Sleep = Never when plugged in; screen lock timeout off; laptop lid = do nothing.
- Run `claude remote-control` in the CUL folder and leave that terminal open.
- Make sure phone and PC use the same Claude account.
- For phone-only work, use a cloud session; files must be in the CUL repo or Drive.

## Open items
- [ ] Check PC sleep / lock settings (steps given in chat; PC cannot be checked from the cloud session).
  - `powercfg /query SCHEME_CURRENT SUB_SLEEP STANDBYIDLE`
  - `powercfg /lastwake`
  - Event ID 42 (Kernel-Power) in the System log shows when the PC went to sleep.
- [ ] Re-enable RC / add the device on the phone after the settings change.
- [ ] If sleep settings are greyed out, ask IT (group policy).

## Context from the desktop session (from screenshot, not verified here)
"JO Creation Status report" follow-ups, for reference: chase offices for J/Os paid in Yikuaibao with no J/O (B26002601, B26002351, B26002865, B26000558, Category C), fix J/Os that already exist (B26002816, B26002348, Category B), X-Press terminal-cost booking rule and claim type, and data checks (B26001916 export amount, 5-digit reference collisions, B26000427 vs B26000687, unifeeder claims B26002867 / B26002985).
