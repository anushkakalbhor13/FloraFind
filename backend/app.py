from flask import Flask, request, jsonify
from flask_cors import CORS
import db
import datetime
from datetime import timedelta
from nlp_search import search_plants_nlp
import mysql.connector

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    print("Home endpoint called")
    return jsonify({
        "message": "FloraFind API - Your Plant Care Companion",
        "version": "1.0",
        "features": ["Plant Search", "Garden Management", "Care Calendar", "Community"]
    })

@app.route("/query", methods=["GET"])
def query_plants():
    try:
        user_query = request.args.get("q", "").strip()
        user_id = request.args.get("user_id", 1, type=int)
        
        print(f"NLP Enhanced Query received: '{user_query}'")
        
        if not user_query:
            return jsonify({"error": "Please provide a query"}), 400
        
        # Database configuration for NLP search
        db_config = {
            'host': 'localhost',
            'database': 'florafind',
            'user': 'root',
            'password': 'anushka'  # Updated to match db.py
        }
        
        # Use advanced NLP search
        search_results = search_plants_nlp(user_query, db_config)
        
        # Log search
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO search_logs (user_id, query, results_count) VALUES (%s, %s, %s)", 
                          (user_id, user_query, len(search_results.get('plants', []))))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Logging error: {e}")
        
        if 'error' in search_results:
            return jsonify({
                "error": "Search failed", 
                "details": search_results['error'],
                "fallback_suggestions": ["tulsi", "neem", "rose", "mint", "aloe vera"]
            }), 500
        
        plants = search_results.get('plants', [])
        search_analysis = search_results.get('search_analysis', {})
        
        if not plants:
            # Smart suggestions based on NLP analysis
            suggestions = {
                "summer": ["zinnia", "portulaca", "vinca", "sunflower", "marigold"],
                "winter": ["rose", "lavender", "mint"],
                "beginner": ["tulsi", "mint", "aloe vera", "snake plant", "peace lily"],
                "indoor": ["snake plant", "peace lily", "aloe vera", "tulsi"],
                "medicinal": ["tulsi", "neem", "aloe vera", "lemon balm", "chamomile"]
            }
            
            # Use NLP analysis to provide better suggestions
            smart_suggestions = ["tulsi", "neem", "rose", "mint", "sunflower"]
            
            for modifier_type, modifier_value in search_analysis.get('modifiers', []):
                if modifier_type == 'difficulty' and modifier_value in suggestions:
                    smart_suggestions = suggestions[modifier_value]
                elif modifier_type == 'season' and modifier_value in suggestions:
                    smart_suggestions = suggestions[modifier_value]
                elif modifier_type == 'type' and modifier_value in suggestions:
                    smart_suggestions = suggestions[modifier_value]
            
            return jsonify({
                "message": f"No plants found for '{user_query}'. Here are some suggestions based on your search:",
                "suggestions": smart_suggestions,
                "search_analysis": search_analysis,
                "search_tips": [
                    "Try: 'easy summer plants for beginners'",
                    "Search: 'indoor medicinal herbs'",
                    "Ask: 'drought tolerant flowering plants'",
                    "Query: 'air purifying plants for home'"
                ]
            })
        
        # Get NLP analysis details if available
        nlp_analysis = search_results.get('nlp_analysis', {})
        
        return jsonify({
            "plants": plants,
            "count": len(plants),
            "search_analysis": search_analysis,
            "nlp_processing": {
                "intent_detected": search_analysis.get('intent', 'search'),
                "plant_mentions": search_analysis.get('plant_mentions', []),
                "care_aspects_found": search_analysis.get('care_aspects', []),
                "query_modifiers": search_analysis.get('modifiers', [])
            },
            "nlp_analysis_details": nlp_analysis
        })
        
    except Exception as e:
        print(f"NLP Query error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": "Advanced search temporarily unavailable", 
            "details": str(e),
            "fallback_suggestions": ["tulsi", "neem", "rose", "mint", "aloe vera"]
        }), 500

