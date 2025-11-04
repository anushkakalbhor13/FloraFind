// Enhanced FloraFind JavaScript
const API_URL = "http://127.0.0.1:5000";
const CURRENT_USER_ID = 1; // Demo user ID

// Global State
let currentLanguage = 'en';
let userLocation = null;
let currentSection = 'chat';
let calendarDate = new Date();
let userStats = { points: 0, level: 1, badges: 0 };

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    loadUserStats();
    loadUserGarden();
});

function initializeApp() {
    // Focus on input when page loads
    document.getElementById('chatBox').focus();
    
    // Add initial animation to welcome section
    setTimeout(() => {
        const welcomeSection = document.getElementById('welcomeSection');
        if (welcomeSection) {
            welcomeSection.style.opacity = '1';
        }
    }, 100);
    
    // Set active nav button
    updateActiveNavButton('chat');
    
    // Initialize calendar
    generateCalendar();
    
    // Load community data
    loadChallenges();
    loadLeaderboard();
    
    // Get user location if available
    getUserLocation();
}

// Navigation Functions
function showSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.app-section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Show selected section
    const targetSection = document.getElementById(`${sectionName}-section`);
    if (targetSection) {
        targetSection.classList.add('active');
        currentSection = sectionName;
        updateActiveNavButton(sectionName);
        
        // Load section-specific data
        if (sectionName === 'garden') {
            loadUserGarden();
        } else if (sectionName === 'community') {
            loadChallenges();
            loadLeaderboard();
        } else if (sectionName === 'calendar') {
            loadUpcomingTasks();
        }
    }
}

function updateActiveNavButton(sectionName) {
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.section === sectionName) {
            btn.classList.add('active');
        }
    });
}

// Enhanced Chat Functions
async function sendMessage() {
    const input = document.getElementById("chatBox");
    const userText = input.value.trim();
    if (!userText) return;

    // Show user message
    addMessage(userText, "user");
    input.value = "";

    // Clear suggestions
    document.getElementById("suggestions").innerHTML = "";

    // Show typing animation
    showTyping();

    try {
        const params = new URLSearchParams({
            q: userText,
            user_id: CURRENT_USER_ID,
            location: userLocation || ''
        });
        
        const res = await fetch(`${API_URL}/query?${params}`);
        const data = await res.json();

        removeTyping();

        if (data.error) {
            addMessage(`❌ Error: ${data.error}`, "bot");
        } else if (data.type === 'care_calendar') {
            displayCareCalendar(data);
        } else if (data.plants && Array.isArray(data.plants)) {
            const formattedCards = formatPlantCards(data.plants, data.total_eco_impact);
            addMessage(formattedCards, "bot", data.nlp_analysis_details);
        } else if (data.message) {
            addMessage(data.message, "bot", data.nlp_analysis_details);
        } else {
            addMessage("🤔 Sorry, I couldn't find anything matching your request.", "bot");
        }

        // Update language if detected
        if (data.language && data.language !== currentLanguage) {
            currentLanguage = data.language;
            updateLanguageDisplay();
        }

    } catch (err) {
        console.error("API Error:", err);
        removeTyping();
        addMessage("⚠️ Sorry, there was a connection error. Please try again.", "bot");
    }
}

function addMessage(text, sender, nlpAnalysis = null) {
    const chat = document.getElementById("chat-container");
    const msg = document.createElement("div");
    msg.className = `message ${sender}`;
    
    // Create message bubble
    const bubble = document.createElement("div");
    bubble.innerHTML = text;
    msg.appendChild(bubble);
    
    // Add NLP analysis section if available (for bot messages only)
    if (sender === 'bot' && nlpAnalysis) {
        const nlpSection = document.createElement("div");
        nlpSection.className = "nlp-analysis";
        nlpSection.innerHTML = formatNlpAnalysis(nlpAnalysis);
        msg.appendChild(nlpSection);
    }
    
    // Hide welcome section when first message is sent
    if (sender === 'user') {
        hideWelcomeSection();
    }
    
    chat.appendChild(msg);
    
    // Smooth scroll to bottom
    setTimeout(() => {
        chat.scrollTop = chat.scrollHeight;
    }, 100);
}

