// ── STATE ──────────────────────────────────────────────────────────────────
const API = 'http://localhost:8000';
let state = {
  lat: null, lon: null,
  lang: 'en',
  filter: 'all',
  services: [],
  severity: 'medium',
  demoRadius: 50,
  isOnline: navigator.onLine,
  sosTriggered: false
};
 
// ── OFFLINE FIRST AID DATA (fallback) ─────────────────────────────────────
const OFFLINE_TIPS = {
  general: [
    {step_number:1, icon:'🛡️', title:'Ensure Safety', content:'Move to safe area. Turn on hazard lights. Call 112.'},
    {step_number:2, icon:'🫀', title:'Check Consciousness', content:"Tap shoulder and shout 'Are you okay?'"},
    {step_number:3, icon:'📞', title:'Call for Help', content:'Dial 108 (Ambulance) or 112 (Unified Emergency) immediately.'},
    {step_number:4, icon:'🩹', title:'Control Bleeding', content:'Press firmly with clean cloth. Do NOT remove if soaked — add more cloth on top.'},
    {step_number:5, icon:'⛔', title:"Don't Move Victim", content:'Unless fire/flood risk — do NOT move someone with possible spinal injury.'},
    {step_number:6, icon:'💓', title:'CPR if Needed', content:'30 chest compressions + 2 breaths. 100/min. Push hard at center of chest.'},
  ],
  bleeding: [
    {step_number:1, icon:'🩸', title:'Apply Direct Pressure', content:'Press clean cloth firmly on wound for 10 continuous minutes.'},
    {step_number:2, icon:'⬆️', title:'Elevate Limb', content:'Raise injured arm or leg above heart level while maintaining pressure.'},
    {step_number:3, icon:'⏱️', title:'Tourniquet (Last Resort)', content:'Only for life-threatening limb bleed: tie tightly 5-7 cm above wound. Note time applied.'},
  ],
  unconscious: [
    {step_number:1, icon:'👁️', title:'Check Breathing', content:'Look, listen, feel for breath 10 sec. Tilt head back, lift chin.'},
    {step_number:2, icon:'💓', title:'Start CPR', content:'No breathing? 30 compressions + 2 breaths. Repeat until ambulance arrives.'},
    {step_number:3, icon:'🚫', title:"Don't Give Fluids", content:'Never give water or food to an unconscious person — choking risk.'},
  ],
  burns: [
    {step_number:1, icon:'💧', title:'Cool the Burn', content:'Hold under cool (not cold) running water for 10-20 minutes.'},
    {step_number:2, icon:'🧥', title:'Remove Constrictions', content:'Carefully remove rings, watches, or tight clothing from the burned area before it swells.'},
    {step_number:3, icon:'🩹', title:'Cover the Burn', content:'Cover loosely with a sterile, non-fluffy dressing or cling film. Do NOT pop blisters.'},
  ],
  fracture: [
    {step_number:1, icon:'⛔', title:'Do Not Move', content:'Keep the injured area totally still. Do not try to realign the bone.'},
    {step_number:2, icon:'🛑', title:'Stop Bleeding', content:'If there is bleeding, apply pressure around the wound, not directly over the exposed bone.'},
    {step_number:3, icon:'🧊', title:'Apply Ice', content:'Wrap an ice pack in a cloth and apply to reduce swelling. Wait for paramedics.'},
  ]
};
 
const OFFLINE_SERVICES = [
  {name:'Call 108 Ambulance', service_type:'ambulance', phone:'108', city:'National', distance_km:0, eta_minutes:0},
  {name:'Call 100 Police', service_type:'police', phone:'100', city:'National', distance_km:0, eta_minutes:0},
  {name:'Call 112 Unified', service_type:'trauma_center', phone:'112', city:'National', distance_km:0, eta_minutes:0},
];
 
