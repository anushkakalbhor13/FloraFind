-- Enhanced FloraFind Database Schema
SHOW DATABASES;
CREATE DATABASE IF NOT EXISTS florafind;
USE florafind;

-- Enhanced Plants table with more comprehensive data
CREATE TABLE plants (
    plant_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    scientific_name VARCHAR(150),
    season VARCHAR(50),
    climate VARCHAR(100),
    care_instructions TEXT,
    watering_frequency_summer INT, -- days between watering in summer
    watering_frequency_winter INT, -- days between watering in winter 
    watering_frequency_monsoon INT, -- days between watering in monsoon
    sunlight_requirement ENUM('full_sun', 'partial_shade', 'full_shade'),
    soil_type VARCHAR(100),
    growth_height VARCHAR(50), -- expected height at maturity
    growth_time_months INT, -- time to reach maturity in months
    difficulty_level ENUM('beginner', 'intermediate', 'expert'),
    native_region VARCHAR(100),
    eco_benefits TEXT, -- carbon sequestration, biodiversity benefits
    eco_impact_score INT DEFAULT 0, -- 1-10 rating
    cultural_significance TEXT, -- regional/cultural uses and lore
    medicinal_properties TEXT,
    ar_model_url VARCHAR(255), -- 3D model for AR visualization
    care_tips_detailed JSON, -- detailed care calendar info
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Enhanced Users table with gamification and preferences
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    location VARCHAR(100),
    preferred_language ENUM('en', 'hi', 'es', 'fr', 'de') DEFAULT 'en',
    plant_health_points INT DEFAULT 0,
    level INT DEFAULT 1,
    badges JSON, -- array of earned badges
    notification_preferences JSON, -- email, sms, push preferences
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- User's personal garden/plant collection
CREATE TABLE user_plants (
    user_plant_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    plant_id INT NOT NULL,
    plant_nickname VARCHAR(100), -- user's custom name for their plant
    date_planted DATE,
    location_in_garden VARCHAR(100), -- "front yard", "balcony", etc.
    current_health_score INT DEFAULT 100, -- 0-100 health rating
    last_watered DATE,
    last_fertilized DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (plant_id) REFERENCES plants(plant_id) ON DELETE CASCADE
);

-- Care Calendar and Reminders
CREATE TABLE care_schedules (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    user_plant_id INT NOT NULL,
    task_type ENUM('watering', 'fertilizing', 'pruning', 'repotting', 'pest_check') NOT NULL,
    frequency_days INT NOT NULL, -- repeat every X days
    next_due_date DATE NOT NULL,
    seasonal_adjustment JSON, -- different schedules for different seasons
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_plant_id) REFERENCES user_plants(user_plant_id) ON DELETE CASCADE
);

-- Care activity logs for gamification
CREATE TABLE care_activities (
    activity_id INT AUTO_INCREMENT PRIMARY KEY,
    user_plant_id INT NOT NULL,
    task_type ENUM('watering', 'fertilizing', 'pruning', 'repotting', 'pest_check', 'photo_upload') NOT NULL,
    completed_date DATE NOT NULL,
    points_earned INT DEFAULT 0,
    notes TEXT,
    photo_url VARCHAR(255),
    weather_conditions VARCHAR(100), -- optional weather context
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_plant_id) REFERENCES user_plants(user_plant_id) ON DELETE CASCADE
);

-- Community Features - User Submissions
CREATE TABLE plant_submissions (
    submission_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    plant_name VARCHAR(100) NOT NULL,
    scientific_name VARCHAR(150),
    care_tip TEXT NOT NULL,
    photo_url VARCHAR(255),
    location VARCHAR(100),
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    admin_notes TEXT,
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    review_date TIMESTAMP NULL,
    votes_up INT DEFAULT 0,
    votes_down INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Community Challenges and Events
CREATE TABLE plant_challenges (
    challenge_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    challenge_type ENUM('growth', 'care_streak', 'photo_contest', 'eco_impact') NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    prize_description TEXT,
    participation_requirements JSON, -- specific rules/requirements
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Challenge Participations
CREATE TABLE challenge_participations (
    participation_id INT AUTO_INCREMENT PRIMARY KEY,
    challenge_id INT NOT NULL,
    user_id INT NOT NULL,
    user_plant_id INT,
    submission_data JSON, -- photos, measurements, etc.
    score INT DEFAULT 0,
    ranking INT,
    joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (challenge_id) REFERENCES plant_challenges(challenge_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (user_plant_id) REFERENCES user_plants(user_plant_id) ON DELETE SET NULL
);

-- Badges and Achievements
CREATE TABLE badges (
    badge_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon_url VARCHAR(255),
    requirements JSON, -- criteria to earn the badge
    points_value INT DEFAULT 0,
    rarity ENUM('common', 'uncommon', 'rare', 'legendary') DEFAULT 'common',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Badge Achievements
CREATE TABLE user_badges (
    user_badge_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    badge_id INT NOT NULL,
    earned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (badge_id) REFERENCES badges(badge_id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_badge (user_id, badge_id)
);

-- Weather and Location Data Cache
CREATE TABLE location_weather (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    current_weather JSON, -- cached weather data
    native_plants JSON, -- list of native plant IDs
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_location (city, country)
);

-- Multilingual Content
CREATE TABLE plant_translations (
    translation_id INT AUTO_INCREMENT PRIMARY KEY,
    plant_id INT NOT NULL,
    language_code VARCHAR(5) NOT NULL,
    name_translated VARCHAR(100),
    care_instructions_translated TEXT,
    cultural_significance_translated TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plant_id) REFERENCES plants(plant_id) ON DELETE CASCADE,
    UNIQUE KEY unique_plant_language (plant_id, language_code)
);

-- Enhanced Search Logs with analytics
CREATE TABLE search_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    query TEXT NOT NULL,
    language_detected VARCHAR(5),
    results_count INT DEFAULT 0,
    user_location VARCHAR(100),
    search_type ENUM('text', 'voice', 'image') DEFAULT 'text',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

-- Notification Queue
CREATE TABLE notification_queue (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    type ENUM('care_reminder', 'achievement', 'challenge', 'community') NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    delivery_method ENUM('email', 'sms', 'push', 'in_app') NOT NULL,
    scheduled_time TIMESTAMP NOT NULL,
    sent_time TIMESTAMP NULL,
    status ENUM('pending', 'sent', 'failed') DEFAULT 'pending',
    metadata JSON, -- additional data for the notification
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

SHOW TABLES;