// Format NLP analysis for display
function formatNlpAnalysis(nlpAnalysis) {
    let html = `
        <div class="nlp-analysis-container">
            <h4>NLP Analysis Results</h4>
            <div class="nlp-tabs">
                <button class="nlp-tab active" onclick="showNlpTab(event, 'tokenization')">Tokenization</button>
                <button class="nlp-tab" onclick="showNlpTab(event, 'pos')">POS Tagging</button>
                <button class="nlp-tab" onclick="showNlpTab(event, 'ner')">Named Entities</button>
                <button class="nlp-tab" onclick="showNlpTab(event, 'dependency')">Dependency</button>
                <button class="nlp-tab" onclick="showNlpTab(event, 'lemma')">Lemmatization</button>
            </div>
            
            <div id="tokenization" class="nlp-tab-content active">
                <h5>Tokenization Results</h5>
                <div class="token-list">
                    ${nlpAnalysis.tokenization && nlpAnalysis.tokenization.length > 0 ? 
                        nlpAnalysis.tokenization.map(token => 
                            `<span class="token">${token.text}</span>`
                        ).join(' ') : 'No tokenization data available'}
                </div>
            </div>
            
            <div id="pos" class="nlp-tab-content">
                <h5>Part-of-Speech Tagging</h5>
                <div class="pos-table">
                    ${nlpAnalysis.pos_tagging && nlpAnalysis.pos_tagging.length > 0 ? 
                        `<table>
                            <tr><th>Token</th><th>POS</th><th>Tag</th></tr>
                            ${nlpAnalysis.pos_tagging.map(pos => 
                                `<tr>
                                    <td>${pos.text}</td>
                                    <td>${pos.pos}</td>
                                    <td>${pos.tag}</td>
                                </tr>`
                            ).join('')}
                        </table>` : 'No POS tagging data available'}
                </div>
            </div>
            
            <div id="ner" class="nlp-tab-content">
                <h5>Named Entity Recognition</h5>
                <div class="ner-list">
                    ${nlpAnalysis.ner && nlpAnalysis.ner.length > 0 ? 
                        nlpAnalysis.ner.map(entity => 
                            `<div class="entity">
                                <span class="entity-text">${entity.text}</span>
                                <span class="entity-label">${entity.label}</span>
                            </div>`
                        ).join('') : 'No named entities found'}
                </div>
            </div>
            
            <div id="dependency" class="nlp-tab-content">
                <h5>Dependency Parsing</h5>
                <div class="dependency-table">
                    ${nlpAnalysis.dependency_parsing && nlpAnalysis.dependency_parsing.length > 0 ? 
                        `<table>
                            <tr><th>Token</th><th>Dependency</th><th>Head</th></tr>
                            ${nlpAnalysis.dependency_parsing.map(dep => 
                                `<tr>
                                    <td>${dep.text}</td>
                                    <td>${dep.dep}</td>
                                    <td>${dep.head}</td>
                                </tr>`
                            ).join('')}
                        </table>` : 'No dependency parsing data available'}
                </div>
            </div>
            
            <div id="lemma" class="nlp-tab-content">
                <h5>Lemmatization</h5>
                <div class="lemma-table">
                    ${nlpAnalysis.lemmatization && nlpAnalysis.lemmatization.length > 0 ? 
                        `<table>
                            <tr><th>Token</th><th>Lemma</th></tr>
                            ${nlpAnalysis.lemmatization.map(lemma => 
                                `<tr>
                                    <td>${lemma.text}</td>
                                    <td>${lemma.lemma}</td>
                                </tr>`
                            ).join('')}
                        </table>` : 'No lemmatization data available'}
                </div>
            </div>
        </div>
    `;
    return html;
}

// Show NLP tab content
function showNlpTab(event, tabName) {
    // Hide all tab contents
    const tabContents = event.target.closest('.nlp-analysis-container').querySelectorAll('.nlp-tab-content');
    tabContents.forEach(content => {
        content.classList.remove('active');
    });
    
    // Remove active class from all tabs
    const tabs = event.target.closest('.nlp-tabs').querySelectorAll('.nlp-tab');
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Show the selected tab content
    event.target.closest('.nlp-analysis-container').querySelector(`#${tabName}`).classList.add('active');
    
    // Add active class to the clicked tab
    event.target.classList.add('active');
}

function showTyping() {
    const chat = document.getElementById("chat-container");
    const typing = document.createElement("div");
    typing.className = "message bot typing-indicator";
    typing.id = "typing";
    typing.innerHTML = `
        <div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <span>🌱</span>
                <span>FloraFind is thinking</span>
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
    `;
    chat.appendChild(typing);
    chat.scrollTop = chat.scrollHeight;
}

function removeTyping() {
    const typing = document.getElementById("typing");
    if (typing) typing.remove();
}

function hideWelcomeSection() {
    // Don't hide the welcome section anymore - keep it visible
    // Users can still see quick actions and suggestions
}

function quickQuery(query) {
    // Switch to chat section first
    showSection('chat');
    
    // Small delay to ensure the section is shown
    setTimeout(() => {
        const input = document.getElementById('chatBox');
        input.value = query;
        sendMessage();
    }, 100);
}

// Enhanced Plant Card Formatting
function formatPlantCards(plants, ecoImpact = 0) {
    if (!Array.isArray(plants) || plants.length === 0) {
        return "🤔 Sorry, I couldn't find any plants matching your criteria.";
    }
    
    let html = `
        <div style="margin: 16px 0; padding: 1rem; background: var(--very-light-green); border-radius: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <strong>🌿 Found ${plants.length} plant${plants.length > 1 ? 's' : ''} for you!</strong>
                ${ecoImpact > 0 ? `<span style="background: var(--success); color: white; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.9rem;">🌍 Eco Impact: ${ecoImpact}/10</span>` : ''}
            </div>
        </div>
    `;
    
    plants.forEach(plant => {
        html += `
            <div class="plant-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                    <h3>${plant.name}${plant.scientific_name ? ` <em>(${plant.scientific_name})</em>` : ''}</h3>
                    <div style="display: flex; gap: 0.5rem;">
                        ${plant.eco_impact_score ? `<span style="background: var(--success); color: white; padding: 0.25rem 0.5rem; border-radius: 10px; font-size: 0.8rem;">🌍 ${plant.eco_impact_score}/10</span>` : ''}
                        ${plant.difficulty_level ? `<span style="background: var(--warning); color: white; padding: 0.25rem 0.5rem; border-radius: 10px; font-size: 0.8rem;">${plant.difficulty_level}</span>` : ''}
                    </div>
                </div>
                
                <div class="plant-info">
                    <div class="plant-detail season">
                        <strong>🌞 Season:</strong> ${plant.season}
                    </div>
                    <div class="plant-detail climate">
                        <strong>🌍 Climate:</strong> ${plant.climate}
                    </div>
                    ${plant.native_region ? `
                        <div class="plant-detail native">
                            <strong>📍 Native to:</strong> ${plant.native_region}
                        </div>
                    ` : ''}
                    ${plant.growth_height ? `
                        <div class="plant-detail height">
                            <strong>📏 Height:</strong> ${plant.growth_height}
                        </div>
                    ` : ''}
                </div>
                
                <div class="care-instructions" style="margin-top: 0.75rem; padding: 0.75rem; font-size: 0.9rem;">
                    ${plant.care_instructions}
                </div>
                
                ${plant.cultural_significance ? `
                    <div style="margin-top: 1rem; padding: 0.75rem; background: rgba(255, 215, 0, 0.1); border-radius: 8px; border-left: 3px solid var(--gold);">
                        <strong>🏛️ Cultural Significance:</strong> ${plant.cultural_significance}
                    </div>
                ` : ''}
                
                ${plant.medicinal_properties ? `
                    <div style="margin-top: 1rem; padding: 0.75rem; background: rgba(39, 174, 96, 0.1); border-radius: 8px; border-left: 3px solid var(--success);">
                        <strong>💊 Medicinal Uses:</strong> ${plant.medicinal_properties}
                    </div>
                ` : ''}
                
                <div style="margin-top: 1rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    <button onclick="addToGarden(${plant.plant_id}, '${plant.name}')" class="quick-btn" style="font-size: 0.9rem; padding: 0.5rem 1rem;">
                        <i class="fas fa-plus"></i> Add to Garden
                    </button>
                    <button onclick="getCareCalendar(${plant.plant_id})" class="quick-btn" style="font-size: 0.9rem; padding: 0.5rem 1rem;">
                        <i class="fas fa-calendar"></i> Care Schedule
                    </button>
                </div>
            </div>
        `;
    });
    
    return html;
}