const UI_TEXT = {
  en: {chat_placeholder:'Describe emergency...', welcome:'🚨 RoadSoS active. Type your emergency or press SOS.<br><small style="opacity:0.6">Supports English, हिंदी, తెలుగు, தமிழ், ಕನ್ನಡ</small>', sos_confirm:'SOS activated! Fetching nearest emergency services...', near_services:'Nearest Services'},
  hi: {chat_placeholder:'आपातकाल बताएं...', welcome:'🚨 RoadSoS सक्रिय। आपातकाल बताएं या SOS दबाएं।<br><small style="opacity:0.6">समर्थन: English, हिंदी, తెలుగు, தமிழ், ಕನ್ನಡ</small>', sos_confirm:'SOS सक्रिय! निकटतम आपातकालीन सेवाएं खोज रहा है...', near_services:'निकटतम सेवाएं'},
  te: {chat_placeholder:'అత్యవసర వివరించండి...', welcome:'🚨 RoadSoS సక్రియం. అత్యవసరం వివరించండి లేదా SOS నొక్కండి.<br><small style="opacity:0.6">మద్దతు: English, हिंदी, తెలుగు, தமிழ், ಕನ್ನಡ</small>', sos_confirm:'SOS సక్రియమైంది! దగ్గర సేవలు వెతుకుతున్నాను...', near_services:'దగ్గర సేవలు'},
  ta: {chat_placeholder:'அவசரத்தை விவரிக்கவும்...', welcome:'🚨 RoadSoS செயலில் உள்ளது. அவசரத்தை விவரிக்கவும் அல்லது SOS ஐ அழுத்தவும்.<br><small style="opacity:0.6">ஆதரவுகள்: English, हिंदी, తెలుగు, தமிழ், ಕನ್ನಡ</small>', sos_confirm:'SOS இயக்கப்பட்டது! அருகில் உள்ள சேவைகளை தேடுகிறது...', near_services:'அருகில் உள்ள சேவைகள்'},
  kn: {chat_placeholder:'ತುರ್ತು ಪರಿಸ್ಥಿತಿಯನ್ನು ವಿವರಿಸಿ...', welcome:'🚨 RoadSoS ಸಕ್ರಿಯವಾಗಿದೆ. ತುರ್ತು ಪರಿಸ್ಥಿತಿಯನ್ನು ವಿವರಿಸಿ ಅಥವಾ SOS ಒತ್ತಿರಿ.<br><small style="opacity:0.6">ಬೆಂಬಲಿಸುತ್ತದೆ: English, हिंदी, తెలుగు, தமிழ், ಕನ್ನಡ</small>', sos_confirm:'SOS ಸಕ್ರಿಯಗೊಂಡಿದೆ! ಹತ್ತಿರದ ಸೇವೆಗಳನ್ನು ಹುಡುಕಲಾಗುತ್ತಿದೆ...', near_services:'ಹತ್ತಿರದ ಸೇವೆಗಳು'},
};
 
const SEV_LABELS = {
  critical: {en:'CRITICAL', hi:'अतिगंभीर', te:'విపత్కరమైన', ta:'மிக முக்கியமானது', kn:'ಅತ್ಯಂತ ಗಂಭೀರ'},
  high:     {en:'HIGH',     hi:'उच्च',     te:'అధిక', ta:'உயர்ந்த', kn:'ಹೆಚ್ಚಿನ'},
  medium:   {en:'MEDIUM',   hi:'मध्यम',   te:'మధ్యస్తం', ta:'நடுத்தர', kn:'ಮಧ್ಯಮ'},
  low:      {en:'LOW',      hi:'कम',       te:'తక్కువ', ta:'குறைந்த', kn:'ಕಡಿಮೆ'},
};
const SEV_DESC = {
  critical:'Immediate life-threatening — call 108 NOW',
  high:'Serious injury — urgent medical attention needed',
  medium:'Standard emergency response',
  low:'Minor injury — seek medical check'
};
 
