# 🌐 AADS Invite Manager - Web Application Guide

## 🚀 Quick Start

**Live Web App**: [https://dowdarts.github.io/invitemanager/](https://dowdarts.github.io/invitemanager/)

No installation needed! Access from any device with a web browser.

---

## ✨ Features

### 💻 Web Application
- **Responsive Design**: Works on desktop, tablet, and mobile
- **No Installation**: Access directly from your browser
- **Offline Capable**: Data stored in browser localStorage
- **Modern UI**: Clean, intuitive interface

### 📊 Dashboard
- Real-time statistics
- Quick overview of all events
- One-click access to key functions

### 👥 Player Management
- Add/view all players
- Filter by province (NB, NS, PEI)
- Search players instantly
- Track player history

### 🏆 Event Management
- Manage 7 events (6 invitationals + TOC)
- Build event rosters (10 players each)
- Set winners
- Auto-qualification for Tournament of Champions

### 📋 Roster Builder
- Add/remove players from events
- Automatic debut/veteran detection
- Province filtering
- Real-time availability

### ☁️ Cloud Sync (Supabase)
- Backup data to cloud
- Sync across devices
- Restore from anywhere
- Secure and encrypted

---

## 📱 First Time Usage

### 1. Open the Web App
Visit: [https://dowdarts.github.io/invitemanager/](https://dowdarts.github.io/invitemanager/)

### 2. Data is Stored Locally
- Your data is saved in your browser
- Works offline after first load
- No account needed to use locally

### 3. (Optional) Set Up Cloud Sync

**Why Cloud Sync?**
- Backup your data
- Access from multiple devices
- Never lose your data

**Setup Steps:**
1. Create free Supabase account at [supabase.com](https://supabase.com)
2. Create a new project
3. In the web app, go to **Settings** tab
4. Enter your Supabase URL and Key
5. Click "Initialize Tables" (copy SQL to Supabase)
6. Click "Test Connection" to verify
7. Click "Push to Cloud" to backup!

---

## 🎯 Common Tasks

### Adding a New Player
1. Go to **Players** tab
2. Click **➕ Add Player**
3. Enter name and select province
4. Click **Save Player**

### Building an Event Roster
1. Go to **Roster** tab
2. Select an event from dropdown
3. Search/filter available players
4. Click **Add** next to players you want
5. Build your 10-person roster

### Setting an Event Winner
1. Go to **Events** tab
2. Find the event
3. Click **🏆 Set Winner**
4. Enter the winner's player ID
5. Winner auto-qualifies for TOC!

### Finding Invite Candidates
1. Go to **Dashboard**
2. Click **Find Invite Candidates**
3. See players who didn't compete in recent event
4. Perfect for roster rotation!

### Backing Up Your Data

**Option 1: Cloud Sync (Recommended)**
1. Go to **Settings** tab
2. Configure Supabase (one-time setup)
3. Click **⬆️ Push to Cloud**
4. Done!

**Option 2: Manual Export**
1. Go to **Settings** tab
2. Click **📥 Export Data (JSON)**
3. Save the file somewhere safe

### Restoring Data

**From Cloud:**
1. Go to **Settings**
2. Click **⬇️ Pull from Cloud**
3. Confirm the restore

**From File:**
1. Go to **Settings**
2. Click **📤 Import Data (JSON)**
3. Select your backup file

---

## 💾 Data Storage

### Local Storage (Browser)
- Data stored in browser's localStorage
- Persists across sessions
- Cleared if you clear browser data
- **Recommendation**: Set up cloud sync!

### Cloud Storage (Supabase)
- PostgreSQL database
- Encrypted in transit
- Free tier: 500MB storage
- Perfect for AADS needs

---

## 🔐 Security & Privacy

### Your Data
- Stored locally in YOUR browser
- Only synced to cloud if YOU set it up
- No data sent without your action
- No tracking or analytics

### Supabase Credentials
- Stored only in your browser
- Never sent to any server except Supabase
- You control your own database

---

## 📱 Mobile Usage

The web app works great on mobile devices!

**Tips:**
- Add to home screen for app-like experience
- Landscape mode recommended for tables
- All features work on mobile

**Add to Home Screen:**
- **iPhone**: Share → Add to Home Screen
- **Android**: Menu → Add to Home Screen

---

## 🆚 Web App vs Desktop App

### Web Application
✅ No installation required  
✅ Access from anywhere  
✅ Works on any device  
✅ Automatic updates  
✅ Mobile friendly  

### Python Desktop App
✅ Fully offline  
✅ Direct database access  
✅ Terminal-based  
✅ Script automation possible  

**Both versions share the same Supabase database** - use whichever you prefer!

---

## 🐛 Troubleshooting

### Data Not Saving
- Check if localStorage is enabled in browser
- Try a different browser
- Clear cache and reload

### Cloud Sync Not Working
- Verify Supabase credentials in Settings
- Click "Test Connection" to diagnose
- Check Supabase project is active
- Ensure tables are initialized

### Can't Add Players
- Check for duplicate names
- Verify all fields are filled
- Try refreshing the page

### Import/Export Issues
- Ensure file is valid JSON
- Don't edit export files manually
- Try exporting again

---

## 💡 Pro Tips

1. **Regular Backups**: Push to cloud after each event
2. **Province Balance**: Use filters to balance representation
3. **Rotation Tool**: Use "Find Invite Candidates" feature
4. **Mobile Access**: Add to home screen for quick access
5. **Multiple Devices**: Use cloud sync across devices

---

## 🔗 Quick Links

- **Live App**: [https://dowdarts.github.io/invitemanager/](https://dowdarts.github.io/invitemanager/)
- **GitHub Repo**: [https://github.com/dowdarts/invitemanager](https://github.com/dowdarts/invitemanager)
- **Supabase**: [https://supabase.com](https://supabase.com)
- **Report Issues**: [GitHub Issues](https://github.com/dowdarts/invitemanager/issues)

---

## ❓ FAQ

**Q: Do I need an account to use the app?**  
A: No! Works completely locally without any account.

**Q: Is my data secure?**  
A: Yes! Data is stored in your browser. Cloud sync is optional and encrypted.

**Q: Can I use this offline?**  
A: Yes! After first load, works offline. Sync when you're back online.

**Q: Does it work on mobile?**  
A: Absolutely! Fully responsive design works on all devices.

**Q: Can multiple people use the same database?**  
A: Yes, if you share Supabase credentials and use cloud sync.

**Q: How much does Supabase cost?**  
A: Free tier is more than enough for AADS needs (500MB storage).

**Q: What if I lose my data?**  
A: If you've enabled cloud sync, just pull from cloud to restore everything!

**Q: Can I contribute to development?**  
A: Yes! Fork the repo and submit pull requests on GitHub.

---

**Made with ❤️ for the Atlantic Armwrestling Development Series**

💪 **Road to the TOC - Now Accessible Anywhere!**