function displayCareCalendar(data) {
    const plant = data.plant;
    const schedule = data.care_schedule;
    
    let html = `
        <div style="background: var(--surface); border-radius: 15px; padding: 2rem; margin: 1rem 0; box-shadow: 0 10px 30px var(--shadow);">
            <h3 style="color: var(--primary-green); margin-bottom: 1rem;">
                📅 Care Calendar for ${schedule.plant_name}
            </h3>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 1rem 0;">
                <div style="background: var(--very-light-green); padding: 1rem; border-radius: 10px;">
                    <strong>Current Season:</strong> ${schedule.current_season}
                </div>
                <div style="background: var(--very-light-green); padding: 1rem; border-radius: 10px;">
                    <strong>💧 Water Every:</strong> ${schedule.watering.frequency_days} days
                </div>
                <div style="background: var(--very-light-green); padding: 1rem; border-radius: 10px;">
                    <strong>Next Watering:</strong> ${schedule.watering.next_due}
                </div>
                <div style="background: var(--very-light-green); padding: 1rem; border-radius: 10px;">
                    <strong>🌍 Eco Impact:</strong> ${schedule.eco_impact_score}/10
                </div>
            </div>
            
            ${schedule.care_tips && Object.keys(schedule.care_tips).length > 0 ? `
                <div style="margin-top: 1.5rem;">
                    <h4 style="color: var(--primary-green); margin-bottom: 0.5rem;">🌱 Seasonal Care Tips:</h4>
                    <div style="background: rgba(164, 195, 178, 0.3); padding: 1rem; border-radius: 10px;">
                        ${formatCareTips(schedule.care_tips)}
                    </div>
                </div>
            ` : ''}
            
            <div style="margin-top: 1.5rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
                <button onclick="addToGarden(${plant.plant_id}, '${plant.name}')" class="quick-btn">
                    <i class="fas fa-plus"></i> Add to My Garden
                </button>
                <button onclick="setupReminder(${plant.plant_id})" class="quick-btn">
                    <i class="fas fa-bell"></i> Set Reminder
                </button>
                <button onclick="showSection('calendar')" class="quick-btn">
                    <i class="fas fa-calendar"></i> View Calendar
                </button>
            </div>
        </div>
    `;
    
    addMessage(html, "bot");
}

function formatCareTips(careTips) {
    let html = '';
    Object.entries(careTips).forEach(([season, tips]) => {
        html += `<div style="margin-bottom: 1rem;"><strong>${season}:</strong><ul style="margin-left: 1rem;">`;
        Object.entries(tips).forEach(([task, instruction]) => {
            html += `<li><strong>${task}:</strong> ${instruction}</li>`;
        });
        html += '</ul></div>';
    });
    return html;
}

// Garden Management Functions
async function addToGarden(plantId, plantName) {
    try {
        const response = await fetch(`${API_URL}/add_to_garden`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: CURRENT_USER_ID,
                plant_id: plantId,
                nickname: plantName,
                location: 'garden',
                date_planted: new Date().toISOString().split('T')[0]
            })
        });
        
        const result = await response.json();
        if (result.success) {
            showNotification(`🌱 ${plantName} added to your garden!`, 'success');
            loadUserStats(); // Refresh user stats
        } else {
            showNotification('Failed to add plant to garden', 'error');
        }
    } catch (error) {
        console.error('Error adding to garden:', error);
        showNotification('Error adding plant to garden', 'error');
    }
}

async function getCareCalendar(plantId) {
    try {
        const response = await fetch(`${API_URL}/care_calendar/${plantId}?location=${userLocation || ''}`);
        const schedule = await response.json();
        
        if (schedule.error) {
            showNotification('Plant not found', 'error');
            return;
        }
        
        displayCareCalendar({ plant: { plant_id: plantId }, care_schedule: schedule });
    } catch (error) {
        console.error('Error getting care calendar:', error);
        showNotification('Error loading care calendar', 'error');
    }
}

async function loadUserGarden() {
    try {
        const response = await fetch(`${API_URL}/my_garden/${CURRENT_USER_ID}`);
        const data = await response.json();
        
        if (data.garden) {
            displayGarden(data);
            updateGardenStats(data);
        }
    } catch (error) {
        console.error('Error loading garden:', error);
    }
}

