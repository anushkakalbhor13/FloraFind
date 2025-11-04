"""
Weather and Climate Integration Module for FloraFind
Provides weather-based plant care recommendations and seasonal adjustments
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import mysql.connector
from dataclasses import dataclass

@dataclass
class WeatherData:
    temperature: float
    humidity: float
    rainfall: float
    season: str
    air_quality: str
    wind_speed: float
    uv_index: int

@dataclass  
class PlantCareRecommendation:
    watering_adjustment: str  # "increase", "decrease", "maintain"
    care_priority: str  # "high", "medium", "low" 
    specific_actions: List[str]
    warning_message: Optional[str] = None

class WeatherIntegration:
    def __init__(self):
        # Free weather APIs (no key required for basic usage)
        self.weather_apis = {
            'openweather': 'https://api.openweathermap.org/data/2.5/weather',
            'weatherapi': 'https://api.weatherapi.com/v1/current.json'
        }
        
        # Seasonal care adjustments
        self.seasonal_care_rules = {
            'winter': {
                'watering_multiplier': 0.6,  # Reduce watering by 40%
                'care_focus': ['protect from frost', 'reduce fertilizing', 'check for pests'],
                'critical_temp': 5,  # Celsius
                'humidity_ideal': (40, 60)
            },
            'spring': {
                'watering_multiplier': 1.2,  # Increase watering by 20%
                'care_focus': ['fertilize', 'prune', 'repot if needed'],
                'critical_temp': 10,
                'humidity_ideal': (50, 70)
            },
            'summer': {
                'watering_multiplier': 1.5,  # Increase watering by 50%
                'care_focus': ['daily watering', 'shade protection', 'pest monitoring'],
                'critical_temp': 35,
                'humidity_ideal': (60, 80)
            },
            'monsoon': {
                'watering_multiplier': 0.4,  # Reduce watering by 60%
                'care_focus': ['drainage check', 'fungal prevention', 'pruning'],
                'critical_temp': 25,
                'humidity_ideal': (70, 90)
            },
            'autumn': {
                'watering_multiplier': 0.8,  # Reduce watering by 20%
                'care_focus': ['prepare for winter', 'harvest', 'soil preparation'],
                'critical_temp': 15,
                'humidity_ideal': (50, 70)
            }
        }
        
        # Plant-specific weather sensitivity
        self.plant_weather_sensitivity = {
            'rose': {
                'temperature_range': (15, 30),
                'humidity_preference': (50, 70),
                'heat_tolerance': 'medium',
                'cold_tolerance': 'high',
                'rain_tolerance': 'medium'
            },
            'tulsi': {
                'temperature_range': (20, 35),
                'humidity_preference': (60, 80),
                'heat_tolerance': 'high',
                'cold_tolerance': 'low',
                'rain_tolerance': 'high'
            },
            'neem': {
                'temperature_range': (25, 40),
                'humidity_preference': (40, 70),
                'heat_tolerance': 'very_high',
                'cold_tolerance': 'medium',
                'rain_tolerance': 'high'
            },
            'snake plant': {
                'temperature_range': (18, 28),
                'humidity_preference': (30, 50),
                'heat_tolerance': 'high',
                'cold_tolerance': 'medium',
                'rain_tolerance': 'low'
            }
        }
    
    def get_weather_data(self, city: str, country: str = "IN") -> Optional[WeatherData]:
        """Get current weather data for a location"""
        try:
            # Using a simple weather service (you can integrate with APIs)
            # For demo purposes, generating realistic weather data
            current_month = datetime.now().month
            
            if current_month in [12, 1, 2]:
                season = "winter"
                temp_range = (10, 25)
                humidity_range = (40, 70)
                rainfall = 5
            elif current_month in [3, 4, 5]:
                season = "spring" 
                temp_range = (20, 30)
                humidity_range = (50, 75)
                rainfall = 15
            elif current_month in [6, 7, 8]:
                if city.lower() in ['mumbai', 'delhi', 'bangalore']:
                    season = "monsoon"
                    temp_range = (24, 32)
                    humidity_range = (70, 95)
                    rainfall = 150
                else:
                    season = "summer"
                    temp_range = (28, 42)
                    humidity_range = (40, 70)
                    rainfall = 20
            else:
                season = "autumn"
                temp_range = (22, 32)
                humidity_range = (55, 75)
                rainfall = 25
            
            # Generate realistic values within ranges
            import random
            temperature = round(random.uniform(*temp_range), 1)
            humidity = round(random.uniform(*humidity_range), 1)
            
            return WeatherData(
                temperature=temperature,
                humidity=humidity,
                rainfall=rainfall,
                season=season,
                air_quality="moderate",
                wind_speed=round(random.uniform(5, 25), 1),
                uv_index=random.randint(3, 11)
            )
            
        except Exception as e:
            print(f"Weather data error: {e}")
            # Return default values
            return WeatherData(
                temperature=25.0,
                humidity=65.0,
                rainfall=10.0,
                season="spring",
                air_quality="moderate",
                wind_speed=10.0,
                uv_index=6
            )
    
    def analyze_plant_weather_compatibility(self, plant_name: str, weather: WeatherData) -> Dict[str, any]:
        """Analyze how current weather affects a specific plant"""
        plant_prefs = self.plant_weather_sensitivity.get(plant_name.lower(), {})
        
        if not plant_prefs:
            # Generic analysis for unknown plants
            temp_range = (15, 35)
            humidity_preference = (40, 80)
        else:
            temp_range = plant_prefs['temperature_range']
            humidity_preference = plant_prefs['humidity_preference']
        
        compatibility = {
            'temperature_status': 'optimal',
            'humidity_status': 'optimal',
            'overall_compatibility': 85,
            'stress_factors': [],
            'recommendations': []
        }
        
        # Temperature analysis
        if weather.temperature < temp_range[0]:
            compatibility['temperature_status'] = 'too_cold'
            compatibility['stress_factors'].append('Cold stress')
            compatibility['recommendations'].append('Protect from cold, reduce watering')
            compatibility['overall_compatibility'] -= 20
        elif weather.temperature > temp_range[1]:
            compatibility['temperature_status'] = 'too_hot'
            compatibility['stress_factors'].append('Heat stress')
            compatibility['recommendations'].append('Increase shade, frequent watering')
            compatibility['overall_compatibility'] -= 15
        
        # Humidity analysis
        if weather.humidity < humidity_preference[0]:
            compatibility['humidity_status'] = 'too_dry'
            compatibility['stress_factors'].append('Low humidity')
            compatibility['recommendations'].append('Increase humidity, mist regularly')
            compatibility['overall_compatibility'] -= 10
        elif weather.humidity > humidity_preference[1]:
            compatibility['humidity_status'] = 'too_humid'
            compatibility['stress_factors'].append('High humidity')
            compatibility['recommendations'].append('Improve ventilation, check for fungal issues')
            compatibility['overall_compatibility'] -= 10
        
        # Rainfall analysis
        if weather.rainfall > 100:
            compatibility['stress_factors'].append('Excessive rainfall')
            compatibility['recommendations'].append('Ensure proper drainage, watch for root rot')
            compatibility['overall_compatibility'] -= 15
        
        return compatibility
    
    def generate_weather_based_care_plan(self, plant_name: str, weather: WeatherData, user_location: str) -> PlantCareRecommendation:
        """Generate specific care recommendations based on current weather"""
        seasonal_rules = self.seasonal_care_rules.get(weather.season, self.seasonal_care_rules['spring'])
        compatibility = self.analyze_plant_weather_compatibility(plant_name, weather)
        
        # Determine watering adjustment
        watering_adjustment = "maintain"
        if weather.temperature > 30 or weather.humidity < 40:
            watering_adjustment = "increase"
        elif weather.rainfall > 50 or weather.humidity > 80:
            watering_adjustment = "decrease"
        
        # Determine care priority
        care_priority = "medium"
        if compatibility['overall_compatibility'] < 60:
            care_priority = "high"
        elif compatibility['overall_compatibility'] > 85:
            care_priority = "low"
        
        # Generate specific actions
        specific_actions = []
        specific_actions.extend(seasonal_rules['care_focus'])
        specific_actions.extend(compatibility['recommendations'])
        
        # Add weather-specific actions
        if weather.temperature > 35:
            specific_actions.append("Provide afternoon shade")
        if weather.uv_index > 8:
            specific_actions.append("Protect from intense UV")
        if weather.wind_speed > 20:
            specific_actions.append("Stake tall plants")
        
        # Generate warning message if needed
        warning_message = None
        if weather.temperature > 40:
            warning_message = "⚠️ Extreme heat warning! Monitor plants closely for heat stress."
        elif weather.temperature < 5:
            warning_message = "❄️ Frost warning! Protect sensitive plants immediately."
        elif weather.rainfall > 200:
            warning_message = "🌧️ Heavy rainfall alert! Check drainage and prevent waterlogging."
        
        return PlantCareRecommendation(
            watering_adjustment=watering_adjustment,
            care_priority=care_priority,
            specific_actions=list(set(specific_actions))[:5],  # Remove duplicates, limit to 5
            warning_message=warning_message
        )
    
    def get_weekly_care_forecast(self, plant_name: str, location: str) -> List[Dict[str, any]]:
        """Generate 7-day care forecast based on weather predictions"""
        forecast = []
        
        for day in range(7):
            date = datetime.now() + timedelta(days=day)
            # Simulate weather forecast (in real implementation, use weather API)
            weather = self.get_weather_data(location.split(',')[0])
            
            # Slightly vary weather for forecast
            if weather:
                import random
                weather.temperature += random.uniform(-3, 3)
                weather.humidity += random.uniform(-10, 10)
                weather.rainfall *= random.uniform(0.5, 1.5)
            
            care_plan = self.generate_weather_based_care_plan(plant_name, weather, location)
            
            forecast.append({
                'date': date.strftime('%Y-%m-%d'),
                'day': date.strftime('%A'),
                'weather': {
                    'temperature': weather.temperature,
                    'humidity': weather.humidity,
                    'season': weather.season,
                    'rainfall': weather.rainfall
                },
                'care_plan': {
                    'watering': care_plan.watering_adjustment,
                    'priority': care_plan.care_priority,
                    'actions': care_plan.specific_actions[:3],
                    'warning': care_plan.warning_message
                }
            })
        
        return forecast
    
    def get_location_native_plants(self, city: str, country: str = "IN") -> List[Dict[str, any]]:
        """Get plants native to a specific location"""
        # Database of native plants by region
        native_plants_db = {
            'mumbai': [
                {'name': 'Flame of the Forest', 'scientific': 'Butea monosperma', 'season': 'spring'},
                {'name': 'Gulmohar', 'scientific': 'Delonix regia', 'season': 'summer'},
                {'name': 'Bougainvillea', 'scientific': 'Bougainvillea spectabilis', 'season': 'all'},
                {'name': 'Ficus', 'scientific': 'Ficus religiosa', 'season': 'all'}
            ],
            'delhi': [
                {'name': 'Neem', 'scientific': 'Azadirachta indica', 'season': 'all'},
                {'name': 'Peepal', 'scientific': 'Ficus religiosa', 'season': 'all'},
                {'name': 'Mango', 'scientific': 'Mangifera indica', 'season': 'summer'},
                {'name': 'Jamun', 'scientific': 'Syzygium cumini', 'season': 'monsoon'}
            ],
            'bangalore': [
                {'name': 'Sandalwood', 'scientific': 'Santalum album', 'season': 'all'},
                {'name': 'Jacaranda', 'scientific': 'Jacaranda mimosifolia', 'season': 'spring'},
                {'name': 'Rain Tree', 'scientific': 'Samanea saman', 'season': 'all'},
                {'name': 'Gulmohar', 'scientific': 'Delonix regia', 'season': 'summer'}
            ]
        }
        
        return native_plants_db.get(city.lower(), [
            {'name': 'Neem', 'scientific': 'Azadirachta indica', 'season': 'all'},
            {'name': 'Tulsi', 'scientific': 'Ocimum tenuiflorum', 'season': 'all'}
        ])
    
    def get_seasonal_plant_recommendations(self, location: str, user_preferences: Dict = None) -> Dict[str, List[Dict]]:
        """Get plant recommendations based on current season and location"""
        weather = self.get_weather_data(location.split(',')[0])
        native_plants = self.get_location_native_plants(location.split(',')[0])
        
        recommendations = {
            'seasonal_favorites': [],
            'low_maintenance': [],
            'climate_perfect': []
        }
        
        # Get seasonal plants
        for plant in native_plants:
            if plant['season'] == weather.season or plant['season'] == 'all':
                recommendations['seasonal_favorites'].append({
                    'name': plant['name'],
                    'scientific_name': plant['scientific'],
                    'reason': f'Perfect for {weather.season} season',
                    'care_level': 'medium'
                })
        
        # Add weather-appropriate plants
        if weather.temperature > 30:
            recommendations['climate_perfect'].extend([
                {'name': 'Aloe Vera', 'reason': 'Heat tolerant, low water needs'},
                {'name': 'Cactus', 'reason': 'Extreme heat tolerance'},
                {'name': 'Bougainvillea', 'reason': 'Thrives in hot climate'}
            ])
        elif weather.temperature < 20:
            recommendations['climate_perfect'].extend([
                {'name': 'Rose', 'reason': 'Prefers cooler temperatures'},
                {'name': 'Marigold', 'reason': 'Cold tolerant annual'},
                {'name': 'Chrysanthemum', 'reason': 'Winter blooming flower'}
            ])
        
        # Always include some low-maintenance options
        recommendations['low_maintenance'] = [
            {'name': 'Snake Plant', 'reason': 'Very low maintenance, air purifying'},
            {'name': 'ZZ Plant', 'reason': 'Extremely drought tolerant'},
            {'name': 'Pothos', 'reason': 'Grows in any light condition'}
        ]
        
        return recommendations

# API endpoint functions for Flask integration
def get_weather_care_recommendations(plant_name: str, location: str) -> Dict[str, any]:
    """Main API function to get weather-based care recommendations"""
    weather_service = WeatherIntegration()
    
    try:
        weather = weather_service.get_weather_data(location.split(',')[0])
        care_plan = weather_service.generate_weather_based_care_plan(plant_name, weather, location)
        compatibility = weather_service.analyze_plant_weather_compatibility(plant_name, weather)
        
        return {
            'success': True,
            'current_weather': {
                'temperature': weather.temperature,
                'humidity': weather.humidity,
                'season': weather.season,
                'rainfall': weather.rainfall,
                'uv_index': weather.uv_index
            },
            'plant_compatibility': compatibility,
            'care_recommendations': {
                'watering': care_plan.watering_adjustment,
                'priority': care_plan.care_priority,
                'actions': care_plan.specific_actions,
                'warning': care_plan.warning_message
            },
            'location': location
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': 'Unable to fetch weather data'
        }

def get_location_plant_suggestions(location: str) -> Dict[str, any]:
    """Get plant suggestions based on location and climate"""
    weather_service = WeatherIntegration()
    
    try:
        recommendations = weather_service.get_seasonal_plant_recommendations(location)
        native_plants = weather_service.get_location_native_plants(location.split(',')[0])
        weather = weather_service.get_weather_data(location.split(',')[0])
        
        return {
            'success': True,
            'location': location,
            'current_season': weather.season,
            'current_temp': weather.temperature,
            'recommendations': recommendations,
            'native_plants': native_plants,
            'climate_summary': {
                'season': weather.season,
                'temperature': weather.temperature,
                'humidity': weather.humidity,
                'best_for': f"Plants that thrive in {weather.season} season"
            }
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': 'Unable to get location-based recommendations'
        }

# Test function
if __name__ == "__main__":
    print("🌤️ Testing Weather Integration Module\n")
    
    weather_service = WeatherIntegration()
    
    # Test weather data
    weather = weather_service.get_weather_data("Mumbai")
    print(f"Mumbai Weather: {weather.temperature}°C, {weather.humidity}% humidity, {weather.season}")
    
    # Test plant compatibility
    compatibility = weather_service.analyze_plant_weather_compatibility("rose", weather)
    print(f"Rose Compatibility: {compatibility['overall_compatibility']}%")
    print(f"Recommendations: {compatibility['recommendations']}")
    
    # Test care plan
    care_plan = weather_service.generate_weather_based_care_plan("tulsi", weather, "Mumbai, India")
    print(f"Tulsi Care Plan: {care_plan.watering_adjustment} watering, {care_plan.care_priority} priority")
    print(f"Actions: {care_plan.specific_actions}")
    
    # Test API function
    api_result = get_weather_care_recommendations("rose", "Mumbai, India")
    print(f"\nAPI Result: {api_result['success']}")
    if api_result['success']:
        print(f"Temperature: {api_result['current_weather']['temperature']}°C")
        print(f"Care Priority: {api_result['care_recommendations']['priority']}")
