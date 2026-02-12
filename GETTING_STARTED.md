# Getting Started with AADS Manager

## 🚀 5-Minute Quick Start (Local Only)

### Step 1: Initialize the Database (1 minute)
```powershell
python initialize_data.py
```

This loads all your existing event data (Events 1-5).

### Step 2: Run the Manager (30 seconds)
```powershell
python aads_manager.py
```

Or double-click `start_aads.bat` on Windows.

### Step 3: Explore Your Data (3 minutes)

Try these menu options:
- **1** - See all players in your database
- **2** - Filter by province (NB, NS, PEI)
- **3** - View all events summary
- **4** - Look at Event 1 roster

**Done!** You're ready to manage Event 6 and beyond.

---

## 📚 What Can I Do Now?

### Build Event 6 Roster

1. **Option 5** - See who didn't play Event 5 (for rotation)
2. **Option 2** - Check province breakdown
3. **Option 8** - Add 10 players to Event 6

### Set Event 5 Winner (if not done yet)

1. **Option 9** - Set Event Winner
2. Enter `5` for Event 5
3. Enter winner's name exactly as shown
4. Winner auto-added to Event 7 (TOC)!

### Add New Players

1. **Option 10** - Add New Player
2. Enter name and province
3. They're now in your scouting database as a "Prospect"

---

## ☁️ Want Cloud Backup? (Optional)

Cloud backup protects your data and lets you access it from multiple computers.

**Time Investment:** 15 minutes one-time setup  
**Cost:** FREE (Supabase free tier)  

### Quick Setup

1. **Create Supabase Account** (5 min)
   - Go to [supabase.com](https://supabase.com)
   - Sign up free
   - Create new project

2. **Install Packages** (1 min)
   ```powershell
   pip install supabase python-dotenv
   ```

3. **Configure** (2 min)
   - Copy `.env.example` to `.env`
   - Add your Supabase URL and Key

4. **Initialize** (5 min)
   - In AADS Manager, select **11** (Cloud Sync)
   - Select **5** (Initialize Tables)
   - Copy SQL to Supabase SQL Editor
   - Run it

5. **First Backup** (2 min)
   - Select **2** (Push to Cloud)
   - Done! Your data is backed up.

**[Full Cloud Setup Guide →](SUPABASE_SETUP.md)**

---

## 📖 Documentation

- **[README.md](README.md)** - Complete feature documentation
- **[SUPABASE_SETUP.md](SUPABASE_SETUP.md)** - Step-by-step cloud setup
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - One-page cheat sheet
- **[CHANGELOG.md](CHANGELOG.md)** - What's new

---

## 💡 Pro Tips

### For First-Time Users

1️⃣ Start with **Option 3** to see all events  
2️⃣ Use **Option 7** to look up any player's history  
3️⃣ **Option 5** is your secret weapon for roster rotation  

### Daily Workflow

**Before Event:**
- Check **Option 5** (Invite Candidates)
- Use **Option 2** to view by province
- Add players with **Option 8**

**After Event:**
- Set winner with **Option 9**
- Backup with **Option 11 → 2** (if using cloud)

---

## ❓ Common Questions

**Q: Do I need internet to use AADS?**  
A: No! Works 100% offline. Cloud is optional for backups.

**Q: Where is my data stored?**  
A: `aads_series.db` file in the same folder as the program.

**Q: How do I backup my data?**  
A: Copy the `.db` file, or use cloud sync (Option 11).

**Q: Can I edit data directly?**  
A: No database editor needed! All editing through the menu.

**Q: What if I make a mistake?**  
A: If you have cloud backup, pull from cloud. Otherwise, restore your `.db` backup.

**Q: Is my data secure in Supabase?**  
A: Yes! Encrypted in transit, access controlled by your credentials.

---

## 🆘 Need Help?

### Database Issues
- **Database not found**: Run `python initialize_data.py`
- **Player not found**: Names are case-sensitive
- **Can't add player**: Check if event is full (10 max)

### Cloud Issues
- **Can't connect**: Check `.env` file exists with correct credentials
- **Tables not found**: Run Initialize Tables (Option 11 → 5)
- **Sync fails**: Test connection first (Option 11 → 4)

### General Issues
- **Program crashes**: Check Python version (need 3.7+)
- **Menu not working**: Type number and press Enter
- **Data looks wrong**: Pull from cloud if you have backup

---

## 🎯 Your First Tasks

Let's get you familiar with the system:

### Task 1: View All Players (30 seconds)
1. Select **1** (Master List)
2. Select **2** (Sort by Province)
3. You'll see everyone grouped by NB, NS, PEI

### Task 2: Check Event 1 Roster (30 seconds)
1. Select **4** (View Event Roster)
2. Type `1` and press Enter
3. See the 10 players and their DEBUT/VETERAN status

### Task 3: Find Rotation Candidates (1 minute)
1. Select **5** (Invite Candidates)
2. See everyone who didn't play Event 5
3. Great for building Event 6!

### Task 4: Look Up a Player (1 minute)
1. Select **7** (Player History)
2. Type any player name (e.g., "Dee Cormier")
3. See their complete event history

---

## ✅ Ready to Go!

You now have:
- ✅ Database with all your event data
- ✅ Easy-to-use menu system
- ✅ Powerful filtering and sorting
- ✅ Automatic TOC management
- ✅ (Optional) Cloud backup

**Next Steps:**
1. Explore the menus
2. Build your Event 6 roster
3. Set up cloud backup when ready
4. Run events with confidence!

---

**Welcome to AADS Series Manager!**  
*Making tournament management simple since 2026* 🏆