function displayGarden(data) {
    const gardenGrid = document.getElementById('garden-plants');
    if (!gardenGrid) return;
    
    if (!data.garden || data.garden.length === 0) {
        gardenGrid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 3rem;">
                <i class="fas fa-seedling" style="font-size: 4rem; color: var(--accent-green); margin-bottom: 1rem;"></i>
                <h3>Your garden is empty</h3>
                <p>Start by adding some plants from search results!</p>
                <button onclick="showSection('chat')" class="quick-btn" style="margin-top: 1rem;">
                    <i class="fas fa-search"></i> Find Plants
                </button>
            </div>
        `;
        return;
    }
    
    gardenGrid.innerHTML = data.garden.map(plant => {
        const info = plant.plant_info;
        const schedule = plant.care_schedule;
        const overdueTasks = schedule.filter(task => task.overdue).length;
        
        return `
            <div class="plant-card" style="position: relative;">
                ${overdueTasks > 0 ? `<div style="position: absolute; top: -5px; right: -5px; background: var(--error); color: white; border-radius: 50%; width: 25px; height: 25px; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; font-weight: bold;">${overdueTasks}</div>` : ''}
                
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                    <div>
                        <h3>${info.nickname || info.name}</h3>
                        ${info.nickname && info.nickname !== info.name ? `<p style="color: var(--text-secondary); font-style: italic;">${info.name}</p>` : ''}
                    </div>
                    <div style="text-align: right;">
                        <div style="background: ${info.health_score >= 80 ? 'var(--success)' : info.health_score >= 60 ? 'var(--warning)' : 'var(--error)'}; color: white; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.9rem; margin-bottom: 0.5rem;">
                            ❤️ ${info.health_score}%
                        </div>
                        ${info.eco_impact_score ? `<div style="background: var(--accent-green); color: white; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.9rem;">🌍 ${info.eco_impact_score}/10</div>` : ''}
                    </div>
                </div>
                
                <div class="plant-info">
                    <div class="plant-detail">
                        <strong>📍 Location:</strong> ${info.location}
                    </div>
                    <div class="plant-detail">
                        <strong>📅 Planted:</strong> ${new Date(info.date_planted).toLocaleDateString()}
                    </div>
                </div>
                
                ${schedule.length > 0 ? `
                    <div style="margin-top: 1rem;">
                        <h4 style="color: var(--primary-green); margin-bottom: 0.5rem;">📋 Care Tasks:</h4>
                        ${schedule.map(task => `
                            <div class="task-item ${task.overdue ? 'overdue' : ''}" style="margin-bottom: 0.5rem;">
                                <div>
                                    <strong>${task.task}:</strong> Due ${new Date(task.next_due).toLocaleDateString()}
                                    ${task.overdue ? ' <span style="color: var(--error);">(Overdue!)</span>' : ''}
                                </div>
                                <button onclick="completeCareTask(${info.user_plant_id}, '${task.task}')" 
                                        class="quick-btn" style="font-size: 0.8rem; padding: 0.25rem 0.75rem;">
                                    <i class="fas fa-check"></i> Done
                                </button>
                            </div>
                        `).join('')}
                    </div>
                ` : ''}
                
                ${info.notes ? `
                    <div style="margin-top: 1rem; padding: 0.75rem; background: var(--very-light-green); border-radius: 8px;">
                        <strong>📝 Notes:</strong> ${info.notes}
                    </div>
                ` : ''}
                
                <div style="margin-top: 1rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    <button onclick="getCareCalendar(${info.plant_id})" class="quick-btn" style="font-size: 0.8rem; padding: 0.5rem 1rem;" title="View detailed care schedule for this plant">
                        <i class="fas fa-calendar-alt"></i> View Care Guide
                    </button>
                    <button onclick="addCustomCareTask(${info.user_plant_id}, '${info.nickname || info.name}')" class="quick-btn" style="font-size: 0.8rem; padding: 0.5rem 1rem;" title="Add custom care tasks">
                        <i class="fas fa-plus-circle"></i> Add Care Task
                    </button>
                    <button onclick="scheduleCustomReminder(${info.user_plant_id}, '${info.nickname || info.name}')" class="quick-btn" style="font-size: 0.8rem; padding: 0.5rem 1rem;" title="Set custom reminders for plant care">
                        <i class="fas fa-bell"></i> Set Reminder
                    </button>
                    <button onclick="editPlantNotes(${info.user_plant_id}, '${info.nickname || info.name}')" class="quick-btn" style="font-size: 0.8rem; padding: 0.5rem 1rem;" title="Add or edit notes about this plant">
                        <i class="fas fa-edit"></i> Edit Notes
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

function updateGardenStats(data) {
    document.getElementById('totalPlants').textContent = data.total_plants || 0;
    document.getElementById('avgHealth').textContent = Math.round(
        data.garden.reduce((sum, plant) => sum + plant.plant_info.health_score, 0) / data.garden.length
    ) || 0;
    document.getElementById('ecoImpact').textContent = data.total_eco_impact || 0;
}

async function completeCareTask(userPlantId, taskType) {
    try {
        const response = await fetch(`${API_URL}/complete_care_task`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_plant_id: userPlantId,
                task_type: taskType,
                user_id: CURRENT_USER_ID
            })
        });
        
        const result = await response.json();
        if (result.success) {
            showNotification(`${result.message}`, 'success');
            loadUserGarden(); // Refresh garden
            loadUserStats(); // Refresh stats
            
            // Check for achievements
            if (result.points_earned >= 50) {
                setTimeout(() => checkAchievements(), 1000);
            }
        } else {
            showNotification('Failed to complete task', 'error');
        }
    } catch (error) {
        console.error('Error completing task:', error);
        showNotification('Error completing task', 'error');
    }
}


