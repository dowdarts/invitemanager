// AADS Invite Manager - Application Logic

// Global state
let supabaseClient = null;
let players = [];
let events = [];
let eventParticipants = [];

// Initialize app on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
    loadSupabaseConfig();
    loadLocalData();
    updateDashboard();
});

// Initialize application
function initializeApp() {
    console.log('AADS Invite Manager v2.0 - Web Edition');
    
    // Initialize demo data if first time
    if (!localStorage.getItem('aads_initialized')) {
        initializeDemoData();
        localStorage.setItem('aads_initialized', 'true');
    }
}

// Setup event listeners
function setupEventListeners() {
    // Tab navigation
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const tab = e.target.dataset.tab;
            showTab(tab);
        });
    });
}

// Tab Navigation
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    
    // Load tab content
    switch(tabName) {
        case 'dashboard':
            updateDashboard();
            break;
        case 'players':
            loadPlayers();
            break;
        case 'events':
            loadEvents();
            break;
        case 'roster':
            populateRosterEventSelect();
            break;
        case 'settings':
            // Settings are static
            break;
    }
}

// Supabase Configuration
function loadSupabaseConfig() {
    const url = localStorage.getItem('supabase_url');
    const key = localStorage.getItem('supabase_key');
    
    if (url && key) {
        document.getElementById('supabase-url').value = url;
        document.getElementById('supabase-key').value = key;
        initializeSupabase(url, key);
    }
}

function saveSupabaseConfig() {
    const url = document.getElementById('supabase-url').value.trim();
    const key = document.getElementById('supabase-key').value.trim();
    
    if (!url || !key) {
        showToast('Please enter both URL and Key', 'error');
        return;
    }
    
    localStorage.setItem('supabase_url', url);
    localStorage.setItem('supabase_key', key);
    
    initializeSupabase(url, key);
    showToast('Supabase configuration saved!', 'success');
}

function initializeSupabase(url, key) {
    try {
        supabaseClient = window.supabase.createClient(url, key);
        updateSyncStatus('Connected to Supabase', true);
        console.log('Supabase initialized');
    } catch (error) {
        console.error('Supabase initialization error:', error);
        updateSyncStatus('Supabase connection error', false);
    }
}

async function testSupabaseConnection() {
    if (!supabaseClient) {
        showToast('Please configure Supabase first', 'warning');
        return;
    }
    
    try {
        const { data, error } = await supabaseClient.from('players').select('count', { count: 'exact', head: true });
        
        if (error) throw error;
        
        showToast('✓ Connection successful!', 'success');
        updateSyncStatus('Connected • Last checked: just now', true);
    } catch (error) {
        console.error('Connection test failed:', error);
        showToast(`Connection failed: ${error.message}`, 'error');
        updateSyncStatus('Connection failed', false);
    }
}

function initializeSupabaseTables() {
    const sql = `
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

-- Indexes
CREATE INDEX IF NOT EXISTS idx_players_province ON players(province);
CREATE INDEX IF NOT EXISTS idx_players_status ON players(status);
CREATE INDEX IF NOT EXISTS idx_event_participants_event ON event_participants(event_id);
CREATE INDEX IF NOT EXISTS idx_event_participants_player ON event_participants(player_id);

-- Enable RLS
ALTER TABLE players ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE event_participants ENABLE ROW LEVEL SECURITY;

-- Policies (allow all for now)
CREATE POLICY "Allow all" ON players FOR ALL USING (true);
CREATE POLICY "Allow all" ON events FOR ALL USING (true);
CREATE POLICY "Allow all" ON event_participants FOR ALL USING (true);
`;
    
    // Copy to clipboard
    navigator.clipboard.writeText(sql).then(() => {
        showToast('SQL copied to clipboard! Paste it in Supabase SQL Editor', 'success');
    });
    
    // Also show in alert for easy access
    alert('SQL Schema copied to clipboard!\n\n' +
          '1. Go to your Supabase project\n' +
          '2. Open SQL Editor\n' +
          '3. Paste and run this SQL\n' +
          '4. Click "Test Connection" to verify');
}

