-- AADS Invite Manager - Supabase Database Setup
-- Atlantic Amateur Darts Series
-- Run this SQL in your Supabase SQL Editor to create the database tables

-- Create players table
CREATE TABLE IF NOT EXISTS players (
    id BIGINT PRIMARY KEY,
    name TEXT NOT NULL,
    province TEXT NOT NULL CHECK (province IN ('NB', 'NS', 'PEI', 'NL')),
    status TEXT NOT NULL DEFAULT 'Prospect' CHECK (status IN ('Prospect', 'Active', 'TOC Qualified')),
    total_events INTEGER NOT NULL DEFAULT 0,
    toc_qualified BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create events table
CREATE TABLE IF NOT EXISTS events (
    id BIGINT PRIMARY KEY,
    name TEXT NOT NULL,
    event_type TEXT NOT NULL CHECK (event_type IN ('Invitational', 'TOC')),
    status TEXT NOT NULL DEFAULT 'Pending' CHECK (status IN ('Pending', 'Active', 'Completed')),
    winner_id BIGINT REFERENCES players(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create event_participants table
CREATE TABLE IF NOT EXISTS event_participants (
    id BIGINT PRIMARY KEY,
    event_id BIGINT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    player_id BIGINT NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    is_debut BOOLEAN NOT NULL DEFAULT false,
    is_veteran BOOLEAN NOT NULL DEFAULT false,
    added_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(event_id, player_id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_players_province ON players(province);
CREATE INDEX IF NOT EXISTS idx_players_status ON players(status);
CREATE INDEX IF NOT EXISTS idx_events_status ON events(status);
CREATE INDEX IF NOT EXISTS idx_event_participants_event ON event_participants(event_id);
CREATE INDEX IF NOT EXISTS idx_event_participants_player ON event_participants(player_id);

-- Enable Row Level Security (RLS)
ALTER TABLE players ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE event_participants ENABLE ROW LEVEL SECURITY;

-- Create policies for public read/write access
-- WARNING: These policies allow anyone to read/write. 
-- For production, you should restrict based on user authentication.

CREATE POLICY "Enable read access for all users" ON players
    FOR SELECT USING (true);

CREATE POLICY "Enable insert access for all users" ON players
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable update access for all users" ON players
    FOR UPDATE USING (true);

CREATE POLICY "Enable delete access for all users" ON players
    FOR DELETE USING (true);

CREATE POLICY "Enable read access for all users" ON events
    FOR SELECT USING (true);

CREATE POLICY "Enable insert access for all users" ON events
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable update access for all users" ON events
    FOR UPDATE USING (true);

CREATE POLICY "Enable delete access for all users" ON events
    FOR DELETE USING (true);

CREATE POLICY "Enable read access for all users" ON event_participants
    FOR SELECT USING (true);

CREATE POLICY "Enable insert access for all users" ON event_participants
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable update access for all users" ON event_participants
    FOR UPDATE USING (true);

CREATE POLICY "Enable delete access for all users" ON event_participants
    FOR DELETE USING (true);

-- Success message
SELECT 'Database setup complete! ✅' AS message;