// Community Functions
async function loadChallenges() {
    try {
        const response = await fetch(`${API_URL}/community/challenges`);
        const data = await response.json();
        displayChallenges(data.challenges || []);
    } catch (error) {
        console.error('Error loading challenges:', error);
    }
}

function displayChallenges(challenges) {
    const challengesList = document.getElementById('challenges-list');
    if (!challengesList) return;
    
    if (challenges.length === 0) {
        challengesList.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 2rem;">
                <i class="fas fa-trophy" style="font-size: 3rem; color: var(--gold); margin-bottom: 1rem;"></i>
                <h3>No active challenges</h3>
                <p>Check back soon for new community challenges!</p>
            </div>
        `;
        return;
    }
    
    challengesList.innerHTML = challenges.map(challenge => `
        <div class="challenge-card">
            <h4>${challenge.title}</h4>
            <p>${challenge.description}</p>
            <div style="margin: 1rem 0;">
                <span style="background: var(--primary-green); color: white; padding: 0.25rem 0.75rem; border-radius: 10px; font-size: 0.9rem;">
                    ${challenge.challenge_type}
                </span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;">
                <small>Ends: ${new Date(challenge.end_date).toLocaleDateString()}</small>
                <button class="quick-btn" style="font-size: 0.9rem; padding: 0.5rem 1rem;">
                    <i class="fas fa-trophy"></i> Join Challenge
                </button>
            </div>
            ${challenge.prize_description ? `
                <div style="margin-top: 0.5rem; padding: 0.5rem; background: rgba(255, 215, 0, 0.1); border-radius: 5px; font-size: 0.9rem;">
                    🏆 Prize: ${challenge.prize_description}
                </div>
            ` : ''}
        </div>
    `).join('');
}

async function loadLeaderboard() {
    try {
        const response = await fetch(`${API_URL}/leaderboard`);
        const data = await response.json();
        displayLeaderboard(data.leaderboard || []);
    } catch (error) {
        console.error('Error loading leaderboard:', error);
    }
}

function displayLeaderboard(leaderboard) {
    const leaderboardList = document.getElementById('leaderboard-list');
    if (!leaderboardList) return;
    
    if (leaderboard.length === 0) {
        leaderboardList.innerHTML = `
            <div style="text-align: center; padding: 2rem;">
                <i class="fas fa-medal" style="font-size: 3rem; color: var(--gold); margin-bottom: 1rem;"></i>
                <h3>No rankings yet</h3>
                <p>Be the first to start growing!</p>
            </div>
        `;
        return;
    }
    
    leaderboardList.innerHTML = leaderboard.map((user, index) => {
        let rankClass = 'other';
        if (index === 0) rankClass = 'gold';
        else if (index === 1) rankClass = 'silver';
        else if (index === 2) rankClass = 'bronze';
        
        return `
            <div class="leaderboard-item">
                <div class="rank ${rankClass}">${index + 1}</div>
                <div style="flex: 1;">
                    <h4 style="margin: 0;">${user.username}</h4>
                    <div style="display: flex; gap: 1rem; margin-top: 0.5rem; font-size: 0.9rem; color: var(--text-secondary);">
                        <span>🌱 ${user.total_plants || 0} plants</span>
                        <span>❤️ ${Math.round(user.avg_health_score) || 0}% health</span>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-weight: bold; color: var(--primary-green);">
                        ${user.plant_health_points} pts
                    </div>
                    <div style="font-size: 0.9rem; color: var(--text-secondary);">
                        Level ${user.level}
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function showCommunityTab(tabName) {
    // Hide all tab contents
    document.querySelectorAll('.community-tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Show selected tab
    const targetTab = document.getElementById(`${tabName}-tab`);
    if (targetTab) {
        targetTab.classList.add('active');
    }
    
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.tab === tabName) {
            btn.classList.add('active');
        }
    });
}

async function submitTip(event) {
    event.preventDefault();
    
    const plantName = document.getElementById('tipPlantName').value;
    const tipContent = document.getElementById('tipContent').value;
    const location = document.getElementById('tipLocation').value;
    
    try {
        const response = await fetch(`${API_URL}/community/submit_tip`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: CURRENT_USER_ID,
                plant_name: plantName,
                care_tip: tipContent,
                location: location
            })
        });
        
        const result = await response.json();
        if (result.success) {
            showNotification(result.message, 'success');
            // Reset form
            document.getElementById('tipPlantName').value = '';
            document.getElementById('tipContent').value = '';
            document.getElementById('tipLocation').value = '';
        } else {
            showNotification('Failed to submit tip', 'error');
        }
    } catch (error) {
        console.error('Error submitting tip:', error);
        showNotification('Error submitting tip', 'error');
    }
}

// Calendar Functions
function generateCalendar() {
    const calendarGrid = document.getElementById('calendar-grid');
    const monthYearEl = document.getElementById('calendar-month-year');
    
    if (!calendarGrid || !monthYearEl) return;
    
    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'];
    
    monthYearEl.textContent = `${monthNames[calendarDate.getMonth()]} ${calendarDate.getFullYear()}`;
    
    const firstDay = new Date(calendarDate.getFullYear(), calendarDate.getMonth(), 1);
    const lastDay = new Date(calendarDate.getFullYear(), calendarDate.getMonth() + 1, 0);
    const firstDayWeek = firstDay.getDay();
    
    let html = '';
    
    // Add day headers
    const dayHeaders = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    dayHeaders.forEach(day => {
        html += `<div style="font-weight: bold; text-align: center; padding: 0.5rem; background: var(--primary-green); color: white;">${day}</div>`;
    });
    
    // Add empty cells for days before month starts
    for (let i = 0; i < firstDayWeek; i++) {
        html += '<div class="calendar-day" style="background: var(--border);"></div>';
    }
    
    // Add days of month
    for (let day = 1; day <= lastDay.getDate(); day++) {
        const hasTask = Math.random() > 0.8; // Mock task indicator
        html += `
            <div class="calendar-day ${hasTask ? 'has-tasks' : ''}">
                <div>${day}</div>
                ${hasTask ? '<div class="task-indicator"></div>' : ''}
            </div>
        `;
    }
    
    calendarGrid.innerHTML = html;
}