@app.route("/add_to_garden", methods=["POST"])
def add_to_garden():
    try:
        data = request.get_json()
        print(f"Add to garden request: {data}")
        
        if not data or 'user_id' not in data or 'plant_id' not in data:
            return jsonify({"error": "Missing user_id or plant_id"}), 400
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Check if plant already in garden
        cursor.execute("SELECT user_plant_id FROM user_plants WHERE user_id = %s AND plant_id = %s", 
                      (data['user_id'], data['plant_id']))
        existing = cursor.fetchone()
        
        if existing:
            cursor.close()
            conn.close()
            return jsonify({"success": True, "message": "Plant is already in your garden!"})
        
        # Add to garden
        cursor.execute("""INSERT INTO user_plants 
                         (user_id, plant_id, plant_nickname, location_in_garden, date_planted) 
                         VALUES (%s, %s, %s, %s, %s)""",
                      (data['user_id'], data['plant_id'], 
                       data.get('nickname', ''), 
                       data.get('location', 'garden'), 
                       datetime.date.today()))
        
        user_plant_id = cursor.lastrowid
        
        # Create basic care schedule
        cursor.execute("""INSERT INTO care_schedules 
                         (user_plant_id, task_type, frequency_days, next_due_date) 
                         VALUES (%s, %s, %s, %s)""",
                      (user_plant_id, 'watering', 3, 
                       datetime.date.today() + timedelta(days=3)))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True, 
            "user_plant_id": user_plant_id, 
            "message": "Plant added to your garden successfully!"
        })
        
    except Exception as e:
        print(f"Add to garden error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/my_garden/<int:user_id>", methods=["GET"])