// Update sync status indicator
function updateSyncStatus(message, isConnected) {
    const statusEl = document.getElementById('sync-status');
    statusEl.textContent = isConnected ? `✓ ${message}` : `✗ ${message}`;
    statusEl.style.background = isConnected ? 'rgba(34, 197, 94, 0.3)' : 'rgba(239, 68, 68, 0.3)';
}

// Local Storage Management
function saveLocalData() {
    localStorage.setItem('aads_players', JSON.stringify(players));
    localStorage.setItem('aads_events', JSON.stringify(events));
    localStorage.setItem('aads_participants', JSON.stringify(eventParticipants));
}

function loadLocalData() {
    const storedPlayers = localStorage.getItem('aads_players');
    const storedEvents = localStorage.getItem('aads_events');
    const storedParticipants = localStorage.getItem('aads_participants');
    
    if (storedPlayers) players = JSON.parse(storedPlayers);
    if (storedEvents) events = JSON.parse(storedEvents);
    if (storedParticipants) eventParticipants = JSON.parse(storedParticipants);
}

// Initialize demo data
function initializeDemoData() {
    // Initialize events
    events = [
        { id: 1, name: 'Event 1 - Invitational', event_type: 'Invitational', status: 'Completed', winner_id: null },
        { id: 2, name: 'Event 2 - Invitational', event_type: 'Invitational', status: 'Completed', winner_id: null },
        { id: 3, name: 'Event 3 - Invitational', event_type: 'Invitational', status: 'Completed', winner_id: null },
        { id: 4, name: 'Event 4 - Invitational', event_type: 'Invitational', status: 'Completed', winner_id: null },
        { id: 5, name: 'Event 5 - Invitational', event_type: 'Invitational', status: 'Completed', winner_id: null },
        { id: 6, name: 'Event 6 - Invitational', event_type: 'Invitational', status: 'Active', winner_id: null },
        { id: 7, name: 'Event 7 - Tournament of Champions', event_type: 'TOC', status: 'Pending', winner_id: null }
    ];
    
    // Complete player roster with all participants from Events 1-5
    const allPlayers = [
        // New Brunswick (NB)
        { name: 'Cory Wallace', province: 'NB' },
        { name: 'Dee Cormier', province: 'NB' },
        { name: 'Royce Milliea', province: 'NB' },
        { name: 'Miguel Velasquez', province: 'NB' },
        { name: 'Gerry Johnston', province: 'NB' },
        { name: 'Tyler Stewart', province: 'NB' },
        { name: 'Denis Leblanc', province: 'NB' },
        { name: 'Micheal Léger', province: 'NB' },
        { name: 'Kyle Gray', province: 'NB' },
        { name: 'Tyler Cyr', province: 'NB' },
        { name: 'Pitou Pellerin', province: 'NB' },
        { name: 'Wayne Chapman', province: 'NB' },
        { name: 'Don Higgins', province: 'NB' },
        { name: 'Zack Davis', province: 'NB' },
        { name: 'Dana Moss', province: 'NB' },
        { name: 'Chad Arsenault', province: 'NB' },
        { name: 'Tony Solomon', province: 'NB' },
        // Nova Scotia (NS)
        { name: 'Steve Rushton', province: 'NS' },
        { name: 'Tom Holden', province: 'NS' },
        { name: 'Corey O\'Brien', province: 'NS' },
        { name: 'Drake Berry', province: 'NS' },
        { name: 'Jon Casey', province: 'NS' },
        { name: 'Jordan Boyd', province: 'NS' },
        { name: 'Colby Burke', province: 'NS' },
        { name: 'Arron Gilbert', province: 'NS' },
        { name: 'Scott Ferdinand', province: 'NS' },
        // Prince Edward Island (PEI)
        { name: 'Ricky Chaisson', province: 'PEI' },
        { name: 'Mark MacEachern', province: 'PEI' },
        { name: 'Kevin Blanchard', province: 'PEI' },
        { name: 'Corey Lefort', province: 'PEI' }
    ];
    
    players = allPlayers.map((p, index) => ({
        id: index + 1,
        ...p,
        status: 'Prospect',
        total_events: 0,
        toc_qualified: false,
        created_at: new Date().toISOString()
    }));
    
    // Event participation data
    const eventRosters = {
        1: ['Cory Wallace', 'Dee Cormier', 'Royce Milliea', 'Miguel Velasquez', 'Gerry Johnston', 'Tyler Stewart', 'Denis Leblanc', 'Micheal Léger', 'Steve Rushton', 'Tom Holden'],
        2: ['Dee Cormier', 'Denis Leblanc', 'Kyle Gray', 'Tyler Cyr', 'Tyler Stewart', 'Micheal Léger', 'Pitou Pellerin', 'Tom Holden', 'Corey O\'Brien', 'Steve Rushton'],
        3: ['Tyler Cyr', 'Kyle Gray', 'Wayne Chapman', 'Don Higgins', 'Pitou Pellerin', 'Zack Davis', 'Drake Berry', 'Jon Casey', 'Ricky Chaisson', 'Mark MacEachern'],
        4: ['Don Higgins', 'Wayne Chapman', 'Dana Moss', 'Cory Wallace', 'Dee Cormier', 'Jordan Boyd', 'Drake Berry', 'Colby Burke', 'Kevin Blanchard', 'Mark MacEachern'],
        5: ['Chad Arsenault', 'Denis Leblanc', 'Tony Solomon', 'Arron Gilbert', 'Corey O\'Brien', 'Steve Rushton', 'Jon Casey', 'Scott Ferdinand', 'Corey Lefort', 'Ricky Chaisson']
    };
    
    // Create event participants and update player stats
    let participantId = 1;
    eventParticipants = [];
    
    Object.keys(eventRosters).forEach(eventId => {
        eventRosters[eventId].forEach(playerName => {
            const player = players.find(p => p.name === playerName);
            if (player) {
                // Determine if debut or veteran
                const isDebut = player.total_events === 0;
                
                eventParticipants.push({
                    id: participantId++,
                    event_id: parseInt(eventId),
                    player_id: player.id,
                    is_debut: isDebut,
                    is_veteran: !isDebut,
                    added_at: new Date().toISOString()
                });
                
                // Update player stats
                player.total_events++;
                player.status = 'Active';
            }
        });
    });
    
    saveLocalData();
}

