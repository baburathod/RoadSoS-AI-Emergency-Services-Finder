"""
RoadSoS - FastAPI Backend
National Road Safety Hackathon 2026 | IIT Madras | CoERS
AI-powered Emergency Services Finder for Road Accident Victims
"""
 
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sqlite3
import math
import os
import re
 
app = FastAPI(
    title="RoadSoS API",
    description="AI-powered Emergency Services Finder for Road Accident Victims",
    version="2.0.0"
)
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
 
DB_PATH = os.path.join(os.path.dirname(__file__), "roadsos.db")
 
 
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
 
 
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
 
 
# ─── CHATBOT LOGIC ────────────────────────────────────────────────────────────
 
INTENT_KEYWORDS = {
    "ambulance": {
        "en": ["ambulance", "hospital", "injured", "bleeding", "unconscious", "hurt", "medical",
               "doctor", "blood", "breathe", "breathing", "pain", "severe", "wound", "fracture",
               "broken bone", "head injury", "chest pain"],
        "hi": ["एम्बुलेंस", "अस्पताल", "चोट", "खून", "बेहोश", "दर्द", "डॉक्टर", "घायल", "दुर्घटना", "सांस"],
        "te": ["అంబులెన్స్", "ఆసుపత్రి", "గాయం", "రక్తం", "స్పృహలేని", "నొప్పి", "వైద్యుడు"],
        "ta": ["ஆம்புலன்ஸ்", "மருத்துவமனை", "காயம்", "இரத்தம்", "மயக்கம்", "வலி", "மருத்துவர்"],
        "kn": ["ಆಂಬ್ಯುಲೆನ್ಸ್", "ಆಸ್ಪತ್ರೆ", "ಗಾಯ", "ರಕ್ತ", "ಪ್ರಜ್ಞೆಯಿಲ್ಲದ", "ನೋವು", "ವೈದ್ಯರು"]
    },
    "police": {
        "en": ["police", "accident", "crash", "collision", "hit", "report", "help", "emergency",
               "dangerous", "threat", "crime", "robbery", "attack"],
        "hi": ["पुलिस", "दुर्घटना", "क्रैश", "टक्कर", "मदद", "आपातकाल", "रिपोर्ट"],
        "te": ["పోలీసు", "ప్రమాదం", "క్రాష్", "ఢీకొనడం", "సహాయం", "అత్యవసర"],
        "ta": ["காவல்துறை", "விபத்து", "மோதல்", "உதவி", "அவசரம்"],
        "kn": ["ಪೊಲೀಸ್", "ಅಪಘಾತ", "ಸಹಾಯ", "ತುರ್ತು"]
    },
    "vehicle_rescue": {
        "en": ["tow", "breakdown", "stuck", "puncture", "tyre", "tire", "vehicle", "car", "bike",
               "truck", "lorry", "stranded", "engine", "fuel", "petrol", "diesel"],
        "hi": ["टो", "ब्रेकडाउन", "गाड़ी", "पंचर", "टायर", "वाहन", "फंसे", "इंजन"],
        "te": ["టో", "బ్రేక్డౌన్", "వాహనం", "పంక్చర్", "టైర్", "చిక్కుకుపోయారు"],
        "ta": ["வாகனம்", "பழுது", "டயர்", "பஞ்சர்", "மாட்டிக்கொண்டது"],
        "kn": ["ವಾಹನ", "ಟೈರ್", "ಪಂಕ್ಚರ್", "ಸಿಲುಕಿದೆ"]
    },
    "trauma_center": {
        "en": ["severe", "critical", "surgery", "spine", "spinal", "head", "neck", "brain",
               "internal", "organ", "coma", "icu", "intensive", "life-threatening"],
        "hi": ["गंभीर", "ऑपरेशन", "रीढ़", "सिर", "दिमाग", "जानलेवा"],
        "te": ["తీవ్రమైన", "శస్త్రచికిత్స", "వెన్నెముక", "తల", "మెదడు", "ప్రాణాంతకమైన"],
        "ta": ["தீவிரமான", "அறுவை சிகிச்சை", "முதுகெலும்பு", "தலை", "மூளை", "ஆபத்தான"],
        "kn": ["ಗಂಭೀರ", "ಶಸ್ತ್ರಚಿಕಿತ್ಸೆ", "ಬೆನ್ನುಹುರಿ", "ತಲೆ", "ಮೆದುಳು", "ಪ್ರಾಣಾಪಾಯ"]
    }
}
 