def get_user_garden(user_id):
    try:
        print(f"Getting garden for user {user_id}")
        
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT up.user_plant_id, up.plant_nickname, up.location_in_garden, 
                   up.date_planted, up.current_health_score, up.notes,
                   p.plant_id, p.name, p.scientific_name, p.eco_impact_score,
                   cs.task_type, cs.next_due_date, cs.frequency_days
            FROM user_plants up 
            JOIN plants p ON up.plant_id = p.plant_id 
            LEFT JOIN care_schedules cs ON up.user_plant_id = cs.user_plant_id 
            WHERE up.user_id = %s
            ORDER BY up.user_plant_id
        """, (user_id,))
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if not results:
            return jsonify({
                "garden": [],
                "total_plants": 0,
                "total_eco_impact": 0,
                "message": "Your garden is empty. Add some plants to get started!"
            })
        
        # Group by plant
        garden = {}
        for row in results:
            plant_id = row['user_plant_id']
            if plant_id not in garden:
                garden[plant_id] = {
                    "plant_info": {
                        "user_plant_id": row['user_plant_id'],
                        "plant_id": row['plant_id'],
                        "name": row['name'],
                        "nickname": row['plant_nickname'] or row['name'],
                        "scientific_name": row['scientific_name'],
                        "health_score": row['current_health_score'] or 100,
                        "location": row['location_in_garden'],
                        "date_planted": str(row['date_planted']),
                        "eco_impact_score": row['eco_impact_score'] or 0,
                        "notes": row['notes']
                    },
                    "care_schedule": []
                }
            
            if row['task_type']:
                garden[plant_id]['care_schedule'].append({
                    "task": row['task_type'],
                    "next_due": str(row['next_due_date']),
                    "frequency_days": row['frequency_days'],
                    "overdue": row['next_due_date'] < datetime.date.today() if row['next_due_date'] else False
                })
        
        garden_list = list(garden.values())
        
        return jsonify({
            "garden": garden_list,
            "total_plants": len(garden_list),
            "total_eco_impact": sum(plant['plant_info']['eco_impact_score'] for plant in garden_list)
        })
        
    except Exception as e:
        print(f"Garden error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/complete_care_task", methods=["POST"])
def complete_care_task():
    try:
        data = request.get_json()
        print(f"Complete care task: {data}")
        
        if not data or 'user_plant_id' not in data or 'task_type' not in data:
            return jsonify({"error": "Missing user_plant_id or task_type"}), 400
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Points mapping
        points_map = {
            'watering': 10,
            'fertilizing': 15,
            'pruning': 20,
            'repotting': 25
        }
        
        points_earned = points_map.get(data['task_type'], 10)
        
        # Log activity
        cursor.execute("""INSERT INTO care_activities 
                         (user_plant_id, task_type, completed_date, points_earned) 
                         VALUES (%s, %s, %s, %s)""",
                      (data['user_plant_id'], data['task_type'], 
                       datetime.date.today(), points_earned))
        
        # Update user points
        user_id = data.get('user_id', 1)
        cursor.execute("UPDATE users SET plant_health_points = plant_health_points + %s WHERE user_id = %s", 
                      (points_earned, user_id))
        
        # Remove completed task from schedule and create next occurrence
        cursor.execute("""DELETE FROM care_schedules 
                         WHERE user_plant_id = %s AND task_type = %s""",
                      (data['user_plant_id'], data['task_type']))
        
        # Create next task with appropriate frequency
        frequency_map = {
            'watering': 3,
            'fertilizing': 30,
            'pruning': 90,
            'repotting': 365
        }
        
        next_frequency = frequency_map.get(data['task_type'], 7)
        next_due_date = datetime.date.today() + timedelta(days=next_frequency)
        
        cursor.execute("""INSERT INTO care_schedules 
                         (user_plant_id, task_type, frequency_days, next_due_date) 
                         VALUES (%s, %s, %s, %s)""",
                      (data['user_plant_id'], data['task_type'], next_frequency, next_due_date))
        
        # Update plant health
        cursor.execute("UPDATE user_plants SET current_health_score = LEAST(100, current_health_score + 5) WHERE user_plant_id = %s", 
                      (data['user_plant_id'],))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True, 
            "points_earned": points_earned, 
            "message": f"Great job! +{points_earned} points!",
            "next_due_date": str(next_due_date)
        })
        
    except Exception as e:
        print(f"Complete task error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/add_care_task", methods=["POST"])
def add_care_task():
    try:
        data = request.get_json()
        print(f"Adding care task: {data}")
        
        if not data or not all(k in data for k in ['user_plant_id', 'task_type', 'frequency_days']):
            return jsonify({"error": "Missing required fields: user_plant_id, task_type, frequency_days"}), 400
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Check if task already exists for this plant
        cursor.execute("SELECT * FROM care_schedules WHERE user_plant_id = %s AND task_type = %s", 
                      (data['user_plant_id'], data['task_type']))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing task
            cursor.execute("""UPDATE care_schedules 
                             SET frequency_days = %s, next_due_date = %s 
                             WHERE user_plant_id = %s AND task_type = %s""",
                          (data['frequency_days'], 
                           datetime.date.today() + timedelta(days=data['frequency_days']),
                           data['user_plant_id'], data['task_type']))
            message = "Care task updated successfully!"
        else:
            # Create new task
            cursor.execute("""INSERT INTO care_schedules 
                             (user_plant_id, task_type, frequency_days, next_due_date) 
                             VALUES (%s, %s, %s, %s)""",
                          (data['user_plant_id'], data['task_type'], data['frequency_days'], 
                           datetime.date.today() + timedelta(days=data['frequency_days'])))
            message = "Care task added successfully!"
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True, 
            "message": message
        })
        
    except Exception as e:
        print(f"Add care task error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/care_calendar/<int:plant_id>", methods=["GET"])
def get_care_calendar(plant_id):
    try:
        print(f"Getting care calendar for plant {plant_id}")
        
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM plants WHERE plant_id = %s", (plant_id,))
        plant = cursor.fetchone()
        
        if not plant:
            cursor.close()
            conn.close()
            return jsonify({"error": "Plant not found"}), 404
        
        # Current season
        current_month = datetime.datetime.now().month
        if current_month in [12, 1, 2]:
            season = "winter"
        elif current_month in [6, 7, 8]:
            season = "summer"
        else:
            season = "spring"
        
        care_schedule = {
            "plant_name": plant['name'],
            "current_season": season,
            "watering": {
                "frequency_days": 3,
                "next_due": (datetime.datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
            },
            "eco_impact_score": plant.get('eco_impact_score', 0),
            "difficulty_level": plant.get('difficulty_level', 'beginner'),
            "care_tips": {
                season: {
                    "watering": "Water every 3 days",
                    "sunlight": "Provide adequate sunlight",
                    "care": plant.get('care_instructions', 'Basic care needed')
                }
            }
        }
        
        cursor.close()
        conn.close()
        
        return jsonify(care_schedule)
        
    except Exception as e:
        print(f"Care calendar error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/community/challenges", methods=["GET"])
def get_challenges():
    try:
        print("Getting community challenges")
        
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""SELECT * FROM plant_challenges 
                         WHERE is_active = 1 AND end_date >= CURDATE() 
                         ORDER BY start_date ASC""")
        challenges = cursor.fetchall()
        
        # Convert dates to strings
        for challenge in challenges:
            challenge['start_date'] = str(challenge['start_date'])
            challenge['end_date'] = str(challenge['end_date'])
        
        cursor.close()
        conn.close()
        
        print(f"Found {len(challenges)} challenges")
        
        return jsonify({"challenges": challenges})
        
    except Exception as e:
        print(f"Challenges error: {str(e)}")
        return jsonify({"challenges": [], "error": str(e)})

