"""
Quick Start Script for AADS Series Manager
This script checks if the database exists and guides you through setup.
"""

import os
import sys

def check_database_exists():
    """Check if the database file exists."""
    return os.path.exists("aads_series.db")

def main():
    print("="*70)
    print("  AADS SERIES MANAGER - Quick Start")
    print("  Atlantic Armwrestling Development Series")
    print("="*70)
    print()
    
    if not check_database_exists():
        print("⚠️  Database not found!")
        print()
        print("This appears to be your first time running the program.")
        print("We need to initialize the database with your event data.")
        print()
        
        response = input("Initialize database now? (yes/no): ").strip().lower()
        
        if response == 'yes':
            print()
            print("Initializing database...")
            print()
            
            # Import and run initialization
            try:
                from initialize_data import initialize_aads_data
                initialize_aads_data()
                print()
                print("✓ Database initialized successfully!")
                print()
            except Exception as e:
                print(f"❌ Error initializing database: {e}")
                print()
                print("Please ensure all files are in the same directory:")
                print("  - quick_start.py")
                print("  - initialize_data.py")
                print("  - aads_database.py")
                print("  - aads_manager.py")
                sys.exit(1)
        else:
            print()
            print("Database initialization cancelled.")
            print("Run this script again when you're ready to initialize.")
            sys.exit(0)
    else:
        print("✓ Database found!")
        print()
    
    # Launch the manager
    print("Launching AADS Manager...")
    print()
    
    try:
        from aads_manager import main as run_manager
        run_manager()
    except Exception as e:
        print(f"❌ Error launching manager: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