SEVERITY_KEYWORDS = {
    "critical": ["unconscious", "not breathing", "severe bleeding", "no pulse", "coma",
                 "बेहोश", "सांस नहीं", "गंभीर खून", "स्పృహలేని", "శ్వాస లేదు",
                 "critical", "life threatening", "dying", "dead"],
    "high": ["bleeding", "fracture", "broken", "head injury", "chest pain", "vomiting blood",
             "खून", "फ्रैक्चर", "सिर चोट", "రక్తం", "పగిలిన", "తల గాయం"],
    "medium": ["accident", "crash", "pain", "hurt", "injury", "collision",
               "दुर्घटना", "दर्द", "चोट", "ప్రమాదం", "నొప్పి", "గాయం"],
    "low": ["minor", "scratch", "small", "little", "slight",
            "छोटा", "थोड़ा", "చిన్న", "కొద్దిగా"]
}
 
PANIC_PATTERNS = [
    r"^help[!? ]*$", r"^sos[!? ]*$", r"^emergency[!? ]*$",
    r"^accident[!? ]*$", r"^please help", r"^help me"
]
 
RESPONSES = {
    "en": {
        "greeting": "🚨 RoadSoS Emergency AI active. Detecting your situation...",
        "ambulance": "🚑 Ambulance needed! Finding nearest services. **Call 108 NOW** for immediate dispatch.",
        "police": "🚔 Police assistance needed! Nearest stations found. **Call 100 or 112** immediately.",
        "vehicle_rescue": "🔧 Vehicle rescue team located near you. Help is on the way!",
        "trauma_center": "🏥 Critical care hospital located. **Time is critical — call 108 NOW.**",
        "panic": "🆘 Emergency detected! I'm alerting all services. **CALL 112 RIGHT NOW.** Stay on the line.",
        "first_aid_bleed": "🩸 **STOP BLEEDING**: Press hard with clean cloth. Keep pressing — do NOT remove. Elevate limb if possible.",
        "first_aid_unconscious": "💓 **CPR**: 30 hard chest compressions + 2 breaths. Push fast (100/min). Don't stop till help arrives.",
        "first_aid_general": "⚠️ Stay calm. Do not move injured person. Keep them warm and conscious. Help is coming.",
        "no_location": "📍 Please share your location so I can find the nearest services.",
        "offline": "📴 Offline mode. Emergency numbers: Ambulance **108** | Police **100** | Unified **112**",
        "good_samaritan": "⚖️ You are protected by the Good Samaritan Law. Help the victim — you cannot be detained for helping.",
    },
    "hi": {
        "greeting": "🚨 RoadSoS आपातकालीन AI सक्रिय। स्थिति का पता लगा रहा हूं...",
        "ambulance": "🚑 एम्बुलेंस की ज़रूरत है! **अभी 108 पर कॉल करें!** निकटतम सेवाएं मिल रही हैं।",
        "police": "🚔 पुलिस सहायता चाहिए! **100 या 112 पर कॉल करें।** निकटतम थाना मिल रहा है।",
        "vehicle_rescue": "🔧 वाहन बचाव टीम आपके पास मिली। मदद रास्ते में है!",
        "trauma_center": "🏥 आपातकालीन अस्पताल मिला। **समय महत्वपूर्ण है — अभी 108 पर कॉल करें।**",
        "panic": "🆘 आपातकाल! सभी सेवाएं सतर्क हो रही हैं। **अभी 112 पर कॉल करें।**",
        "first_aid_bleed": "🩸 **खून रोकें**: साफ कपड़े से कसकर दबाएं। कपड़ा मत हटाएं। अंग ऊपर उठाएं।",
        "first_aid_unconscious": "💓 **CPR**: 30 बार छाती दबाएं + 2 सांस दें। तेज़ दबाएं (100/मिनट)।",
        "first_aid_general": "⚠️ शांत रहें। घायल को मत हिलाएं। गर्म और होश में रखें। मदद आ रही है।",
        "no_location": "📍 कृपया अपना स्थान साझा करें ताकि निकटतम सेवाएं मिल सकें।",
        "offline": "📴 ऑफलाइन मोड। एम्बुलेंस: **108** | पुलिस: **100** | एकीकृत: **112**",
        "good_samaritan": "⚖️ आप गुड सेमेरिटन कानून से सुरक्षित हैं। पीड़ित की मदद करें — आपको रोका नहीं जा सकता।",
    },
    "te": {
        "greeting": "🚨 RoadSoS అత్యవసర AI సక్రియంగా ఉంది. మీ పరిస్థితిని గుర్తిస్తున్నాను...",
        "ambulance": "🚑 అంబులెన్స్ అవసరం! **ఇప్పుడే 108 కి కాల్ చేయండి!** దగ్గర సేవలు వెతుకుతున్నాను.",
        "police": "🚔 పోలీస్ సహాయం కావాలి! **100 లేదా 112 కి కాల్ చేయండి।** దగ్గర స్టేషన్ వెతుకుతున్నాను.",
        "vehicle_rescue": "🔧 వాహన రెస్క్యూ టీమ్ మీ దగ్గర ఉంది. సహాయం వస్తోంది!",
        "trauma_center": "🏥 అత్యవసర ఆసుపత్రి కనుగొన్నారు. **సమయం విలువైనది — ఇప్పుడే 108 కి కాల్ చేయండి।**",
        "panic": "🆘 అత్యవసర పరిస్థితి! అన్ని సేవలు హెచ్చరించబడుతున్నాయి. **ఇప్పుడే 112 కి కాల్ చేయండి।**",
        "first_aid_bleed": "🩸 **రక్తస్రావం ఆపండి**: శుభ్రమైన గుడ్డతో గట్టిగా అదుముండి. గుడ్డ తీయకండి. అంగం పైకి ఎత్తండి.",
        "first_aid_unconscious": "💓 **CPR**: 30 రొమ్ము నొక్కులు + 2 శ్వాసలు. వేగంగా నొక్కండి (100/నిమిషం).",
        "first_aid_general": "⚠️ శాంతంగా ఉండండి. గాయపడిన వ్యక్తిని కదపకండి. వెచ్చగా మరియు స్పృహలో ఉంచండి.",
        "no_location": "📍 దగ్గర సేవలు కనుగొనడానికి దయచేసి మీ స్థానాన్ని పంచుకోండి.",
        "offline": "📴 ఆఫ్లైన్ మోడ్. అంబులెన్స్: **108** | పోలీస్: **100** | ఏకీకృత: **112**",
        "good_samaritan": "⚖️ మీరు గుడ్ సమారిటన్ చట్టం ద్వారా రక్షించబడ్డారు. బాధితుడికి సహాయం చేయండి.",
    },
    "ta": {
        "greeting": "🚨 RoadSoS அவசர AI செயலில் உள்ளது. உங்கள் நிலைமையை கண்டறிகிறது...",
        "ambulance": "🚑 ஆம்புலன்ஸ் தேவை! **உடனடியாக 108 ஐ அழைக்கவும்!** அருகில் உள்ள சேவைகளை தேடுகிறது.",
        "police": "🚔 காவல் உதவி தேவை! **100 அல்லது 112 ஐ அழைக்கவும்.**",
        "vehicle_rescue": "🔧 வாகன மீட்பு குழு உங்கள் அருகில் உள்ளது. உதவி வருகிறது!",
        "trauma_center": "🏥 அவசர மருத்துவமனை கண்டறியப்பட்டது. **நேரம் முக்கியமானது — உடனடியாக 108 ஐ அழைக்கவும்.**",
        "panic": "🆘 அவசரம்! அனைத்து சேவைகளும் உஷார்படுத்தப்படுகின்றன. **உடனடியாக 112 ஐ அழைக்கவும்.**",
        "first_aid_bleed": "🩸 **இரத்தப்போக்கை நிறுத்தவும்**: சுத்தமான துணியால் அழுத்தவும். துணியை அகற்ற வேண்டாம். உறுப்பை உயர்த்தவும்.",
        "first_aid_unconscious": "💓 **CPR**: 30 மார்பு அழுத்தங்கள் + 2 சுவாசங்கள். வேகமாக அழுத்தவும் (100/நிமிடம்).",
        "first_aid_general": "⚠️ அமைதியாக இருங்கள். காயம் அடைந்தவரை நகர்த்த வேண்டாம்.",
        "no_location": "📍 அருகில் உள்ள சேவைகளை கண்டறிய தயவுசெய்து உங்கள் இருப்பிடத்தை பகிரவும்.",
        "offline": "📴 ஆஃப்லைன் முறை. ஆம்புலன்ஸ்: **108** | காவல்துறை: **100** | ஒருங்கிணைந்த: **112**",
        "good_samaritan": "⚖️ நல்ல சமாரியன் சட்டத்தால் நீங்கள் பாதுகாக்கப்படுகிறீர்கள். பாதிக்கப்பட்டவருக்கு உதவுங்கள்.",
    },
    "kn": {
        "greeting": "🚨 RoadSoS ತುರ್ತು AI ಸಕ್ರಿಯವಾಗಿದೆ. ನಿಮ್ಮ ಪರಿಸ್ಥಿತಿಯನ್ನು ಪತ್ತೆಹಚ್ಚಲಾಗುತ್ತಿದೆ...",
        "ambulance": "🚑 ಆಂಬ್ಯುಲೆನ್ಸ್ ಅಗತ್ಯವಿದೆ! **ಈಗಲೇ 108 ಗೆ ಕರೆ ಮಾಡಿ!**",
        "police": "🚔 ಪೊಲೀಸ್ ಸಹಾಯ ಬೇಕು! **100 ಅಥವಾ 112 ಗೆ ಕರೆ ಮಾಡಿ.**",
        "vehicle_rescue": "🔧 ವಾಹನ ಪಾರುಗಾಣಿಕಾ ತಂಡ ನಿಮ್ಮ ಸಮೀಪದಲ್ಲಿದೆ. ಸಹಾಯ ಬರುತ್ತಿದೆ!",
        "trauma_center": "🏥 ತುರ್ತು ಆಸ್ಪತ್ರೆ ಪತ್ತೆಯಾಗಿದೆ. **ಸಮಯ ಮುಖ್ಯ — ಈಗಲೇ 108 ಗೆ ಕರೆ ಮಾಡಿ.**",
        "panic": "🆘 ತುರ್ತು! ಎಲ್ಲಾ ಸೇವೆಗಳನ್ನು ಎಚ್ಚರಿಸಲಾಗುತ್ತಿದೆ. **ಈಗಲೇ 112 ಗೆ ಕರೆ ಮಾಡಿ.**",
        "first_aid_bleed": "🩸 **ರಕ್ತಸ್ರಾವ ನಿಲ್ಲಿಸಿ**: ಸ್ವಚ್ಛವಾದ ಬಟ್ಟೆಯಿಂದ ಗಟ್ಟಿಯಾಗಿ ಒತ್ತಿ ಹಿಡಿಯಿರಿ. ಬಟ್ಟೆಯನ್ನು ತೆಗೆಯಬೇಡಿ.",
        "first_aid_unconscious": "💓 **CPR**: 30 ಎದೆ ಒತ್ತಡಗಳು + 2 ಉಸಿರಾಟಗಳು. ವೇಗವಾಗಿ ಒತ್ತಿರಿ (100/ನಿಮಿಷ).",
        "first_aid_general": "⚠️ ಶಾಂತವಾಗಿರಿ. ಗಾಯಾಳುವನ್ನು ಸರಿಸಬೇಡಿ.",
        "no_location": "📍 ಹತ್ತಿರದ ಸೇವೆಗಳನ್ನು ಹುಡುಕಲು ದಯವಿಟ್ಟು ನಿಮ್ಮ ಸ್ಥಳವನ್ನು ಹಂಚಿಕೊಳ್ಳಿ.",
        "offline": "📴 ಆಫ್‌ಲೈನ್ ಮೋಡ್. ಆಂಬ್ಯುಲೆನ್ಸ್: **108** | ಪೊಲೀಸ್: **100** | ಏಕೀಕೃತ: **112**",
        "good_samaritan": "⚖️ ನೀವು ಗುಡ್ ಸಮರಿಟನ್ ಕಾನೂನಿನಿಂದ ರಕ್ಷಿಸಲ್ಪಟ್ಟಿದ್ದೀರಿ. ಸಂತ್ರಸ್ತರಿಗೆ ಸಹಾಯ ಮಾಡಿ.",
    }
}
 
 
def detect_language(text: str) -> str:
    """Detect language from Unicode ranges."""
    # Kannada Unicode range: 0C80–0CFF
    if re.search(r'[\u0C80-\u0CFF]', text):
        return "kn"
    # Tamil Unicode range: 0B80–0BFF
    if re.search(r'[\u0B80-\u0BFF]', text):
        return "ta"
    # Telugu Unicode range: 0C00–0C7F
    if re.search(r'[\u0C00-\u0C7F]', text):
        return "te"
    # Devanagari (Hindi) Unicode range: 0900–097F
    if re.search(r'[\u0900-\u097F]', text):
        return "hi"
    return "en"
 
 
