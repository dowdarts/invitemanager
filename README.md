# 🎯 AADS Invite Manager

**Atlantic Amateur Darts Series Management System**

## 🌐 **[LAUNCH WEB APP](https://dowdarts.github.io/invitemanager/)** 🌐

A comprehensive scouting and roster management system for the AADS tournament series.

**✨ Now Available as a Web Application! ✨**

---

## 🚀 Quick Start

### Web App (Recommended)
**No installation needed!** Just visit:
### **[https://dowdarts.github.io/invitemanager/](https://dowdarts.github.io/invitemanager/)**

- ✅ Works on any device (desktop, tablet, mobile)
- ✅ No installation required
- ✅ Instant access
- ✅ Cloud sync with Supabase

**[📖 Web App Guide](WEBAPP_GUIDE.md)**

### Desktop App (Advanced Users)
Traditional Python application for offline use:
```bash
python initialize_data.py    # One-time setup
python aads_manager.py        # Run program
```

**[📖 Desktop Setup Guide](GETTING_STARTED.md)**

---

## 🌟 What's New in v2.0

Your AADS data can now be backed up to the cloud! Features include:
- ☁️ **Automatic Cloud Backup**: Never lose your tournament data
- 🔄 **Multi-Device Sync**: Access from multiple computers
- 🆓 **Free Tier Available**: Up to 500MB storage (plenty for years of data)
- 🔒 **Secure & Private**: Your data, your control

**[📖 See Supabase Setup Guide](SUPABASE_SETUP.md)** for step-by-step instructions.

---

## Features

### 🎯 Core Capabilities

- **Master Scouting Database**: Track all regional prospects and active players across NB, NS, and PEI
- **Event Management**: Manage 7 events (6 invitationals + Tournament of Champions)
- **Automatic TOC Qualification**: Winners automatically qualify for Event 7
- **Smart Roster Tracking**: Automatically flags player debuts vs. returning veterans
- **Historical Records**: Complete event participation history for every player

### 📊 Viewing & Filtering

- **Sort by Province**: Group all players by NB, NS, or PEI
- **Sort by Participation**: See most active players vs. prospects
- **Invite Candidates**: Filter players who didn't participate in recent events
- **Prospects View**: See all players who have never competed

## Quick Start

### 1. Initialize the Database

Run this **ONCE** to set up the database with your event data:

```bash
python initialize_data.py
```

This will:
- Create the database structure
- Load all players from Events 1-5
- Set up Event 6 (Active) and Event 7 (TOC)

### 2. Run the Manager

```bash
python aads_manager.py
```

## Main Menu Options

### Viewing Options

1. **View Master Scouting List** - See all players with multiple sorting options
2. **View by Province** - Filter players by NB, NS, or PEI
3. **View All Events Summary** - Quick overview of all 7 events
4. **View Specific Event Roster** - See detailed roster for any event
5. **View Invite Candidates** - Players who didn't compete in the most recent event
6. **View Prospects** - Players who have never competed
7. **View Player History** - Complete event history for any player

### Management Options

8. **Add Player to Event** - Add a player to an event roster (max 10 per event)
9. **Set Event Winner** - Mark a winner for Events 1-6 (auto-adds to TOC)
10. **Add New Player** - Add a new prospect to the master scouting list

### Cloud Backup (Optional)

11. **Cloud Sync** - Supabase backup and restore
    - Push to Cloud (backup your data)
    - Pull from Cloud (restore data)
    - Test Connection
    - View Sync Status
    - Initialize Supabase Tables

---

## Cloud Backup Setup (Optional)

Want to protect your data? Set up cloud backup in 15 minutes:

