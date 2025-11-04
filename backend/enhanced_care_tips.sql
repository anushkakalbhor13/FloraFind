-- Enhanced FloraFind Database with More Care Tips and Plants
USE florafind;

-- Add more plants with detailed care tips for summer beginners
INSERT INTO plants (name, scientific_name, season, climate, care_instructions, 
    watering_frequency_summer, watering_frequency_winter, watering_frequency_monsoon,
    sunlight_requirement, soil_type, growth_height, growth_time_months, 
    difficulty_level, native_region, eco_benefits, eco_impact_score, 
    cultural_significance, medicinal_properties, care_tips_detailed) VALUES

-- Summer Beginner Plants
('Zinnia', 'Zinnia elegans', 'summer', 'warm,tropical', 
'Zinnias are perfect for summer beginners. They love full sun and are drought tolerant once established. Deadhead regularly for continuous blooms.',
3, 5, 4, 'full_sun', 'well-draining', '1-4 feet', 3, 'beginner', 'Mexico',
'Attracts butterflies and pollinators, continuous summer color, low maintenance', 7,
'Popular in Mexican gardens and Day of the Dead celebrations. Represents endurance and lasting friendship.',
'Edible flowers, used in traditional medicine for wounds and inflammation',
'{"summer": {"watering": "water deeply every 3 days", "care": "deadhead spent blooms daily", "planting": "sow seeds after last frost"}, "general": {"fertilizing": "light feeding monthly", "pest_control": "naturally pest resistant"}}'),

('Portulaca', 'Portulaca grandiflora', 'summer', 'hot,dry', 
'Also called Moss Rose, perfect for hot summer conditions. Needs minimal water and thrives in poor soil. Great for beginners.',
7, 10, 5, 'full_sun', 'sandy,poor', '4-6 inches', 2, 'beginner', 'South America',
'Drought tolerant, low water needs, colorful ground cover', 6,
'Known as "10 o clock flower" in India. Popular in rock gardens and dry areas.',
'Used traditionally for treating burns and skin conditions',
'{"summer": {"watering": "water sparingly - drought tolerant", "care": "flowers open in morning sun", "soil": "thrives in poor, sandy soil"}, "propagation": {"seeds": "self-seeds readily"}}'),

('Vinca', 'Catharanthus roseus', 'summer,monsoon', 'tropical,humid', 
'Madagascar Periwinkle is excellent for hot, humid summers. Very low maintenance and blooms continuously.',
2, 4, 3, 'full_sun', 'well-draining', '1-2 feet', 3, 'beginner', 'Madagascar',
'Heat tolerant, continuous blooms, drought resistant when established', 7,
'Sacred flower in Hindu culture, used in religious ceremonies and temple decorations.',
'Contains alkaloids used in cancer treatment research, traditional fever remedy',
'{"summer": {"watering": "every 2-3 days", "heat_tolerance": "thrives in extreme heat", "blooming": "flowers continuously"}, "care": {"pruning": "pinch tips for bushier growth"}}'),

-- Indoor Plants for Beginners
('Peace Lily', 'Spathiphyllum', 'all_seasons', 'indoor,humid', 
'Perfect indoor plant for beginners. Low light tolerant and tells you when it needs water by drooping.',
3, 4, 3, 'partial_shade', 'potting-mix', '1-3 feet', 6, 'beginner', 'Tropical Americas',
'Air purifying, removes toxins, adds humidity to indoor air', 8,
'Symbol of peace and prosperity. Popular houseplant worldwide for air purification.',
'NASA study shows it removes harmful chemicals from indoor air',
'{"indoor_care": {"light": "bright indirect light best", "watering": "water when leaves droop slightly", "humidity": "mist leaves regularly"}, "signs": {"thirsty": "leaves droop when needs water", "happy": "white blooms indicate good health"}}'),

('Snake Plant', 'Sansevieria trifasciata', 'all_seasons', 'indoor,dry', 
'Extremely hardy indoor plant, perfect for beginners. Tolerates neglect and low light conditions.',
10, 15, 12, 'partial_shade', 'cactus-mix', '1-4 feet', 12, 'beginner', 'West Africa',
'Excellent air purifier, produces oxygen at night, very low maintenance', 9,
'Called "Mother-in-Law\'s Tongue" in many cultures. Symbol of patience and persistence.',
'Releases oxygen at night, improving sleep quality. Used in traditional medicine.',
'{"care": {"watering": "water only when soil completely dry", "light": "tolerates low light", "neglect": "thrives with minimal care"}, "propagation": {"leaf_cuttings": "propagate from leaf cuttings"}}'),