def detect_severity(text: str) -> str:
    text_lower = text.lower()
    for level in ["critical", "high", "medium", "low"]:
        if any(kw in text_lower for kw in SEVERITY_KEYWORDS[level]):
            return level
    return "medium"  # default
 
 
def detect_intents(text: str) -> list:
    text_lower = text.lower()
    detected = []
    for intent, lang_keywords in INTENT_KEYWORDS.items():
        for lang_kws in lang_keywords.values():
            if any(kw in text_lower for kw in lang_kws):
                detected.append(intent)
                break
    if not detected:
        detected = ["ambulance", "police", "trauma_center"]
    return list(dict.fromkeys(detected))  # deduplicate while preserving order
 
 
def is_panic_input(text: str) -> bool:
    t = text.strip().lower()
    return any(re.match(p, t) for p in PANIC_PATTERNS) or len(t.split()) <= 2
 
 
def build_response(intents: list, lang: str, severity: str, is_panic: bool) -> str:
    r = RESPONSES.get(lang, RESPONSES["en"])
    parts = []
 
    if is_panic or severity == "critical":
        parts.append(r["panic"])
    
    for intent in intents:
        if intent in r:
            parts.append(r[intent])
 
    if "bleeding" in ["high", "critical"] and severity in ["high", "critical"]:
        parts.append(r["first_aid_bleed"])
    
    if not parts:
        parts.append(r["first_aid_general"])
 
    parts.append(r["good_samaritan"])
    return "\n\n".join(parts)
 
 