// ── INIT ──────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // 1. Immediately load demo data so the map is never empty
  useDemoLocation();
  // 2. Try to get actual GPS in the background
  getLocation();
  checkOnlineStatus();
  window.addEventListener('online', () => { state.isOnline=true; updateStatusUI(); });
  window.addEventListener('offline', () => { state.isOnline=false; updateStatusUI(); });
});
 
function checkOnlineStatus() {
  state.isOnline = navigator.onLine;
  updateStatusUI();
}
 
function updateStatusUI() {
  const dot = document.getElementById('status-dot');
  const label = document.getElementById('status-label');
  const banner = document.getElementById('offline-banner');
  if (state.isOnline) {
    dot.className = 'status-dot online';
    label.textContent = 'Online';
    banner.classList.remove('show');
  } else {
    dot.className = 'status-dot offline';
    label.textContent = 'Offline';
    banner.classList.add('show');
  }
}
 
// ── LOCATION ──────────────────────────────────────────────────────────────
function getLocation() {
  const locText = document.getElementById('loc-text');
  locText.innerHTML = '<span style="color:var(--amber)">Detecting GPS... (Waiting for permission)</span>';
  
  if (!navigator.geolocation) {
    useDemoLocation();
    return;
  }

  // If user ignores the prompt for 3 seconds, revert to demo mode visually
  let fallbackTimer = setTimeout(() => {
    if (locText.innerHTML.includes('Detecting')) {
      useDemoLocation();
    }
  }, 3000);
  
  navigator.geolocation.getCurrentPosition(
    pos => {
      clearTimeout(fallbackTimer);
      state.lat = pos.coords.latitude;
      state.lon = pos.coords.longitude;
      locText.innerHTML = `<strong>GPS Acquired</strong> — ${state.lat.toFixed(4)}, ${state.lon.toFixed(4)}`;
      fetchNearbyServices();
      updateMapMarker();
    },
    () => {
      clearTimeout(fallbackTimer);
      // Fallback to demo location (Hyderabad)
      useDemoLocation();
    },
    { timeout: 8000, enableHighAccuracy: true }
  );
}
 
function changeDemoCity() {
  useDemoLocation();
}

function useDemoLocation() {
  const sel = document.getElementById('demo-city-select');
  const city = sel ? sel.value : 'hyderabad';
  
  const cities = {
    hyderabad: { lat: 17.385, lon: 78.4867, name: 'Hyderabad, Telangana' },
    mumbai: { lat: 19.0760, lon: 72.8777, name: 'Mumbai, Maharashtra' },
    delhi: { lat: 28.6139, lon: 77.2090, name: 'New Delhi, Delhi' },
    bangalore: { lat: 12.9716, lon: 77.5946, name: 'Bengaluru, Karnataka' },
    chennai: { lat: 13.0827, lon: 80.2707, name: 'Chennai, Tamil Nadu' },
    all: { lat: 17.385, lon: 78.4867, name: 'Pan-India (5 Cities)' }
  };
  
  const c = cities[city] || cities['hyderabad'];
  state.lat = c.lat;
  state.lon = c.lon;
  state.demoRadius = (city === 'all') ? 50000 : 80; // 80km covers the single city
  
  document.getElementById('loc-text').innerHTML = `<strong>Demo Mode</strong> — ${c.name}`;
  fetchNearbyServices();
  updateMapMarker();
  showToast(`📍 Showing Demo: ${c.name}`, 'success');
}
 
function updateMapMarker() {
  const marker = document.getElementById('user-marker');
  marker.style.display = 'block';
  
  // Find which city is currently selected
  const sel = document.getElementById('demo-city-select');
  const city = sel ? sel.value : 'hyderabad';
  
  const cityPositions = {
    'hyderabad': [0.55, 0.55],
    'mumbai': [0.20, 0.50],
    'delhi': [0.50, 0.15],
    'bangalore': [0.40, 0.85],
    'chennai': [0.75, 0.85],
  };
  
  const pos = cityPositions[city] || [0.5, 0.5];
  
  // Update marker position dynamically!
  marker.style.left = (pos[0] * 100) + '%';
  marker.style.top = (pos[1] * 100) + '%';

  placeServicesOnMap();
}
 
