# Halcyon content calendar

TikTok and Instagram posting calendar for Halcyon Trader Funding, Fri 6 to Fri 20 Nov 2026. Open `index.html`, or the GitHub Pages site, and use the switch to change apps. Click any post for its caption, notes and media.

## Editing on screen

The calendar is always editable. Drag a post to another day to move it, or onto another post on the same app to swap them (on a phone, press and hold first). Tap a status dot to cycle not scheduled, scheduled, posted and automatic. Tap a post to change its date, time and copy, or to delete it. Tap **+** on any day, or **+ Add post** in the bar, to add a post.

Changes auto-save: a couple of seconds after each change the page commits it into `index.html` here, which is the calendar's source of truth, and GitHub Pages shows it about a minute later. Turning auto-save on needs a fine-grained GitHub token with Contents read and write on this repo only, entered once per browser. If the repo changed after the page loaded, auto-save pauses and asks for a reload instead of overwriting. The editor lives in `edit.js`; the page before the editor was added is kept in `versions/`.