-- More Summer Plants
('Celosia', 'Celosia argentea', 'summer', 'warm,humid', 
'Cockscomb flowers are heat-loving annuals perfect for summer gardens. Easy to grow from seeds.',
2, 4, 3, 'full_sun', 'fertile', '6 inches-3 feet', 3, 'beginner', 'Africa,South America',
'Attracts pollinators, heat tolerant, good cut flowers', 6,
'Used in African traditional medicine. Flowers symbolize immortality and unfading love.',
'Leaves and flowers are edible and nutritious, high in vitamins',
'{"summer": {"watering": "keep soil moist but not waterlogged", "heat": "loves hot weather", "cutting": "excellent for cut flowers"}, "harvesting": {"flowers": "cut in morning for longest vase life"}}'),

('Four O Clock', 'Mirabilis jalapa', 'summer,evening', 'warm,temperate', 
'Marvel of Peru opens flowers in late afternoon. Very easy to grow and self-seeds readily.',
3, 6, 4, 'full_sun', 'any', '2-3 feet', 3, 'beginner', 'Peru',
'Evening fragrance attracts night pollinators, self-seeding annual', 6,
'Called "4 o clock" because flowers open in late afternoon. Used in Peruvian folk medicine.',
'Roots used traditionally for medicinal purposes, leaves for skin conditions',
'{"unique": {"blooming_time": "flowers open around 4 PM", "fragrance": "sweet evening fragrance"}, "care": {"easy": "very low maintenance", "self_seeding": "will return next year from seeds"}}'),

-- Medicinal Plants for Beginners
('Lemon Balm', 'Melissa officinalis', 'spring,summer', 'temperate', 
'Easy-to-grow herb with lemony scent. Perfect for beginners interested in medicinal plants.',
2, 3, 2, 'partial_shade', 'moist', '1-2 feet', 2, 'beginner', 'Mediterranean',
'Attracts beneficial insects, natural pest deterrent, culinary and medicinal uses', 7,
'Used since ancient times for calming effects. Popular in monastery gardens.',
'Natural calming agent, helps with sleep and anxiety, digestive aid',
'{"growing": {"spreading": "can spread rapidly - contain in pots", "harvesting": "harvest leaves before flowering"}, "uses": {"tea": "make calming tea from fresh or dried leaves", "cooking": "use in salads and desserts"}}'),

('Chamomile', 'Matricaria chamomilla', 'spring,summer', 'cool,temperate', 
'German Chamomile is easy to grow and self-seeds. Perfect introduction to medicinal gardening.',
3, 4, 3, 'full_sun', 'well-draining', '1-2 feet', 3, 'beginner', 'Europe',
'Attracts beneficial insects, companion plant for vegetables, calming tea', 8,
'Ancient Egyptian sacred flower. Used for centuries in European folk medicine.',
'Famous for calming tea, anti-inflammatory properties, natural sleep aid',
'{"growing": {"self_seeding": "will self-seed in suitable conditions", "companion": "good companion for cabbage family"}, "harvesting": {"flowers": "harvest flowers when fully open in morning"}}');

-- Add more detailed care tips for existing plants
UPDATE plants SET care_tips_detailed = '{"summer": {"watering": "water deeply every 2 days in morning", "fertilizing": "rose fertilizer every 2 weeks", "deadheading": "remove spent blooms to encourage more flowers", "pest_control": "watch for aphids and spider mites"}, "spring": {"pruning": "major pruning in early spring", "planting": "best time to plant new roses", "fertilizing": "start feeding when new growth appears"}, "winter": {"protection": "mulch around base in cold areas", "pruning": "light pruning to remove dead wood"}, "general": {"soil": "prefers slightly acidic, well-draining soil", "spacing": "plant 3 feet apart for good air circulation"}}' 
WHERE name = 'Rose';