// Find invite candidates based on TOC eligibility
function loadInviteCandidates() {
    const candidates = players.filter(p => {
        // Eligible if participated in 1-2 events (not TOC qualified yet)
        return p.total_events > 0 && p.total_events < 3 && !p.toc_qualified;
    }).sort((a, b) => b.total_events - a.total_events);
    
    const modal = document.createElement('div');
    modal.className = 'modal active';
    modal.innerHTML = `
        <div class="modal-content">
            <h2>🎯 Invite Candidates</h2>
            <p>Players eligible for upcoming invitations (1-2 events, not TOC qualified)</p>
            ${candidates.length > 0 ? `
                <table style="margin-top: 20px;">
                    <thead>
                        <tr>
                            <th>Player</th>
                            <th>Province</th>
                            <th>Events</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${candidates.map(p => `
                            <tr>
                                <td>${p.name}</td>
                                <td>${p.province}</td>
                                <td>${p.total_events}</td>
                                <td>${p.status}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            ` : '<p>No candidates found. Players need 1-2 event participations.</p>'}
            <div style="margin-top: 20px; text-align: right;">
                <button class="btn btn-secondary" onclick="this.closest('.modal').remove()">Close</button>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
}

// Dashboard Functions
function updateDashboard() {
    // Update stats
    document.getElementById('total-players').textContent = players.length;
    document.getElementById('completed-events').textContent = events.filter(e => e.status === 'Completed').length;
    document.getElementById('toc-qualified').textContent = players.filter(p => p.toc_qualified).length;
    document.getElementById('prospects-count').textContent = players.filter(p => p.total_events === 0).length;
    
    // Update events summary
    const summaryHTML = events.map(event => {
        const participants = eventParticipants.filter(ep => ep.event_id === event.id).length;
        const winner = event.winner_id ? players.find(p => p.id === event.winner_id)?.name : 'TBD';
        
        return `
            <div class="event-card">
                <div class="event-header">
                    <h4>${event.name}</h4>
                    <span class="event-status status-${event.status.toLowerCase()}">${event.status}</span>
                </div>
                <p>Participants: ${participants}/10 • Winner: ${winner}</p>
            </div>
        `;
    }).join('');
    
    document.getElementById('events-summary').innerHTML = summaryHTML || '<p>No events yet</p>';
}

// Player Functions
function loadPlayers() {
    filterPlayers();
}

function filterPlayers() {
    const provinceFilter = document.getElementById('province-filter').value;
    const statusFilter = document.getElementById('status-filter').value;
    const searchText = document.getElementById('search-players').value.toLowerCase();
    
    let filtered = players;
    
    if (provinceFilter !== 'all') {
        filtered = filtered.filter(p => p.province === provinceFilter);
    }
    
    if (statusFilter !== 'all') {
        filtered = filtered.filter(p => p.status === statusFilter);
    }
    
    if (searchText) {
        filtered = filtered.filter(p => p.name.toLowerCase().includes(searchText));
    }
    
    displayPlayers(filtered);
}

function displayPlayers(playersList) {
    if (playersList.length === 0) {
        document.getElementById('players-list').innerHTML = '<p class="loading">No players found</p>';
        return;
    }
    
    const html = `
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Province</th>
                    <th>Status</th>
                    <th>Events</th>
                    <th>TOC</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                ${playersList.map(player => `
                    <tr>
                        <td><strong>${player.name}</strong></td>
                        <td>${player.province}</td>
                        <td><span class="badge badge-${player.status.toLowerCase().replace(' ', '-')}">${player.status}</span></td>
                        <td>${player.total_events}</td>
                        <td>${player.toc_qualified ? '✓' : ''}</td>
                        <td>
                            <button class="btn btn-secondary" style="padding: 6px 12px; font-size: 0.85rem;" onclick="viewPlayerHistory(${player.id})">History</button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
    
    document.getElementById('players-list').innerHTML = html;
}

function showAddPlayerModal() {
    document.getElementById('player-modal-title').textContent = 'Add New Player';
    document.getElementById('player-form').reset();
    document.getElementById('player-modal').style.display = 'block';
}

function savePlayer(event) {
    event.preventDefault();
    
    const name = document.getElementById('player-name').value.trim();
    const province = document.getElementById('player-province').value;
    
    if (!name || !province) {
        showToast('Please fill all fields', 'error');
        return;
    }
    
    // Check for duplicate
    if (players.some(p => p.name.toLowerCase() === name.toLowerCase())) {
        showToast('Player already exists', 'error');
        return;
    }
    
    const newPlayer = {
        id: Math.max(0, ...players.map(p => p.id)) + 1,
        name,
        province,
        status: 'Prospect',
        total_events: 0,
        toc_qualified: false,
        created_at: new Date().toISOString()
    };
    
    players.push(newPlayer);
    saveLocalData();
    closeModal('player-modal');
    loadPlayers();
    updateDashboard();
    showToast(`✓ ${name} added successfully!`, 'success');
}

function viewPlayerHistory(playerId) {
    const player = players.find(p => p.id === playerId);
    if (!player) return;
    
    const playerEvents = eventParticipants.filter(ep => ep.player_id === playerId);
    const eventsList = playerEvents.map(ep => {
        const event = events.find(e => e.id === ep.event_id);
        const isWinner = event.winner_id === playerId;
        return `
            <div style="padding: 10px; border-bottom: 1px solid var(--border-color);">
                <strong>${event.name}</strong>
                ${ep.is_debut ? '<span class="badge badge-debut">DEBUT</span>' : '<span class="badge badge-veteran">VETERAN</span>'}
                ${isWinner ? '<span class="badge badge-winner">WINNER</span>' : ''}
            </div>
        `;
    }).join('');
    
    alert(`Player: ${player.name}\nProvince: ${player.province}\nStatus: ${player.status}\nTotal Events: ${player.total_events}\n\nEvent History:\n${playerEvents.length === 0 ? 'No events yet' : 'See details'}`);
}

// Event Functions
function loadEvents() {
    const html = events.map(event => {
        const participants = eventParticipants.filter(ep => ep.event_id === event.id);
        const winner = event.winner_id ? players.find(p => p.id === event.winner_id) : null;
        
        return `
            <div class="event-card">
                <div class="event-header">
                    <h3>${event.name}</h3>
                    <span class="event-status status-${event.status.toLowerCase()}">${event.status}</span>
                </div>
                <p><strong>Participants:</strong> ${participants.length}/10</p>
                ${winner ? `<p><strong>Winner:</strong> ${winner.name}</p>` : ''}
                <div class="button-group" style="margin-top: 15px;">
                    <button class="btn btn-primary" onclick="manageEventRoster(${event.id})">📋 Manage Roster</button>
                    ${event.id <= 6 && event.status !== 'Pending' ? `<button class="btn btn-success" onclick="setEventWinner(${event.id})">🏆 Set Winner</button>` : ''}
                </div>
            </div>
        `;
    }).join('');
    
    document.getElementById('events-list').innerHTML = html;
}

function manageEventRoster(eventId) {
    showTab('roster');
    document.getElementById('roster-event-select').value = eventId;
    loadEventRoster();
}

function populateRosterEventSelect() {
    const select = document.getElementById('roster-event-select');
    select.innerHTML = '<option value="">Select Event...</option>' +
        events.slice(0, 6).map(e => `<option value="${e.id}">${e.name}</option>`).join('');
}

function loadEventRoster() {
    const eventId = parseInt(document.getElementById('roster-event-select').value);
    if (!eventId) {
        document.getElementById('roster-content').innerHTML = '<p>Select an event to manage roster</p>';
        return;
    }
    
    const event = events.find(e => e.id === eventId);
    const participants = eventParticipants.filter(ep => ep.event_id === eventId);
    
    const availablePlayers = players.filter(p => 
        !participants.some(ep => ep.player_id === p.id)
    );
    
    const html = `
        <h3>Current Roster (${participants.length}/10)</h3>
        ${participants.length > 0 ? `
            <table>
                <thead>
                    <tr>
                        <th>Player</th>
                        <th>Province</th>
                        <th>Type</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${participants.map(ep => {
                        const player = players.find(p => p.id === ep.player_id);
                        return `
                            <tr>
                                <td>${player.name}</td>
                                <td>${player.province}</td>
                                <td><span class="badge badge-${ep.is_debut ? 'debut' : 'veteran'}">${ep.is_debut ? 'DEBUT' : 'VETERAN'}</span></td>
                                <td>
                                    <button class="btn btn-danger" style="padding: 6px 12px; font-size: 0.85rem;" onclick="removeFromRoster(${eventId}, ${player.id})">Remove</button>
                                </td>
                            </tr>
                        `;
                    }).join('')}
                </tbody>
            </table>
        ` : '<p>No participants yet</p>'}
        
        ${participants.length < 10 ? `
            <h3 style="margin-top: 30px;">Add Players</h3>
            <div class="filters">
                <input type="text" id="roster-search" placeholder="🔍 Search players..." onkeyup="filterRosterCandidates()">
                <select id="roster-province-filter" onchange="filterRosterCandidates()">
                    <option value="all">All Provinces</option>
                    <option value="NB">New Brunswick (NB)</option>
                    <option value="NS">Nova Scotia (NS)</option>
                    <option value="PEI">Prince Edward Island (PEI)</option>
                </select>
            </div>
            <div id="roster-candidates"></div>
        ` : '<p style="color: var(--success-color); font-weight: bold;">✓ Roster is full (10/10)</p>'}
    `;
    
    document.getElementById('roster-content').innerHTML = html;
    
    if (participants.length < 10) {
        filterRosterCandidates();
    }
}

function filterRosterCandidates() {
    const eventId = parseInt(document.getElementById('roster-event-select').value);
    const participants = eventParticipants.filter(ep => ep.event_id === eventId);
    
    let availablePlayers = players.filter(p => 
        !participants.some(ep => ep.player_id === p.id)
    );
    
    const search = document.getElementById('roster-search')?.value.toLowerCase() || '';
    const province = document.getElementById('roster-province-filter')?.value || 'all';
    
    if (search) {
        availablePlayers = availablePlayers.filter(p => p.name.toLowerCase().includes(search));
    }
    
    if (province !== 'all') {
        availablePlayers = availablePlayers.filter(p => p.province === province);
    }
    
    const html = availablePlayers.length > 0 ? `
        <table style="margin-top: 15px;">
            <thead>
                <tr>
                    <th>Player</th>
                    <th>Province</th>
                    <th>Events</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                ${availablePlayers.slice(0, 10).map(player => `
                    <tr>
                        <td>${player.name}</td>
                        <td>${player.province}</td>
                        <td>${player.total_events}</td>
                        <td>
                            <button class="btn btn-success" style="padding: 6px 12px; font-size: 0.85rem;" onclick="addToRoster(${eventId}, ${player.id})">Add</button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    ` : '<p>No available players</p>';
    
    document.getElementById('roster-candidates').innerHTML = html;
}

function addToRoster(eventId, playerId) {
    const player = players.find(p => p.id === playerId);
    const isDebut = player.total_events === 0;
    
    eventParticipants.push({
        id: Math.max(0, ...eventParticipants.map(ep => ep.id)) + 1,
        event_id: eventId,
        player_id: playerId,
        is_debut: isDebut,
        is_veteran: !isDebut,
        added_at: new Date().toISOString()
    });
    
    // Update player stats
    player.total_events++;
    if (player.status === 'Prospect') {
        player.status = 'Active';
    }
    
    saveLocalData();
    loadEventRoster();
    updateDashboard();
    showToast(`✓ ${player.name} added to roster!`, 'success');
}

function removeFromRoster(eventId, playerId) {
    const index = eventParticipants.findIndex(ep => ep.event_id === eventId && ep.player_id === playerId);
    if (index !== -1) {
        eventParticipants.splice(index, 1);
        
        // Update player stats
        const player = players.find(p => p.id === playerId);
        player.total_events = Math.max(0, player.total_events - 1);
        if (player.total_events === 0) {
            player.status = 'Prospect';
        }
        
        saveLocalData();
        loadEventRoster();
        updateDashboard();
        showToast('Player removed from roster', 'success');
    }
}

function setEventWinner(eventId) {
    const participants = eventParticipants.filter(ep => ep.event_id === eventId);
    if (participants.length === 0) {
        showToast('No participants in this event', 'error');
        return;
    }
    
    const playersList = participants.map(ep => {
        const player = players.find(p => p.id === ep.player_id);
        return `${ep.player_id}: ${player.name}`;
    }).join('\n');
    
    const winnerId = prompt(`Select winner by entering their ID:\n\n${playersList}`);
    
    if (!winnerId) return;
    
    const winnerIdNum = parseInt(winnerId);
    const winner = players.find(p => p.id === winnerIdNum);
    
    if (!winner || !participants.some(ep => ep.player_id === winnerIdNum)) {
        showToast('Invalid winner selection', 'error');
        return;
    }
    
    // Set winner
    const event = events.find(e => e.id === eventId);
    event.winner_id = winnerIdNum;
    event.status = 'Completed';
    
    // Update player status
    winner.status = 'Winner';
    winner.toc_qualified = true;
    
    // Add to TOC (Event 7)
    if (!eventParticipants.some(ep => ep.event_id === 7 && ep.player_id === winnerIdNum)) {
        eventParticipants.push({
            id: Math.max(0, ...eventParticipants.map(ep => ep.id)) + 1,
            event_id: 7,
            player_id: winnerIdNum,
            is_debut: false,
            is_veteran: true,
            added_at: new Date().toISOString()
        });
    }
    
    saveLocalData();
    loadEvents();
    updateDashboard();
    showToast(`🏆 ${winner.name} is the winner! Auto-qualified for TOC!`, 'success');
}

// Cloud Sync Functions
async function syncToCloud() {
    if (!supabaseClient) {
        showToast('Please configure Supabase first', 'warning');
        showTab('settings');
        return;
    }
    
    if (!confirm('This will upload all local data to Supabase. Continue?')) {
        return;
    }
    
    try {
        showToast('Syncing to cloud...', 'success');
        
        // Sync players
        for (const player of players) {
            await supabaseClient.from('players').upsert(player);
        }
        
        // Sync events
        for (const event of events) {
            await supabaseClient.from('events').upsert(event);
        }
        
        // Sync participants
        for (const ep of eventParticipants) {
            await supabaseClient.from('event_participants').upsert(ep);
        }
        
        showToast('✓ Successfully synced to cloud!', 'success');
        updateSyncStatus('Synced • Last: just now', true);
    } catch (error) {
        console.error('Sync error:', error);
        showToast(`Sync failed: ${error.message}`, 'error');
    }
}

async function pullFromCloud() {
    if (!supabaseClient) {
        showToast('Please configure Supabase first', 'warning');
        showTab('settings');
        return;
    }
    
    if (!confirm('This will REPLACE all local data with cloud data. Continue?')) {
        return;
    }
    
    try {
        showToast('Pulling from cloud...', 'success');
        
        // Pull players
        const { data: cloudPlayers } = await supabaseClient.from('players').select('*');
        if (cloudPlayers) players = cloudPlayers;
        
        // Pull events
        const { data: cloudEvents } = await supabaseClient.from('events').select('*');
        if (cloudEvents) events = cloudEvents;
        
        // Pull participants
        const { data: cloudParticipants } = await supabaseClient.from('event_participants').select('*');
        if (cloudParticipants) eventParticipants = cloudParticipants;
        
        saveLocalData();
        updateDashboard();
        showTab('dashboard');
        showToast('✓ Successfully pulled from cloud!', 'success');
        updateSyncStatus('Synced • Last: just now', true);
    } catch (error) {
        console.error('Pull error:', error);
        showToast(`Pull failed: ${error.message}`, 'error');
    }
}

// Export/Import
function exportData() {
    const data = {
        players,
        events,
        eventParticipants,
        exportedAt: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `aads-export-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
    
    showToast('Data exported successfully!', 'success');
}

function importData() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'application/json';
    
    input.onchange = (e) => {
        const file = e.target.files[0];
        const reader = new FileReader();
        
        reader.onload = (event) => {
            try {
                const data = JSON.parse(event.target.result);
                
                if (data.players) players = data.players;
                if (data.events) events = data.events;
                if (data.eventParticipants) eventParticipants = data.eventParticipants;
                
                saveLocalData();
                updateDashboard();
                showTab('dashboard');
                showToast('Data imported successfully!', 'success');
            } catch (error) {
                showToast('Import failed: Invalid file', 'error');
            }
        };
        
        reader.readAsText(file);
    };
    
    input.click();
}

// Utility Functions
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.style.display = 'block';
    
    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}

// Close modals when clicking outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}
