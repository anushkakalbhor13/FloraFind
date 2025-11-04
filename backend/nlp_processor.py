"""
Enhanced NLP module for FloraFind with advanced plant query processing
Includes intent recognition, entity extraction, and multilingual support
"""

import spacy
import re
from rapidfuzz import fuzz, process
from langdetect import detect
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

class PlantQueryProcessor:
    def __init__(self):
        """Initialize the NLP processor with language models"""
        try:
            # Load English model
            self.nlp_en = spacy.load("en_core_web_sm")
        except OSError:
            print("⚠️ English spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp_en = None
        
        # Plant care intent patterns
        self.intent_patterns = {
            'watering': ['water', 'hydrate', 'irrigation', 'wet', 'moisture', 'drink'],
            'fertilizing': ['fertilize', 'feed', 'nutrition', 'nutrients', 'compost', 'manure'],
            'pruning': ['prune', 'trim', 'cut', 'deadhead', 'shape', 'remove'],
            'pests': ['pest', 'insect', 'bug', 'disease', 'fungus', 'aphid', 'spider mite'],
            'repotting': ['repot', 'transplant', 'soil', 'pot', 'container', 'root bound'],
            'light': ['light', 'sun', 'shade', 'bright', 'dark', 'sunlight', 'exposure'],
            'seasonal': ['season', 'winter', 'summer', 'spring', 'autumn', 'monsoon'],
            'indoor': ['indoor', 'house', 'inside', 'apartment', 'office', 'home'],
            'outdoor': ['outdoor', 'garden', 'yard', 'balcony', 'terrace', 'outside'],
            'beginner': ['easy', 'beginner', 'simple', 'low maintenance', 'care-free'],
            'climate': ['climate', 'temperature', 'humid', 'dry', 'tropical', 'cold']
        }
        
        # Plant categories for filtering
        self.plant_categories = {
            'fruit': ['fruit', 'fruiting', 'berry', 'berries', 'apple', 'orange', 'citrus', 'edible fruit'],
            'flower': ['flower', 'flowering', 'bloom', 'blossom', 'ornamental', 'decorative'],
            'medicinal': ['medicinal', 'medicine', 'healing', 'therapeutic', 'remedy', 'health', 'ayurvedic'],
            'herb': ['herb', 'herbs', 'spice', 'seasoning', 'culinary', 'kitchen', 'cooking'],
            'vegetable': ['vegetable', 'vegetables', 'veggie', 'edible', 'food', 'crop'],
            'succulent': ['succulent', 'cactus', 'cacti', 'desert', 'drought-resistant'],
            'tree': ['tree', 'shrub', 'woody', 'timber', 'shade'],
            'climber': ['climber', 'vine', 'creeper', 'climbing', 'trailing'],
            'aquatic': ['aquatic', 'water', 'pond', 'floating', 'submerged'],
            'air_purifying': ['air purifying', 'air purifier', 'clean air', 'oxygen', 'detoxifying']
        }
        
        # Plant name aliases and common names
        self.plant_aliases = {
            'rose': ['roses', 'rosa', 'flower rose'],
            'tulsi': ['holy basil', 'ocimum tenuiflorum', 'sacred basil'],
            'neem': ['neem tree', 'azadirachta indica', 'margosa'],
            'basil': ['sweet basil', 'ocimum basilicum', 'tulsi'],
            'mint': ['peppermint', 'spearmint', 'mentha'],
            'aloe': ['aloe vera', 'burn plant', 'medicine plant'],
            'snake plant': ['sansevieria', 'mother-in-law tongue'],
            'peace lily': ['spathiphyllum', 'white lily'],
            'spider plant': ['chlorophytum comosum', 'airplane plant'],
            'pothos': ['devil\'s ivy', 'golden pothos', 'epipremnum aureum']
        }
    
    def detect_language(self, text: str) -> str:
        """Detect the language of input text"""
        try:
            return detect(text)
        except:
            return 'en'
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities from text using spaCy"""
        entities = {
            'plants': [],
            'locations': [],
            'seasons': [],
            'care_actions': [],
            'problems': [],
            'categories': []  # Added categories field
        }
        
        if not self.nlp_en:
            return entities
        
        doc = self.nlp_en(text.lower())
        
        # Extract plant names using aliases
        for plant, aliases in self.plant_aliases.items():
            for alias in aliases + [plant]:
                if alias.lower() in text.lower():
                    if plant not in entities['plants']:
                        entities['plants'].append(plant)
        
        # Extract locations and seasonal info
        for token in doc:
            if token.pos_ in ['NOUN', 'PROPN']:
                # Check for location indicators
                if any(loc in token.text for loc in ['indoor', 'outdoor', 'garden', 'balcony']):
                    entities['locations'].append(token.text)
                
                # Check for seasons
                if token.text in ['summer', 'winter', 'spring', 'autumn', 'monsoon', 'rainy']:
                    entities['seasons'].append(token.text)
        
        # Extract plant categories
        entities['categories'] = self.extract_plant_categories(text)
        
        return entities
        
    def extract_plant_categories(self, text: str) -> List[str]:
        """Extract plant categories from the query text"""
        text_lower = text.lower()
        categories = []
        
        # Check for category keywords in the text
        for category, keywords in self.plant_categories.items():
            for keyword in keywords:
                if keyword in text_lower:
                    categories.append(category)
                    break
        
        return list(set(categories))  # Remove duplicates
    
    def classify_intent(self, text: str) -> Tuple[str, float]:
        """Classify the main intent of the query"""
        text_lower = text.lower()
        intent_scores = {}
        
        for intent, keywords in self.intent_patterns.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
                # Check for fuzzy matches
                matches = process.extract(keyword, text_lower.split(), limit=1)
                if matches and matches[0][1] > 80:
                    score += 0.5
            
            if score > 0:
                intent_scores[intent] = score
        
        if intent_scores:
            best_intent = max(intent_scores, key=intent_scores.get)
            confidence = min(intent_scores[best_intent] / len(self.intent_patterns[best_intent]), 1.0)
            return best_intent, confidence
        
        return 'general_info', 0.5
    
    def extract_care_context(self, text: str) -> Dict[str, any]:
        """Extract care-specific context from the query"""
        context = {
            'urgency': 'normal',
            'season_specific': False,
            'difficulty_preference': None,
            'location_preference': None,
            'problem_indicators': []
        }
        
        text_lower = text.lower()
        
        # Check urgency
        urgent_words = ['urgent', 'emergency', 'dying', 'help', 'quickly', 'asap']
        if any(word in text_lower for word in urgent_words):
            context['urgency'] = 'high'
        
        # Check for seasonal context
        seasonal_words = ['summer', 'winter', 'spring', 'monsoon', 'season']
        context['season_specific'] = any(word in text_lower for word in seasonal_words)
        
        # Check difficulty preference
        if any(word in text_lower for word in ['easy', 'beginner', 'simple']):
            context['difficulty_preference'] = 'beginner'
        elif any(word in text_lower for word in ['advanced', 'expert', 'difficult']):
            context['difficulty_preference'] = 'expert'
        
        # Check location preference
        if any(word in text_lower for word in ['indoor', 'inside', 'house', 'apartment']):
            context['location_preference'] = 'indoor'
        elif any(word in text_lower for word in ['outdoor', 'garden', 'yard', 'balcony']):
            context['location_preference'] = 'outdoor'
        
        # Check for problem indicators
        problem_words = ['dying', 'wilting', 'yellow', 'brown', 'pest', 'disease', 'problem', 'sick']
        context['problem_indicators'] = [word for word in problem_words if word in text_lower]
        
        return context
    
    def generate_search_terms(self, text: str) -> List[str]:
        """Generate optimized search terms for database queries"""
        entities = self.extract_entities(text)
        intent, confidence = self.classify_intent(text)
        context = self.extract_care_context(text)
        
        search_terms = []
        
        # Add plant names
        search_terms.extend(entities['plants'])
        
        # Add intent-based terms
        if intent in self.intent_patterns:
            search_terms.extend(self.intent_patterns[intent][:3])  # Top 3 keywords
        
        # Add seasonal terms
        if context['season_specific']:
            current_season = self.get_current_season()
            search_terms.append(current_season)
        
        # Add difficulty terms
        if context['difficulty_preference']:
            search_terms.append(context['difficulty_preference'])
        
        # Add location terms
        if context['location_preference']:
            search_terms.append(context['location_preference'])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_terms = []
        for term in search_terms:
            if term not in seen:
                unique_terms.append(term)
                seen.add(term)
        
        return unique_terms
    
    def get_current_season(self) -> str:
        """Get current season based on month"""
        month = datetime.now().month
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        elif month in [9, 10, 11]:
            return 'autumn'
    
    def generate_response_context(self, text: str) -> Dict[str, any]:
        """Generate context for response generation"""
        return {
            'entities': self.extract_entities(text),
            'intent': self.classify_intent(text),
            'care_context': self.extract_care_context(text),
            'search_terms': self.generate_search_terms(text),
            'language': self.detect_language(text),
            'current_season': self.get_current_season()
        }
    
    def process_voice_query(self, audio_text: str) -> Dict[str, any]:
        """Process voice-to-text queries with additional context"""
        # Clean up common voice-to-text artifacts
        cleaned_text = re.sub(r'\bum\b|\buh\b|\ber\b', '', audio_text, flags=re.IGNORECASE)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        
        # Process the query and add NLP analysis
        result = self.generate_response_context(cleaned_text)
        
        # Add detailed NLP analysis if model is available
        if self.nlp_en:
            doc = self.nlp_en(cleaned_text)
            result['nlp_analysis'] = {
                'tokenization': [{'text': token.text, 'index': token.i} for token in doc],
                'pos_tagging': [{'text': token.text, 'pos': token.pos_, 'tag': token.tag_} for token in doc],
                'ner': [{'text': ent.text, 'label': ent.label_, 'start': ent.start_char, 'end': ent.end_char} for ent in doc.ents],
                'dependency_parsing': [{'text': token.text, 'dep': token.dep_, 'head': token.head.text} for token in doc],
                'lemmatization': [{'text': token.text, 'lemma': token.lemma_} for token in doc]
            }
        
        return result
    
    def suggest_follow_up_questions(self, processed_query: Dict[str, any]) -> List[str]:
        """Generate intelligent follow-up question suggestions"""
        suggestions = []
        intent = processed_query['intent'][0]
        entities = processed_query['entities']
        
        if intent == 'watering':
            suggestions.extend([
                "How often should I water in different seasons?",
                "What are signs of overwatering?",
                "Best time of day to water plants?"
            ])
        elif intent == 'pests':
            suggestions.extend([
                "Natural pest control methods?",
                "How to identify common plant pests?",
                "Preventive pest management tips?"
            ])
        elif intent == 'light':
            suggestions.extend([
                "Low light indoor plants?",
                "How to provide adequate light indoors?",
                "Plants for south-facing windows?"
            ])
        
        # Add plant-specific suggestions
        if entities['plants']:
            plant = entities['plants'][0]
            suggestions.extend([
                f"When is {plant} blooming season?",
                f"Common problems with {plant}?",
                f"Best companion plants for {plant}?"
            ])
        
        return suggestions[:4]  # Limit to 4 suggestions


# Conversation memory for context-aware responses
class ConversationMemory:
    def __init__(self, max_history=10):
        self.history = []
        self.max_history = max_history
        self.user_preferences = {}
    
    def add_interaction(self, query: str, response: str, context: Dict):
        """Add a new interaction to memory"""
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response,
            'context': context
        }
        
        self.history.append(interaction)
        
        # Keep only recent history
        if len(self.history) > self.max_history:
            self.history.pop(0)
        
        # Update user preferences based on context
        self._update_preferences(context)
    
    def _update_preferences(self, context: Dict):
        """Update user preferences based on interaction context"""
        care_context = context.get('care_context', {})
        
        if care_context.get('difficulty_preference'):
            self.user_preferences['difficulty'] = care_context['difficulty_preference']
        
        if care_context.get('location_preference'):
            self.user_preferences['location'] = care_context['location_preference']
    
    def get_conversation_context(self) -> Dict:
        """Get relevant context from conversation history"""
        if not self.history:
            return {}
        
        recent_plants = []
        recent_intents = []
        
        # Analyze recent interactions
        for interaction in self.history[-3:]:  # Last 3 interactions
            context = interaction['context']
            if 'entities' in context:
                recent_plants.extend(context['entities'].get('plants', []))
            if 'intent' in context:
                recent_intents.append(context['intent'][0])
        
        return {
            'recent_plants': list(set(recent_plants)),
            'recent_intents': list(set(recent_intents)),
            'user_preferences': self.user_preferences,
            'interaction_count': len(self.history)
        }


# Initialize global instances
query_processor = PlantQueryProcessor()
conversation_memory = ConversationMemory()

def process_plant_query(query: str, user_id: int = None) -> Dict[str, any]:
    """
    Main function to process plant queries with full NLP analysis
    """
    # Process the query
    processed = query_processor.generate_response_context(query)
    
    # Add conversation context
    conv_context = conversation_memory.get_conversation_context()
    processed['conversation_context'] = conv_context
    
    # Generate suggestions
    processed['follow_up_suggestions'] = query_processor.suggest_follow_up_questions(processed)
    
    return processed

def update_conversation_memory(query: str, response: str, context: Dict):
    """Update conversation memory with new interaction"""
    conversation_memory.add_interaction(query, response, context)

if __name__ == "__main__":
    # Test the NLP processor
    test_queries = [
        "How do I care for roses in summer?",
        "My basil plant is dying, help!",
        "Easy indoor plants for beginners?",
        "When should I water my snake plant?",
        "Natural pest control for garden plants"
    ]
    
    print("🌱 Testing Enhanced NLP Processor\n")
    
    for query in test_queries:
        print(f"Query: {query}")
        result = process_plant_query(query)
        print(f"Intent: {result['intent']}")
        print(f"Entities: {result['entities']}")
        print(f"Search Terms: {result['search_terms']}")
        print(f"Suggestions: {result['follow_up_suggestions'][:2]}")
        print("-" * 50)
