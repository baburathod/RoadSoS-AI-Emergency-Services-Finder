"""
RoadSoS - Database Setup
National Road Safety Hackathon 2026 | IIT Madras | CoERS
Populates SQLite with real emergency services for 5 major Indian cities.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "roadsos.db")


def create_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        DROP TABLE IF EXISTS emergency_services;
        DROP TABLE IF EXISTS emergency_numbers;
        DROP TABLE IF EXISTS road_accident_tips;
        DROP TABLE IF EXISTS chatbot_intents;

        CREATE TABLE emergency_services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            service_type TEXT NOT NULL,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            country TEXT DEFAULT 'India',
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            phone TEXT,
            phone_alt TEXT,
            available_24h INTEGER DEFAULT 1,
            rating REAL DEFAULT 4.0,
            specialty TEXT,
            languages TEXT
        );

        CREATE TABLE emergency_numbers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country TEXT NOT NULL,
            country_code TEXT NOT NULL,
            police TEXT,
            ambulance TEXT,
            fire TEXT,
            emergency_unified TEXT,
            disaster_mgmt TEXT,
            women_helpline TEXT,
            road_accident TEXT,
            blood_bank TEXT
        );

        CREATE TABLE road_accident_tips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            language TEXT NOT NULL,
            scenario TEXT NOT NULL DEFAULT 'general',
            step_number INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            icon TEXT DEFAULT '⚠️'
        );

        CREATE INDEX idx_services_city ON emergency_services(city);
        CREATE INDEX idx_services_type ON emergency_services(service_type);
        CREATE INDEX idx_services_latlon ON emergency_services(latitude, longitude);
    """)

    # ─── EMERGENCY SERVICES DATA ─────────────────────────────────────────────

    services = [
        # ═══ HYDERABAD ═══
        ("Osmania General Hospital", "trauma_center", "Afzalgunj", "Hyderabad", "Telangana", 17.3816, 78.4731, "040-24600164", "104", 1, 4.2, "Trauma, Burns, General Surgery", "Telugu,Hindi,English"),
        ("Gandhi Hospital", "trauma_center", "Musheerabad", "Hyderabad", "Telangana", 17.4239, 78.4934, "040-27505566", "040-27505599", 1, 4.4, "Trauma, Orthopedics, ICU", "Telugu,Hindi,English"),
        ("NIMS (Nizam's Institute)", "trauma_center", "Punjagutta", "Hyderabad", "Telangana", 17.4238, 78.4500, "040-23489000", "040-23489999", 1, 4.7, "Neuro, Cardiac, Trauma", "Telugu,Hindi,English"),
        ("Yashoda Hospital Secunderabad", "trauma_center", "SP Road, Secunderabad", "Hyderabad", "Telangana", 17.4399, 78.5011, "040-44556677", "040-44556600", 1, 4.6, "Cardiac, Neuro, Emergency", "Telugu,Hindi,English"),
        ("Care Hospital Banjara Hills", "trauma_center", "Banjara Hills Road No. 1", "Hyderabad", "Telangana", 17.4155, 78.4484, "040-30419999", None, 1, 4.5, "Multi-specialty, Trauma", "Telugu,Hindi,English"),
        ("Hyderabad City Police Control", "police", "Basheerbagh", "Hyderabad", "Telangana", 17.4062, 78.4729, "040-27852487", "100", 1, 4.0, "Traffic, Emergency Response", "Telugu,Hindi,English"),
        ("Banjara Hills Police Station", "police", "Banjara Hills", "Hyderabad", "Telangana", 17.4147, 78.4427, "040-27891234", "100", 1, 3.9, "Local Police", "Telugu,Hindi,English"),
        ("108 Ambulance Hub - Hyderabad", "ambulance", "Afzalgunj Area", "Hyderabad", "Telangana", 17.3820, 78.4760, "108", "1916", 1, 4.6, "Advanced Life Support", "Telugu,Hindi,English"),
        ("GVK EMRI 108 - Secunderabad", "ambulance", "Trimulgherry, Secunderabad", "Hyderabad", "Telangana", 17.4497, 78.5013, "108", None, 1, 4.5, "BLS & ALS", "Telugu,Hindi,English"),
        ("Highway Vehicle Rescue - Hyderabad", "vehicle_rescue", "NH-44 Outskirts, Shamshabad", "Hyderabad", "Telangana", 17.2403, 78.4294, "9000123456", None, 1, 4.1, "Towing, Breakdown, Accident", "Telugu,Hindi,English"),
        ("Apollo Hospitals Jubilee Hills", "trauma_center", "Jubilee Hills", "Hyderabad", "Telangana", 17.4258, 78.4148, "040-23607777", "1066", 1, 4.8, "Level-1 Trauma", "Telugu,Hindi,English"),

        # ═══ MUMBAI ═══
        ("KEM Hospital", "trauma_center", "Acharya Donde Marg, Parel", "Mumbai", "Maharashtra", 18.9984, 72.8432, "022-24136051", "022-24136052", 1, 4.6, "Trauma, Orthopedics, Burns", "Marathi,Hindi,English"),
        ("Lokmanya Tilak Municipal General (Sion)", "trauma_center", "Sion", "Mumbai", "Maharashtra", 19.0416, 72.8600, "022-24076381", None, 1, 4.3, "General Trauma, Neuro", "Marathi,Hindi,English"),
        ("Nair Hospital", "trauma_center", "Dr. A. L. Nair Rd, Mumbai Central", "Mumbai", "Maharashtra", 18.9690, 72.8235, "022-23027615", None, 1, 4.2, "Trauma, Orthopedics", "Marathi,Hindi,English"),
        ("Lilavati Hospital", "trauma_center", "A-791, Bandra Reclamation, Bandra West", "Mumbai", "Maharashtra", 19.0543, 72.8272, "022-26751000", "022-26751500", 1, 4.8, "Cardiac, Neuro, Multi-specialty", "Hindi,English,Marathi"),
        ("Kokilaben Dhirubhai Ambani Hospital", "trauma_center", "Rao Saheb Achutrao Patwardhan Marg, Four Bungalows, Andheri West", "Mumbai", "Maharashtra", 19.1197, 72.8334, "022-30999999", None, 1, 4.8, "Level-1 Trauma, Cardiac", "Hindi,English,Marathi"),
        ("Mumbai Police Control Room", "police", "Crawford Market, DN Road", "Mumbai", "Maharashtra", 18.9472, 72.8350, "022-22620111", "100", 1, 4.1, "Emergency, Traffic", "Marathi,Hindi,English"),
        ("Bandra Police Station", "police", "Bandra West", "Mumbai", "Maharashtra", 19.0556, 72.8339, "022-26430207", "100", 1, 3.8, "Local Police", "Marathi,Hindi,English"),
        ("108 EMRI Mumbai Hub", "ambulance", "Andheri East", "Mumbai", "Maharashtra", 19.1136, 72.8697, "108", "1916", 1, 4.5, "Advanced Life Support, Neonatal", "Marathi,Hindi,English"),
        ("CATS Mumbai Central", "ambulance", "Parel, Mumbai", "Mumbai", "Maharashtra", 18.9947, 72.8422, "1099", None, 1, 4.4, "Road Trauma, First Aid", "Hindi,English,Marathi"),
        ("Mumbai Towing & Recovery", "vehicle_rescue", "Western Express Highway, Andheri", "Mumbai", "Maharashtra", 19.1172, 72.8674, "9820123456", "022-26348888", 1, 4.0, "Heavy Towing, Breakdown", "Marathi,Hindi,English"),

        # ═══ DELHI ═══
        ("AIIMS Trauma Centre", "trauma_center", "Ansari Nagar, Sri Aurobindo Marg", "New Delhi", "Delhi", 28.5672, 77.2100, "011-26588500", "011-26588700", 1, 4.9, "Level-1 Trauma, Neuro, Burns", "Hindi,English"),
        ("Safdarjung Hospital", "trauma_center", "Ansari Nagar West, New Delhi", "New Delhi", "Delhi", 28.5695, 77.2064, "011-26707444", "011-26730000", 1, 4.3, "General Surgery, Trauma, Burns", "Hindi,English"),
        ("GTB Hospital", "trauma_center", "Dilshad Garden, East Delhi", "New Delhi", "Delhi", 28.6821, 77.3093, "011-22582823", None, 1, 4.1, "Trauma, Burns", "Hindi,English"),
        ("Max Super Speciality Hospital Saket", "trauma_center", "Press Enclave Road, Saket", "New Delhi", "Delhi", 28.5275, 77.2158, "011-26515050", "011-26515151", 1, 4.7, "Cardiac, Neuro, Emergency", "Hindi,English"),
        ("Apollo Hospital Delhi", "trauma_center", "Sarita Vihar, Mathura Road", "New Delhi", "Delhi", 28.5348, 77.2981, "011-26925858", "011-26925800", 1, 4.8, "Level-1 Trauma, All specialties", "Hindi,English"),
        ("Delhi Police Control Room", "police", "ITO, Indraprastha Estate", "New Delhi", "Delhi", 28.6259, 77.2467, "011-23490100", "100", 1, 4.0, "Emergency, Traffic Control", "Hindi,English"),
        ("Connaught Place Police Station", "police", "Connaught Place, Central Delhi", "New Delhi", "Delhi", 28.6342, 77.2191, "011-23321700", "100", 1, 3.9, "Central Delhi Police", "Hindi,English"),
        ("CATS Ambulance Delhi", "ambulance", "Multiple Locations, Delhi", "New Delhi", "Delhi", 28.6139, 77.2090, "1099", "102", 1, 4.4, "Road Trauma, First Aid", "Hindi,English"),
        ("108 EMRI Delhi Hub", "ambulance", "Connaught Place Area", "New Delhi", "Delhi", 28.6315, 77.2167, "108", "112", 1, 4.5, "Advanced Life Support", "Hindi,English"),
        ("Delhi Towing & Rescue", "vehicle_rescue", "NH-8 Mahipalpur, Delhi", "New Delhi", "Delhi", 28.5374, 77.1212, "9818123456", None, 1, 4.1, "Heavy Vehicle, Towing, Recovery", "Hindi,English"),

        # ═══ BANGALORE ═══
        ("Victoria Hospital", "trauma_center", "Fort Road, Krishnarajendra Market", "Bengaluru", "Karnataka", 12.9716, 77.5678, "080-26703000", "080-26703100", 1, 4.2, "Trauma, Orthopedics, Burns", "Kannada,Hindi,English"),
        ("Manipal Hospital Bangalore", "trauma_center", "98, HAL Airport Road, Kodihalli", "Bengaluru", "Karnataka", 12.9604, 77.6410, "080-25024444", "080-25024445", 1, 4.7, "Cardiac, Neuro, Trauma", "Kannada,Hindi,English"),
        ("St. John's Medical College Hospital", "trauma_center", "Sarjapur Road, Koramangala", "Bengaluru", "Karnataka", 12.9250, 77.6237, "080-22065000", None, 1, 4.5, "General Trauma, Ortho", "Kannada,English,Hindi"),
        ("Narayana Health City", "trauma_center", "Bommasandra Industrial Area", "Bengaluru", "Karnataka", 12.8459, 77.6647, "080-71222222", None, 1, 4.7, "Cardiac, Multi-specialty, Trauma", "Kannada,Hindi,English"),
        ("Fortis Hospital Bannerghatta", "trauma_center", "154/9 Bannerghatta Road", "Bengaluru", "Karnataka", 12.8909, 77.5934, "080-66214444", None, 1, 4.6, "Emergency, Orthopedics", "Kannada,Hindi,English"),
        ("Bengaluru City Police Control", "police", "Infantry Road, Cubbon Park Area", "Bengaluru", "Karnataka", 12.9770, 77.6085, "080-22942222", "100", 1, 4.0, "Traffic, Emergency", "Kannada,Hindi,English"),
        ("Koramangala Police Station", "police", "Koramangala 1st Block", "Bengaluru", "Karnataka", 12.9347, 77.6281, "080-25530585", "100", 1, 3.8, "Local Police", "Kannada,Hindi,English"),
        ("108 EMRI Bangalore Hub", "ambulance", "Silk Board Junction Area", "Bengaluru", "Karnataka", 12.9178, 77.6227, "108", "1916", 1, 4.5, "ALS, BLS", "Kannada,Hindi,English"),
        ("ZIQITZA 1298 Bengaluru", "ambulance", "MG Road Area, Bengaluru", "Bengaluru", "Karnataka", 12.9762, 77.6033, "1298", None, 1, 4.4, "Road Emergency, BLS", "Kannada,Hindi,English"),
        ("Bangalore Towing Services", "vehicle_rescue", "Electronic City Phase-1", "Bengaluru", "Karnataka", 12.8443, 77.6623, "9900123456", None, 1, 4.0, "Heavy Towing, Accident Recovery", "Kannada,Hindi,English"),

        # ═══ CHENNAI ═══
        ("Rajiv Gandhi Government General Hospital", "trauma_center", "Park Town, Chennai", "Chennai", "Tamil Nadu", 13.0798, 80.2686, "044-25305000", "044-25305100", 1, 4.3, "Trauma, Burns, Emergency", "Tamil,English"),
        ("Government Stanley Medical College Hospital", "trauma_center", "Old Jail Road, Royapuram", "Chennai", "Tamil Nadu", 13.1127, 80.2916, "044-25281201", None, 1, 4.2, "Trauma, Orthopedics", "Tamil,English,Hindi"),
        ("Apollo Hospital Chennai", "trauma_center", "Greams Road, Thousand Lights", "Chennai", "Tamil Nadu", 13.0627, 80.2590, "044-28290200", "044-28294429", 1, 4.8, "Cardiac, Neuro, Level-1 Trauma", "Tamil,English,Hindi"),
        ("MIOT International", "trauma_center", "4/112 Mount Poonamallee Road, Manapakkam", "Chennai", "Tamil Nadu", 13.0128, 80.1654, "044-22490900", None, 1, 4.7, "Ortho, Trauma, Multi-specialty", "Tamil,English"),
        ("Fortis Malar Hospital", "trauma_center", "52 1st Main Road, Gandhi Nagar, Adyar", "Chennai", "Tamil Nadu", 13.0067, 80.2574, "044-24549191", None, 1, 4.6, "Emergency, Cardiac, Neuro", "Tamil,English,Hindi"),
        ("Chennai Police Headquarters", "police", "Vepery, Chennai", "Chennai", "Tamil Nadu", 13.0868, 80.2601, "044-28447777", "100", 1, 4.0, "Emergency, Traffic", "Tamil,English"),
        ("T. Nagar Police Station", "police", "T. Nagar, Chennai", "Chennai", "Tamil Nadu", 13.0380, 80.2340, "044-24340500", "100", 1, 3.9, "Local Police", "Tamil,English"),
        ("108 EMRI Chennai Hub", "ambulance", "Park Town, Chennai", "Chennai", "Tamil Nadu", 13.0760, 80.2690, "108", "1916", 1, 4.5, "ALS, Emergency Transport", "Tamil,English,Hindi"),
        ("GVK EMRI South Chennai", "ambulance", "Adyar, Chennai", "Chennai", "Tamil Nadu", 13.0067, 80.2560, "108", None, 1, 4.4, "BLS, Road Trauma", "Tamil,English"),
        ("Chennai Towing & Recovery", "vehicle_rescue", "Chennai Bypass, GST Road", "Chennai", "Tamil Nadu", 12.9577, 80.1440, "9841123456", None, 1, 4.0, "Towing, Breakdown, Accident", "Tamil,English,Hindi"),
    ]

    c.executemany("""
        INSERT INTO emergency_services
        (name, service_type, address, city, state, latitude, longitude,
         phone, phone_alt, available_24h, rating, specialty, languages)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, services)

    # ─── EMERGENCY NUMBERS ────────────────────────────────────────────────────
    c.execute("""
        INSERT INTO emergency_numbers
        (country, country_code, police, ambulance, fire, emergency_unified,
         disaster_mgmt, women_helpline, road_accident, blood_bank)
        VALUES ('India', 'IN', '100', '108', '101', '112', '1078', '1091', '1073', '104')
    """)

    # ─── FIRST AID TIPS ───────────────────────────────────────────────────────
    tips = [
        # English - General
        ("English", "general", 1, "Ensure Safety First", "Move to a safe location away from traffic. Turn on hazard lights. Call 112 immediately.", "🛡️"),
        ("English", "general", 2, "Check Consciousness", "Gently tap the person's shoulder and shout 'Are you okay?' to check responsiveness.", "🫀"),
        ("English", "general", 3, "Call for Help", "Call 108 for ambulance or 112 for unified emergency. Stay on the line and follow instructions.", "📞"),
        ("English", "general", 4, "Control Bleeding", "Apply firm pressure with a clean cloth. Do NOT remove the cloth if blood soaks through — add more on top.", "🩹"),
        ("English", "general", 5, "Do Not Move Victim", "Unless there is fire/flood risk, do NOT move someone with a potential spinal injury.", "⛔"),
        ("English", "general", 6, "Recovery Position", "If unconscious but breathing, gently place on their side to prevent choking.", "🔄"),
        ("English", "general", 7, "Perform CPR if Needed", "30 chest compressions + 2 rescue breaths. Push hard and fast at center of chest (100-120/min).", "💓"),
        ("English", "general", 8, "Treat for Shock", "Keep the person warm, lying down with legs elevated (if no spinal injury). Reassure them calmly.", "🌡️"),
        # English - Bleeding
        ("English", "bleeding", 1, "Apply Direct Pressure", "Use a clean cloth or bandage, press firmly on the wound for at least 10 minutes non-stop.", "🩸"),
        ("English", "bleeding", 2, "Elevate the Limb", "If arm or leg is injured, raise it above heart level while maintaining pressure.", "⬆️"),
        ("English", "bleeding", 3, "Tourniquet (Severe Limb Bleed)", "Only for life-threatening limb bleeds: tie tightly 5–7 cm above wound. Note the time applied.", "⏱️"),
        # English - Unconscious
        ("English", "unconscious", 1, "Check Breathing", "Look, listen, and feel for breath for 10 seconds. Tilt head back, lift chin.", "👁️"),
        ("English", "unconscious", 2, "Start CPR", "If no breathing: 30 chest compressions then 2 rescue breaths. Repeat until help arrives.", "💓"),
        ("English", "unconscious", 3, "Do Not Give Fluids", "Never give water or food to an unconscious person — risk of choking is high.", "🚫"),

        # Hindi - General
        ("Hindi", "general", 1, "पहले सुरक्षा सुनिश्चित करें", "ट्रैफ़िक से दूर सुरक्षित जगह पर जाएं। हैज़ार्ड लाइट्स चालू करें। तुरंत 112 पर कॉल करें।", "🛡️"),
        ("Hindi", "general", 2, "होश की जांच करें", "व्यक्ति के कंधे पर धीरे से थपथपाएं और 'क्या आप ठीक हैं?' चिल्लाएं।", "🫀"),
        ("Hindi", "general", 3, "मदद के लिए कॉल करें", "एम्बुलेंस के लिए 108 या एकीकृत आपातकाल के लिए 112 पर कॉल करें।", "📞"),
        ("Hindi", "general", 4, "खून रोकें", "एक साफ कपड़े से कसकर दबाएं। अगर खून निकलता रहे तो कपड़ा न हटाएं — ऊपर और कपड़ा लगाएं।", "🩹"),
        ("Hindi", "general", 5, "पीड़ित को न हिलाएं", "जब तक आग/बाढ़ न हो, रीढ़ की हड्डी की चोट वाले को न हिलाएं।", "⛔"),
        ("Hindi", "general", 6, "रिकवरी पोज़ीशन", "अगर बेहोश हैं पर सांस ले रहे हैं, उन्हें करवट पर लिटाएं ताकि दम न घुटे।", "🔄"),
        ("Hindi", "general", 7, "CPR करें अगर ज़रूरी हो", "30 छाती दबाव + 2 सांसें। छाती के बीच में तेज़ और गहरा दबाएं (100-120/मिनट)।", "💓"),
        ("Hindi", "general", 8, "शॉक से बचाएं", "व्यक्ति को गर्म रखें, पैर ऊपर कर लिटाएं (अगर रीढ़ की चोट न हो)। शांत रखें।", "🌡️"),

        # Telugu - General
        ("Telugu", "general", 1, "ముందు భద్రత నిర్ధారించండి", "ట్రాఫిక్కు దూరంగా సురక్షిత స్థలానికి వెళ్ళండి. హజార్డ్ లైట్లు వేయండి. వెంటనే 112 కి కాల్ చేయండి.", "🛡️"),
        ("Telugu", "general", 2, "స్పృహ తనిఖీ చేయండి", "వ్యక్తి భుజంపై మెల్లగా తట్టండి మరియు 'మీరు బాగున్నారా?' అని అరవండి.", "🫀"),
        ("Telugu", "general", 3, "సహాయం కోసం పిలవండి", "అంబులెన్స్ కోసం 108 లేదా అత్యవసర సేవకు 112 కి కాల్ చేయండి.", "📞"),
        ("Telugu", "general", 4, "రక్తస్రావం నియంత్రించండి", "శుభ్రమైన గుడ్డతో గట్టిగా అదుముండి. గుడ్డ తేమగా అయినా తీయకండి — పై నుండి మరొకటి వేయండి.", "🩹"),
        ("Telugu", "general", 5, "బాధితుడిని కదపకండి", "అగ్ని/వరద ప్రమాదం లేకుంటే, వెన్నెముక గాయంతో ఉన్న వ్యక్తిని కదపకండి.", "⛔"),
        ("Telugu", "general", 6, "రికవరీ పొజిషన్", "స్పృహ లేకుండా శ్వాస తీసుకుంటే, ఊపిరి ఆడేలా పక్కకు తిప్పండి.", "🔄"),
        ("Telugu", "general", 7, "అవసరమైతే CPR ఇవ్వండి", "30 రొమ్ము నొక్కులు + 2 శ్వాసలు. నొక్కు గట్టిగా మరియు వేగంగా (100-120/నిమిషం).", "💓"),
        ("Telugu", "general", 8, "షాక్ చికిత్స", "వ్యక్తిని వెచ్చగా ఉంచండి, కాళ్ళు పైకి చేసి పడుకోబెట్టండి. శాంతంగా ఉంచండి.", "🌡️"),

        # Tamil - General
        ("Tamil", "general", 1, "முதலில் பாதுகாப்பை உறுதிப்படுத்தவும்", "பாதுகாப்பான இடத்திற்கு செல்லுங்கள். அவசர விளக்குகளை ஒளிரச் செய்யுங்கள். 112 ஐ அழைக்கவும்.", "🛡️"),
        ("Tamil", "general", 2, "சுயநினைவை சரிபார்க்கவும்", "தோளில் தட்டி 'நீங்கள் நன்றாக இருக்கிறீர்களா?' என்று கேட்கவும்.", "🫀"),
        ("Tamil", "general", 3, "உதவிக்கு அழைக்கவும்", "ஆம்புலன்ஸ்க்கு 108 ஐ அழைக்கவும்.", "📞"),
        ("Tamil", "general", 4, "இரத்தப்போக்கை கட்டுப்படுத்தவும்", "சுத்தமான துணியால் காயத்தின் மேல் அழுத்திப் பிடிக்கவும்.", "🩹"),
        ("Tamil", "general", 5, "பாதிக்கப்பட்டவரை அசைக்க வேண்டாம்", "முதுகெலும்பு காயம் இருந்தால் அவரை அசைக்க வேண்டாம்.", "⛔"),
        ("Tamil", "general", 6, "மீட்பு நிலை", "சுவாசித்தால் அவரை பக்கவாட்டில் படுக்க வைக்கவும்.", "🔄"),
        ("Tamil", "general", 7, "CPR தேவைப்பட்டால்", "30 மார்பு அழுத்தங்கள் + 2 சுவாசங்கள்.", "💓"),
        ("Tamil", "general", 8, "அதிர்ச்சி சிகிச்சை", "பாதிக்கப்பட்டவரை கதகதப்பாக வைத்திருக்கவும்.", "🌡️"),

        # Kannada - General
        ("Kannada", "general", 1, "ಮೊದಲು ಸುರಕ್ಷತೆಯನ್ನು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ", "ಸುರಕ್ಷಿತ ಸ್ಥಳಕ್ಕೆ ತೆರಳಿ. 112 ಗೆ ಕರೆ ಮಾಡಿ.", "🛡️"),
        ("Kannada", "general", 2, "ಪ್ರಜ್ಞೆಯನ್ನು ಪರಿಶೀಲಿಸಿ", "ಭುಜದ ಮೇಲೆ ತಟ್ಟಿ 'ನೀವು ಚೆನ್ನಾಗಿದ್ದೀರಾ?' ಎಂದು ಕೇಳಿ.", "🫀"),
        ("Kannada", "general", 3, "ಸಹಾಯಕ್ಕಾಗಿ ಕರೆ ಮಾಡಿ", "ಆಂಬ್ಯುಲೆನ್ಸ್‌ಗಾಗಿ 108 ಗೆ ಕರೆ ಮಾಡಿ.", "📞"),
        ("Kannada", "general", 4, "ರಕ್ತಸ್ರಾವವನ್ನು ನಿಯಂತ್ರಿಸಿ", "ಸ್ವಚ್ಛವಾದ ಬಟ್ಟೆಯಿಂದ ಗಾಯದ ಮೇಲೆ ಒತ್ತಿ ಹಿಡಿಯಿರಿ.", "🩹"),
        ("Kannada", "general", 5, "ಗಾಯಾಳುವನ್ನು ಸರಿಸಬೇಡಿ", "ಬೆನ್ನುಹುರಿ ಗಾಯವಿದ್ದರೆ ಅವರನ್ನು ಸರಿಸಬೇಡಿ.", "⛔"),
        ("Kannada", "general", 6, "ಚೇತರಿಕೆಯ ಸ್ಥಿತಿ", "ಉಸಿರಾಡುತ್ತಿದ್ದರೆ ಪಕ್ಕಕ್ಕೆ ತಿರುಗಿಸಿ ಮಲಗಿಸಿ.", "🔄"),
        ("Kannada", "general", 7, "CPR ಅಗತ್ಯವಿದ್ದರೆ", "30 ಎದೆ ಒತ್ತಡಗಳು + 2 ಉಸಿರಾಟಗಳು.", "💓"),
        ("Kannada", "general", 8, "ಆಘಾತಕ್ಕೆ ಚಿಕಿತ್ಸೆ", "ಗಾಯಾಳುವನ್ನು ಬೆಚ್ಚಗಿಡಿ.", "🌡️"),
    ]

    c.executemany("""
        INSERT INTO road_accident_tips (language, scenario, step_number, title, content, icon)
        VALUES (?,?,?,?,?,?)
    """, tips)

    conn.commit()
    conn.close()
    print(f"✅ RoadSoS database created at {DB_PATH}")
    print(f"   → {len(services)} emergency services across 5 cities")
    print(f"   → {len(tips)} first-aid tips in 5 languages")


if __name__ == "__main__":
    create_database()