@app.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    try:
        print("Getting leaderboard")
        
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""SELECT u.username, u.plant_health_points, u.level,
                               COUNT(up.user_plant_id) as total_plants
                         FROM users u 
                         LEFT JOIN user_plants up ON u.user_id = up.user_id 
                         GROUP BY u.user_id
                         ORDER BY u.plant_health_points DESC 
                         LIMIT 10""")
        
        leaderboard = cursor.fetchall()
        cursor.close()
        conn.close()
        
        print(f"Found {len(leaderboard)} users in leaderboard")
        
        return jsonify({"leaderboard": leaderboard})
        
    except Exception as e:
        print(f"Leaderboard error: {str(e)}")
        return jsonify({"leaderboard": [], "error": str(e)})

@app.route("/community/submit_tip", methods=["POST"])
def submit_tip():
    try:
        data = request.get_json()
        print(f"Submitting tip: {data}")
        
        if not data or not all(k in data for k in ['user_id', 'plant_name', 'care_tip']):
            return jsonify({"error": "Missing required fields"}), 400
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""INSERT INTO plant_submissions 
                         (user_id, plant_name, care_tip, location) 
                         VALUES (%s, %s, %s, %s)""",
                      (data['user_id'], data['plant_name'], 
                       data['care_tip'], data.get('location', '')))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True, 
            "message": "Thank you for sharing your plant wisdom! Your tip has been submitted."
        })
        
    except Exception as e:
        print(f"Submit tip error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/user_stats/<int:user_id>", methods=["GET"])
def get_user_stats(user_id):
    try:
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get user stats
        cursor.execute("SELECT plant_health_points, level FROM users WHERE user_id = %s", (user_id,))
        user_stats = cursor.fetchone()
        
        if not user_stats:
            # Create default user if not exists
            cursor.execute("INSERT INTO users (user_id, username, plant_health_points, level) VALUES (%s, %s, %s, %s)",
                          (user_id, f"User{user_id}", 0, 1))
            conn.commit()
            user_stats = {"plant_health_points": 0, "level": 1}
        
        # Get badge count
        cursor.execute("SELECT COUNT(*) as badge_count FROM user_badges WHERE user_id = %s", (user_id,))
        badge_result = cursor.fetchone()
        badge_count = badge_result['badge_count'] if badge_result else 0
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "points": user_stats['plant_health_points'],
            "level": user_stats['level'],
            "badges": badge_count
        })
        
    except Exception as e:
        print(f"User stats error: {str(e)}")
        return jsonify({"points": 0, "level": 1, "badges": 0})

if __name__ == "__main__":
    print("FloraFind API starting...")
    print("Features: Plant Search | Garden Management | Care Calendar | Community")
    app.run(debug=True, port=5000, host='127.0.0.1')
