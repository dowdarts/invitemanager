"""
Supabase Sync Module for AADS Series
Handles cloud backup and synchronization with Supabase
"""

import os
import json
from typing import Dict, List, Optional
from datetime import datetime

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    print("Warning: supabase-py not installed. Cloud sync disabled.")
    print("Install with: pip install supabase")


class SupabaseSync:
    def __init__(self, url: Optional[str] = None, key: Optional[str] = None):
        """Initialize Supabase connection."""
        self.client: Optional[Client] = None
        self.enabled = False
        
        if not SUPABASE_AVAILABLE:
            print("Supabase sync is disabled - supabase-py package not installed.")
            return
        
        # Try to get credentials from parameters or environment
        self.url = url or os.getenv('SUPABASE_URL')
        self.key = key or os.getenv('SUPABASE_KEY')
        
        if self.url and self.key:
            try:
                self.client = create_client(self.url, self.key)
                self.enabled = True
                print("✓ Supabase connection established")
            except Exception as e:
                print(f"Failed to connect to Supabase: {e}")
                self.enabled = False
        else:
            print("Supabase credentials not found. Cloud sync disabled.")
            print("Set SUPABASE_URL and SUPABASE_KEY in .env file or environment variables.")
    
    def initialize_tables(self) -> bool:
        """Create tables in Supabase if they don't exist."""
        if not self.enabled:
            return False
        
        print("\nInitializing Supabase tables...")
        print("Please run the following SQL in your Supabase SQL Editor:\n")
        
        sql = """
-- AADS Series Database Schema for Supabase

-- Players table
CREATE TABLE IF NOT EXISTS players (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    province TEXT NOT NULL CHECK(province IN ('NB', 'NS', 'PEI')),
    status TEXT DEFAULT 'Prospect' CHECK(status IN ('Prospect', 'Active', 'Winner', 'TOC Qualified')),
    total_events INTEGER DEFAULT 0,
    toc_qualified BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Events table
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    event_type TEXT NOT NULL CHECK(event_type IN ('Invitational', 'TOC')),
    event_date TEXT,
    winner_id BIGINT REFERENCES players(id),
    status TEXT DEFAULT 'Pending' CHECK(status IN ('Pending', 'Active', 'Completed'))
);

-- Event Participants table
CREATE TABLE IF NOT EXISTS event_participants (
    id BIGSERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(id),
    player_id BIGINT NOT NULL REFERENCES players(id),
    is_debut BOOLEAN DEFAULT false,
    is_veteran BOOLEAN DEFAULT false,
    placement INTEGER,
    added_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(event_id, player_id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_players_province ON players(province);
CREATE INDEX IF NOT EXISTS idx_players_status ON players(status);
CREATE INDEX IF NOT EXISTS idx_event_participants_event ON event_participants(event_id);
CREATE INDEX IF NOT EXISTS idx_event_participants_player ON event_participants(player_id);

-- Enable Row Level Security (RLS)
ALTER TABLE players ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE event_participants ENABLE ROW LEVEL SECURITY;

-- Create policies (adjust based on your security needs)
-- For development/testing - allow all operations
CREATE POLICY "Allow all operations on players" ON players FOR ALL USING (true);
CREATE POLICY "Allow all operations on events" ON events FOR ALL USING (true);
CREATE POLICY "Allow all operations on event_participants" ON event_participants FOR ALL USING (true);

-- Last sync tracking table
CREATE TABLE IF NOT EXISTS sync_metadata (
    id INTEGER PRIMARY KEY DEFAULT 1,
    last_sync TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    local_changes INTEGER DEFAULT 0,
    CHECK (id = 1)
);

INSERT INTO sync_metadata (id) VALUES (1) ON CONFLICT (id) DO NOTHING;
"""
        
        print(sql)
        print("\n" + "="*70)
        print("After running this SQL, press Enter to continue...")
        input()
        return True
    
    def sync_players_to_cloud(self, players: List[Dict]) -> bool:
        """Push players data to Supabase."""
        if not self.enabled:
            return False
        
        try:
            print(f"Syncing {len(players)} players to Supabase...")
            
            for player in players:
                # Convert SQLite format to Supabase format
                player_data = {
                    'id': player['id'],
                    'name': player['name'],
                    'province': player['province'],
                    'status': player['status'],
                    'total_events': player['total_events'],
                    'toc_qualified': bool(player['toc_qualified'])
                }
                
                # Upsert (insert or update)
                self.client.table('players').upsert(player_data).execute()
            
            print(f"✓ Synced {len(players)} players")
            return True
            
        except Exception as e:
            print(f"Error syncing players: {e}")
            return False
    
    def sync_events_to_cloud(self, events: List[Dict]) -> bool:
        """Push events data to Supabase."""
        if not self.enabled:
            return False
        
        try:
            print(f"Syncing {len(events)} events to Supabase...")
            
            for event in events:
                event_data = {
                    'id': event['id'],
                    'name': event['name'],
                    'event_type': event['event_type'],
                    'event_date': event.get('event_date'),
                    'winner_id': event.get('winner_id'),
                    'status': event['status']
                }
                
                self.client.table('events').upsert(event_data).execute()
            
            print(f"✓ Synced {len(events)} events")
            return True
            
        except Exception as e:
            print(f"Error syncing events: {e}")
            return False
    
    def sync_participants_to_cloud(self, participants: List[Dict]) -> bool:
        """Push event participants data to Supabase."""
        if not self.enabled:
            return False
        
        try:
            print(f"Syncing {len(participants)} event participants to Supabase...")
            
            for participant in participants:
                participant_data = {
                    'id': participant['id'],
                    'event_id': participant['event_id'],
                    'player_id': participant['player_id'],
                    'is_debut': bool(participant['is_debut']),
                    'is_veteran': bool(participant['is_veteran']),
                    'placement': participant.get('placement')
                }
                
                self.client.table('event_participants').upsert(participant_data).execute()
            
            print(f"✓ Synced {len(participants)} participants")
            return True
            
        except Exception as e:
            print(f"Error syncing participants: {e}")
            return False
    
    def full_sync_to_cloud(self, db) -> bool:
        """Perform a complete sync of all data to Supabase."""
        if not self.enabled:
            print("Supabase sync is not enabled.")
            return False
        
        print("\n" + "="*70)
        print("SYNCING LOCAL DATABASE TO SUPABASE")
        print("="*70 + "\n")
        
        try:
            # Get all data from local database
            db.cursor.execute("SELECT * FROM players")
            players = [dict(row) for row in db.cursor.fetchall()]
            
            db.cursor.execute("SELECT * FROM events")
            events = [dict(row) for row in db.cursor.fetchall()]
            
            db.cursor.execute("SELECT * FROM event_participants")
            participants = [dict(row) for row in db.cursor.fetchall()]
            
            # Sync to cloud
            success = True
            success &= self.sync_players_to_cloud(players)
            success &= self.sync_events_to_cloud(events)
            success &= self.sync_participants_to_cloud(participants)
            
            if success:
                # Update sync metadata
                self.client.table('sync_metadata').update({
                    'last_sync': datetime.now().isoformat(),
                    'local_changes': 0
                }).eq('id', 1).execute()
                
                print("\n" + "="*70)
                print("✓ FULL SYNC COMPLETED SUCCESSFULLY")
                print("="*70)
            
            return success
            
        except Exception as e:
            print(f"\n❌ Sync failed: {e}")
            return False
    
    def pull_from_cloud(self, db) -> bool:
        """Pull data from Supabase to local database."""
        if not self.enabled:
            print("Supabase sync is not enabled.")
            return False
        
        print("\n" + "="*70)
        print("PULLING DATA FROM SUPABASE TO LOCAL DATABASE")
        print("="*70 + "\n")
        
        try:
            # Fetch all data from Supabase
            players_response = self.client.table('players').select('*').execute()
            events_response = self.client.table('events').select('*').execute()
            participants_response = self.client.table('event_participants').select('*').execute()
            
            players = players_response.data
            events = events_response.data
            participants = participants_response.data
            
            print(f"Retrieved {len(players)} players from cloud")
            print(f"Retrieved {len(events)} events from cloud")
            print(f"Retrieved {len(participants)} participants from cloud")
            
            # Clear local database and insert cloud data
            print("\nUpdating local database...")
            
            # Players
            for player in players:
                db.cursor.execute("""
                    INSERT OR REPLACE INTO players 
                    (id, name, province, status, total_events, toc_qualified, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    player['id'], player['name'], player['province'], player['status'],
                    player['total_events'], 1 if player['toc_qualified'] else 0,
                    player.get('created_at'), player.get('updated_at')
                ))
            
            # Events
            for event in events:
                db.cursor.execute("""
                    INSERT OR REPLACE INTO events 
                    (id, name, event_type, event_date, winner_id, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    event['id'], event['name'], event['event_type'],
                    event.get('event_date'), event.get('winner_id'), event['status']
                ))
            
            # Participants
            for participant in participants:
                db.cursor.execute("""
                    INSERT OR REPLACE INTO event_participants 
                    (id, event_id, player_id, is_debut, is_veteran, placement, added_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    participant['id'], participant['event_id'], participant['player_id'],
                    1 if participant['is_debut'] else 0,
                    1 if participant['is_veteran'] else 0,
                    participant.get('placement'), participant.get('added_at')
                ))
            
            db.conn.commit()
            
            print("\n" + "="*70)
            print("✓ DATA PULLED FROM CLOUD SUCCESSFULLY")
            print("="*70)
            return True
            
        except Exception as e:
            print(f"\n❌ Pull failed: {e}")
            db.conn.rollback()
            return False
    
    def get_last_sync_time(self) -> Optional[str]:
        """Get the timestamp of the last sync."""
        if not self.enabled:
            return None
        
        try:
            response = self.client.table('sync_metadata').select('last_sync').eq('id', 1).execute()
            if response.data:
                return response.data[0]['last_sync']
        except:
            pass
        return None
    
    def test_connection(self) -> bool:
        """Test the Supabase connection."""
        if not self.enabled:
            return False
        
        try:
            # Try to query the players table
            response = self.client.table('players').select('count', count='exact').execute()
            print(f"✓ Connection successful! Found {response.count} players in cloud.")
            return True
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False
