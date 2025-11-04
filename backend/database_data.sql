-- Enhanced FloraFind Seed Data
USE florafind;

-- Insert comprehensive plant data including fruits for all seasons
INSERT INTO plants (name, scientific_name, season, climate, care_instructions, 
    watering_frequency_summer, watering_frequency_winter, watering_frequency_monsoon,
    sunlight_requirement, soil_type, growth_height, growth_time_months, 
    difficulty_level, native_region, eco_benefits, eco_impact_score, 
    cultural_significance, medicinal_properties, ar_model_url, care_tips_detailed) VALUES

('Rose', 'Rosa', 'spring,summer', 'temperate,tropical', 
'Roses require regular watering, well-draining soil, and at least 6 hours of sunlight daily. Prune in late winter and apply mulch around the base.',
2, 4, 3, 'full_sun', 'loamy,well-draining', '1-3 feet', 6, 'intermediate', 'Asia,Europe',
'Attracts pollinators, moderate carbon sequestration, supports beneficial insects', 7,
'Symbol of love and beauty across cultures. Used in Persian gardens, Victorian flower language. Rose water used in Middle Eastern cuisine.',
'Rose hips rich in Vitamin C, petals used in aromatherapy, anti-inflammatory properties',
'/models/rose_bush.glb',
'{"spring": {"watering": "every 2 days", "fertilizing": "monthly", "pruning": "deadhead spent blooms"}, "summer": {"watering": "daily in heat", "fertilizing": "bi-weekly", "pest_check": "weekly for aphids"}, "winter": {"watering": "weekly", "pruning": "major pruning in late winter", "protection": "mulch around base"}}'),

('Tulsi', 'Ocimum tenuiflorum', 'summer,monsoon', 'tropical,humid', 
'Sacred basil thrives in warm weather with regular watering. Pinch flowers to encourage leaf growth. Harvest leaves regularly.',
1, 3, 2, 'full_sun', 'well-draining', '1-3 feet', 3, 'beginner', 'India',
'Excellent air purifier, attracts beneficial insects, natural pest deterrent', 9,
'Sacred in Hinduism, planted in courtyards for spiritual significance. Used in daily prayers and rituals. Called "Queen of Herbs" in Ayurveda.',
'Adaptogenic properties, boosts immunity, anti-stress, respiratory health, used in traditional Indian medicine for centuries',
'/models/tulsi_plant.glb',
'{"summer": {"watering": "daily", "harvesting": "morning harvest for maximum potency", "pest_check": "natural pest resistance"}, "monsoon": {"watering": "every 2 days", "drainage": "ensure good drainage"}, "winter": {"watering": "every 3 days", "protection": "bring indoors in cold climates"}}'),

('Neem', 'Azadirachta indica', 'all_seasons', 'tropical,arid', 
'Neem is drought-tolerant once established. Water deeply but infrequently. Can grow in poor soil conditions.',
7, 10, 5, 'full_sun', 'sandy,clay', '15-20 feet', 24, 'beginner', 'India,Myanmar',
'High carbon sequestration, natural pesticide, improves soil quality, supports biodiversity', 10,
'Village pharmacy tree in India. Used in Ayurveda for thousands of years. Planted for shade and natural pest control in agricultural areas.',
'Natural antiseptic, antifungal, antibacterial. Leaves, bark, and oil used in traditional medicine. Supports oral health.',
'/models/neem_tree.glb',
'{"general": {"watering": "deep watering weekly", "pruning": "remove dead branches", "harvesting": "leaves year-round"}, "benefits": {"pest_control": "natural insecticide for garden", "medicinal": "harvest young leaves and bark"}}'),

