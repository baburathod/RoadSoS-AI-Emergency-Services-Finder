🚨 RoadSoS — AI Emergency Services Finder
National Road Safety Hackathon 2026 | IIT Madras | CoERS

"We save lives by connecting accident victims to emergency services in seconds — even offline."

Team:
- RAMAVATH BABU (Team Leader) - Guru Ghasidas Vishwavidyalaya (GGU), Bilaspur
- Dyaga Nishmitha - Sreenidhi Institute of Science and Technology
- Anvita Sharma - Dr. Akhilesh Das Gupta Institute of Technology and Management (ADGITM), New Delhi
- Arpita Patel - Rewa Engineering College (REC), Rewa, Madhya Pradesh
- Maithili Pandey - Padmabhushan Vasantdada Patil Pratishthan's College of Engineering (PVPPCE), Mumbai, Maharashtra

🎯 What is RoadSoS?
RoadSoS is a full-stack, AI-powered emergency response system that provides instant guidance to road accident victims and bystanders. It works in panic conditions, low-network environments, and supports English, Hindi, and Telugu.

🚀 Quick Start (2 minutes)
1. Backend Setup
```bash
cd backend/

# Install dependencies
pip install fastapi uvicorn

# Create the database
python database_setup.py

# Start the API server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
2. Frontend
```bash
# Option A: Open directly (no server needed)
open frontend/index.html

# Option B: Serve locally
cd frontend/
python -m http.server 3000
# Visit: http://localhost:3000
```

🏗️ Architecture
RoadSoS/
├── backend/
│   ├── main.py              # FastAPI app — all routes
│   ├── database_setup.py    # SQLite schema + data population
│   └── roadsos.db           # Auto-generated SQLite database
│
├── frontend/
│   ├── index.html           # Main PWA HTML structure
│   ├── style.css            # Stylesheets and theming
│   └── script.js            # Chatbot, map, and offline logic
│
└── README.md

📡 API Endpoints
Method | Endpoint | Description
--- | --- | ---
GET | / | Health check
GET | /api/nearby?lat=&lon= | Nearest emergency services
POST | /api/chatbot | AI chatbot (intent + severity detection)
GET | /api/first-aid | First aid steps (3 languages)
GET | /api/emergency-numbers/IN | India emergency numbers
GET | /api/cities | Coverage stats
GET | /api/stats | Database stats
GET | /docs | Interactive API docs (FastAPI auto-generated)

Chatbot Example
```bash
curl -X POST http://localhost:8000/api/chatbot \
  -H "Content-Type: application/json" \
  -d '{"message": "मेरा एक्सीडेंट हो गया है", "lat": 17.385, "lon": 78.487}'
```

🗃️ Database Schema
emergency_services
* 50 real services across 5 major Indian cities
* Types: trauma_center, ambulance, police, vehicle_rescue
* GPS coordinates for haversine distance calculation

emergency_numbers
* National helpline numbers (India)
* 108 Ambulance | 100 Police | 101 Fire | 112 Unified | 1073 Road Accident

road_accident_tips
* 30 first-aid steps
* 3 languages: English, Hindi, Telugu
* 3 scenarios: general, bleeding, unconscious


🧠 AI System
The chatbot uses:
* Unicode-based language detection (Devanagari → Hindi, Telugu script → Telugu)
* Multi-language keyword intent detection (ambulance, police, vehicle_rescue, trauma_center)
* Severity scoring (critical → high → medium → low) based on keyword analysis
* Panic detection for short/urgent inputs ("help", "accident", etc.)
* Contextual responses in the detected language


🌍 City Coverage
Phase 1 (Live — MVP)
✅ Hyderabad — 10 services
✅ Mumbai — 10 services
✅ New Delhi — 10 services
✅ Bengaluru — 10 services
✅ Chennai — 10 services

Phase 2 (Planned)
Pune · Kolkata · Ahmedabad · Jaipur · Lucknow · Chandigarh
Phase 3 (Future)
Pan-India · Rural/Highway zones · International

Design philosophy: Phase 1 covers India's highest-accident-density cities for demo clarity and real data accuracy. The database schema supports unlimited city expansion with zero code changes.


🛡️ Key Features
Feature | Status
--- | ---
One-tap SOS button | ✅
AI chatbot (EN/HI/TE) | ✅
GPS-based service finder | ✅
Offline mode (SQLite fallback) | ✅
First-aid step guides | ✅
Quick-call emergency numbers | ✅
Good Samaritan law info | ✅
Haversine distance calculation | ✅
Severity detection | ✅
Panic input handling | ✅
Map visualization | ✅
Mobile-first PWA-ready UI | ✅

🧪 Test Scenarios
```bash
# Test 1: Clear English input
curl -X POST http://localhost:8000/api/chatbot -d '{"message":"I met with an accident, I am bleeding"}'

# Test 2: Panic input
curl -X POST http://localhost:8000/api/chatbot -d '{"message":"help fast accident"}'

# Test 3: Hindi input
curl -X POST http://localhost:8000/api/chatbot -d '{"message":"मेरा एक्सीडेंट हो गया है", "lat":28.61, "lon":77.21}'

# Test 4: Telugu input
curl -X POST http://localhost:8000/api/chatbot -d '{"message":"నాకు యాక్సిడెంట్ అయింది", "lat":17.38, "lon":78.49}'

# Test 5: Critical injury
curl -X POST http://localhost:8000/api/chatbot -d '{"message":"unconscious person, severe bleeding, not breathing"}'

# Test 6: Location-based search
curl "http://localhost:8000/api/nearby?lat=19.076&lon=72.877&radius_km=30"
```

🏆 Hackathon Presentation Note

"We implemented RoadSoS with 5 major cities for maximum accuracy and demo reliability, while designing the system to scale across India and beyond. Our offline-first architecture ensures the system works even in low-network accident zones, and our AI chatbot handles panicked, short, and multilingual inputs — because in a real emergency, every second counts."


📊 Technical Stack
* Backend: Python 3.9+ · FastAPI · SQLite · Uvicorn
* Frontend: Vanilla HTML/CSS/JS · PWA-ready · Mobile-first
* AI: Heuristic NLP · Unicode language detection · Keyword intent scoring
* Distance: Haversine formula (GPS accuracy)
* Database: SQLite (offline-capable, embeddable)

Built for the National Road Safety Hackathon 2026 | IIT Madras | CoERS
