"""
AADS Series Database Module
Handles all database operations for the Atlantic Armwrestling Development Series
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

# Load environment variables if .env file exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, will use system environment variables

from supabase_sync import SupabaseSync

class AADSDatabase:
    def __init__(self, db_path: str = "aads_series.db", enable_sync: bool = True):
        """Initialize database connection and create tables if they don't exist."""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_tables()
        
        # Initialize Supabase sync
        self.supabase = SupabaseSync() if enable_sync else None
        self.auto_sync = os.getenv('AUTO_SYNC', 'false').lower() == 'true'
    
    def create_tables(self):
        """Create all necessary database tables."""
        
        # Players Master List
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                province TEXT NOT NULL CHECK(province IN ('NB', 'NS', 'PEI')),
                status TEXT DEFAULT 'Prospect' CHECK(status IN ('Prospect', 'Active', 'Winner', 'TOC Qualified')),
                total_events INTEGER DEFAULT 0,
                toc_qualified INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Events
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                event_type TEXT NOT NULL CHECK(event_type IN ('Invitational', 'TOC')),
                event_date TEXT,
                winner_id INTEGER,
                status TEXT DEFAULT 'Pending' CHECK(status IN ('Pending', 'Active', 'Completed')),
                FOREIGN KEY (winner_id) REFERENCES players(id)
            )
        """)
        
        # Event Participants (join table)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS event_participants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER NOT NULL,
                player_id INTEGER NOT NULL,
                is_debut INTEGER DEFAULT 0,
                is_veteran INTEGER DEFAULT 0,
                placement INTEGER,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (event_id) REFERENCES events(id),
                FOREIGN KEY (player_id) REFERENCES players(id),
                UNIQUE(event_id, player_id)
            )
        """)
        
        self.conn.commit()
    
    def initialize_events(self):
        """Initialize the 7 events in the series."""
        events = [
            (1, "Event 1 - Invitational", "Invitational", None, "Completed"),
            (2, "Event 2 - Invitational", "Invitational", None, "Completed"),
            (3, "Event 3 - Invitational", "Invitational", None, "Completed"),
            (4, "Event 4 - Invitational", "Invitational", None, "Completed"),
            (5, "Event 5 - Invitational", "Invitational", None, "Completed"),
            (6, "Event 6 - Invitational", "Invitational", None, "Active"),
            (7, "Event 7 - Tournament of Champions", "TOC", None, "Pending")
        ]
        
        for event in events:
            self.cursor.execute("""
                INSERT OR IGNORE INTO events (id, name, event_type, event_date, status)
                VALUES (?, ?, ?, ?, ?)
            """, event)
        
        self.conn.commit()
    
    def add_player(self, name: str, province: str) -> int:
        """Add a new player to the master list."""
        try:
            self.cursor.execute("""
                INSERT INTO players (name, province, status)
                VALUES (?, ?, 'Prospect')
            """, (name, province))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            # Player already exists, return their id
            self.cursor.execute("SELECT id FROM players WHERE name = ?", (name,))
            return self.cursor.fetchone()[0]
    
    def get_or_create_player(self, name: str, province: str) -> int:
        """Get player ID or create if doesn't exist."""
        self.cursor.execute("SELECT id FROM players WHERE name = ?", (name,))
        result = self.cursor.fetchone()
        
        if result:
            return result[0]
        else:
            return self.add_player(name, province)
    
    def add_player_to_event(self, event_id: int, player_name: str, province: str):
        """Add a player to an event roster."""
        # Get or create player
        player_id = self.get_or_create_player(player_name, province)
        
        # Check if this is their debut
        self.cursor.execute("""
            SELECT COUNT(*) as event_count 
            FROM event_participants 
            WHERE player_id = ?
        """, (player_id,))
        
        previous_events = self.cursor.fetchone()[0]
        is_debut = 1 if previous_events == 0 else 0
        is_veteran = 0 if previous_events == 0 else 1
        
        # Add to event
        try:
            self.cursor.execute("""
                INSERT INTO event_participants (event_id, player_id, is_debut, is_veteran)
                VALUES (?, ?, ?, ?)
            """, (event_id, player_id, is_debut, is_veteran))
            
            # Update player status and event count
            self.cursor.execute("""
                UPDATE players 
                SET status = CASE 
                    WHEN status = 'Prospect' THEN 'Active'
                    ELSE status
                END,
                total_events = (SELECT COUNT(DISTINCT event_id) FROM event_participants WHERE player_id = ?),
                updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (player_id, player_id))
            
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"Player {player_name} is already in Event {event_id}")
    
    def set_event_winner(self, event_id: int, player_name: str):
        """Mark a player as the winner of an event."""
        # Get player ID
        self.cursor.execute("SELECT id FROM players WHERE name = ?", (player_name,))
        result = self.cursor.fetchone()
        
        if not result:
            print(f"Player {player_name} not found!")
            return False
        
        player_id = result[0]
        
        # Update event winner
        self.cursor.execute("""
            UPDATE events 
            SET winner_id = ?, status = 'Completed'
            WHERE id = ?
        """, (player_id, event_id))
        
        # Update player status
        self.cursor.execute("""
            UPDATE players 
            SET status = 'Winner', toc_qualified = 1
            WHERE id = ?
        """, (player_id,))
        
        # Add winner to TOC (Event 7) automatically
        if event_id != 7:
            try:
                self.cursor.execute("""
                    INSERT INTO event_participants (event_id, player_id, is_veteran)
                    VALUES (7, ?, 1)
                """, (player_id,))
            except sqlite3.IntegrityError:
                pass  # Already in TOC
        
        self.conn.commit()
        return True
    
    def get_event_roster(self, event_id: int) -> List[Dict]:
        """Get all players in an event roster."""
        self.cursor.execute("""
            SELECT 
                p.name,
                p.province,
                p.status,
                p.total_events,
                ep.is_debut,
                ep.is_veteran,
                ep.placement
            FROM event_participants ep
            JOIN players p ON ep.player_id = p.id
            WHERE ep.event_id = ?
            ORDER BY p.name
        """, (event_id,))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_all_players(self, sort_by: str = "name") -> List[Dict]:
        """Get all players from master list."""
        valid_sorts = {
            "name": "name",
            "province": "province, name",
            "participation": "total_events DESC, name",
            "status": "status, name"
        }
        
        order_clause = valid_sorts.get(sort_by, "name")
        
        query = f"""
            SELECT 
                id,
                name,
                province,
                status,
                total_events,
                toc_qualified,
                created_at
            FROM players
            ORDER BY {order_clause}
        """
        
        self.cursor.execute(query)
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_players_by_province(self, province: str) -> List[Dict]:
        """Get all players from a specific province."""
        self.cursor.execute("""
            SELECT 
                id,
                name,
                province,
                status,
                total_events,
                toc_qualified
            FROM players
            WHERE province = ?
            ORDER BY name
        """, (province,))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_players_not_in_event(self, event_id: int) -> List[Dict]:
        """Get players who did NOT participate in a specific event."""
        self.cursor.execute("""
            SELECT 
                p.id,
                p.name,
                p.province,
                p.status,
                p.total_events
            FROM players p
            WHERE p.id NOT IN (
                SELECT player_id 
                FROM event_participants 
                WHERE event_id = ?
            )
            AND p.total_events > 0
            ORDER BY p.province, p.total_events DESC
        """, (event_id,))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_prospects(self) -> List[Dict]:
        """Get all players who have never competed (prospects)."""
        self.cursor.execute("""
            SELECT 
                id,
                name,
                province,
                status
            FROM players
            WHERE total_events = 0
            ORDER BY province, name
        """)
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_event_details(self, event_id: int) -> Optional[Dict]:
        """Get details about a specific event."""
        self.cursor.execute("""
            SELECT 
                e.id,
                e.name,
                e.event_type,
                e.status,
                e.event_date,
                p.name as winner_name,
                (SELECT COUNT(*) FROM event_participants WHERE event_id = e.id) as participant_count
            FROM events e
            LEFT JOIN players p ON e.winner_id = p.id
            WHERE e.id = ?
        """, (event_id,))
        
        result = self.cursor.fetchone()
        return dict(result) if result else None
    
    def get_all_events_summary(self) -> List[Dict]:
        """Get summary of all events."""
        self.cursor.execute("""
            SELECT 
                e.id,
                e.name,
                e.event_type,
                e.status,
                p.name as winner_name,
                (SELECT COUNT(*) FROM event_participants WHERE event_id = e.id) as participant_count
            FROM events e
            LEFT JOIN players p ON e.winner_id = p.id
            ORDER BY e.id
        """)
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_player_history(self, player_name: str) -> Dict:
        """Get complete history for a specific player."""
        self.cursor.execute("""
            SELECT 
                p.id,
                p.name,
                p.province,
                p.status,
                p.total_events,
                p.toc_qualified
            FROM players p
            WHERE p.name = ?
        """, (player_name,))
        
        player = self.cursor.fetchone()
        if not player:
            return None
        
        player_dict = dict(player)
        
        # Get events participated in
        self.cursor.execute("""
            SELECT 
                e.id,
                e.name,
                ep.is_debut,
                e.winner_id = p.id as won_event
            FROM event_participants ep
            JOIN events e ON ep.event_id = e.id
            JOIN players p ON ep.player_id = p.id
            WHERE p.name = ?
            ORDER BY e.id
        """, (player_name,))
        
        player_dict['events'] = [dict(row) for row in self.cursor.fetchall()]
        
        return player_dict
    
    def sync_to_cloud(self) -> bool:
        """Sync local database to Supabase cloud."""
        if self.supabase and self.supabase.enabled:
            return self.supabase.full_sync_to_cloud(self)
        return False
    
    def pull_from_cloud(self) -> bool:
        """Pull data from Supabase cloud to local database."""
        if self.supabase and self.supabase.enabled:
            return self.supabase.pull_from_cloud(self)
        return False
    
    def test_cloud_connection(self) -> bool:
        """Test connection to Supabase."""
        if self.supabase and self.supabase.enabled:
            return self.supabase.test_connection()
        return False
    
    def get_sync_status(self) -> Dict:
        """Get sync status information."""
        if not self.supabase or not self.supabase.enabled:
            return {
                'enabled': False,
                'last_sync': None,
                'message': 'Supabase sync not configured'
            }
        
        last_sync = self.supabase.get_last_sync_time()
        return {
            'enabled': True,
            'last_sync': last_sync,
            'auto_sync': self.auto_sync,
            'message': 'Connected to Supabase'
        }
    
    def close(self):
        """Close database connection."""
        self.conn.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