# ─── MODELS ──────────────────────────────────────────────────────────────────
 
class ChatRequest(BaseModel):
    message: str = ""
    lat: Optional[float] = None
    lon: Optional[float] = None
    language: Optional[str] = None
 
 
# ─── ROUTES ──────────────────────────────────────────────────────────────────
 
@app.get("/")
def root():
    return {
        "status": "RoadSoS API Running ✅",
        "version": "2.0.0",
        "hackathon": "IIT Madras Road Safety Hackathon 2026",
        "cities": ["Hyderabad", "Mumbai", "New Delhi", "Bengaluru", "Chennai"]
    }
 
 
@app.get("/api/nearby")
def get_nearby_services(
    lat: float = Query(...),
    lon: float = Query(...),
    radius_km: float = Query(50.0),
    service_type: Optional[str] = Query(None),
    limit: int = Query(5)
):
    conn = get_db()
    query = "SELECT * FROM emergency_services"
    params = []
    if service_type:
        query += " WHERE service_type = ?"
        params.append(service_type)
    rows = conn.execute(query, params).fetchall()
    conn.close()
 
    results = []
    for row in rows:
        dist = haversine(lat, lon, row["latitude"], row["longitude"])
        if dist <= radius_km:
            results.append({
                "id": row["id"],
                "name": row["name"],
                "service_type": row["service_type"],
                "address": row["address"],
                "city": row["city"],
                "state": row["state"],
                "latitude": row["latitude"],
                "longitude": row["longitude"],
                "phone": row["phone"],
                "phone_alt": row["phone_alt"],
                "available_24h": bool(row["available_24h"]),
                "rating": row["rating"],
                "specialty": row["specialty"],
                "languages": row["languages"].split(",") if row["languages"] else [],
                "distance_km": round(dist, 2),
                "eta_minutes": max(1, round(dist / 40 * 60))
            })
 
    results.sort(key=lambda x: x["distance_km"])
 
    grouped = {}
    counts = {}
    for r in results:
        t = r["service_type"]
        counts[t] = counts.get(t, 0) + 1
        if counts[t] <= limit:
            grouped.setdefault(t, []).append(r)
 
    return {
        "status": "success",
        "user_location": {"lat": lat, "lon": lon},
        "radius_km": radius_km,
        "total_found": len(results),
        "services": grouped
    }
 
 