// ── FETCH NEARBY SERVICES ─────────────────────────────────────────────────
async function fetchNearbyServices() {
  if (!state.lat) return;
  
  if (!state.isOnline) {
    renderCards(OFFLINE_SERVICES);
    return;
  }
  
  try {
    const r = state.demoRadius || 50000;
    const url = `${API}/api/nearby?lat=${state.lat}&lon=${state.lon}&radius_km=${r}&limit=50`;
    const res = await fetch(url);
    const data = await res.json();
    
    // Flatten all service types
    let all = [];
    for (const type in data.services) {
      all.push(...data.services[type]);
    }
    
    // Auto-fallback to Demo Mode if no services found in current location
    if (all.length === 0 && state.lat !== 17.385) {
      showToast('No local services found. Switching to Demo Location...', 'error');
      useDemoLocation();
      return;
    }
    
    all.sort((a,b) => a.distance_km - b.distance_km);
    state.services = all;
    
    document.getElementById('map-subtitle').textContent = 
      `${all.length} services found • ${data.radius_km}km radius`;
    
    // Also re-apply active filter if one is selected
    renderCards(all);
    placeServicesOnMap();
  } catch(e) {
    renderCards(OFFLINE_SERVICES);
    showToast('⚠️ Using offline data', 'error');
  }
}
 
// ── RENDER SERVICE CARDS ──────────────────────────────────────────────────
function renderCards(services) {
  const container = document.getElementById('cards-container');
  const filtered = state.filter === 'all' ? services 
    : services.filter(s => s.service_type === state.filter);
  
  if (!filtered.length) {
    container.innerHTML = '<div class="empty-state" style="height:80px"><div>No services found nearby</div></div>';
    return;
  }
  
  container.innerHTML = filtered.slice(0,8).map(s => {
    const typeLabels = {trauma_center:'Hospital', ambulance:'Ambulance', police:'Police', vehicle_rescue:'Vehicle Rescue'};
    const etaText = s.eta_minutes > 0 ? `⏱ ${s.eta_minutes}min` : 'Immediate';
    const distText = s.distance_km > 0 ? `${s.distance_km}km` : 'Call';
    return `
    <div class="card ${s.service_type}" onclick="callNumber('${s.phone}')">
      <div class="card-stripe"></div>
      <div class="card-head">
        <div class="card-name">${s.name}</div>
        <div class="card-type">${typeLabels[s.service_type] || s.service_type}</div>
      </div>
      <div class="card-meta">
        <span class="card-dist">📍 ${distText}</span>
        <span class="card-phone">${s.phone}</span>
        <span class="card-eta">${etaText}</span>
      </div>
      <button class="card-call">📞 Call ${s.phone}</button>
    </div>`;
  }).join('');
}
 
