"""
AADS Series Manager - Main Program Interface
Atlantic Armwrestling Development Series Management System
"""

from aads_database import AADSDatabase
from typing import Optional
import os

class AADSManager:
    def __init__(self):
        self.db = AADSDatabase()
    
    def clear_screen(self):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str):
        """Print a formatted header."""
        print("\n" + "="*70)
        print(f"  {title}")
        print("="*70 + "\n")
    
    def print_player_table(self, players: list, show_events: bool = True):
        """Print players in a formatted table."""
        if not players:
            print("  No players found.")
            return
        
        if show_events:
            print(f"{'Name':<25} {'Province':<10} {'Status':<15} {'Events':<8} {'TOC':<5}")
            print("-" * 70)
            for player in players:
                toc = "✓" if player.get('toc_qualified', 0) else ""
                print(f"{player['name']:<25} {player['province']:<10} {player['status']:<15} "
                      f"{player.get('total_events', 0):<8} {toc:<5}")
        else:
            print(f"{'Name':<25} {'Province':<10} {'Status':<15}")
            print("-" * 50)
            for player in players:
                print(f"{player['name']:<25} {player['province']:<10} {player['status']:<15}")
    
    def print_event_roster(self, event_id: int):
        """Print the roster for a specific event."""
        event = self.db.get_event_details(event_id)
        if not event:
            print(f"Event {event_id} not found!")
            return
        
        self.print_header(event['name'])
        print(f"Status: {event['status']}")
        if event['winner_name']:
            print(f"Winner: {event['winner_name']}")
        print(f"Participants: {event['participant_count']}/10\n")
        
        roster = self.db.get_event_roster(event_id)
        if roster:
            print(f"{'Name':<25} {'Province':<10} {'Status':<12} {'Type':<10}")
            print("-" * 57)
            for player in roster:
                player_type = "DEBUT" if player['is_debut'] else "VETERAN"
                print(f"{player['name']:<25} {player['province']:<10} "
                      f"{player['status']:<12} {player_type:<10}")
        else:
            print("  No participants yet.")
    
    def view_master_list(self):
        """Display the master scouting list with sorting options."""
        while True:
            self.print_header("MASTER SCOUTING LIST")
            print("Sort Options:")
            print("  1. By Name (A-Z)")
            print("  2. By Province")
            print("  3. By Participation (Most Active)")
            print("  4. By Status")
            print("  5. Back to Main Menu")
            
            choice = input("\nSelect sorting option: ").strip()
            
            sort_map = {
                '1': 'name',
                '2': 'province',
                '3': 'participation',
                '4': 'status'
            }
            
            if choice == '5':
                break
            elif choice in sort_map:
                self.clear_screen()
                sort_by = sort_map[choice]
                players = self.db.get_all_players(sort_by=sort_by)
                
                self.print_header(f"All Players (Sorted by {sort_by.title()})")
                print(f"Total Players: {len(players)}\n")
                self.print_player_table(players)
                
                input("\nPress Enter to continue...")
                self.clear_screen()
    
    def view_by_province(self):
        """View players filtered by province."""
        while True:
            self.print_header("VIEW BY PROVINCE")
            print("Select Province:")
            print("  1. New Brunswick (NB)")
            print("  2. Nova Scotia (NS)")
            print("  3. Prince Edward Island (PEI)")
            print("  4. Back to Main Menu")
            
            choice = input("\nSelect province: ").strip()
            
            province_map = {'1': 'NB', '2': 'NS', '3': 'PEI'}
            
            if choice == '4':
                break
            elif choice in province_map:
                self.clear_screen()
                province = province_map[choice]
                players = self.db.get_players_by_province(province)
                
                province_names = {'NB': 'New Brunswick', 'NS': 'Nova Scotia', 'PEI': 'Prince Edward Island'}
                self.print_header(f"{province_names[province]} Players")
                print(f"Total: {len(players)} players\n")
                self.print_player_table(players)
                
                input("\nPress Enter to continue...")
                self.clear_screen()
    
    def view_invite_candidates(self):
        """Show players who didn't participate in the most recent event."""
        self.clear_screen()
        self.print_header("INVITE CANDIDATES - Players Not in Most Recent Event")
        
        # Find the most recent completed event
        recent_event = 5  # Event 5 is the most recent completed
        
        candidates = self.db.get_players_not_in_event(recent_event)
        
        print(f"Players who did NOT participate in Event {recent_event}:")
        print(f"Total Candidates: {len(candidates)}\n")
        self.print_player_table(candidates)
        
        input("\nPress Enter to continue...")
    
    def view_prospects(self):
        """Show all prospects (players with 0 events)."""
        self.clear_screen()
        self.print_header("PROSPECTS - Players Who Have Never Competed")
        
        prospects = self.db.get_prospects()
        print(f"Total Prospects: {len(prospects)}\n")
        self.print_player_table(prospects, show_events=False)
        
        input("\nPress Enter to continue...")
    
    def view_all_events(self):
        """Display summary of all events."""
        self.clear_screen()
        self.print_header("ALL EVENTS SUMMARY")
        
        events = self.db.get_all_events_summary()
        
        print(f"{'ID':<5} {'Event Name':<35} {'Status':<12} {'Participants':<15} {'Winner':<20}")
        print("-" * 95)
        
        for event in events:
            winner = event['winner_name'] if event['winner_name'] else "TBD"
            print(f"{event['id']:<5} {event['name']:<35} {event['status']:<12} "
                  f"{event['participant_count']:<15} {winner:<20}")
        
        input("\nPress Enter to continue...")
    
    def view_specific_event(self):
        """View roster for a specific event."""
        self.clear_screen()
        self.print_header("VIEW EVENT ROSTER")
        
        event_id = input("Enter event number (1-7): ").strip()
        
        try:
            event_id = int(event_id)
            if 1 <= event_id <= 7:
                self.clear_screen()
                self.print_event_roster(event_id)
                input("\nPress Enter to continue...")
            else:
                print("Invalid event number. Must be 1-7.")
                input("Press Enter to continue...")
        except ValueError:
            print("Please enter a valid number.")
            input("Press Enter to continue...")
    
    def add_player_to_event(self):
        """Add a player to an event roster."""
        self.clear_screen()
        self.print_header("ADD PLAYER TO EVENT")
        
        event_id = input("Enter event number (1-7): ").strip()
        
        try:
            event_id = int(event_id)
            if not (1 <= event_id <= 7):
                print("Invalid event number. Must be 1-7.")
                input("Press Enter to continue...")
                return
            
            # Check if event 7 (TOC)
            if event_id == 7:
                print("\nEvent 7 is the Tournament of Champions.")
                print("Players are automatically added when they win Events 1-6.")
                input("Press Enter to continue...")
                return
            
            # Show current roster
            event = self.db.get_event_details(event_id)
            print(f"\nEvent: {event['name']}")
            print(f"Current participants: {event['participant_count']}/10\n")
            
            if event['participant_count'] >= 10:
                print("This event is already full (10 players)!")
                input("Press Enter to continue...")
                return
            
            player_name = input("Enter player name: ").strip()
            
            print("\nSelect province:")
            print("  1. New Brunswick (NB)")
            print("  2. Nova Scotia (NS)")
            print("  3. Prince Edward Island (PEI)")
            
            province_choice = input("Select province (1-3): ").strip()
            province_map = {'1': 'NB', '2': 'NS', '3': 'PEI'}
            
            if province_choice in province_map:
                province = province_map[province_choice]
                self.db.add_player_to_event(event_id, player_name, province)
                print(f"\n✓ {player_name} ({province}) added to Event {event_id}!")
                input("Press Enter to continue...")
            else:
                print("Invalid province selection.")
                input("Press Enter to continue...")
                
        except ValueError:
            print("Please enter a valid number.")
            input("Press Enter to continue...")
    
    def set_event_winner(self):
        """Set the winner for an event."""
        self.clear_screen()
        self.print_header("SET EVENT WINNER")
        
        event_id = input("Enter event number (1-6): ").strip()
        
        try:
            event_id = int(event_id)
            if not (1 <= event_id <= 6):
                print("Invalid event number. Winners can only be set for Events 1-6.")
                input("Press Enter to continue...")
                return
            
            # Show event roster
            self.print_event_roster(event_id)
            
            player_name = input("\nEnter winner's name (exactly as shown above): ").strip()
            
            confirm = input(f"\nSet {player_name} as winner of Event {event_id}? (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                success = self.db.set_event_winner(event_id, player_name)
                if success:
                    print(f"\n✓ {player_name} is now the winner of Event {event_id}!")
                    print(f"✓ {player_name} has been automatically added to the Tournament of Champions!")
                else:
                    print("\nError setting winner. Please check the player name.")
                input("Press Enter to continue...")
            else:
                print("Cancelled.")
                input("Press Enter to continue...")
                
        except ValueError:
            print("Please enter a valid number.")
            input("Press Enter to continue...")
    
    def view_player_history(self):
        """View complete history for a specific player."""
        self.clear_screen()
        self.print_header("PLAYER HISTORY")
        
        player_name = input("Enter player name: ").strip()
        
        history = self.db.get_player_history(player_name)
        
        if not history:
            print(f"\nPlayer '{player_name}' not found in database.")
            input("Press Enter to continue...")
            return
        
        self.clear_screen()
        self.print_header(f"Player Profile: {history['name']}")
        
        print(f"Province: {history['province']}")
        print(f"Status: {history['status']}")
        print(f"Total Events: {history['total_events']}")
        print(f"TOC Qualified: {'Yes' if history['toc_qualified'] else 'No'}")
        
        if history['events']:
            print(f"\nEvent History:")
            print(f"{'Event':<35} {'Type':<10} {'Won':<10}")
            print("-" * 55)
            for event in history['events']:
                event_type = "DEBUT" if event['is_debut'] else "VETERAN"
                won = "✓ WINNER" if event['won_event'] else ""
                print(f"{event['name']:<35} {event_type:<10} {won:<10}")
        else:
            print("\nNo event history (Prospect)")
        
        input("\nPress Enter to continue...")
    
    def view_sync_status(self):
        """Display Supabase sync status."""
        self.clear_screen()
        self.print_header("SUPABASE CLOUD SYNC STATUS")
        
        status = self.db.get_sync_status()
        
        print(f"Cloud Sync: {'✓ ENABLED' if status['enabled'] else '✗ DISABLED'}")
        print(f"Message: {status['message']}")
        
        if status['enabled']:
            print(f"Auto-Sync: {'ON' if status.get('auto_sync') else 'OFF'}")
            if status['last_sync']:
                print(f"Last Sync: {status['last_sync']}")
            else:
                print("Last Sync: Never")
        
        print("\nWhat is Supabase Sync?")
        print("  - Backs up your data to the cloud")
        print("  - Access your data from anywhere")
        print("  - Automatic disaster recovery")
        print("  - Share data across multiple devices")
        
        if not status['enabled']:
            print("\nTo enable Supabase sync:")
            print("  1. Create a free account at supabase.com")
            print("  2. Create a new project")
            print("  3. Copy .env.example to .env")
            print("  4. Add your Supabase URL and Key to .env")
            print("  5. Run 'Initialize Supabase Tables' from the sync menu")
        
        input("\nPress Enter to continue...")
    
    def sync_to_cloud(self):
        """Sync local database to Supabase cloud."""
        self.clear_screen()
        self.print_header("SYNC TO CLOUD")
        
        status = self.db.get_sync_status()
        if not status['enabled']:
            print("❌ Supabase sync is not enabled.")
            print("\nPlease configure Supabase first (see Sync Status for instructions).")
            input("\nPress Enter to continue...")
            return
        
        print("This will upload all local data to Supabase cloud.")
        confirm = input("Continue? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            print()
            success = self.db.sync_to_cloud()
            if success:
                print("\n✓ Your data has been backed up to Supabase!")
            else:
                print("\n❌ Sync failed. Check your connection and credentials.")
            input("\nPress Enter to continue...")
        else:
            print("Sync cancelled.")
            input("Press Enter to continue...")
    
    def pull_from_cloud(self):
        """Pull data from Supabase cloud to local database."""
        self.clear_screen()
        self.print_header("PULL FROM CLOUD")
        
        status = self.db.get_sync_status()
        if not status['enabled']:
            print("❌ Supabase sync is not enabled.")
            print("\nPlease configure Supabase first (see Sync Status for instructions).")
            input("\nPress Enter to continue...")
            return
        
        print("⚠️  WARNING: This will REPLACE your local data with cloud data!")
        print("Make sure you've backed up any local changes you want to keep.")
        print()
        confirm = input("Are you sure you want to continue? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            print()
            success = self.db.pull_from_cloud()
            if success:
                print("\n✓ Local database updated with cloud data!")
            else:
                print("\n❌ Pull failed. Check your connection and credentials.")
            input("\nPress Enter to continue...")
        else:
            print("Pull cancelled.")
            input("Press Enter to continue...")
    
    def test_cloud_connection(self):
        """Test connection to Supabase."""
        self.clear_screen()
        self.print_header("TEST CLOUD CONNECTION")
        
        print("Testing connection to Supabase...")
        print()
        
        success = self.db.test_cloud_connection()
        
        if success:
            print("\n✓ Connection to Supabase is working!")
        else:
            print("\n❌ Could not connect to Supabase.")
            print("\nCheck that:")
            print("  - Your .env file exists with correct credentials")
            print("  - Your Supabase project is active")
            print("  - You have internet connection")
            print("  - The tables are initialized in Supabase")
        
        input("\nPress Enter to continue...")
    
    def initialize_supabase_tables(self):
        """Initialize tables in Supabase."""
        self.clear_screen()
        self.print_header("INITIALIZE SUPABASE TABLES")
        
        if not self.db.supabase or not self.db.supabase.enabled:
            print("❌ Supabase is not configured.")
            print("\nPlease set up your .env file first.")
            input("\nPress Enter to continue...")
            return
        
        print("This will show you the SQL needed to create tables in Supabase.")
        print("You'll need to run this SQL in your Supabase SQL Editor.")
        print()
        confirm = input("Continue? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            self.db.supabase.initialize_tables()
        else:
            print("Cancelled.")
            input("Press Enter to continue...")
    
    def cloud_sync_menu(self):
        """Display cloud sync submenu."""
        while True:
            self.clear_screen()
            self.print_header("CLOUD SYNC - SUPABASE BACKUP")
            
            status = self.db.get_sync_status()
            
            print(f"Status: {'✓ Connected' if status['enabled'] else '✗ Not Configured'}")
            if status['enabled'] and status['last_sync']:
                print(f"Last Sync: {status['last_sync']}")
            print()
            
            print("SYNC OPTIONS:")
            print("  1. View Sync Status")
            print("  2. Push to Cloud (Backup)")
            print("  3. Pull from Cloud (Restore)")
            print("  4. Test Connection")
            print("  5. Initialize Supabase Tables")
            print()
            print("  0. Back to Main Menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == '1':
                self.view_sync_status()
            elif choice == '2':
                self.sync_to_cloud()
            elif choice == '3':
                self.pull_from_cloud()
            elif choice == '4':
                self.test_cloud_connection()
            elif choice == '5':
                self.initialize_supabase_tables()
            elif choice == '0':
                break
            else:
                print("Invalid option. Please try again.")
                input("Press Enter to continue...")
    
    def add_new_player(self):
        """Add a new player to the master list."""
        self.clear_screen()
        self.print_header("ADD NEW PLAYER TO MASTER LIST")
        
        player_name = input("Enter player name: ").strip()
        
        if not player_name:
            print("Player name cannot be empty.")
            input("Press Enter to continue...")
            return
        
        print("\nSelect province:")
        print("  1. New Brunswick (NB)")
        print("  2. Nova Scotia (NS)")
        print("  3. Prince Edward Island (PEI)")
        
        province_choice = input("Select province (1-3): ").strip()
        province_map = {'1': 'NB', '2': 'NS', '3': 'PEI'}
        
        if province_choice in province_map:
            province = province_map[province_choice]
            player_id = self.db.add_player(player_name, province)
            print(f"\n✓ {player_name} ({province}) added to Master Scouting List as a Prospect!")
            input("Press Enter to continue...")
        else:
            print("Invalid province selection.")
            input("Press Enter to continue...")
    
    def main_menu(self):
        """Display main menu and handle user input."""
        while True:
            self.clear_screen()
            self.print_header("AADS SERIES MANAGER - Atlantic Armwrestling Development Series")
            
            print("VIEWING OPTIONS:")
            print("  1.  View Master Scouting List (with sorting)")
            print("  2.  View by Province")
            print("  3.  View All Events Summary")
            print("  4.  View Specific Event Roster")
            print("  5.  View Invite Candidates (Not in Recent Event)")
            print("  6.  View Prospects (Never Competed)")
            print("  7.  View Player History")
            print()
            print("MANAGEMENT OPTIONS:")
            print("  8.  Add Player to Event")
            print("  9.  Set Event Winner")
            print("  10. Add New Player to Master List")
            print()
            print("CLOUD BACKUP:")
            print("  11. Cloud Sync (Supabase)")
            print()
            print("  0.  Exit Program")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == '1':
                self.view_master_list()
            elif choice == '2':
                self.view_by_province()
            elif choice == '3':
                self.view_all_events()
            elif choice == '4':
                self.view_specific_event()
            elif choice == '5':
                self.view_invite_candidates()
            elif choice == '6':
                self.view_prospects()
            elif choice == '7':
                self.view_player_history()
            elif choice == '8':
                self.add_player_to_event()
            elif choice == '9':
                self.set_event_winner()
            elif choice == '10':
                self.add_new_player()
            elif choice == '11':
                self.cloud_sync_menu()
            elif choice == '0':
                print("\nThank you for using AADS Series Manager!")
                break
            else:
                print("Invalid option. Please try again.")
                input("Press Enter to continue...")
    
    def close(self):
        """Close database connection."""
        self.db.close()

def main():
    """Main entry point for the AADS Manager."""
    manager = AADSManager()
    try:
        manager.main_menu()
    finally:
        manager.close()

if __name__ == "__main__":
    main()
