# How to host this wiki on GitHub Pages (free, public)

End result: a URL like `https://<your-username>.github.io/cyberlogitec-opus-wiki/` that you and your colleagues can open from anywhere — no file path, no OneDrive prefix, always points to the latest version you pushed.

> **Note:** GitHub Pages on **free accounts works only for public repos.** If you need it private, you'd need GitHub Pro ($4/mo). The sensitivity scan confirmed this HTML has no confidential data, so public is fine.

## Step 1 — Create the repo (public this time)

1. Go to [github.com/new](https://github.com/new)
2. **Repository name**: `cyberlogitec-opus-wiki` (or any short name you like — this becomes part of the URL)
3. **Description**: `Interactive reference wiki for the CyberLogitec OPUS / Allegro shipping system`
4. **Visibility**: **Public** (required for free Pages)
5. Leave "Add a README" and ".gitignore" **unticked** — we have our own
6. Click **Create repository**

## Step 2 — Upload the files

1. On the empty repo page, click **"uploading an existing file"** (or **Add file → Upload files**)
2. Drag-and-drop from this `github-upload` folder:
   - `index.html` (this is what Pages serves by default — keep this filename!)
   - `CyberLogitec_OPUS_Wiki.html` (optional duplicate for direct download)
   - `README.md`
   - `.gitignore`
3. Commit message: `Initial commit — OPUS wiki v1`
4. Click **Commit changes**

## Step 3 — Turn on GitHub Pages

1. In the repo, click **Settings** (top-right tab)
2. In the left sidebar, click **Pages** (under "Code and automation")
3. Under "Build and deployment":
   - **Source**: `Deploy from a branch`
   - **Branch**: `main` → `/ (root)`
4. Click **Save**
5. Wait 30-90 seconds. Refresh the Pages settings page. You'll see a green box:

   > Your site is live at `https://<your-username>.github.io/cyberlogitec-opus-wiki/`

## Step 4 — Bookmark the clean URL

1. Open the new URL in your browser
2. Press **Ctrl+D** → rename to **"OPUS Wiki"** → save to Bookmarks bar
3. It now sits alongside your CUL Portal / Alphaliner bookmarks with the same clean appearance

## Updating the wiki later

Whenever you have a new version of the HTML:

**Web UI way** (easiest): go to the repo → click the `index.html` file → click the pencil (Edit) icon → paste the new content → Commit. Pages rebuilds in ~1 minute.

**Drag-and-drop way**: go to repo → **Add file → Upload files** → drop the new `index.html` → commit. Uploads overwrite the old file.

## Sharing with colleagues

Just send them the URL. They don't need a GitHub account. Works on phones, tablets, any browser.

## Common problems

| Problem | Fix |
|---|---|
| "404 — page not found" after enabling Pages | Wait 2 min, hard-refresh (Ctrl+F5). First build can take time. |
| Pages shows old version | GitHub caches aggressively. Hard-refresh or wait ~5 min after a commit. |
| I want a custom domain like `wiki.cul.com` | Settings → Pages → Custom domain. Requires DNS config at your domain registrar. |
| I want to take it offline temporarily | Settings → Pages → Unpublish site. Files stay in repo. |

## Direct link to the accrual flow diagram

Once live, the deep-linked URL is:

```
https://<your-username>.github.io/cyberlogitec-opus-wiki/#AccrualFlow
```

Same anchor-navigation as the local file — `#COA-CostTable`, `#JOO-Monthly`, etc. all work.
