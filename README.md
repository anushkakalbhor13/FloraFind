# 🌱 FloraFind - AI-Powered Plant Care Assistant

FloraFind is an intelligent, NLP-enhanced web application that helps users discover, manage, and care for plants through natural language queries. The platform combines advanced natural language processing, weather integration, and gamification to create an engaging plant care experience.

## ✨ Key Features

### 🤖 Intelligent Plant Search
- **NLP-Powered Queries**: Ask questions in natural language like "easy indoor plants for beginners" or "medicinal herbs for summer"
- **Semantic Understanding**: Advanced intent recognition and entity extraction using spaCy
- **Multi-language Support**: Detect and process queries in multiple languages
- **Smart Suggestions**: Context-aware plant recommendations based on your query

### 🌿 Garden Management
- **Personal Garden**: Track all your plants in one place
- **Care Schedules**: Automated reminders for watering, fertilizing, pruning, and more
- **Health Tracking**: Monitor plant health scores and care history
- **Custom Tasks**: Create personalized care schedules for each plant

### 📅 Care Calendar
- **Seasonal Care**: Weather-based care recommendations
- **Task Reminders**: Never miss a watering or care task
- **Export Calendar**: Download your care schedule
- **Upcoming Tasks**: View all pending care activities

### 🌍 Community Features
- **Plant Challenges**: Participate in community gardening challenges
- **Share Tips**: Contribute your plant care wisdom
- **Leaderboard**: Compete with other plant enthusiasts
- **Community Tips**: Learn from experienced gardeners

### 🎮 Gamification
- **Points System**: Earn points for completing care tasks
- **Achievements & Badges**: Unlock badges as you progress
- **Level Progression**: Level up as you care for more plants
- **Eco Impact Score**: Track your environmental contribution

### 🌤️ Weather Integration
- **Location-Based Recommendations**: Get plants suited to your climate
- **Weather-Aware Care**: Adjust care schedules based on current weather
- **Seasonal Suggestions**: Discover plants perfect for your current season
- **Native Plant Finder**: Find plants native to your region

## 🛠️ Technology Stack

### Backend
- **Python 3.10+**
- **Flask**: Web framework for RESTful API
- **MySQL**: Relational database for plant data and user management
- **spaCy**: Advanced NLP for natural language processing
- **RapidFuzz**: Fuzzy string matching for plant name recognition
- **langdetect**: Language detection for multilingual support

### Frontend
- **HTML5/CSS3**: Modern, responsive web interface
- **JavaScript (ES6+)**: Interactive client-side functionality
- **Font Awesome**: Icon library
- **Google Fonts (Inter)**: Typography

### Database Schema
- **Plants**: Comprehensive plant database with care instructions
- **Users**: User profiles with gamification data
- **User Plants**: Personal garden tracking
- **Care Schedules**: Automated care reminders
- **Community Features**: Challenges, submissions, leaderboard
- **Search Logs**: Analytics and query tracking

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- MySQL 5.7 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/FloraFind.git
cd FloraFind
```

2. **Navigate to backend directory**
```bash
cd backend
```

3. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Install spaCy language model**
```bash
python -m spacy download en_core_web_sm
```

6. **Set up MySQL database**
   - Create a MySQL database named `florafind`
   - Update database credentials in `db.py`:
   ```python
   host="localhost"
   user="your_username"
   password="your_password"
   database="florafind"
   ```

7. **Initialize database schema**
```bash
mysql -u your_username -p florafind < database_schema.sql
mysql -u your_username -p florafind < database_data.sql
```

8. **Run the Flask server**
```bash
python app.py
```

The backend API will be available at `http://127.0.0.1:5000`

### Frontend Setup

1. **Open the frontend**
   - Simply open `frontend/index.html` in a web browser, or
   - Use a local web server (recommended):
   ```bash
   # Using Python
   cd frontend
   python -m http.server 8000
   
   # Using Node.js (if installed)
   npx http-server -p 8000
   ```

2. **Access the application**
   - Navigate to `http://localhost:8000` in your browser

## 🚀 Usage

### Starting the Application

1. **Start the backend server** (from `backend/` directory):
   ```bash
   python app.py
   ```

2. **Open the frontend** (from `frontend/` directory):
   - Use a local server or open `index.html` directly

3. **Start exploring**:
   - Use the chat interface to search for plants
   - Add plants to your garden
   - Set up care schedules
   - Participate in community challenges

### Example Queries

- "Show me easy indoor plants for beginners"
- "What are the best summer plants for Mumbai?"
- "Medicinal herbs that grow in monsoon"
- "How do I care for roses?"
- "Air purifying plants for home"
- "Native plants for my location"

## 📁 Project Structure

```
FloraFind/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── db.py                  # Database connection
│   ├── nlp_processor.py       # Advanced NLP processing
│   ├── nlp_search.py         # Semantic plant search
│   ├── weather.py            # Weather integration
│   ├── models.py             # Data models
│   ├── database_schema.sql   # Database schema
│   ├── database_data.sql     # Seed data
│   ├── requirements.txt      # Python dependencies
│   └── venv/                  # Virtual environment
├── frontend/
│   ├── index.html            # Main HTML file
│   ├── app.js               # JavaScript functionality
│   └── main.css             # Styling
└── README.md                # This file
```

## 🔌 API Endpoints

### Plant Search
- `GET /query?q=<query>&user_id=<id>` - Search plants using NLP

### Garden Management
- `GET /my_garden/<user_id>` - Get user's garden
- `POST /add_to_garden` - Add plant to garden
- `POST /complete_care_task` - Mark care task as complete
- `POST /add_care_task` - Add custom care task

### Care Calendar
- `GET /care_calendar/<plant_id>` - Get care schedule for plant

### Community
- `GET /community/challenges` - Get active challenges
- `GET /leaderboard` - Get user rankings
- `POST /community/submit_tip` - Submit plant care tip

### User Stats
- `GET /user_stats/<user_id>` - Get user statistics

## 🎯 Key Features Explained

### NLP Processing
FloraFind uses advanced NLP techniques including:
- **Tokenization**: Breaking queries into meaningful tokens
- **POS Tagging**: Identifying parts of speech
- **Named Entity Recognition**: Extracting plant names and locations
- **Dependency Parsing**: Understanding query structure
- **Lemmatization**: Normalizing words to root forms
- **Intent Classification**: Determining user intent (care advice, search, etc.)

### Semantic Search
The search system understands:
- Plant categories (fruit, flower, medicinal, herb, etc.)
- Care requirements (watering, sunlight, difficulty)
- Seasonal preferences
- Location-based recommendations
- Fuzzy matching for plant name variations

## 🐛 Troubleshooting

### Backend Issues
- **Database connection error**: Check MySQL credentials in `db.py`
- **spaCy model not found**: Run `python -m spacy download en_core_web_sm`
- **Import errors**: Ensure virtual environment is activated and dependencies are installed

### Frontend Issues
- **API connection error**: Ensure backend server is running on port 5000
- **CORS errors**: Backend includes CORS support - check Flask-CORS is installed

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- spaCy for excellent NLP capabilities
- Flask community for robust web framework
- All the plant enthusiasts who contribute tips and knowledge

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for plant lovers everywhere** 🌿

