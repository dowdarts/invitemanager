# Supabase Cloud Backup Setup Guide

## What is Supabase?

Supabase is a free, open-source alternative to Firebase that provides:
- **Cloud Database**: PostgreSQL database hosted in the cloud
- **Automatic Backups**: Your data is safely backed up
- **Multi-Device Access**: Access your AADS data from anywhere
- **Disaster Recovery**: Never lose your tournament data

## Why Use Supabase with AADS?

✅ **Free Tier Available**: Up to 500MB database storage free  
✅ **Cloud Backup**: Protect against data loss  
✅ **Easy Sync**: Push/pull data with one click  
✅ **Multi-Computer**: Use AADS on multiple computers  
✅ **No Server Setup**: Everything managed for you  

## Step-by-Step Setup

### 1. Create a Supabase Account (5 minutes)

1. Go to [https://supabase.com](https://supabase.com)
2. Click "Start your project"
3. Sign up with GitHub, Google, or email
4. Verify your email if required

### 2. Create a New Project (2 minutes)

1. Click "New Project" in your dashboard
2. Choose an organization (or create one)
3. Fill in project details:
   - **Name**: `aads-series` (or any name you like)
   - **Database Password**: Create a strong password (save this!)
   - **Region**: Choose closest to you (e.g., `East US`)
   - **Pricing Plan**: Select "Free" tier
4. Click "Create new project"
5. Wait 1-2 minutes for project to be provisioned

### 3. Get Your API Credentials (1 minute)

1. In your project dashboard, click on the **Settings** icon (⚙️) in the left sidebar
2. Click **API** in the settings menu
3. You'll see two important values:

   **Project URL** (looks like):
   ```
   https://abcdefghijklmnop.supabase.co
   ```

   **API Key** - Copy the `anon` `public` key (looks like):
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

### 4. Configure AADS Manager (2 minutes)

1. Navigate to your AADS program folder
2. Copy the `.env.example` file and rename it to `.env`
3. Open `.env` in a text editor
4. Fill in your credentials:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-here

# Optional: Enable automatic sync after every change
AUTO_SYNC=false
```

5. Save the file

### 5. Install Required Python Packages (1 minute)

Open PowerShell in your AADS folder and run:

```powershell
pip install supabase python-dotenv
```

Or install all at once:
```powershell
pip install -r requirements.txt
```

### 6. Initialize Supabase Tables (3 minutes)

1. Run the AADS Manager: `python aads_manager.py`
2. Select option **11** (Cloud Sync)
3. Select option **5** (Initialize Supabase Tables)
4. You'll see SQL code displayed
5. Copy the entire SQL code
6. Go back to your Supabase dashboard
7. Click **SQL Editor** in the left sidebar
8. Click **New Query**
9. Paste the SQL code
10. Click **Run** (or press Ctrl+Enter)
11. You should see "Success. No rows returned"

### 7. Test Your Connection (1 minute)

1. Back in AADS Manager, select **4** (Test Connection)
2. You should see: "✓ Connection to Supabase is working!"

### 8. Perform Your First Backup (1 minute)

1. Select option **2** (Push to Cloud)
2. Type `yes` to confirm
3. Wait for sync to complete
4. You should see: "✓ Your data has been backed up to Supabase!"

🎉 **Setup Complete!** Your AADS data is now backed up to the cloud!

---

## Daily Usage

### Backup Your Data (Push to Cloud)

After making changes to your AADS data:
1. Go to **Cloud Sync** menu (option 11)
2. Select **Push to Cloud** (option 2)
3. Confirm with `yes`

### Restore Data (Pull from Cloud)

To restore data on a new computer or after data loss:
1. Set up your `.env` file with credentials
2. Go to **Cloud Sync** menu
3. Select **Pull from Cloud** (option 3)
4. ⚠️ This will replace local data with cloud data
5. Confirm with `yes`

---

## Common Scenarios

### Scenario 1: Using AADS on Multiple Computers

**Computer 1 (Primary):**
1. Set up Supabase as described above
2. Work normally and push to cloud when done

**Computer 2 (Secondary):**
1. Install AADS Manager
2. Copy your `.env` file to the AADS folder
3. Run `python aads_manager.py`
4. Go to Cloud Sync → Pull from Cloud
5. Your data is now synced!

### Scenario 2: Disaster Recovery

**Lost your local database?**
1. Reinstall AADS Manager
2. Set up your `.env` file
3. Pull from Cloud
4. All your data is restored!

### Scenario 3: Regular Backups

**Best Practice:**
- Push to cloud after each event
- Set up automatic backups: Set `AUTO_SYNC=true` in `.env`
- Manual backup before major changes

---

## Viewing Your Data in Supabase

1. Log into Supabase dashboard
2. Click **Table Editor** in left sidebar
3. Browse your tables:
   - **players**: All your fighters
   - **events**: All 7 events
   - **event_participants**: Event rosters
   - **sync_metadata**: Last sync time

You can view, search, and filter data directly in the web interface!

---

## Troubleshooting

### "Supabase sync is not enabled"

**Solution:**
1. Check that `.env` file exists (not `.env.example`)
2. Verify credentials are correct
3. Run: `pip install supabase python-dotenv`

### "Could not connect to Supabase"

**Possible causes:**
- No internet connection
- Wrong credentials in `.env`
- Supabase project is paused (free tier inactive)
- Tables not initialized

**Solution:**
1. Check internet connection
2. Verify credentials match Supabase dashboard
3. Run Test Connection to see specific error
4. Initialize tables if not done yet

### "Table doesn't exist" error

**Solution:**
Run the Initialize Supabase Tables option and execute the SQL in Supabase SQL Editor.

### Sync is slow

**Why?**
Supabase free tier has rate limits. Syncing 50+ players + events may take 10-30 seconds.

**Solution:**
This is normal. Wait for sync to complete. Consider upgrading to Pro tier if you need faster syncs.

---

## Security Notes

### Is My Data Safe?

✅ **Encrypted in Transit**: All data sent using HTTPS/TLS  
✅ **Access Control**: Only you have the credentials  
✅ **PostgreSQL**: Industry-standard database  
✅ **Automatic Backups**: Supabase backs up your database daily  

### Protecting Your Credentials

⚠️ **Never share your `.env` file publicly**  
⚠️ **Don't commit `.env` to GitHub**  
⚠️ **Keep your API key secret**  

The `.env` file is listed in `.gitignore` to prevent accidental commits.

### Row Level Security (RLS)

The setup SQL includes basic RLS policies. For production use with multiple users, you should:
1. Create separate API keys per user
2. Implement proper RLS policies
3. Use Supabase Auth for user management

---

## Upgrading from Free to Pro

If you need more:
- **Storage**: Free = 500MB, Pro = 8GB
- **Bandwidth**: Free = 2GB, Pro = 50GB
- **Backup Retention**: Free = 7 days, Pro = 30 days

Visit Supabase dashboard → Settings → Billing to upgrade.

---

## Cost Breakdown

### Free Tier (Forever Free)
- 500MB database space
- 2GB bandwidth per month
- Unlimited API requests
- Perfect for AADS with 100-200 players

### Pro Tier ($25/month)
- 8GB database space
- 50GB bandwidth per month
- Daily backups retained for 30 days
- Point-in-time recovery

For AADS use case, **Free Tier is more than sufficient** for years of tournament data!

---

## FAQ

**Q: Do I need internet to use AADS?**  
A: No! AADS works offline with local SQLite database. Supabase sync is optional for cloud backup.

**Q: Can I disable Supabase after setting it up?**  
A: Yes! Simply delete or rename your `.env` file. AADS will work normally without cloud sync.

**Q: What happens if I exceed free tier limits?**  
A: Supabase will notify you. Your project will be paused, but data is safe. Upgrade or wait for monthly reset.

**Q: Can multiple people use the same Supabase project?**  
A: Yes! Share the `.env` file securely. But be careful - whoever pushes last overwrites previous changes.

**Q: Does AUTO_SYNC slow down the program?**  
A: Yes, slightly. Each change takes 1-2 seconds to sync. Recommended for reliable internet only.

**Q: Can I export my Supabase data?**  
A: Yes! Use Supabase dashboard → Database → Backups or export tables as CSV.

---

## Getting Help

- **Supabase Docs**: [https://supabase.com/docs](https://supabase.com/docs)
- **AADS Issues**: Check your local setup first, then database file
- **Support**: Supabase has excellent community support on Discord

---

**You're all set!** Enjoy peace of mind knowing your AADS tournament data is safely backed up to the cloud. 🎉