// ── MAP PINS ──────────────────────────────────────────────────────────────
function placeServicesOnMap() {
  const canvas = document.getElementById('map-canvas');
  const pins = document.getElementById('service-pins');
  const W = canvas.offsetWidth;
  const H = canvas.offsetHeight;
  
  const cityPositions = {
    'Hyderabad': [0.55, 0.55],
    'Mumbai': [0.20, 0.50],
    'New Delhi': [0.50, 0.15],
    'Bengaluru': [0.40, 0.85],
    'Chennai': [0.75, 0.85],
  };
  
  // Place service pins
  
  // Place service pins
  pins.innerHTML = '';
  const filtered = state.filter === 'all' ? state.services : state.services.filter(s => s.service_type === state.filter);
  
  filtered.slice(0,50).forEach(s => {
    const city = s.city;
    
    const pos = cityPositions[city] || [0.5,0.5];
    // Offset each type slightly
    const offsets = {trauma_center:[-15,-15], ambulance:[10,-10], police:[15,15], vehicle_rescue:[-10,20]};
    const off = offsets[s.service_type] || [0,0];
    
    // Add jitter (-20 to +20 px) to spread out the pins so they are easy to click
    const jitterX = (Math.random() - 0.5) * 40;
    const jitterY = (Math.random() - 0.5) * 40;
    
    const x = pos[0] * W + off[0] + jitterX;
    const y = pos[1] * H + off[1] + jitterY;
    
    const pin = document.createElement('div');
    pin.className = 'service-pin';
    pin.style.left = x+'px';
    pin.style.top = y+'px';
    pin.innerHTML = `
      <div class="pin-dot ${s.service_type}"></div>
      <div class="pin-label">${s.name.substring(0,22)}${s.name.length>22?'...':''}<br><small>${s.phone}</small></div>
    `;
    pin.onclick = () => callNumber(s.phone);
    pins.appendChild(pin);
  });
  
  // City labels
  Object.entries(cityPositions).forEach(([city, pos]) => {
    const el = document.createElement('div');
    el.className = 'map-city-label';
    el.style.left = (pos[0]*W - 20)+'px';
    el.style.top = (pos[1]*H + 12)+'px';
    el.textContent = city.toUpperCase();
    pins.appendChild(el);
  });
}
 
// ── CHATBOT ───────────────────────────────────────────────────────────────
async function sendChat() {
  const input = document.getElementById('chat-input');
  const msg = input.value.trim();
  if (!msg) return;
  
  appendMsg(msg, 'user');
  input.value = '';
  
  // Typing indicator
  const typingId = appendTyping();
  
  if (!state.isOnline) {
    removeMsg(typingId);
    appendMsg(getOfflineReply(msg), 'bot');
    return;
  }
  
  try {
    const res = await fetch(`${API}/api/chatbot`, {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({
        message: msg,
        lat: state.lat,
        lon: state.lon,
        language: state.lang
      })
    });
    const data = await res.json();
    removeMsg(typingId);
    
    // Update severity
    updateSeverity(data.severity || 'medium');
    
    // Format reply with markdown-like bold
    const reply = data.reply.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    appendMsg(reply, 'bot', true);
    
    // Update services if nearby returned
    if (data.nearby_services) {
      let all = [];
      for (const k in data.nearby_services) all.push(...data.nearby_services[k]);
      all.sort((a,b) => a.distance_km - b.distance_km);
      if (all.length) {
        state.services = all;
        renderCards(all);
      }
    }
  } catch(e) {
    removeMsg(typingId);
    appendMsg(getOfflineReply(msg), 'bot');
  }
}
 
function getOfflineReply(msg) {
  const m = msg.toLowerCase();
  if (/bleed|blood|खून|రక్తం|இரத்தம்|ರಕ್ತ/.test(m)) return '🩸 Apply firm pressure to wound. Press hard with clean cloth 10min. Elevate limb. Call 108.';
  if (/unconscious|बेहोश|స్పృహలేని|மயக்கம்|ಪ್ರಜ್ಞಾಹೀನ/.test(m)) return '💓 Check breathing. If no breath: 30 chest compressions + 2 breaths. Keep going. Call 108 immediately.';
  if (/accident|दुर्घटना|ప్రమాదం|விபத்து|ಅಪಘಾತ|crash/.test(m)) return '🆘 Call 112 NOW. Do not move injured person. Press SOS button for nearest services.';
  if (/help|help|मदद|సహాయం|உதவி|ಸಹಾಯ/.test(m)) return '🚨 Emergency detected! CALL 112 NOW. Ambulance: 108 | Police: 100 | Fire: 101';
  return '📴 Offline mode. Emergency numbers — Ambulance: 108 | Police: 100 | Unified: 112. Call immediately!';
}
 