@app.get("/api/emergency-numbers/{country_code}")
def get_emergency_numbers(country_code: str):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM emergency_numbers WHERE UPPER(country_code) = UPPER(?)",
        (country_code,)
    ).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail=f"No data for: {country_code}")
    return dict(row)
 
 
@app.get("/api/first-aid")
def get_first_aid(
    language: str = Query("English"),
    scenario: str = Query("general")
):
    lang_map = {"english": "English", "hindi": "Hindi", "telugu": "Telugu", "tamil": "Tamil", "kannada": "Kannada",
                "en": "English", "hi": "Hindi", "te": "Telugu", "ta": "Tamil", "kn": "Kannada"}
    lang = lang_map.get(language.lower(), "English")
 
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM road_accident_tips WHERE language=? AND scenario=? ORDER BY step_number",
        (lang, scenario)
    ).fetchall()
    if not rows:
        rows = conn.execute(
            "SELECT * FROM road_accident_tips WHERE language='English' AND scenario=? ORDER BY step_number",
            (scenario,)
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
 
 
@app.post("/api/chatbot")
async def chatbot(req: ChatRequest):
    message = req.message.strip()
    lat, lon = req.lat, req.lon
 
    # Detect language
    lang = req.language if req.language in ("en", "hi", "te", "ta", "kn") else detect_language(message)
 
    # Detect severity, intent, panic
    severity = detect_severity(message)
    intents = detect_intents(message)
    is_panic = is_panic_input(message) or not message
 
    # Build AI reply
    reply = build_response(intents, lang, severity, is_panic)
 
    # Fetch nearby services if location provided
    nearby = None
    if lat and lon:
        conn = get_db()
        all_rows = conn.execute("SELECT * FROM emergency_services").fetchall()
        conn.close()
        nearby = {}
        for intent in intents:
            typed = []
            for row in all_rows:
                if row["service_type"] == intent:
                    dist = haversine(lat, lon, row["latitude"], row["longitude"])
                    typed.append({
                        "name": row["name"],
                        "service_type": row["service_type"],
                        "phone": row["phone"],
                        "city": row["city"],
                        "address": row["address"],
                        "distance_km": round(dist, 2),
                        "eta_minutes": max(1, round(dist / 40 * 60))
                    })
            typed.sort(key=lambda x: x["distance_km"])
            nearby[intent] = typed[:3]
 
    return {
        "reply": reply,
        "detected_intents": intents,
        "severity": severity,
        "language_detected": lang,
        "is_panic": is_panic,
        "nearby_services": nearby,
        "sos_numbers": {"ambulance": "108", "police": "100", "fire": "101", "unified": "112"}
    }
 
 
@app.get("/api/cities")
def get_cities():
    conn = get_db()
    rows = conn.execute(
        "SELECT DISTINCT city, state, COUNT(*) as service_count FROM emergency_services GROUP BY city"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
 
 
@app.get("/api/stats")
def get_stats():
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) FROM emergency_services").fetchone()[0]
    by_type = conn.execute(
        "SELECT service_type, COUNT(*) as count FROM emergency_services GROUP BY service_type"
    ).fetchall()
    cities = conn.execute("SELECT COUNT(DISTINCT city) FROM emergency_services").fetchone()[0]
    conn.close()
    return {
        "total_services": total,
        "cities_covered": cities,
        "by_type": [dict(r) for r in by_type],
        "phase": "MVP Phase 1 — 5 Cities"
    }
 
 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