function changeMonth(direction) {
    calendarDate.setMonth(calendarDate.getMonth() + direction);
    generateCalendar();
}

async function loadUpcomingTasks() {
    // Mock upcoming tasks for now
    const tasksList = document.getElementById('upcoming-tasks-list');
    if (!tasksList) return;
    
    tasksList.innerHTML = `
        <div class="task-item due-soon">
            <div>
                <strong>Water Rose Bush</strong>
                <div style="font-size: 0.9rem; color: var(--text-secondary);">Due today</div>
            </div>
            <button class="quick-btn" style="font-size: 0.9rem; padding: 0.5rem 1rem;">
                <i class="fas fa-check"></i> Mark Done
            </button>
        </div>
        
        <div class="task-item">
            <div>
                <strong>Fertilize Tulsi</strong>
                <div style="font-size: 0.9rem; color: var(--text-secondary);">Due in 2 days</div>
            </div>
            <button class="quick-btn" style="font-size: 0.9rem; padding: 0.5rem 1rem;">
                <i class="fas fa-check"></i> Mark Done
            </button>
        </div>
        
        <div class="task-item overdue">
            <div>
                <strong>Prune Lavender</strong>
                <div style="font-size: 0.9rem; color: var(--error);">2 days overdue</div>
            </div>
            <button class="quick-btn" style="font-size: 0.9rem; padding: 0.5rem 1rem;">
                <i class="fas fa-check"></i> Mark Done
            </button>
        </div>
    `;
}

function exportCalendar() {
    try {
        // Create a simple calendar data structure
        const calendarData = {
            month: calendarDate.getMonth() + 1,
            year: calendarDate.getFullYear(),
            tasks: [
                { date: '2024-09-05', task: 'Water Rose Bush' },
                { date: '2024-09-07', task: 'Fertilize Tulsi' },
                { date: '2024-09-10', task: 'Prune Lavender' }
            ]
        };
        
        // Convert to CSV format
        let csvContent = "Date,Task\n";
        calendarData.tasks.forEach(item => {
            csvContent += `${item.date},${item.task}\n`;
        });
        
        // Create and download file
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement("a");
        const url = URL.createObjectURL(blob);
        link.setAttribute("href", url);
        link.setAttribute("download", `FloraFind_Calendar_${calendarData.month}_${calendarData.year}.csv`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        showNotification('📅 Calendar exported successfully!', 'success');
    } catch (error) {
        console.error('Export error:', error);
        showNotification('❌ Failed to export calendar', 'error');
    }
}

function setupReminders() {
    if ('Notification' in window) {
        if (Notification.permission === 'granted') {
            scheduleReminders();
        } else if (Notification.permission !== 'denied') {
            Notification.requestPermission().then(permission => {
                if (permission === 'granted') {
                    scheduleReminders();
                } else {
                    showNotification('❌ Permission denied for notifications', 'error');
                }
            });
        } else {
            showNotification('❌ Notifications are blocked. Please enable them in browser settings.', 'error');
        }
    } else {
        showNotification('❌ This browser does not support notifications', 'error');
    }
}

function scheduleReminders() {
    // Set up demo reminders (in a real app, this would be more sophisticated)
    showNotification('🔔 Reminders set up! You will be notified about plant care tasks.', 'success');
    
    // Schedule a demo notification after 10 seconds
    setTimeout(() => {
        if (Notification.permission === 'granted') {
            new Notification('🌱 FloraFind Reminder', {
                body: 'Time to water your Rose Bush!',
                icon: 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/325/seedling_1f331.png'
            });
        }
    }, 10000);
}

function scheduleCustomReminder(userPlantId, plantName) {
    // Check if notifications are supported
    if (!('Notification' in window)) {
        showNotification('❌ This browser does not support notifications', 'error');
        return;
    }
    
    // Request permission if not already granted
    if (Notification.permission === 'default') {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                showReminderDialog(userPlantId, plantName);
            } else {
                showNotification('❌ Permission denied for notifications', 'error');
            }
        });
    } else if (Notification.permission === 'granted') {
        showReminderDialog(userPlantId, plantName);
    } else {
        showNotification('❌ Notifications are blocked. Please enable them in browser settings.', 'error');
    }
}