('Sunflower', 'Helianthus annuus', 'summer', 'temperate,warm', 
'Sunflowers need full sun and regular watering. Support tall varieties with stakes. Face east to track the sun.',
2, 5, 3, 'full_sun', 'well-draining', '6-10 feet', 4, 'beginner', 'North America',
'Attracts pollinators, phytoremediates soil, provides bird food, moderate carbon storage', 8,
'Symbol of loyalty and devotion. Used by Native Americans for food and dye. Associated with solar deities in many cultures.',
'Seeds rich in Vitamin E and healthy fats. Oil used for cooking. Stalks used in traditional crafts.',
'/models/sunflower.glb',
'{"summer": {"watering": "deep watering every 2 days", "staking": "support tall varieties", "deadheading": "remove spent blooms"}, "harvesting": {"seeds": "harvest when back of flower turns brown"}}'),

('Lavender', 'Lavandula', 'spring,summer', 'mediterranean,dry', 
'Lavender prefers well-draining soil and minimal watering once established. Prune after flowering to maintain shape.',
5, 10, 7, 'full_sun', 'sandy,well-draining', '1-4 feet', 12, 'intermediate', 'Mediterranean',
'Attracts pollinators, drought-resistant, supports beneficial insects, aromatic properties', 7,

-- Adding fruit plants for summer
('Watermelon', 'Citrullus lanatus', 'summer', 'warm,tropical', 
'Watermelon needs consistent moisture and full sun. Plant in well-draining soil and provide plenty of space for vines to spread.',
1, 0, 2, 'full_sun', 'sandy,loamy', 'vine spread 10-15 feet', 3, 'intermediate', 'Africa',
'Provides ground cover, attracts pollinators, high water content fruit for wildlife', 6,
'Popular summer fruit across cultures. Used in traditional celebrations and summer festivals.',
'High water content, vitamins A and C, lycopene with antioxidant properties',
'/models/watermelon.glb',
'{"summer": {"watering": "daily", "spacing": "6-8 feet between plants", "harvesting": "when underside turns yellow"}}'),

('Strawberry', 'Fragaria × ananassa', 'spring,summer', 'temperate,cool', 
'Strawberries need regular watering and rich soil. Mulch to prevent fruit contact with soil and protect from frost.',
2, 5, 3, 'full_sun,partial_shade', 'loamy,rich', '8-12 inches', 2, 'beginner', 'North America,Europe',
'Excellent ground cover, erosion control, attracts beneficial insects', 8,
'Symbol of perfection and purity in many cultures. Used in traditional desserts worldwide.',
'Rich in vitamin C, antioxidants, and fiber. Used in traditional remedies for skin health.',
'/models/strawberry.glb',
'{"spring": {"planting": "early spring", "mulching": "pine straw or clean hay"}, "summer": {"watering": "every 2 days", "harvesting": "when fully red"}}'),

('Blueberry', 'Vaccinium corymbosum', 'summer', 'temperate,cool', 
'Blueberries require acidic soil and consistent moisture. Mulch with pine needles or acidic compost.',
2, 4, 3, 'full_sun,partial_shade', 'acidic,well-draining', '4-6 feet', 24, 'intermediate', 'North America',
'Supports native wildlife, excellent carbon sequestration, provides habitat', 9,
'Important food source for indigenous North American peoples. Symbol of health and longevity.',
'High in antioxidants, particularly anthocyanins. Supports eye health and cognitive function.',
'/models/blueberry.glb',
'{"summer": {"watering": "consistent moisture", "mulching": "pine needles", "harvesting": "when berries turn deep blue"}}'),

('Mango', 'Mangifera indica', 'summer', 'tropical,warm', 
'Mango trees need full sun and protection from frost. Water deeply but infrequently once established.',
3, 7, 2, 'full_sun', 'well-draining,loamy', '30-100 feet', 60, 'advanced', 'India,Southeast Asia',
'Significant carbon sequestration, provides habitat, supports biodiversity', 10,
'National fruit of India, Philippines, and Pakistan. Symbol of love in many cultures.',
'Rich in vitamins A, C, and E. Contains enzymes that aid digestion. Used in Ayurvedic medicine.',
'/models/mango.glb',
'{"summer": {"watering": "deep watering weekly", "pruning": "after fruiting", "harvesting": "when fruit yields to gentle pressure"}}'),
'Used in French perfumery and cuisine. Symbol of purity and cleanliness. Traditional use in wedding ceremonies and linen storage.',
'Natural relaxant, aromatherapy uses, antiseptic properties, helps with sleep and anxiety',
'/models/lavender_bush.glb',
'{"spring": {"pruning": "prune after last frost", "planting": "best time to plant"}, "summer": {"watering": "minimal - drought tolerant", "harvesting": "harvest flowers in morning"}, "general": {"soil": "ensure excellent drainage", "spacing": "allow air circulation"}}'),