1. **Create free Supabase account**: [supabase.com](https://supabase.com)
2. **Install packages**: `pip install supabase python-dotenv`
3. **Configure**: Copy `.env.example` to `.env` and add your credentials
4. **Initialize**: Run option 11 → 5 in the program
5. **Backup**: Use option 11 → 2 to push your data to the cloud

**[📖 Full Setup Guide](SUPABASE_SETUP.md)** - Complete step-by-step instructions

---

## Management Options

### Player Status System

- **Prospect**: Never competed (0 events)
- **Active**: Currently participating in events
- **Winner**: Won an event (Events 1-6)
- **TOC Qualified**: Automatically set when a player wins an event

### Event Flow

1. **Events 1-6**: Standard invitationals (10 players each)
2. **Event 7**: Tournament of Champions (automatically populated)

### Automatic Features

✅ **Debut/Veteran Flagging**: System automatically detects if a player is making their debut or returning
✅ **TOC Auto-Population**: Winners are immediately added to Event 7 roster
✅ **Participation Tracking**: Every player's event count is updated automatically
✅ **Status Updates**: Player status changes from Prospect → Active → Winner automatically

## Usage Examples

### Example 1: Scouting for Event 6

You need to invite PEI players for Event 6. Here's how:

1. Select option **2** (View by Province)
2. Choose **3** (PEI)
3. Review the list and check their event history
4. Select option **5** (View Invite Candidates) to see who didn't play Event 5
5. Use option **8** (Add Player to Event) to build your Event 6 roster

### Example 2: Setting a Winner

Event 6 is complete and you need to record the winner:

1. Select option **9** (Set Event Winner)
2. Enter event number: `6`
3. Review the roster displayed
4. Enter the winner's name exactly as shown
5. Confirm - the winner is automatically added to Event 7!

### Example 3: Finding Active NS Players

You want to see all Nova Scotia players who are actively competing:

1. Select option **2** (View by Province)
2. Choose **2** (Nova Scotia)
3. Players are shown with their event counts
4. Look for "Active" or "Winner" status with event counts > 0

## Database Information

- **Local Database**: `aads_series.db` (SQLite)
- **Cloud Database**: Supabase PostgreSQL (optional)
- **Location**: Same directory as the programs
- **Local Backup**: Simply copy the `.db` file
- **Cloud Backup**: Use option 11 → 2 in the program

### Backup Strategy

**Option 1: Local Only**
- Copy `aads_series.db` file regularly
- Store backups on external drive or cloud storage

**Option 2: Cloud Sync (Recommended)**
- Automatic backup to Supabase
- Access from multiple computers
- Disaster recovery built-in
- See [SUPABASE_SETUP.md](SUPABASE_SETUP.md)

---

## Files Overview

- `aads_database.py` - Core database functions
- `aads_manager.py` - Main program interface
- `initialize_data.py` - One-time data loader
- `aads_series.db` - SQLite database (created on first run)

### Data Tracked

Each player record includes:
- Name
- Province (NB, NS, PEI)
- Status (Prospect, Active, Winner, TOC Qualified)
- Total Events participated in
- TOC Qualification flag
- Complete event history

Each event record includes:
- Event name and number
- Event type (Invitational or TOC)
- Status (Pending, Active, Completed)
- Participant list (max 10)
- Winner (if set)
- Debut/Veteran flags for each participant

## Requirements

- Python 3.7 or higher
- SQLite3 (included with Python)

No additional packages required! The program uses only Python standard library.

## Tips

💡 **Roster Rotation**: Use "View Invite Candidates" to ensure you're rotating through players fairly

💡 **Province Balance**: Check "View by Province" before each event to balance representation

💡 **Player History**: Before inviting someone, check their history to see their participation pattern

💡 **Backup Your Data**: Regularly copy `aads_series.db` to a backup location

## Support

For issues or questions about the AADS Series Manager, check:
1. Is the database initialized? (Run `initialize_data.py` first)
2. Are player names spelled consistently? (Case-sensitive)
3. Is the database file in the same directory?

---

**AADS Series Manager v1.0**  
*Built for the Atlantic Armwrestling Development Series*  
*"Road to the TOC" - Tournament Management Made Simple*
