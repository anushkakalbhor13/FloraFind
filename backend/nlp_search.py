import spacy
import mysql.connector
from collections import defaultdict
import re
from fuzzywuzzy import fuzz, process
import json
from datetime import datetime

class FloraFindNLPSearch:
    def __init__(self, db_config):
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("SpaCy model not found. Please install: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        self.db_config = db_config
        
        # Plant-specific vocabulary and synonyms
        self.plant_vocabulary = {
            'seasons': {
                'summer': ['summer', 'hot', 'sunny', 'warm', 'heat'],
                'winter': ['winter', 'cold', 'cool', 'frost', 'chilly'],
                'spring': ['spring', 'bloom', 'flowering', 'growth'],
                'monsoon': ['monsoon', 'rainy', 'rain', 'wet', 'humid'],
                'all_seasons': ['year-round', 'always', 'continuous', 'perennial']
            },
            'difficulty': {
                'beginner': ['beginner', 'easy', 'simple', 'low-maintenance', 'basic', 'starter', 'first-time'],
                'intermediate': ['intermediate', 'moderate', 'medium', 'some-care'],
                'advanced': ['advanced', 'expert', 'difficult', 'challenging', 'high-maintenance']
            },
            'care_type': {
                'watering': ['water', 'watering', 'irrigation', 'hydration', 'moisture'],
                'sunlight': ['sun', 'light', 'sunlight', 'bright', 'shade', 'shadow'],
                'soil': ['soil', 'earth', 'ground', 'dirt', 'compost', 'fertilizer'],
                'pruning': ['prune', 'trim', 'cut', 'deadhead', 'pinch'],
                'pest_control': ['pest', 'insect', 'bug', 'disease', 'fungus']
            },
            'plant_types': {
                'indoor': ['indoor', 'houseplant', 'inside', 'home', 'apartment'],
                'outdoor': ['outdoor', 'garden', 'yard', 'outside'],
                'medicinal': ['medicinal', 'healing', 'herb', 'remedy', 'therapeutic'],
                'flowering': ['flower', 'bloom', 'blossom', 'colorful'],
                'foliage': ['leaves', 'green', 'foliage']
            },
            'benefits': {
                'air_purifying': ['air-purifying', 'clean-air', 'oxygen', 'purify'],
                'fragrant': ['fragrant', 'scented', 'aromatic', 'smell'],
                'edible': ['edible', 'eat', 'cooking', 'culinary']
            }
        }
        
        # Common plant names and their variations
        self.plant_aliases = {
            'tulsi': ['holy basil', 'sacred basil', 'ocimum'],
            'neem': ['margosa', 'indian lilac'],
            'aloe vera': ['aloe', 'burn plant'],
            'rose': ['rosa', 'roses'],
            'mint': ['mentha', 'peppermint', 'spearmint'],
            'sunflower': ['helianthus', 'sun flower'],
            'marigold': ['tagetes', 'calendula'],
            'jasmine': ['jasminum', 'mogra'],
            'lavender': ['lavandula'],
            'snake plant': ['sansevieria', 'mother-in-law tongue']
        }

    def preprocess_query(self, query):
        """Advanced NLP preprocessing with lemmatization and POS tagging"""
        if not self.nlp:
            return self._basic_preprocess(query)
        
        # Process with spaCy
        doc = self.nlp(query.lower())
        
        processed_info = {
            'original_query': query,
            'tokens': [],
            'lemmas': [],
            'entities': [],
            'keywords': [],
            'intent': self._determine_intent(doc),
            'plant_mentions': [],
            'care_aspects': [],
            'modifiers': []
        }
        
        for token in doc:
            if not token.is_stop and not token.is_punct and len(token.text) > 1:
                processed_info['tokens'].append({
                    'text': token.text,
                    'lemma': token.lemma_,
                    'pos': token.pos_,
                    'tag': token.tag_,
                    'is_plant_related': self._is_plant_related(token.lemma_)
                })
                
                # Extract important lemmas
                if token.pos_ in ['NOUN', 'ADJ', 'VERB']:
                    processed_info['lemmas'].append(token.lemma_)
                    
                    # Check for plant-specific keywords
                    if self._is_plant_keyword(token.lemma_):
                        processed_info['keywords'].append(token.lemma_)
        
        # Extract named entities
        for ent in doc.ents:
            if ent.label_ in ['PLANT', 'PRODUCT', 'ORG']:  # Custom entity types
                processed_info['entities'].append({
                    'text': ent.text,
                    'label': ent.label_
                })
        
        # Find plant mentions and care aspects
        processed_info['plant_mentions'] = self._extract_plant_mentions(processed_info['lemmas'])
        processed_info['care_aspects'] = self._extract_care_aspects(processed_info['lemmas'])
        processed_info['modifiers'] = self._extract_modifiers(processed_info['lemmas'])
        
        return processed_info

    def _basic_preprocess(self, query):
        """Fallback preprocessing without spaCy"""
        words = re.findall(r'\b\w+\b', query.lower())
        return {
            'original_query': query,
            'lemmas': words,
            'keywords': [w for w in words if len(w) > 2],
            'intent': 'search',
            'plant_mentions': self._extract_plant_mentions(words),
            'care_aspects': self._extract_care_aspects(words),
            'modifiers': []
        }

    def _determine_intent(self, doc):
        """Determine user intent from the query"""
        intent_patterns = {
            'care_advice': ['how', 'care', 'grow', 'maintain', 'water', 'fertilize'],
            'plant_identification': ['what', 'which', 'identify', 'name'],
            'recommendation': ['suggest', 'recommend', 'best', 'good', 'suitable'],
            'problem_solving': ['problem', 'issue', 'dying', 'yellow', 'pest', 'disease'],
            'search': ['find', 'show', 'list', 'get']
        }
        
        query_text = doc.text.lower()
        for intent, patterns in intent_patterns.items():
            if any(pattern in query_text for pattern in patterns):
                return intent
        
        return 'search'  # default intent

    def _is_plant_related(self, lemma):
        """Check if a lemma is plant-related"""
        plant_terms = ['plant', 'flower', 'herb', 'tree', 'shrub', 'vine', 'grass', 'leaf', 'root', 'stem', 'bloom']
        return lemma in plant_terms

    def _is_plant_keyword(self, lemma):
        """Check if lemma is a plant-specific keyword"""
        for category, synonyms in self.plant_vocabulary.items():
            if isinstance(synonyms, dict):
                for subcategory, terms in synonyms.items():
                    if lemma in terms:
                        return True
            elif lemma in synonyms:
                return True
        return False

    def _extract_plant_mentions(self, lemmas):
        """Extract potential plant name mentions"""
        plant_mentions = []
        
        # Check against plant aliases
        for plant_name, aliases in self.plant_aliases.items():
            for alias in aliases:
                if any(alias.split() and all(word in lemmas for word in alias.split()) for alias in [alias]):
                    plant_mentions.append(plant_name)
                    break
        
        return list(set(plant_mentions))

    def _extract_care_aspects(self, lemmas):
        """Extract care-related aspects from lemmas"""
        care_aspects = []
        
        for aspect, terms in self.plant_vocabulary['care_type'].items():
            if any(term in lemmas for term in terms):
                care_aspects.append(aspect)
        
        return care_aspects

    def _extract_modifiers(self, lemmas):
        """Extract modifying terms like difficulty, season, etc."""
        modifiers = []
        
        # Check seasons
        for season, terms in self.plant_vocabulary['seasons'].items():
            if any(term in lemmas for term in terms):
                modifiers.append(('season', season))
        
        # Check difficulty
        for difficulty, terms in self.plant_vocabulary['difficulty'].items():
            if any(term in lemmas for term in terms):
                modifiers.append(('difficulty', difficulty))
        
        # Check plant types
        for plant_type, terms in self.plant_vocabulary['plant_types'].items():
            if any(term in lemmas for term in terms):
                modifiers.append(('type', plant_type))
        
        return modifiers

    def semantic_search(self, processed_query):
        """Perform semantic search based on processed query"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)
            
            # Build dynamic query based on semantic understanding
            search_conditions = []
            search_params = []
            
            # Check for plant categories in the query (NEW)
            if 'categories' in processed_query and processed_query['categories']:
                print(f"Processing categories in search: {processed_query['categories']}")
                category_conditions = []
                for category in processed_query['categories']:
                    if category == 'fruit':
                        category_conditions.append("(LOWER(name) LIKE %s OR LOWER(eco_benefits) LIKE %s)")
                        search_params.extend(["%fruit%", "%edible fruit%"])
                    elif category == 'flower':
                        category_conditions.append("(LOWER(name) LIKE %s)")
                        search_params.append("%flower%")
                    elif category == 'medicinal':
                        category_conditions.append("(medicinal_properties IS NOT NULL AND medicinal_properties != '')")
                    elif category == 'herb':
                        category_conditions.append("(LOWER(name) LIKE %s)")
                        search_params.append("%herb%")
                    elif category == 'vegetable':
                        category_conditions.append("(LOWER(name) LIKE %s OR LOWER(eco_benefits) LIKE %s)")
                        search_params.extend(["%vegetable%", "%edible%"])
                    elif category == 'succulent':
                        category_conditions.append("(LOWER(name) LIKE %s OR LOWER(climate) LIKE %s)")
                        search_params.extend(["%succulent%", "%arid%"])
                    elif category == 'tree':
                        category_conditions.append("(LOWER(name) LIKE %s OR LOWER(growth_height) > %s)")
                        search_params.extend(["%tree%", "200"])
                    elif category == 'climber':
                        category_conditions.append("(LOWER(name) LIKE %s OR LOWER(care_instructions) LIKE %s)")
                        search_params.extend(["%climber%", "%climbing%"])
                    elif category == 'aquatic':
                        category_conditions.append("(LOWER(name) LIKE %s OR LOWER(climate) LIKE %s)")
                        search_params.extend(["%aquatic%", "%water%"])
                    elif category == 'air_purifying':
                        category_conditions.append("(LOWER(eco_benefits) LIKE %s)")
                        search_params.append("%air purif%")
                
                if category_conditions:
                    search_conditions.append(f"({' OR '.join(category_conditions)})")
                    print(f"Added category conditions: {' OR '.join(category_conditions)}")
            
            # 1. Direct plant mentions (HIGHEST priority - exact matching)
            if processed_query['plant_mentions']:
                plant_name_conditions = []
                for plant in processed_query['plant_mentions']:
                    # Exact name matching gets highest priority
                    plant_name_conditions.append("(LOWER(name) = %s OR LOWER(name) LIKE %s OR LOWER(scientific_name) LIKE %s)")
                    search_params.extend([plant.lower(), f"%{plant}%", f"%{plant}%"])
                search_conditions.append(f"({' OR '.join(plant_name_conditions)})")
            
            # 2. Check for specific plant keywords in the query
            query_lower = processed_query['original_query'].lower()
            direct_plant_matches = []
            for plant_name, aliases in self.plant_aliases.items():
                if plant_name in query_lower or any(alias in query_lower for alias in aliases):
                    direct_plant_matches.append(plant_name)
            
            if direct_plant_matches:
                plant_exact_conditions = []
                for plant in direct_plant_matches:
                    plant_exact_conditions.append("(LOWER(name) = %s OR LOWER(name) LIKE %s)")
                    search_params.extend([plant.lower(), f"%{plant}%"])
                search_conditions.append(f"({' OR '.join(plant_exact_conditions)})")
            
            # 3. Apply season filters STRICTLY
            season_filter_applied = False
            for modifier_type, modifier_value in processed_query['modifiers']:
                if modifier_type == 'season' and modifier_value != 'all_seasons':
                    search_conditions.append("(LOWER(season) LIKE %s OR LOWER(season) = %s)")
                    search_params.extend([f"%{modifier_value}%", modifier_value])
                    season_filter_applied = True
                elif modifier_type == 'difficulty':
                    search_conditions.append("difficulty_level = %s")
                    search_params.append(modifier_value)
                elif modifier_type == 'type':
                    if modifier_value == 'medicinal':
                        search_conditions.append("medicinal_properties IS NOT NULL AND medicinal_properties != ''")
                    elif modifier_value == 'indoor':
                        search_conditions.append("(LOWER(climate) LIKE %s OR LOWER(care_instructions) LIKE %s)")
                        search_params.extend(["%indoor%", "%indoor%"])
            
            # 4. Only do broad keyword matching if no specific plant was found and no category filter
            if not processed_query['plant_mentions'] and not direct_plant_matches and not ('categories' in processed_query and processed_query['categories']):
                if processed_query['keywords']:
                    keyword_conditions = []
                    for keyword in processed_query['keywords'][:2]:  # Limit to 2 most important keywords
                        if keyword not in ['plant', 'plants', 'care', 'grow']:  # Skip generic terms
                            keyword_conditions.append("""
                                (LOWER(name) LIKE %s OR 
                                 LOWER(care_instructions) LIKE %s OR
                                 LOWER(medicinal_properties) LIKE %s)
                            """)
                            search_params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])
                    
                    if keyword_conditions:
                        search_conditions.append(f"({' OR '.join(keyword_conditions)})")
            
            # Combine all conditions
            where_clause = " AND ".join(search_conditions) if search_conditions else "1=1"
            
            # Build final query with intelligent ranking
            final_query = f"""
                SELECT plant_id, name, scientific_name, season, climate, 
                       care_instructions, native_region, eco_impact_score, 
                       difficulty_level, cultural_significance, medicinal_properties,
                       watering_frequency_summer, watering_frequency_winter, watering_frequency_monsoon,
                       sunlight_requirement, soil_type, growth_height, growth_time_months, eco_benefits,
                       care_tips_detailed
                FROM plants 
                WHERE {where_clause}
                ORDER BY 
                    CASE 
                        WHEN LOWER(name) LIKE %s THEN 1
                        WHEN difficulty_level = 'beginner' AND %s THEN 2
                        WHEN eco_impact_score >= 7 THEN 3
                        ELSE 4
                    END,
                    eco_impact_score DESC,
                    name ASC
                LIMIT 20
            """
            
            # Add ordering parameters
            main_query_term = processed_query['original_query'].lower()
            search_params.extend([f"%{main_query_term}%", 'beginner' in processed_query['keywords']])
            
            print(f"Semantic search executing with {len(search_conditions)} conditions")
            print(f"SQL query: {final_query}")
            print(f"Search params: {search_params}")
            cursor.execute(final_query, search_params)
            results = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            # Rank results based on semantic relevance
            ranked_results = self._rank_results(results, processed_query)
            
            return {
                'plants': ranked_results,
                'search_analysis': {
                    'intent': processed_query['intent'],
                    'plant_mentions': processed_query['plant_mentions'],
                    'care_aspects': processed_query['care_aspects'],
                    'modifiers': processed_query['modifiers'],
                    'total_results': len(ranked_results)
                }
            }
            
        except Exception as e:
            print(f"Semantic search error: {e}")
            import traceback
            traceback.print_exc()
            return {'plants': [], 'error': str(e)}

    def _get_similar_terms(self, keyword):
        """Get similar terms using fuzzy matching and synonyms"""
        similar_terms = [keyword]
        
        # Add synonyms from vocabulary
        for category, subcategories in self.plant_vocabulary.items():
            if isinstance(subcategories, dict):
                for subcat, terms in subcategories.items():
                    if keyword in terms:
                        similar_terms.extend(terms)
            elif isinstance(subcategories, list) and keyword in subcategories:
                similar_terms.extend(subcategories)
        
        # Add plant aliases
        for plant_name, aliases in self.plant_aliases.items():
            if keyword in aliases or keyword == plant_name:
                similar_terms.extend(aliases + [plant_name])
        
        return list(set(similar_terms))

    def _rank_results(self, results, processed_query):
        """Rank results based on semantic relevance"""
        if not results:
            return []
        
        ranked_plants = []
        
        for plant in results:
            relevance_score = 0
            
            # Name matching score
            name_similarity = fuzz.partial_ratio(processed_query['original_query'].lower(), plant['name'].lower())
            relevance_score += name_similarity * 0.3
            
            # Plant mention bonus
            if processed_query['plant_mentions']:
                for mention in processed_query['plant_mentions']:
                    if mention.lower() in plant['name'].lower():
                        relevance_score += 50
            
            # Difficulty preference
            if 'beginner' in processed_query['keywords'] and plant['difficulty_level'] == 'beginner':
                relevance_score += 30
            
            # Care aspect matching
            care_text = (plant['care_instructions'] or '').lower()
            for aspect in processed_query['care_aspects']:
                if aspect in care_text:
                    relevance_score += 20
            
            # Eco-friendliness bonus
            if plant['eco_impact_score'] and plant['eco_impact_score'] >= 7:
                relevance_score += 15
            
            plant_dict = dict(plant)
            plant_dict['relevance_score'] = relevance_score
            
            # Add enhanced metadata
            plant_dict['quick_actions'] = self._generate_quick_actions(plant)
            plant_dict['care_summary'] = self._generate_care_summary(plant)
            plant_dict['semantic_tags'] = self._generate_semantic_tags(plant, processed_query)
            
            ranked_plants.append(plant_dict)
        
        # Sort by relevance score
        ranked_plants.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return ranked_plants

    def _generate_quick_actions(self, plant):
        """Generate context-aware quick actions"""
        actions = []
        
        if plant['difficulty_level'] == 'beginner':
            actions.append({"action": "perfect_for_beginners", "icon": "🌱", "text": "Perfect for Beginners"})
        
        if 'summer' in (plant['season'] or '').lower():
            actions.append({"action": "summer_friendly", "icon": "☀️", "text": "Summer Friendly"})
        
        if plant['eco_impact_score'] and plant['eco_impact_score'] >= 8:
            actions.append({"action": "eco_champion", "icon": "🌍", "text": "Eco Champion"})
        
        if plant['medicinal_properties']:
            actions.append({"action": "medicinal_uses", "icon": "💊", "text": "Medicinal Uses"})
        
        if 'air' in (plant['eco_benefits'] or '').lower():
            actions.append({"action": "air_purifier", "icon": "🌬️", "text": "Air Purifier"})
        
        return actions

    def _generate_care_summary(self, plant):
        """Generate intelligent care summary"""
        return {
            "difficulty": plant['difficulty_level'],
            "sunlight": plant['sunlight_requirement'] or "Natural light",
            "water_frequency": self._get_watering_advice(plant),
            "growth_time": f"{plant['growth_time_months']} months" if plant['growth_time_months'] else "Variable",
            "special_care": self._extract_special_care_tips(plant)
        }

    def _get_watering_advice(self, plant):
        """Get intelligent watering advice based on season"""
        summer_freq = plant['watering_frequency_summer']
        winter_freq = plant['watering_frequency_winter']
        
        if summer_freq and winter_freq:
            return f"Every {summer_freq} days (summer), {winter_freq} days (winter)"
        elif summer_freq:
            return f"Every {summer_freq} days in summer"
        else:
            return "Regular watering"

    def _extract_special_care_tips(self, plant):
        """Extract key care tips from detailed care instructions"""
        care_text = plant['care_instructions'] or ""
        
        # Extract key phrases using simple NLP
        tips = []
        if 'deadhead' in care_text.lower():
            tips.append("Regular deadheading")
        if 'prune' in care_text.lower():
            tips.append("Pruning required")
        if 'full sun' in care_text.lower():
            tips.append("Needs full sun")
        if 'shade' in care_text.lower():
            tips.append("Tolerates shade")
        
        return tips[:3]  # Return top 3 tips

    def _generate_semantic_tags(self, plant, processed_query):
        """Generate semantic tags based on query understanding"""
        tags = []
        
        # Add intent-based tags
        if processed_query['intent'] == 'recommendation':
            tags.append("recommended")
        
        # Add query-relevant tags
        for modifier_type, modifier_value in processed_query['modifiers']:
            tags.append(f"{modifier_type}_{modifier_value}")
        
        # Add care-related tags
        for care_aspect in processed_query['care_aspects']:
            if care_aspect in (plant['care_instructions'] or '').lower():
                tags.append(f"good_for_{care_aspect}")
        
        return tags

# Usage example function
def search_plants_nlp(query, db_config):
    """Main function to search plants using NLP"""
    nlp_search = FloraFindNLPSearch(db_config)
    
    # Process query with NLP
    processed_query = nlp_search.preprocess_query(query)
    print(f"Processed query: {processed_query}")
    
    # Extract categories directly from the query
    categories = []
    if 'fruit' in query.lower():
        categories.append('fruit')
    if 'flower' in query.lower():
        categories.append('flower')
    if 'medicinal' in query.lower():
        categories.append('medicinal')
    if 'herb' in query.lower():
        categories.append('herb')
    if 'vegetable' in query.lower():
        categories.append('vegetable')
    if 'succulent' in query.lower():
        categories.append('succulent')
    if 'tree' in query.lower():
        categories.append('tree')
    if 'climber' in query.lower():
        categories.append('climber')
    if 'aquatic' in query.lower():
        categories.append('aquatic')
    if 'air purifying' in query.lower() or 'air-purifying' in query.lower():
        categories.append('air_purifying')
    
    if categories:
        processed_query['categories'] = categories
        print(f"Detected categories: {categories}")
    
    # Add medicinal category if medicinal intent is detected
    if 'medicinal' in query.lower() and ('categories' not in processed_query or 'medicinal' not in processed_query.get('categories', [])):
        processed_query.setdefault('categories', []).append('medicinal')
        # Also add medicinal type modifier
        processed_query.setdefault('modifiers', []).append(('type', 'medicinal'))
    
    # Perform semantic search
    results = nlp_search.semantic_search(processed_query)
    
    return results
