# AADS Manager - Quick Reference Card

## First Time Setup

```bash
# 1. Initialize database
python initialize_data.py

# 2. (Optional) Install cloud backup
pip install supabase python-dotenv

# 3. Run program
python aads_manager.py
```

---

## Daily Operations

### View Data
- **1** - Master List (all players)
- **2** - Filter by Province (NB/NS/PEI)
- **3** - All Events Summary
- **4** - Specific Event Roster
- **5** - Invite Candidates (rotation tool)
- **6** - Prospects (never competed)
- **7** - Player History

### Manage Events
- **8** - Add Player to Event
- **9** - Set Event Winner (auto-adds to TOC)
- **10** - Add New Player to Master List

### Cloud Backup
- **11** - Cloud Sync Menu
  - **1** - View Status
  - **2** - Push to Cloud (Backup)
  - **3** - Pull from Cloud (Restore)
  - **4** - Test Connection

---

## Common Tasks

### Building Event 6 Roster

1. Select option **5** (Invite Candidates)
2. Review who didn't play Event 5
3. Use option **2** to check province breakdown
4. Use option **8** to add 10 players to Event 6

### Recording Event Winner

1. Select option **9** (Set Event Winner)
2. Enter event number (1-6)
3. Enter winner's exact name
4. Winner auto-added to Event 7 TOC!

### Backing Up Your Data

**Local Backup:**
- Copy `aads_series.db` file to safe location

**Cloud Backup:**
1. Option **11** → **2** (Push to Cloud)
2. Confirm with `yes`
3. Done! ✓

---

## Keyboard Shortcuts

- **Enter** - Confirm/Continue
- **Ctrl+C** - Exit program quickly
- Type menu number and press Enter

---

## File Locations

```
d:\invite program\
├── aads_manager.py       ← Main program
├── initialize_data.py    ← Run once to setup
├── quick_start.py        ← Easy launcher
├── aads_series.db        ← Your data (backup this!)
├── .env                  ← Cloud credentials (keep secret!)
└── SUPABASE_SETUP.md     ← Cloud setup guide
```

---

## Emergency Recovery

### Lost Local Database?
1. Option **11** → **3** (Pull from Cloud)
2. All data restored! ✓

### Can't Find a Player?
- Check option **7** (Player History)
- Search is case-sensitive
- Try option **1** to browse all players

### Need to Rotate Roster?
- Use option **5** (Invite Candidates)
- Shows who didn't play recent event
- Sort by province for balance

---

## Pro Tips

💡 **Weekly Backup**: After each event, push to cloud (Option 11 → 2)

💡 **Province Balance**: Before event, check option 2 to see province counts

💡 **Prospect Tracking**: Option 6 shows players who've never competed

💡 **Event History**: Option 7 shows complete player history

💡 **Auto-Sync**: Set `AUTO_SYNC=true` in `.env` for automatic cloud backup

---

## Need Help?

**Local Issues:**
- Check `aads_series.db` exists
- Verify player names (case-sensitive)
- Run `initialize_data.py` if database missing

**Cloud Issues:**
- Check `.env` file exists and has correct credentials
- Use option 11 → 4 to test connection
- See `SUPABASE_SETUP.md` for full guide

---

## Quick Stats

At any time, option **3** shows:
- All 7 events
- Participant counts
- Event status
- Winners

---

**AADS Series Manager** - Making tournament management simple!