UPDATE plants SET care_tips_detailed = '{"daily_care": {"morning": "best time to harvest leaves", "watering": "water at base, avoid wetting leaves", "pinching": "pinch flower buds to keep leaves tender"}, "seasonal": {"summer": "provide afternoon shade in extreme heat", "monsoon": "ensure good drainage", "winter": "protect from frost"}, "spiritual": {"placement": "plant in east-facing area for spiritual benefits", "harvesting": "offer prayers before harvesting"}, "medicinal": {"preparation": "chew fresh leaves or make tea", "timing": "most potent when consumed on empty stomach"}}' 
WHERE name = 'Tulsi';

UPDATE plants SET care_tips_detailed = '{"long_term": {"establishment": "drought tolerant after first year", "pruning": "prune annually to maintain size", "harvesting": "sustainable leaf harvest year-round"}, "natural_pesticide": {"preparation": "boil leaves to make natural spray", "application": "spray on affected plants in evening"}, "medicinal": {"leaves": "fresh leaves for daily consumption", "bark": "bark for serious ailments", "oil": "neem oil for skin conditions"}, "environmental": {"companion_planting": "plant near vegetables for pest control", "soil_improvement": "leaves improve soil when composted"}}' 
WHERE name = 'Neem';

-- Add care tips table for quick reference
CREATE TABLE IF NOT EXISTS quick_care_tips (
    tip_id INT AUTO_INCREMENT PRIMARY KEY,
    plant_name VARCHAR(100),
    season ENUM('spring', 'summer', 'monsoon', 'autumn', 'winter', 'all'),
    tip_category ENUM('watering', 'fertilizing', 'pruning', 'pest_control', 'general', 'harvesting'),
    tip_text TEXT,
    difficulty_level ENUM('beginner', 'intermediate', 'advanced'),
    is_urgent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert quick care tips for common scenarios
INSERT INTO quick_care_tips (plant_name, season, tip_category, tip_text, difficulty_level, is_urgent) VALUES
('All Plants', 'summer', 'watering', 'Water plants early morning (6-8 AM) to reduce evaporation and prevent fungal diseases.', 'beginner', FALSE),
('All Plants', 'summer', 'watering', 'Check soil moisture by inserting finger 2 inches deep before watering.', 'beginner', FALSE),
('All Plants', 'summer', 'general', 'Provide afternoon shade during heat waves to prevent stress.', 'beginner', TRUE),

('Beginner Plants', 'all', 'general', 'Start with tulsi, mint, or marigold - they are very forgiving and grow easily.', 'beginner', FALSE),
('Beginner Plants', 'summer', 'watering', 'Summer beginners: Water every 2-3 days, more in extreme heat.', 'beginner', FALSE),
('Beginner Plants', 'all', 'fertilizing', 'Use organic compost every 15 days for healthy growth.', 'beginner', FALSE),

('Indoor Plants', 'all', 'watering', 'Indoor plants need less water - check soil dryness before watering.', 'beginner', FALSE),
('Indoor Plants', 'all', 'general', 'Place near bright window but avoid direct afternoon sun.', 'beginner', FALSE),
('Indoor Plants', 'all', 'general', 'Dust leaves weekly for better photosynthesis.', 'beginner', FALSE),

('Summer Plants', 'summer', 'general', 'Mulch around plants to retain moisture and keep roots cool.', 'beginner', FALSE),
('Summer Plants', 'summer', 'pest_control', 'Spray neem oil solution in evening to control summer pests.', 'intermediate', FALSE),

('Medicinal Plants', 'all', 'harvesting', 'Harvest medicinal plants in early morning after dew dries.', 'intermediate', FALSE),
('Medicinal Plants', 'all', 'general', 'Avoid chemical fertilizers on medicinal plants - use organic methods only.', 'beginner', TRUE);

-- Update care schedules for better seasonal adaptation
UPDATE care_schedules SET seasonal_adjustment = '{"summer": 2, "winter": 5, "monsoon": 3, "spring": 3, "autumn": 4}' WHERE task_type = 'watering';
UPDATE care_schedules SET seasonal_adjustment = '{"summer": 14, "winter": 30, "monsoon": 21, "spring": 14, "autumn": 21}' WHERE task_type = 'fertilizing';
