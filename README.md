# Halcyon content calendar

TikTok and Instagram posting calendar for Halcyon Trader Funding, Fri 6 to Fri 20 Nov 2026. Open `index.html`, or the GitHub Pages site, and use the switch to change apps. Click any post for its caption, notes and media.

## Editing on screen

Click **Edit** in the header. Drag a post to another day to move it, or drop it on another post on the same app to swap their dates and times. Click a status dot to cycle not scheduled, scheduled, posted and automatic. Click a post to change its date, time and copy in the side panel.

Use **+ Add post** (on any day, or in the edit bar) to add a post, and **Delete post** in a post's panel to remove it.

Changes wait in that browser until you click **Save to GitHub**, which commits them into `index.html`. This repo is the calendar's source of truth, and GitHub Pages shows the change about a minute later. The first save asks for a fine-grained GitHub token with Contents read and write on this repo only; it stays in that browser. **Copy my edits** still copies the changes as JSON for Claude, for example to attach a video to a new post. The editor lives in `edit.js`. The page before the editor was added is kept in `versions/`.