('Aloe Vera', 'Aloe barbadensis', 'all_seasons', 'arid,dry', 
'Aloe vera is highly drought-tolerant. Water only when soil is completely dry. Excellent indoor plant.',
10, 15, 12, 'partial_shade', 'sandy,cactus-mix', '1-2 feet', 6, 'beginner', 'Arabian Peninsula',
'Low water requirements, air purifying, minimal maintenance, supports xerophytic ecosystems', 6,
'Called "plant of immortality" by ancient Egyptians. Used in traditional medicine across cultures. Symbol of healing and protection.',
'Gel used for burns, skin conditions, digestive health. Rich in vitamins and minerals. Natural moisturizer.',
'/models/aloe_plant.glb',
'{"care": {"watering": "only when soil completely dry", "light": "bright indirect light best", "soil": "fast-draining cactus mix"}, "harvesting": {"gel": "cut outer leaves for gel extraction"}, "propagation": {"offsets": "remove and replant baby plants"}}'),

('Marigold', 'Tagetes', 'summer,monsoon', 'tropical,temperate', 
'Marigolds are easy to grow and bloom continuously. Deadhead regularly for more flowers. Natural pest deterrent.',
2, 4, 3, 'full_sun', 'well-draining', '6 inches-3 feet', 2, 'beginner', 'Mexico,Central America',
'Companion planting benefits, attracts pollinators, natural pest control, supports beneficial insects', 8,
'Sacred flowers in Hindu and Mexican cultures. Used in Day of the Dead celebrations. Symbol of passion and creativity.',
'Edible petals, anti-inflammatory properties, used in traditional healing for skin conditions',
'/models/marigold.glb',
'{"summer": {"watering": "regular but not excessive", "deadheading": "remove spent blooms daily", "companion_planting": "plant with tomatoes and peppers"}, "pest_control": {"natural": "deters nematodes and aphids"}}'),

('Bamboo', 'Bambuseae', 'all_seasons', 'tropical,temperate', 
'Bamboo grows rapidly with regular watering. Contains spreading with barriers. Harvest mature canes sustainably.',
3, 5, 2, 'partial_shade', 'moist,well-draining', '10-100 feet', 12, 'intermediate', 'Asia',
'Highest carbon sequestration rate, prevents soil erosion, renewable resource, oxygen producer', 10,
'Symbol of flexibility and strength in Asian cultures. Used in construction, crafts, and music instruments. Represents prosperity.',
'Young shoots edible and nutritious. Used in traditional construction and paper making.',
'/models/bamboo_grove.glb',
'{"growth": {"watering": "keep soil moist", "containment": "use barriers for clumping varieties", "harvesting": "harvest 3-5 year old canes"}, "sustainability": {"carbon": "fastest carbon sequestration", "renewable": "harvest without killing plant"}}'),

('Jasmine', 'Jasminum', 'spring,summer', 'tropical,subtropical', 
'Jasmine needs regular watering and support for climbing varieties. Prune after flowering to control growth.',
3, 5, 4, 'full_sun', 'well-draining,fertile', '3-15 feet', 8, 'intermediate', 'Himalaya,Asia',
'Attracts night pollinators, aromatic properties, supports nocturnal wildlife', 7,
'Sacred in many Asian cultures. Used in wedding ceremonies and religious rituals. Symbol of love and sensuality.',
'Flowers used in perfumery and tea. Aromatherapy benefits for relaxation and mood enhancement.',
'/models/jasmine_vine.glb',
'{"flowering": {"watering": "consistent moisture during blooming", "support": "provide trellis for climbers", "harvesting": "pick flowers at dawn for strongest scent"}, "pruning": {"timing": "after flowering season", "method": "light pruning to maintain shape"}}'),