function appendMsg(text, who, isHtml=false) {
  const msgs = document.getElementById('chat-msgs');
  const div = document.createElement('div');
  div.className = `msg ${who}`;
  const avatar = who === 'bot' ? '🤖' : '👤';
  div.innerHTML = `<div class="msg-av">${avatar}</div><div class="msg-bubble">${isHtml ? text : escHtml(text)}</div>`;
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
  return div.id = 'msg-' + Date.now();
}
 
function appendTyping() {
  const msgs = document.getElementById('chat-msgs');
  const id = 'typing-' + Date.now();
  const div = document.createElement('div');
  div.className = 'msg bot';
  div.id = id;
  div.innerHTML = `<div class="msg-av">🤖</div><div class="msg-bubble"><span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span></div>`;
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
  return id;
}
 
function removeMsg(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}
 
function escHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\n/g,'<br>');
}
 
// ── SEVERITY ──────────────────────────────────────────────────────────────
function updateSeverity(level) {
  state.severity = level;
  const bar = document.getElementById('severity-bar');
  const lbl = document.getElementById('sev-label');
  const desc = document.getElementById('sev-desc');
  bar.dataset.level = level;
  lbl.textContent = (SEV_LABELS[level] || SEV_LABELS.medium)[state.lang] || level.toUpperCase();
  desc.textContent = SEV_DESC[level] || SEV_DESC.medium;
}
 
// ── SOS BUTTON ────────────────────────────────────────────────────────────
function triggerSOS(event) {
  // Ripple effect
  const btn = document.getElementById('sos-btn');
  const ripple = document.createElement('div');
  ripple.className = 'sos-ripple';
  const rect = btn.getBoundingClientRect();
  
  if (event && event.clientX) {
    ripple.style.left = (event.clientX - rect.left - 150) + 'px';
    ripple.style.top = (event.clientY - rect.top - 150) + 'px';
  } else {
    ripple.style.left = '50%';
    ripple.style.top = '50%';
  }
  
  btn.appendChild(ripple);
  setTimeout(() => ripple.remove(), 600);
  
  state.sosTriggered = true;
  btn.classList.remove('pulsing');
  btn.classList.add('triggered');
  btn.innerHTML = '<span>🚨</span><span>SOS ACTIVE</span>';
  
  const ui = UI_TEXT[state.lang];
  appendMsg(ui.sos_confirm, 'bot');
  updateSeverity('critical');
  
  // Fetch all nearby services
  fetchNearbyServices();
  
  // Auto-send panic message to chatbot
  if (state.isOnline) {
    sendSOSMessage();
  }
  
  showToast('🆘 SOS Activated! Call 112 now!', 'error');
  
  // Reset after 10s
  setTimeout(() => {
    btn.classList.remove('triggered');
    btn.classList.add('pulsing');
    btn.innerHTML = '<span>🆘</span><span>SOS EMERGENCY</span>';
  }, 10000);
}
 
async function sendSOSMessage() {
  try {
    const res = await fetch(`${API}/api/chatbot`, {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ message:'', lat:state.lat, lon:state.lon, language:state.lang })
    });
    const data = await res.json();
    const reply = data.reply.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    appendMsg(reply, 'bot', true);
    updateSeverity(data.severity || 'critical');
  } catch(e) {}
}
 
// ── FILTER ────────────────────────────────────────────────────────────────
function setFilter(filter, btn) {
  state.filter = filter;
  document.querySelectorAll('.chip').forEach(c => {
    c.className = 'chip';
  });
  const clsMap = {all:'active-all', trauma_center:'active-trauma', ambulance:'active-ambulance', police:'active-police', vehicle_rescue:'active-rescue'};
  btn.classList.add(clsMap[filter] || 'active-all');
  renderCards(state.services.length ? state.services : OFFLINE_SERVICES);
  placeServicesOnMap();
}
 