function showReminderDialog(userPlantId, plantName) {
    // Create a simple prompt-based dialog for demo purposes
    // In a real app, this would be a proper modal dialog
    const reminderType = prompt(
        `Set a reminder for ${plantName}:\n\n` +
        "Choose reminder type:\n" +
        "1. Water (every few days)\n" +
        "2. Fertilize (weekly/monthly)\n" +
        "3. Prune (seasonal)\n" +
        "4. Custom\n\n" +
        "Enter 1, 2, 3, or 4:"
    );
    
    if (!reminderType || !['1', '2', '3', '4'].includes(reminderType)) {
        return;
    }
    
    const reminderTypes = {
        '1': { name: 'Water', defaultDays: 3, action: 'watering' },
        '2': { name: 'Fertilize', defaultDays: 14, action: 'fertilizing' },
        '3': { name: 'Prune', defaultDays: 90, action: 'pruning' },
        '4': { name: 'Custom', defaultDays: 7, action: 'caring for' }
    };
    
    const selectedType = reminderTypes[reminderType];
    
    let reminderDays;
    if (reminderType === '4') {
        // Custom reminder
        const customTask = prompt(`Enter custom task for ${plantName}:`);
        if (!customTask) return;
        
        reminderDays = parseInt(prompt(
            `How many days from now should you be reminded about "${customTask}" for ${plantName}?\n\n` +
            "Enter number of days:"
        ));
        
        if (isNaN(reminderDays) || reminderDays < 1) {
            showNotification('❌ Invalid number of days', 'error');
            return;
        }
        
        selectedType.name = customTask;
        selectedType.action = customTask.toLowerCase();
    } else {
        // Standard reminder
        reminderDays = parseInt(prompt(
            `Set reminder for ${selectedType.name.toLowerCase()} ${plantName}\n\n` +
            `Default: every ${selectedType.defaultDays} days\n` +
            "Enter number of days (or press OK for default):"
        )) || selectedType.defaultDays;
        
        if (isNaN(reminderDays) || reminderDays < 1) {
            reminderDays = selectedType.defaultDays;
        }
    }
    
    // Set the reminder
    const reminderTime = reminderDays * 24 * 60 * 60 * 1000; // Convert days to milliseconds
    const reminderDate = new Date(Date.now() + reminderTime);
    
    // Store reminder (in a real app, this would be saved to backend)
    const reminderId = Date.now(); // Simple ID generation
    const reminderData = {
        id: reminderId,
        userPlantId: userPlantId,
        plantName: plantName,
        task: selectedType.name,
        action: selectedType.action,
        scheduledFor: reminderDate.toISOString(),
        created: new Date().toISOString()
    };
    
    // Get existing reminders from localStorage
    const existingReminders = JSON.parse(localStorage.getItem('floraFindReminders') || '[]');
    existingReminders.push(reminderData);
    localStorage.setItem('floraFindReminders', JSON.stringify(existingReminders));
    
    // Schedule the actual notification
    setTimeout(() => {
        if (Notification.permission === 'granted') {
            new Notification(`🌱 FloraFind Reminder: ${selectedType.name}`, {
                body: `Time for ${selectedType.action} ${plantName}!`,
                icon: 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/325/seedling_1f331.png',
                tag: `reminder-${reminderId}` // Prevents duplicate notifications
            });
        }
    }, reminderTime);
    
    // Show confirmation
    const reminderDateStr = reminderDate.toLocaleDateString() + ' at ' + reminderDate.toLocaleTimeString();
    showNotification(
        `🔔 Reminder set for ${plantName}! You'll be notified to ${selectedType.action} on ${reminderDateStr}`,
        'success'
    );
    
    // For demo purposes, also schedule a quick demo notification in 5 seconds
    setTimeout(() => {
        if (Notification.permission === 'granted') {
            new Notification(`🌱 FloraFind Demo Reminder`, {
                body: `This is how your reminder for ${selectedType.action} ${plantName} will look!`,
                icon: 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/325/seedling_1f331.png'
            });
        }
    }, 5000);
}