('Mint', 'Mentha', 'spring,summer,monsoon', 'temperate,humid', 
'Mint spreads rapidly and prefers moist soil. Grow in containers to control spread. Harvest regularly to encourage growth.',
1, 3, 2, 'partial_shade', 'moist,fertile', '1-2 feet', 2, 'beginner', 'Europe,Asia',
'Ground cover, attracts beneficial insects, natural pest deterrent, culinary value', 6,
'Used in Middle Eastern, Indian, and Mediterranean cuisines. Symbol of hospitality. Traditional digestive aid.',
'Digestive properties, natural breath freshener, antimicrobial effects, rich in antioxidants',
'/models/mint_plant.glb',
'{"growing": {"containment": "grow in pots to prevent spreading", "watering": "keep soil consistently moist", "harvesting": "pinch flowers to encourage leaf growth"}, "culinary": {"best_time": "harvest leaves in morning after dew dries"}}');

-- Insert sample badges
INSERT INTO badges (name, description, icon_url, requirements, points_value, rarity) VALUES
('Green Thumb', 'Successfully care for your first plant for 30 days', '/icons/green_thumb.png', '{"care_streak": 30, "plant_count": 1}', 100, 'common'),
('Plant Parent', 'Add 5 plants to your garden', '/icons/plant_parent.png', '{"plant_count": 5}', 150, 'common'),
('Water Warrior', 'Complete 50 watering tasks', '/icons/water_warrior.png', '{"watering_count": 50}', 200, 'uncommon'),
('Harvest Hero', 'Harvest from your plants 25 times', '/icons/harvest_hero.png', '{"harvest_count": 25}', 250, 'uncommon'),
('Eco Champion', 'Grow plants with total eco-impact score of 50+', '/icons/eco_champion.png', '{"eco_score": 50}', 400, 'rare'),
('Garden Guru', 'Maintain 10 healthy plants simultaneously', '/icons/garden_guru.png', '{"plant_count": 10, "health_threshold": 80}', 500, 'rare'),
('Seasonal Sage', 'Successfully care for plants through all 4 seasons', '/icons/seasonal_sage.png', '{"seasons_completed": 4}', 600, 'legendary'),
('Community Helper', 'Submit 10 approved plant care tips', '/icons/community_helper.png', '{"approved_submissions": 10}', 300, 'uncommon');

-- Insert sample plant challenges
INSERT INTO plant_challenges (title, description, challenge_type, start_date, end_date, prize_description, participation_requirements) VALUES
('Tallest Sunflower Challenge', 'Grow the tallest sunflower this summer! Upload photos monthly to track progress.', 'growth', '2024-03-01', '2024-09-30', 'Premium seeds package and garden tools', '{"plant_type": "sunflower", "photo_frequency": "monthly", "measurement_required": true}'),
('30-Day Care Streak', 'Maintain perfect care for 30 consecutive days', 'care_streak', '2024-01-01', '2024-12-31', 'Exclusive care calendar and plant health monitor', '{"streak_length": 30, "perfect_score": true}'),
('Best Garden Photo Contest', 'Share your most beautiful garden photo', 'photo_contest', '2024-04-01', '2024-04-30', 'Professional photography session with plants', '{"photo_quality": "high", "original_content": true}'),
('Carbon Capture Champions', 'Collectively plant trees with highest carbon sequestration', 'eco_impact', '2024-02-01', '2024-12-31', 'Tree planted in your honor in urban forest', '{"eco_score_minimum": 8, "collective_goal": 1000}');