// ── LANGUAGE ──────────────────────────────────────────────────────────────
function setLang(lang) {
  state.lang = lang;
  document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('lang-'+lang).classList.add('active');
  
  const input = document.getElementById('chat-input');
  input.placeholder = UI_TEXT[lang].chat_placeholder;
  
  updateSeverity(state.severity);
}
 
// ── TABS ──────────────────────────────────────────────────────────────────
function showTab(tab, btn) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
  
  ['map','firstaid','info'].forEach(t => {
    const el = document.getElementById('tab-'+t);
    el.style.display = t === tab ? 'flex' : 'none';
  });
  
  if (tab === 'firstaid') loadFirstAid('general');
  if (tab === 'map') { placeServicesOnMap(); }
}
 
// ── FIRST AID ─────────────────────────────────────────────────────────────
async function loadFirstAid(scenario, tabEl=null) {
  if (tabEl) {
    document.querySelectorAll('.sc-tab').forEach(t => t.classList.remove('active'));
    tabEl.classList.add('active');
  }
  
  const container = document.getElementById('firstaid-steps');
  container.innerHTML = '<div class="empty-state"><div class="spinner"></div></div>';
  
  let tips = null;
  
  if (state.isOnline) {
    try {
      const langMap = {en:'English', hi:'Hindi', te:'Telugu', ta:'Tamil', kn:'Kannada'};
      const res = await fetch(`${API}/api/first-aid?language=${langMap[state.lang]}&scenario=${scenario}`);
      tips = await res.json();
    } catch(e) {}
  }
  
  if (!tips || !tips.length) {
    tips = OFFLINE_TIPS[scenario] || OFFLINE_TIPS.general;
  }
  
  container.innerHTML = tips.map(t => `
    <div class="tip-step">
      <div class="step-num">${t.step_number}</div>
      <div class="step-icon">${t.icon || '⚠️'}</div>
      <div class="step-body">
        <div class="step-title">${t.title}</div>
        <div class="step-content">${t.content}</div>
      </div>
    </div>
  `).join('');
}
 
// ── UTILITIES ─────────────────────────────────────────────────────────────
function callNumber(num) {
  if (!num) return;
  showToast(`📞 Dialing ${num}... (Simulated Call)`, 'success');
  // Disabled actual 'tel:' link for the desktop demo to prevent the Windows "Pick an app" popup
}
 
function showToast(msg, type='', duration=3000) {
  const toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.className = `show ${type}`;
  clearTimeout(toast._t);
  toast._t = setTimeout(() => { toast.className = ''; }, duration);
}
 
// Handle window resize for map
window.addEventListener('resize', () => {
  if (state.services.length) placeServicesOnMap();
});

// ── FUTURE SCOPE: SIMULATE AUTO-CRASH ─────────────────────────────────────
function simulateCrash() {
  showToast('Monitoring accelerometer...', 'info');
  setTimeout(() => {
    // Vibrate device if supported
    if (navigator.vibrate) navigator.vibrate([500, 200, 500]);
    
    // Flash screen red
    const overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.inset = '0';
    overlay.style.background = 'rgba(255, 0, 0, 0.4)';
    overlay.style.zIndex = '9999';
    overlay.style.pointerEvents = 'none';
    overlay.style.transition = 'opacity 0.5s';
    document.body.appendChild(overlay);
    
    setTimeout(() => { overlay.style.opacity = '0'; setTimeout(() => overlay.remove(), 500); }, 200);

    // Auto trigger SOS
    updateSeverity('critical');
    document.getElementById('chat-input').value = 'Severe crash detected automatically';
    appendMsg('⚠️ [SYSTEM] Sudden high-G impact detected via Edge-AI. Auto-triggering SOS protocol...', 'user');
    
    triggerSOS(null);
    
    // Simulate Drone dispatch
    setTimeout(() => {
      appendMsg('🚁 Dispatching Autonomous First-Aid Drone to your exact GPS coordinates... ETA: 4 mins', 'bot');
    }, 2500);
    
  }, 1500);
}