async function addCustomCareTask(userPlantId, plantName) {
    // Create a simple prompt-based dialog for demo purposes
    // In a real app, this would be a proper modal dialog
    const taskType = prompt(
        `Add a care task for ${plantName}:\n\n` +
        "Choose task type:\n" +
        "1. Watering\n" +
        "2. Fertilizing\n" +
        "3. Pruning\n" +
        "4. Repotting\n" +
        "5. Pest Check\n" +
        "6. Custom Task\n\n" +
        "Enter 1, 2, 3, 4, 5, or 6:"
    );
    
    if (!taskType || !['1', '2', '3', '4', '5', '6'].includes(taskType)) {
        return;
    }
    
    const taskTypes = {
        '1': { name: 'watering', defaultDays: 3 },
        '2': { name: 'fertilizing', defaultDays: 30 },
        '3': { name: 'pruning', defaultDays: 90 },
        '4': { name: 'repotting', defaultDays: 365 },
        '5': { name: 'pest_check', defaultDays: 14 },
        '6': { name: 'custom', defaultDays: 7 }
    };
    
    let selectedTask = taskTypes[taskType];
    
    if (taskType === '6') {
        // Custom task
        const customTaskName = prompt(`Enter custom task name for ${plantName}:`);
        if (!customTaskName) return;
        
        selectedTask.name = customTaskName.toLowerCase().replace(/\s+/g, '_');
    }
    
    // Get frequency
    const frequencyDays = parseInt(prompt(
        `How often should this task repeat for ${plantName}?\n\n` +
        `Default for ${selectedTask.name}: every ${selectedTask.defaultDays} days\n\n` +
        "Enter number of days (or press OK for default):"
    )) || selectedTask.defaultDays;
    
    if (isNaN(frequencyDays) || frequencyDays < 1) {
        showNotification('❌ Invalid number of days', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/add_care_task`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_plant_id: userPlantId,
                task_type: selectedTask.name,
                frequency_days: frequencyDays
            })
        });
        
        const result = await response.json();
        if (result.success) {
            showNotification(`✅ ${result.message}`, 'success');
            loadUserGarden(); // Refresh garden to show new task
        } else {
            showNotification('❌ Failed to add care task', 'error');
        }
    } catch (error) {
        console.error('Error adding care task:', error);
        showNotification('❌ Error adding care task', 'error');
    }
}

function editPlantNotes(userPlantId, plantName) {
    // Get current notes (in a real app, this would fetch from backend)
    const existingNotes = localStorage.getItem(`plantNotes_${userPlantId}`) || '';
    
    // Simple prompt for demo purposes (in a real app, this would be a proper modal)
    const newNotes = prompt(`Edit notes for ${plantName}:\n\nCurrent notes: ${existingNotes || 'No notes yet'}\n\nEnter new notes:`, existingNotes);
    
    // If user didn't cancel
    if (newNotes !== null) {
        // Save notes (in a real app, this would save to backend)
        localStorage.setItem(`plantNotes_${userPlantId}`, newNotes);
        
        // Show confirmation
        if (newNotes.trim()) {
            showNotification(`📝 Notes updated for ${plantName}!`, 'success');
        } else {
            showNotification(`📝 Notes cleared for ${plantName}!`, 'info');
        }
        
        // Refresh garden to show updated notes
        loadUserGarden();
    }
}

// User Stats and Achievements
async function loadUserStats() {
    // Mock user stats for now
    userStats = { points: 250, level: 2, badges: 3 };
    updateUserStatsDisplay();
}

function updateUserStatsDisplay() {
    // Add null checks to prevent errors if elements don't exist
    const userPointsEl = document.getElementById('userPoints');
    const userLevelEl = document.getElementById('userLevel');
    const totalBadgesEl = document.getElementById('totalBadges');
    
    if (userPointsEl) userPointsEl.textContent = userStats.points;
    if (userLevelEl) userLevelEl.textContent = userStats.level;
    if (totalBadgesEl) totalBadgesEl.textContent = userStats.badges;
}

async function checkAchievements() {
    // Mock achievement check
    const achievements = [
        { name: 'Green Thumb', description: 'Care for your first plant for 30 days', points: 100 },
        { name: 'Plant Parent', description: 'Add 5 plants to your garden', points: 150 }
    ];
    
    // Simulate achievement unlock
    if (Math.random() > 0.7) {
        const achievement = achievements[Math.floor(Math.random() * achievements.length)];
        showAchievement(achievement);
    }
}

function showAchievement(achievement) {
    const popup = document.getElementById('achievement-popup');
    if (!popup) return;
    
    document.getElementById('achievement-badge-name').textContent = achievement.name;
    document.getElementById('achievement-badge-desc').textContent = achievement.description;
    document.getElementById('achievement-points').textContent = achievement.points;
    
    popup.style.display = 'flex';
}

function closeAchievement() {
    const popup = document.getElementById('achievement-popup');
    if (popup) {
        popup.style.display = 'none';
    }
}

// Location and Language Functions
function getUserLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                // For demo, we'll use a mock location
                userLocation = "Mumbai, India";
            },
            (error) => {
                console.log('Location access denied');
            }
        );
    }
}

async function showLocationSuggestions() {
    if (!userLocation) {
        userLocation = prompt("Enter your city name:") || "Mumbai";
    }
    
    try {
        const response = await fetch(`${API_URL}/location_suggestions?city=${userLocation}`);
        const data = await response.json();
        displayLocationSuggestions(data);
    } catch (error) {
        console.error('Error getting location suggestions:', error);
        showNotification('Error getting location-based suggestions', 'error');
    }
}

function displayLocationSuggestions(data) {
    let html = `
        <div style="background: var(--surface); border-radius: 15px; padding: 2rem; margin: 1rem 0; box-shadow: 0 10px 30px var(--shadow);">
            <h3 style="color: var(--primary-green); margin-bottom: 1rem;">
                🌍 Plants for ${data.location}
            </h3>
    `;
    
    if (data.eco_tips && data.eco_tips.length > 0) {
        html += `
            <div style="background: var(--very-light-green); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
                <h4>🌿 Eco Tips:</h4>
                <ul style="margin-left: 1rem;">
                    ${data.eco_tips.map(tip => `<li>${tip}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    if (data.climate_suggestions && data.climate_suggestions.length > 0) {
        html += formatPlantCards(data.climate_suggestions, data.total_eco_impact);
    }
    
    html += '</div>';
    addMessage(html, "bot");
}

function getLocation() {
    getUserLocation();
    if (userLocation) {
        showLocationSuggestions();
    }
}

function toggleLanguage() {
    const languages = ['en', 'hi', 'es'];
    const currentIndex = languages.indexOf(currentLanguage);
    currentLanguage = languages[(currentIndex + 1) % languages.length];
    updateLanguageDisplay();
    showNotification(`Language changed to ${currentLanguage.toUpperCase()}`, 'info');
}

function updateLanguageDisplay() {
    document.getElementById('currentLang').textContent = currentLanguage.toUpperCase();
}

// Utility Functions
function showSuggestions(inputText) {
    const suggestionsBox = document.getElementById("suggestions");
    suggestionsBox.innerHTML = "";
    if (!inputText) return;
    
    const sampleQueries = [
        "Summer plants for beginners",
        "How to care for roses",
        "Indoor plants low light",
        "What grows in monsoon?",
        "Best plants for tropical climate",
        "Native plants Mumbai",
        "Tulsi care instructions"
    ];
    
    const filtered = sampleQueries.filter(q =>
        q.toLowerCase().includes(inputText.toLowerCase())
    );
    
    filtered.forEach(q => {
        const div = document.createElement("div");
        div.className = "suggestion-item";
        div.textContent = q;
        div.onclick = () => {
            document.getElementById("chatBox").value = q;
            suggestionsBox.innerHTML = "";
        };
        suggestionsBox.appendChild(div);
    });
}

function showNotification(message, type = 'info') {
    const container = document.getElementById('notification-container');
    if (!container) return;
    
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" 
                    style="background: none; border: none; color: var(--text-secondary); cursor: pointer;">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    container.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Event Listeners
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && document.activeElement.id === 'chatBox') {
        sendMessage();
    }
});

// Initialize suggestions
document.getElementById('chatBox').addEventListener('input', (e) => {
    showSuggestions(e.target.value);
});

// Close suggestions when clicking outside
document.addEventListener('click', (e) => {
    if (!e.target.closest('.input-section')) {
        document.getElementById('suggestions').innerHTML = '';
    }
});
