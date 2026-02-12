"""
Data Initialization Script for AADS Series
Loads the initial event data provided by the user
"""

from aads_database import AADSDatabase

def initialize_aads_data():
    """Initialize the database with all provided event data."""
    
    print("Initializing AADS Series Database...")
    
    db = AADSDatabase()
    
    # Initialize events
    print("Creating events...")
    db.initialize_events()
    
    # Event 1 Data
    print("\nLoading Event 1 participants...")
    event1_players = [
        ("Cory Wallace", "NB"),
        ("Steve Rushton", "NS"),
        ("Dee Cormier", "NB"),
        ("Royce Milliea", "NB"),
        ("Miguel Velasquez", "NB"),
        ("Gerry Johnston", "NB"),
        ("Tyler Stewart", "NB"),
        ("Tom Holden", "NS"),
        ("Denis Leblanc", "NB"),
        ("Micheal Léger", "NB")
    ]
    
    for name, province in event1_players:
        db.add_player_to_event(1, name, province)
        print(f"  Added: {name} ({province})")
    
    # Event 2 Data
    print("\nLoading Event 2 participants...")
    event2_players = [
        ("Dee Cormier", "NB"),
        ("Denis Leblanc", "NB"),
        ("Kyle Gray", "NB"),
        ("Tyler Cyr", "NB"),
        ("Tyler Stewart", "NB"),
        ("Micheal Léger", "NB"),
        ("Pitou Pellerin", "NB"),
        ("Tom Holden", "NS"),
        ("Corey O'Brien", "NS"),
        ("Steve Rushton", "NS")
    ]
    
    for name, province in event2_players:
        db.add_player_to_event(2, name, province)
        print(f"  Added: {name} ({province})")
    
    # Event 3 Data
    print("\nLoading Event 3 participants...")
    event3_players = [
        ("Tyler Cyr", "NB"),
        ("Kyle Gray", "NB"),
        ("Wayne Chapman", "NB"),
        ("Don Higgins", "NB"),
        ("Pitou Pellerin", "NB"),
        ("Zack Davis", "NB"),
        ("Drake Berry", "NS"),
        ("Jon Casey", "NS"),
        ("Ricky Chaisson", "PEI"),
        ("Mark MacEachern", "PEI")
    ]
    
    for name, province in event3_players:
        db.add_player_to_event(3, name, province)
        print(f"  Added: {name} ({province})")
    
    # Event 4 Data
    print("\nLoading Event 4 participants...")
    event4_players = [
        ("Kevin Blanchard", "PEI"),
        ("Mark MacEachern", "PEI"),
        ("Jordan Boyd", "NS"),
        ("Drake Berry", "NS"),
        ("Don Higgins", "NB"),
        ("Wayne Chapman", "NB"),
        ("Dana Moss", "NB"),
        ("Colby Burke", "NS"),
        ("Cory Wallace", "NB"),
        ("Dee Cormier", "NB")
    ]
    
    for name, province in event4_players:
        db.add_player_to_event(4, name, province)
        print(f"  Added: {name} ({province})")
    
    # Event 5 Data
    print("\nLoading Event 5 participants...")
    event5_players = [
        ("Arron Gilbert", "NS"),
        ("Corey O'Brien", "NS"),
        ("Steve Rushton", "NS"),
        ("Jon Casey", "NS"),
        ("Scott Ferdinand", "NS"),
        ("Chad Arsenault", "NB"),
        ("Denis Leblanc", "NB"),
        ("Tony Solomon", "NB"),
        ("Corey Lefort", "PEI"),
        ("Ricky Chaisson", "PEI")
    ]
    
    for name, province in event5_players:
        db.add_player_to_event(5, name, province)
        print(f"  Added: {name} ({province})")
    
    # Event 6 - Mark as Active (in progress)
    print("\nEvent 6 is marked as Active (in progress)")
    
    print("\n" + "="*60)
    print("Database initialization complete!")
    print("="*60)
    
    # Print summary statistics
    all_players = db.get_all_players()
    print(f"\nTotal Players in Database: {len(all_players)}")
    
    print("\nBreakdown by Province:")
    for province in ['NB', 'NS', 'PEI']:
        province_players = db.get_players_by_province(province)
        print(f"  {province}: {len(province_players)} players")
    
    print("\nEvent Summary:")
    events = db.get_all_events_summary()
    for event in events:
        print(f"  {event['name']}: {event['participant_count']} participants - Status: {event['status']}")
    
    db.close()
    print("\nReady to use! Run 'python aads_manager.py' to start managing the series.")

if __name__ == "__main__":
    initialize_aads_data()