-- Insert multilingual translations (Hindi examples)
INSERT INTO plant_translations (plant_id, language_code, name_translated, care_instructions_translated, cultural_significance_translated) VALUES
(2, 'hi', 'तुलसी', 'तुलसी को नियमित पानी और धूप की जरूरत होती है। फूलों को तोड़ते रहें ताकि पत्तियां बढ़ती रहें।', 'हिंदू धर्म में पवित्र पौधा। घरों के आंगन में लगाया जाता है और पूजा में उपयोग होता है।'),
(3, 'hi', 'नीम', 'नीम सूखा सहने वाला पेड़ है। कम पानी की जरूरत होती है। किसी भी मिट्टी में उग सकता है।', 'भारत में गांव की फार्मेसी कहलाता है। आयुर्वेद में हजारों साल से उपयोग।');

-- Insert sample location weather data
INSERT INTO location_weather (city, country, latitude, longitude, current_weather, native_plants) VALUES
('Mumbai', 'India', 19.0760, 72.8777, '{"temp": 28, "humidity": 85, "rainfall": "high", "season": "monsoon"}', '[2, 3, 7]'),
('Delhi', 'India', 28.7041, 77.1025, '{"temp": 32, "humidity": 60, "rainfall": "low", "season": "summer"}', '[1, 2, 3, 9]'),
('Bangalore', 'India', 12.9716, 77.5946, '{"temp": 24, "humidity": 70, "rainfall": "medium", "season": "pleasant"}', '[2, 5, 8, 9]');

-- Insert sample users for testing
INSERT INTO users (username, password, email, phone, location, preferred_language, plant_health_points, level) VALUES
('demo_user', 'hashed_password_123', 'demo@florafind.com', '+1234567890', 'Mumbai, India', 'en', 250, 2),
('hindi_user', 'hashed_password_456', 'hindi@florafind.com', '+9876543210', 'Delhi, India', 'hi', 150, 1);

-- Insert sample user plants
INSERT INTO user_plants (user_id, plant_id, plant_nickname, date_planted, location_in_garden, current_health_score, last_watered, notes) VALUES
(1, 1, 'My Beautiful Rose', '2024-01-15', 'front garden', 90, '2024-01-20', 'Growing well, needs more fertilizer'),
(1, 2, 'Sacred Tulsi', '2024-01-10', 'kitchen window', 95, '2024-01-21', 'Very healthy, using leaves for tea'),
(2, 3, 'Neem Tree', '2023-06-01', 'backyard', 85, '2024-01-18', 'Large tree, provides good shade');

-- Insert sample care schedules
INSERT INTO care_schedules (user_plant_id, task_type, frequency_days, next_due_date, seasonal_adjustment) VALUES
(1, 'watering', 2, '2024-01-22', '{"summer": 1, "winter": 4, "monsoon": 3}'),
(1, 'fertilizing', 30, '2024-02-15', '{"spring": 21, "summer": 21, "winter": 45}'),
(2, 'watering', 1, '2024-01-22', '{"summer": 1, "winter": 3, "monsoon": 2}'),
(3, 'watering', 7, '2024-01-25', '{"summer": 5, "winter": 10, "monsoon": 7}');

-- Insert sample notifications
INSERT INTO notification_queue (user_id, type, title, message, delivery_method, scheduled_time, metadata) VALUES
(1, 'care_reminder', 'Time to water your Rose! 🌹', 'Your "My Beautiful Rose" needs watering today. Check soil moisture and water thoroughly.', 'email', '2024-01-22 09:00:00', '{"user_plant_id": 1, "task_type": "watering"}'),
(1, 'achievement', 'Badge Earned! 🎉', 'Congratulations! You earned the "Green Thumb" badge for 30 days of consistent care.', 'in_app', '2024-01-21 18:00:00', '{"badge_id": 1, "points_earned": 100}'),
(2, 'care_reminder', 'तुलसी को पानी दें! 💧', 'आपकी तुलसी को आज पानी की जरूरत है।', 'sms', '2024-01-22 08:00:00', '{"user_plant_id": 2, "task_type": "watering"}')
