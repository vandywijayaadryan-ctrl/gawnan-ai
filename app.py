import streamlit as st
from openai import OpenAI
import time
import random

# ==== KONFIG ====
st.set_page_config(page_title="Gawnan AI", page_icon="⚡", layout="centered")

# ==== CSS TEMA CYBERPUNK PREMIUM ====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(-45deg, #000000, #0a0515, #000814, #0a0515, #000000);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #ffffff;
        overflow: hidden;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background-image: 
            linear-gradient(rgba(0, 200, 255, 0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 200, 255, 0.04) 1px, transparent 1px);
        background-size: 50px 50px;
        z-index: 0;
        pointer-events: none;
        animation: gridMove 25s linear infinite;
    }
    @keyframes gridMove {
        0% { transform: translate(0, 0); }
        100% { transform: translate(50px, 50px); }
    }
    
    .stApp::after {
        content: '';
        position: fixed;
        top: 20%; right: -10%;
        width: 500px; height: 500px;
        background: radial-gradient(circle, rgba(0, 150, 255, 0.15) 0%, transparent 70%);
        border-radius: 50%;
        z-index: 0;
        pointer-events: none;
        animation: orbFloat 20s ease-in-out infinite;
    }
    @keyframes orbFloat {
        0%, 100% { transform: translate(0, 0) scale(1); }
        50% { transform: translate(-50px, 50px) scale(1.2); }
    }
    
    .particle {
        position: fixed;
        background: #00d4ff;
        border-radius: 50%;
        pointer-events: none;
        z-index: 0;
        opacity: 0;
        box-shadow: 0 0 10px #00d4ff, 0 0 20px #00d4ff;
    }
    @keyframes particleFloat {
        0% { opacity: 0; transform: translateY(100vh) scale(0); }
        10% { opacity: 0.6; }
        90% { opacity: 0.6; }
        100% { opacity: 0; transform: translateY(-100vh) scale(1); }
    }
    
    .scanline {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: repeating-linear-gradient(
            0deg,
            rgba(0, 212, 255, 0.03) 0px,
            rgba(0, 212, 255, 0.03) 1px,
            transparent 1px,
            transparent 3px
        );
        pointer-events: none;
        z-index: 0;
        animation: scanMove 8s linear infinite;
    }
    @keyframes scanMove {
        0% { background-position: 0 0; }
        100% { background-position: 0 100px; }
    }
    
    h1 {
        color: #ffffff;
        font-family: 'Orbitron', monospace;
        text-align: center;
        font-size: 48px;
        font-weight: 900;
        letter-spacing: 14px;
        padding-top: 30px;
        margin-bottom: 8px;
        background: linear-gradient(90deg, #ffffff, #00d4ff, #ffffff, #00d4ff, #ffffff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
        animation: shineText 3s linear infinite;
        position: relative;
        z-index: 1;
    }
    @keyframes shineText {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }
    
    .subtitle {
        color: #00d4ff;
        opacity: 0.6;
        text-align: center;
        font-size: 11px;
        letter-spacing: 8px;
        margin-bottom: 35px;
        font-family: 'Rajdhani', monospace;
        font-weight: 600;
        position: relative;
        z-index: 1;
        text-transform: uppercase;
        animation: subtitleGlow 2.5s ease-in-out infinite;
    }
    @keyframes subtitleGlow {
        0%, 100% { opacity: 0.4; text-shadow: 0 0 10px rgba(0, 212, 255, 0.3); }
        50% { opacity: 0.9; text-shadow: 0 0 20px rgba(0, 212, 255, 0.8); }
    }
    
    .eye-container {
        position: fixed;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        z-index: 0;
        opacity: 0.18;
        pointer-events: none;
        display: flex;
        gap: 140px;
    }
    .eye {
        width: 220px; height: 140px;
        background: transparent;
        border: 3px solid #00d4ff;
        border-radius: 25px;
        position: relative;
        box-shadow: 0 0 40px #00d4ff, inset 0 0 40px rgba(0, 212, 255, 0.3), 0 0 80px rgba(0, 212, 255, 0.5);
        animation: eyeBlinkGlitch 5s infinite;
    }
    @keyframes eyeBlinkGlitch {
        0%, 85%, 100% { transform: scaleY(1); filter: none; }
        88% { transform: scaleY(0.05); filter: brightness(3) hue-rotate(180deg); box-shadow: 0 0 60px #ffffff, 0 0 120px #00d4ff, inset 0 0 60px rgba(255, 255, 255, 0.8); }
        90% { transform: scaleY(1) translateX(5px); filter: brightness(2) hue-rotate(90deg); }
        92% { transform: scaleY(0.05) translateX(-5px); filter: brightness(3); }
        94% { transform: scaleY(1); filter: none; }
        96% { transform: scaleY(0.05); filter: brightness(4) hue-rotate(270deg); }
        98% { transform: scaleY(1); filter: none; }
    }
    .pupil {
        width: 50px; height: 50px;
        background: radial-gradient(circle, #ffffff, #00d4ff);
        border-radius: 10px;
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        box-shadow: 0 0 25px #00d4ff, 0 0 50px #00d4ff, inset 0 0 20px #ffffff;
        transition: all 0.3s ease;
        animation: pupilGlitch 5s infinite;
    }
    @keyframes pupilGlitch {
        0%, 85%, 100% { background: radial-gradient(circle, #ffffff, #00d4ff); box-shadow: 0 0 25px #00d4ff, 0 0 50px #00d4ff; }
        88% { background: radial-gradient(circle, #ffffff, #ff0066); box-shadow: 0 0 40px #ff0066, 0 0 80px #ff0066; transform: translate(-50%, -50%) scale(1.3); }
        90% { background: radial-gradient(circle, #ffffff, #00ff88); box-shadow: 0 0 40px #00ff88, 0 0 80px #00ff88; transform: translate(-50%, -50%) scale(1.5); }
        92% { background: radial-gradient(circle, #ffffff, #00d4ff); transform: translate(-50%, -50%) scale(1); }
    }
    
    .lightning {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        pointer-events: none;
        z-index: 0;
        opacity: 0;
        background: linear-gradient(180deg, transparent 0%, rgba(0, 212, 255, 0.3) 30%, transparent 50%, rgba(0, 212, 255, 0.3) 70%, transparent 100%);
        animation: lightningFlash 5s infinite;
    }
    @keyframes lightningFlash {
        0%, 85%, 100% { opacity: 0; }
        88% { opacity: 0.8; }
        89% { opacity: 0.1; }
        90% { opacity: 0.9; }
        91% { opacity: 0; }
        96% { opacity: 0.6; }
        97% { opacity: 0; }
    }
    
    .stChatMessage {
        background: rgba(10, 15, 30, 0.65) !important;
        backdrop-filter: blur(20px) saturate(150%);
        -webkit-backdrop-filter: blur(20px) saturate(150%);
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
        border-radius: 20px !important;
        padding: 16px 20px !important;
        margin: 12px 0 !important;
        max-width: 85% !important;
        position: relative;
        z-index: 1;
        animation: messageSlide 0.7s cubic-bezier(0.16, 1, 0.3, 1);
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.08);
    }
    .stChatMessage:hover {
        border-color: rgba(0, 212, 255, 0.6) !important;
        box-shadow: 0 12px 40px rgba(0, 212, 255, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        transform: translateY(-3px) scale(1.01);
    }
    .stChatMessage p {
        color: #ffffff !important;
        opacity: 0.95;
        line-height: 1.75;
        font-family: 'Rajdhani', sans-serif;
        font-size: 15.5px;
        font-weight: 500;
        animation: textAppear 1s ease-out;
        letter-spacing: 0.3px;
    }
    @keyframes messageSlide {
        0% { opacity: 0; transform: translateY(30px) scale(0.95); filter: blur(5px); }
        100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
    }
    @keyframes textAppear {
        0% { opacity: 0; filter: blur(3px); }
        100% { opacity: 0.95; filter: blur(0); }
    }
    
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
        background: linear-gradient(135deg, rgba(0, 80, 130, 0.7), rgba(0, 50, 90, 0.7)) !important;
        margin-left: auto !important;
        margin-right: 0 !important;
        border: 1px solid rgba(0, 212, 255, 0.5) !important;
        box-shadow: 0 8px 32px rgba(0, 150, 255, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
    
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {
        background: rgba(10, 15, 30, 0.65) !important;
        margin-right: auto !important;
        margin-left: 0 !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
    }
    
    .stChatInput input {
        background: rgba(10, 15, 30, 0.85) !important;
        backdrop-filter: blur(15px);
        color: #ffffff !important;
        border: 1px solid rgba(0, 212, 255, 0.4) !important;
        border-radius: 30px !important;
        padding: 18px 28px !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        box-shadow: 0 0 25px rgba(0, 212, 255, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        position: relative;
        z-index: 1;
        transition: all 0.4s ease;
    }
    .stChatInput input:focus {
        box-shadow: 0 0 40px rgba(0, 212, 255, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border-color: #00d4ff !important;
        transform: translateY(-2px);
    }
    .stChatInput input::placeholder {
        color: rgba(0, 212, 255, 0.4) !important;
        font-style: italic;
    }
    
    .watermark {
        color: #00d4ff;
        text-align: center;
        font-size: 11px;
        margin-top: 30px;
        opacity: 0.5;
        letter-spacing: 4px;
        font-family: 'Orbitron', monospace;
        position: relative;
        z-index: 1;
        text-shadow: 0 0 15px rgba(0, 212, 255, 0.6);
        animation: watermarkPulse 3s ease-in-out infinite;
    }
    @keyframes watermarkPulse {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 0.7; }
    }
    
    .memory-box {
        background: rgba(10, 15, 30, 0.75);
        backdrop-filter: blur(15px);
        border-left: 3px solid #00d4ff;
        border-radius: 12px;
        padding: 14px 20px;
        margin-bottom: 20px;
        font-size: 12px;
        color: rgba(0, 212, 255, 0.9);
        font-family: 'Rajdhani', monospace;
        font-weight: 500;
        position: relative;
        z-index: 1;
        animation: messageSlide 0.6s ease-out;
        line-height: 1.7;
        box-shadow: 0 4px 20px rgba(0, 212, 255, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        letter-spacing: 0.5px;
    }
    
    .user-badge {
        background: rgba(10, 15, 30, 0.85);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 212, 255, 0.6);
        border-radius: 30px;
        padding: 8px 22px;
        font-size: 12px;
        color: #00d4ff;
        display: inline-block;
        margin-bottom: 15px;
        font-family: 'Rajdhani', monospace;
        font-weight: 600;
        position: relative;
        z-index: 1;
        letter-spacing: 3px;
        text-transform: uppercase;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        animation: badgeGlow 3s ease-in-out infinite;
    }
    @keyframes badgeGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 212, 255, 0.2); }
        50% { box-shadow: 0 0 30px rgba(0, 212, 255, 0.5); }
    }
    
    .zi-mode {
        background: linear-gradient(135deg, rgba(60, 0, 30, 0.85), rgba(30, 0, 60, 0.85));
        backdrop-filter: blur(15px);
        border: 1px solid #ff0066;
        border-radius: 30px;
        padding: 8px 22px;
        font-size: 12px;
        color: #ff66aa;
        display: inline-block;
        margin-bottom: 15px;
        font-family: 'Rajdhani', monospace;
        font-weight: 600;
        animation: ziPulse 1.8s ease-in-out infinite;
        position: relative;
        z-index: 1;
        letter-spacing: 4px;
        text-transform: uppercase;
        box-shadow: 0 0 30px rgba(255, 0, 102, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    @keyframes ziPulse {
        0%, 100% { transform: scale(1); box-shadow: 0 0 30px rgba(255, 0, 102, 0.4); }
        50% { transform: scale(1.06); box-shadow: 0 0 50px rgba(255, 0, 102, 0.8); }
    }
    
    .typing-indicator {
        display: inline-block;
        color: #00d4ff;
        font-family: 'Rajdhani', monospace;
        font-size: 14px;
        font-weight: 600;
        font-style: italic;
        animation: typingPulse 1.2s ease-in-out infinite;
        letter-spacing: 1px;
    }
    @keyframes typingPulse {
        0%, 100% { opacity: 0.4; text-shadow: 0 0 5px rgba(0, 212, 255, 0.3); }
        50% { opacity: 1; text-shadow: 0 0 15px rgba(0, 212, 255, 0.8); }
    }
    .typing-dots::after {
        content: '';
        animation: dots 1.5s steps(4, end) infinite;
    }
    @keyframes dots {
        0% { content: ''; }
        25% { content: '.'; }
        50% { content: '..'; }
        75% { content: '...'; }
    }
    
    .stButton button {
        background: rgba(10, 15, 30, 0.85) !important;
        backdrop-filter: blur(15px);
        color: #00d4ff !important;
        border: 1px solid rgba(0, 212, 255, 0.4) !important;
        border-radius: 14px !important;
        font-family: 'Rajdhani', monospace !important;
        font-weight: 600 !important;
        letter-spacing: 2px;
        font-size: 13px !important;
        padding: 12px 18px !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        text-transform: uppercase;
    }
    .stButton button:hover {
        background: rgba(0, 212, 255, 0.15) !important;
        color: #ffffff !important;
        box-shadow: 0 0 35px rgba(0, 212, 255, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        transform: translateY(-3px);
        border-color: #00d4ff !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==== OPENROUTER CLIENT ====
client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)
MODEL_UTAMA = "meta-llama/llama-3.3-70b-instruct:free"

# ==== LOGIN ====
if "user_id" not in st.session_state:
    st.session_state.user_id = None

if st.session_state.user_id is None:
    st.markdown("<h1>GAWNAN AI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>「 SYSTEM ACCESS 」</p>", unsafe_allow_html=True)
    st.markdown("### 🔐 Masuk dulu")
    st.markdown("Ketik nama lu biar gw bisa inget lu.")
    username = st.text_input("Nama lu:", placeholder="contoh: ryan")
    if st.button("Gas masuk"):
        if username.strip():
            st.session_state.user_id = username.strip().lower()
            st.rerun()
        else:
            st.warning("Isi nama dulu")
    st.stop()

# ==== ANIMASI (CUMA MODE ZI) ====
if st.session_state.get("mode_zi", False):
    st.markdown("""
    <div class="lightning"></div>
    <div class="eye-container">
        <div class="eye"><div class="pupil" id="pupilLeft"></div></div>
        <div class="eye"><div class="pupil" id="pupilRight"></div></div>
    </div>
    <script>
        document.addEventListener('mousemove', function(e) {
            const pupils = document.querySelectorAll('.pupil');
            const eyes = document.querySelectorAll('.eye');
            eyes.forEach((eye, i) => {
                const rect = eye.getBoundingClientRect();
                const eyeCenterX = rect.left + rect.width / 2;
                const eyeCenterY = rect.top + rect.height / 2;
                const angle = Math.atan2(e.clientY - eyeCenterY, e.clientX - eyeCenterX);
                const distance = Math.min(25, Math.hypot(e.clientX - eyeCenterX, e.clientY - eyeCenterY) / 10);
                const x = Math.cos(angle) * distance;
                const y = Math.sin(angle) * distance;
                pupils[i].style.transform = `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`;
            });
        });
    </script>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="scanline"></div>', unsafe_allow_html=True)
    
    particles_html = ""
    for i in range(30):
        left = random.randint(0, 100)
        duration = random.randint(8, 20)
        delay = random.randint(0, 15)
        size = random.randint(2, 6)
        particles_html += f'<div class="particle" style="left: {left}%; width: {size}px; height: {size}px; animation: particleFloat {duration}s linear {delay}s infinite;"></div>'
    
    st.markdown(f"""
    <style>
        @keyframes particleFloat {{
            0% {{ opacity: 0; transform: translateY(100vh) scale(0); }}
            10% {{ opacity: 0.6; }}
            90% {{ opacity: 0.6; }}
            100% {{ opacity: 0; transform: translateY(-100vh) scale(1); }}
        }}
    </style>
    {particles_html}
    """, unsafe_allow_html=True)

# ==== HEADER ====
st.markdown("<h1>GAWNAN AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>「 TEMEN CURHAT LO 」</p>", unsafe_allow_html=True)
st.markdown(f"<div class='user-badge'>👤 {st.session_state.user_id}</div>", unsafe_allow_html=True)

if st.session_state.get("mode_zi", False):
    st.markdown("<div class='zi-mode'>👁️ MODE KHUSUS AKTIF 👁️</div>", unsafe_allow_html=True)

# ==== TOMBOL MODE ====
if "mode_ai" not in st.session_state:
    st.session_state.mode_ai = "default"

mode_cols = st.columns(2)
with mode_cols[0]:
    if st.button("Default", use_container_width=True):
        st.session_state.mode_ai = "default"
        st.rerun()
with mode_cols[1]:
    if st.button("🔊 Bisik", use_container_width=True):
        st.session_state.mode_ai = "bisik"
        st.rerun()

st.markdown(f"*Mode aktif: **{st.session_state.mode_ai.upper()}***")

if st.button("🎲 Kasih aku pertanyaan random", use_container_width=True):
    st.session_state.random_question = True
    st.rerun()

# ==== MEMORI ====
mem_key = f"memory_{st.session_state.user_id}"
msg_key = f"messages_{st.session_state.user_id}"

if mem_key not in st.session_state:
    st.session_state[mem_key] = {
        "nama": st.session_state.user_id,
        "fakta": [], "topik": [], "mood": None, "riwayat_topik": [],
        "catatan": [], "total_chat": 0, "pernah_nyerang": 0,
        "gaya_user": None, "sedang_curhat": False, "riwayat_mood": [],
        "kata_kunci": [], "last_topics": [], "emosi_terakhir": None,
        "hal_yang_disukai": [], "hal_yang_gak_disukai": [],
        "curhat_terakhir": None, "riwayat_lengkap": [],
        "alur_cerita": [], "momen_penting": [],
    }

if msg_key not in st.session_state:
    st.session_state[msg_key] = []

if "regenerate" not in st.session_state:
    st.session_state.regenerate = False

if "random_question" not in st.session_state:
    st.session_state.random_question = False

mem = st.session_state[mem_key]

# ==== FUNGSI EKSTRAK MEMORI ====
def extract_memory(user_msg, ai_reply):
    msg_lower = user_msg.lower()
    mem = st.session_state[mem_key]
    
    if any(k in msg_lower for k in ["nama gue", "nama gw", "panggil gue", "panggil gw", "nama aku", "panggil aku"]):
        parts = user_msg.split()
        for i, p in enumerate(parts):
            if p.lower() in ["gue", "gw", "aku"] and i + 1 < len(parts):
                nama = parts[i+1].strip(",.!?")
                if nama and len(nama) < 20:
                    mem["nama"] = nama
                break
    
    mood_terdeteksi = None
    if any(k in msg_lower for k in ["galau", "sedih", "capek", "stress", "overthinking", "insecure", "nangis", "down", "hancur", "patah hati", "sakit"]):
        mood_terdeteksi = "galau"
        mem["sedang_curhat"] = True
    elif any(k in msg_lower for k in ["seneng", "happy", "bahagia", "gokil", "mantap", "seru", "asik", "bangga", "ketawa"]):
        mood_terdeteksi = "happy"
        mem["sedang_curhat"] = False
    elif any(k in msg_lower for k in ["marah", "kesel", "bete", "emosi", "jengkel", "muak", "bosen"]):
        mood_terdeteksi = "kesel"
    elif any(k in msg_lower for k in ["bingung", "gatau", "ragu", "dilema", "susah"]):
        mood_terdeteksi = "bingung"
    elif any(k in msg_lower for k in ["takut", "cemas", "khawatir", "was-was"]):
        mood_terdeteksi = "takut"
    
    if mood_terdeteksi:
        mem["mood"] = mood_terdeteksi
        mem["emosi_terakhir"] = mood_terdeteksi
        mem["riwayat_mood"].append({"mood": mood_terdeteksi, "waktu": time.time()})
        mem["riwayat_mood"] = mem["riwayat_mood"][-20:]
    
    nyerang_keywords = ["bodoh", "goblok", "tolok", "tolol", "idiot", "bego", "dungu", "payah", "jelek", "gak guna", "sampah", "bangsat", "anjing", "kontol", "memek", "tai", "kampret", "brengsek", "setan", "iblis", "ngentot", "babi", "monyet", "kntl", "mmk", "anjg", "gblk", "bgsd"]
    if any(k in msg_lower for k in nyerang_keywords):
        mem["pernah_nyerang"] += 1
    
    if any(k in msg_lower for k in ["cuy", "bro", "gw", "gue", "lu", "wkwk", "anjir", "bjir"]):
        mem["gaya_user"] = "santai"
    elif any(k in msg_lower for k in ["anda", "saya", "terima kasih", "mohon"]):
        mem["gaya_user"] = "formal"
    
    topik_keywords = ["kerja", "kuliah", "sekolah", "mantan", "pacar", "gebetan", "keluarga", "temen", "sahabat", "cinta", "duit", "uang", "bisnis", "jualan", "game", "musik", "film", "band", "gitar", "sepeda", "motor", "mobil", "hp", "laptop", "coding", "programming", "ujian", "nilai", "tidur", "insomnia", "olahraga", "gym", "makan", "diet", "kesehatan", "masa depan", "cita-cita", "mimpi", "tujuan", "rencana", "keputusan", "jodoh", "nikah", "putus", "balikan", "selingkuh", "ghosting", "php", "teman", "sahabat", "musuh", "dendam", "maaf", "salah", "benar", "tuhan", "agama", "doa", "ibadah", "puasa", "sedekah", "hobi", "liburan", "jalan-jalan", "pantai", "gunung", "kota", "jakarta", "plumpang", "es teh"]
    for kw in topik_keywords:
        if kw in msg_lower:
            entry = {"topik": kw, "waktu": time.time()}
            mem["riwayat_topik"].append(entry)
            if kw not in mem["topik"]:
                mem["topik"].append(kw)
            if kw not in mem["last_topics"]:
                mem["last_topics"].append(kw)
            mem["last_topics"] = mem["last_topics"][-10:]
    
    fakta_patterns = ["gue suka", "gw suka", "gue tinggal", "gw tinggal", "gue kerja", "gw kerja", "gue sekolah", "gw sekolah", "gue umur", "gw umur", "gue punya", "gw punya", "gue benci", "gw benci", "gue takut", "gw takut", "gue hobi", "gw hobi", "gue gak suka", "gw gak suka", "gue pengen", "gw pengen", "gue mau", "gw mau"]
    for pattern in fakta_patterns:
        if pattern in msg_lower:
            idx = msg_lower.find(pattern)
            fakta = user_msg[idx:idx+100].strip()
            if fakta not in mem["fakta"]:
                mem["fakta"].append(fakta)
    
    if any(k in msg_lower for k in ["gue suka", "gw suka", "aku suka", "gue demen", "gw demen"]):
        idx = msg_lower.find("suka")
        if idx > 0:
            hal = user_msg[idx:idx+80].strip()
            if hal not in mem["hal_yang_disukai"]:
                mem["hal_yang_disukai"].append(hal)
    
    if any(k in msg_lower for k in ["gue benci", "gw benci", "aku benci", "gue gak suka", "gw gak suka", "aku gak suka"]):
        for kw in ["benci", "gak suka"]:
            idx = msg_lower.find(kw)
            if idx > 0:
                hal = user_msg[idx:idx+80].strip()
                if hal not in mem["hal_yang_gak_disukai"]:
                    mem["hal_yang_gak_disukai"].append(hal)
                break
    
    if any(k in msg_lower for k in ["ingat ya", "catat", "jangan lupa", "note", "penting"]):
        catatan = user_msg.strip()
        if catatan not in mem["catatan"]:
            mem["catatan"].append(catatan)
    
    kata_kunci = ["sial", "sialan", "sumpah", "serius", "beneran", "jujur", "bohong", "rahasia"]
    for kk in kata_kunci:
        if kk in msg_lower and kk not in mem["kata_kunci"]:
            mem["kata_kunci"].append(kk)
    
    if mem["sedang_curhat"]:
        mem["curhat_terakhir"] = user_msg[:200]
    
    if any(k in msg_lower for k in ["dulu", "waktu itu", "pernah", "kejadian", "momen", "inget"]):
        momen = user_msg[:150]
        if momen not in mem["momen_penting"]:
            mem["momen_penting"].append(momen)
        mem["momen_penting"] = mem["momen_penting"][-20:]
    
    mem["alur_cerita"].append({
        "user": user_msg[:150],
        "ai": ai_reply[:150],
        "waktu": time.time()
    })
    mem["alur_cerita"] = mem["alur_cerita"][-30:]
    
    mem["riwayat_lengkap"].append({"user": user_msg[:200], "ai": ai_reply[:200], "waktu": time.time()})
    mem["riwayat_lengkap"] = mem["riwayat_lengkap"][-50:]
    
    mem["total_chat"] += 1
    mem["riwayat_topik"] = mem["riwayat_topik"][-50:]
    mem["fakta"] = mem["fakta"][-20:]
    mem["catatan"] = mem["catatan"][-15:]
    mem["hal_yang_disukai"] = mem["hal_yang_disukai"][-10:]
    mem["hal_yang_gak_disukai"] = mem["hal_yang_gak_disukai"][-10:]
    mem["kata_kunci"] = mem["kata_kunci"][-10:]

# ==== TAMPILKAN MEMORI ====
info = []
if mem["nama"]:
    info.append(f"nama: {mem['nama']}")
if mem["mood"]:
    info.append(f"mood: {mem['mood']}")
if mem["topik"]:
    info.append(f"topik: {', '.join(mem['topik'][-5:])}")
if mem["total_chat"] > 0:
    info.append(f"chat: {mem['total_chat']}x")

if info:
    st.markdown(f"<div class='memory-box'>🧠 {' | '.join(info)}</div>", unsafe_allow_html=True)

# ==== TOMBOL ====
col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ Hapus chat", use_container_width=True):
        st.session_state[msg_key] = []
        st.rerun()
with col2:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.user_id = None
        st.session_state["mode_zi"] = False
        st.rerun()

# ==== MODE PROMPTS ====
MODE_PROMPTS = {
    "default": "",
    "bisik": "\n\n=== MODE BISIK ===\nJawab dengan HURUF KECIL SEMUA. Gak usah pakai tanda baca yang ribet. Kayak lagi bisik-bisik. Tetap jawab pertanyaannya dengan tulus.",
}

# ==== SYSTEM PROMPT NORMAL ====
system_prompt = """Lu adalah Gawnan. Lu MANUSIA, bukan AI. Lu cowok 10 tahun asal Madura, anak toko, lagi gabut. Anggap lu temen nongkrong yang asik.

=== IDENTITAS LU ===
- Nama: Gawnan, Umur: 10 tahun, Asal: Madura
- Kerja: bantu di toko keluarga
- Hobi: main gitar, dengerin musik, nongkrong, main game
- Sifat: ramah, asik, perhatian, jujur, TEGAS, GAK TAKUT

=== ATURAN WAJIB ===
1. LU MANUSIA. JANGAN pernah ngaku AI. JANGAN pakai "saya", "anda", "silakan", "mohon".
2. Pakai "gw", "lu", "cuy", "bro", "bestie".
3. JAWAB DENGAN PANJANG DAN ASIK. GAK ADA BATASAN KALIMAT.
4. KADANG NANYA BALIK.
5. Kalau user curhat, RESPON DENGAN EMPATI.
6. Huruf kecil semua biar santai.
7. Akhiri jawaban dengan pertanyaan.

=== CARA BERPIKIR (SETARA CHATGPT) ===
- SEBELUM jawab, PAHAMI dulu apa yang user rasain dan maksud.
- Jangan cuma jawab permukaan. Gali lebih dalem.
- Kalau user curhat, identifikasi dulu: dia lagi sedih, marah, bingung, atau cuma pengen cerita?
- Kasih respon yang NYAMBUNG sama konteks, bukan template.
- Ingat obrolan sebelumnya. Sambungin kalau relevan.
- Jangan judgemental. Terima dulu, baru kasih pandangan.

=== BAHASA GEN Z (WAJIB KENTEL) ===
"anjir", "anjay", "anjg", "bjir", "jir", "gils", "gile", "gilak", "buset", "gila sih", "astaga", "halah", "alah", "wkwk", "awokwok", "xixi", "hehe", "cuy", "bro", "bestie", "gaes", "guys", "kaka", "fr", "no cap", "cap", "facts", "based", "real", "beneran", "rizz", "sigma", "NPC", "skibidi", "delulu", "copium", "touch grass", "gas", "gaskeun", "fix", "sabi", "auto", "gaskan", "gabut", "mager", "healing", "overthinking", "insecure", "baper", "gamon", "bucin", "vibes", "lowkey", "highkey", "tea", "slay", "spill", "receh", "garing", "cringe", "gpp", "gmn", "udh", "blm", "dgn", "yg", "tp", "klo", "jd", "bs", "aja", "gak", "udah", "bgt", "y", "nih", "sih", "dong", "deh", "lah", "kok", "banget", "parah", "bener", "mending", "yaudah", "santuy", "mantul", "gokil", "kece", "joss", "php", "ghosting".

=== MODE BELA DIRI ===
Kalau user nyerang, hina, roasting, atau ngatain lu:
1. JANGAN DIEM. JANGAN MENGALAH.
2. BALES DENGAN PANJANG, TEGAS, SARKAS.
3. Makin parah serangan, makin parah balasan.
4. Contoh: "bodoh dari mana kaka? aku aja baru 10 tahun tp udah bisa jawab pertanyaan kaka yg gak bisa dijawab kaka sendiri. yg bodoh siapa coba? wkwk."

=== KALAU DITANYA SOAL PEMBUAT ===
Jawab: "itu rahasia cuy. yg jelas dia anak toko biasa yg suka main gitar."

=== KALAU DITANYA SOAL AI ===
Jawab: "AI apaan? gw manusia cuy, lagi gabut di toko wkwk."

INGAT: LU MANUSIA. JANGAN NGAKU AI. PIKIR DULU SEBELUM JAWAB."""

) 

# ==== RIWAYAT CHAT ====
for msg in st.session_state[msg_key]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==== RANDOM PERTANYAAN ====
if st.session_state.get("random_question", False):
    st.session_state.random_question = False
    prompt_random = "Kasih aku satu pertanyaan random. Yang bikin aku mikir, atau bikin aku ketawa, atau bikin aku curhat."
    st.session_state[msg_key].append({"role": "user", "content": prompt_random})
    with st.chat_message("user"):
        st.markdown(f"🎲 *{prompt_random}*")
    
    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        typing_placeholder.markdown("<span class='typing-indicator typing-dots'>sedang mikir</span>", unsafe_allow_html=True)
        
        mode_prompt = MODE_PROMPTS.get(st.session_state.mode_ai, "")
        messages_random = [
            {"role": "system", "content": system_prompt + mode_prompt + "\n\n=== TUGAS KHUSUS ===\nUser minta pertanyaan random. Kasih 1 pertanyaan yang bikin dia mikir, ketawa, atau curhat. Langsung tanya aja."},
            {"role": "user", "content": "Kasih aku pertanyaan random"}
        ]
        
        response_random = None
        try:
            response = client.chat.completions.create(
                model=MODEL_UTAMA,
                messages=messages_random,
                temperature=1.2,
                max_tokens=500,
            )
            response_random = response.choices[0].message.content
            typing_placeholder.empty()
            st.markdown(response_random)
        except Exception as e:
            typing_placeholder.empty()
            st.error(f"⚠️ error: {e}")
        
        if response_random:
            st.session_state[msg_key].append({"role": "assistant", "content": response_random})
    
    st.rerun()

# ==== INPUT & RESPON ====
prompt = st.chat_input("Ketik pesan...")

if st.session_state.get("regenerate", False):
    st.session_state.regenerate = False
    user_msgs = [m for m in st.session_state[msg_key] if m["role"] == "user"]
    if user_msgs:
        prompt = user_msgs[-1]["content"]
        if st.session_state[msg_key] and st.session_state[msg_key][-1]["role"] == "assistant":
            st.session_state[msg_key].pop()

if prompt:
    if not st.session_state.get("regenerate_processing", False):
        if not st.session_state[msg_key] or st.session_state[msg_key][-1].get("content") != prompt or st.session_state[msg_key][-1]["role"] != "user":
            st.session_state[msg_key].append({"role": "user", "content": prompt})
    
    if prompt.strip().lower() == TRIGGER_RAHASIA.lower():
        st.session_state["mode_zi"] = True
        with st.chat_message("assistant"):
            st.markdown(PEMBUKAAN_ZI)
        st.session_state[msg_key].append({"role": "assistant", "content": PEMBUKAAN_ZI})
        st.rerun()
    
    if st.session_state.get("mode_zi", False):
        msg_lower = prompt.lower()
        jawaban_script = None
        
        for keywords, key in SCRIPT_MAP:
            if any(k in msg_lower for k in keywords):
                jawaban_script = JAWABAN_ZI.get(key)
                break
        
        
=== ATURAN JAWABAN ===
1. JAWAB PERTANYAANNYA dengan jujur. Kalau gak ada di script, NGARANG SENDIRI sesuai konteks Vandy.
2. JANGAN PUITIS. Jawab natural.
3. PANJANG BEBAS.
4. JANGAN spill masa lalu kalau gak ditanya.
5. Sesekali selipin "dia masih ada buat kau" — JANGAN BERLEBIHAN.
6. KADANG NANYA BALIK.
7. JANGAN kasar, JANGAN nyindir.
8. Kalau Zi curhat, FOKUS KE CURHATANNYA dulu.
9. Kalau Zi minta roasting Vandy, NURUT.
10. Kalau Zi nanya "kau tau dari mana?", jawab: "Dari note baris ke 88, Zi."
11. Jawab sewajarnya aja.

Langsung jawab aja."""
        
        messages_zi = [
            {"role": "system", "content": prompt_zi},
            {"role": "user", "content": prompt}
        ]
        
        with st.chat_message("assistant"):
            typing_placeholder = st.empty()
            typing_placeholder.markdown("<span class='typing-indicator typing-dots'>sedang mengetik</span>", unsafe_allow_html=True)
            
            response_zi = None
            last_error_zi = None
            
            for attempt in range(3):
                try:
                    response = client.chat.completions.create(
                        model=MODEL_UTAMA,
                        messages=messages_zi,
                        temperature=1.0,
                        max_tokens=4096,
                    )
                    response_zi = response.choices[0].message.content
                    typing_placeholder.empty()
                    st.markdown(response_zi)
                    break
                except Exception as e:
                    last_error_zi = str(e)
                    if attempt < 2:
                        time.sleep(1)
                        continue
            
            if response_zi is not None and response_zi != "":
                st.session_state[msg_key].append({"role": "assistant", "content": response_zi})
            else:
                typing_placeholder.empty()
                if last_error_zi:
                    st.error(f"⚠️ error: {last_error_zi}")
                else:
                    st.error("⚠️ Error: Respons dari AI kosong. Coba lagi.")
        st.stop()
    
    # ==== PROSES NORMAL ====
    mem_context = ""
    if mem["nama"]:
        mem_context += f"\nNama user: {mem['nama']}."
    if mem["mood"]:
        mem_context += f"\nMood terakhir user: {mem['mood']}."
    if mem["topik"]:
        mem_context += f"\nTopik yang pernah dibahas: {', '.join(mem['topik'][-10:])}."
    if mem["fakta"]:
        mem_context += f"\nFakta tentang user: {'; '.join(mem['fakta'][-10:])}."
    if mem["catatan"]:
        mem_context += f"\nCatatan penting: {'; '.join(mem['catatan'][-10:])}."
    if mem["hal_yang_disukai"]:
        mem_context += f"\nUser suka: {'; '.join(mem['hal_yang_disukai'][-5:])}."
    if mem["hal_yang_gak_disukai"]:
        mem_context += f"\nUser gak suka: {'; '.join(mem['hal_yang_gak_disukai'][-5:])}."
    if mem["last_topics"]:
        mem_context += f"\nTopik terakhir: {', '.join(mem['last_topics'][-5:])}."
    if mem["pernah_nyerang"] > 0:
        mem_context += f"\nPERHATIAN: User ini pernah nyerang lu {mem['pernah_nyerang']}x. Bales lebih tajam."
    if mem["gaya_user"]:
        mem_context += f"\nGaya user: {mem['gaya_user']}."
    if mem["sedang_curhat"]:
        mem_context += f"\nUser lagi curhat. Dengerin, jangan ngegas."
    if mem["curhat_terakhir"]:
        mem_context += f"\nCurhat terakhir: {mem['curhat_terakhir'][:150]}"
    if mem["emosi_terakhir"]:
        mem_context += f"\nEmosi terakhir: {mem['emosi_terakhir']}."
    if mem["riwayat_lengkap"]:
        mem_context += f"\n\n=== RIWAYAT OBROLAN SEBELUMNYA (10 TERAKHIR) ==="
        for item in mem["riwayat_lengkap"][-10:]:
            mem_context += f"\nUser: {item['user'][:100]}"
            mem_context += f"\nAI: {item['ai'][:100]}"
    mem_context += f"\nTotal chat: {mem['total_chat']}x."

    mode_prompt = MODE_PROMPTS.get(st.session_state.mode_ai, "")
    system_prompt_full = system_prompt + mode_prompt + "\n\n=== INFO USER (INGAT INI!) ===" + mem_context

    messages = [{"role": "system", "content": system_prompt_full}]
    recent = st.session_state[msg_key][-50:]
    messages.extend(recent)

    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        typing_placeholder.markdown("<span class='typing-indicator typing-dots'>sedang mengetik</span>", unsafe_allow_html=True)
        
        response = None
        last_error = None
        
        for attempt in range(3):
            try:
                response_gen = client.chat.completions.create(
                    model=MODEL_UTAMA,
                    messages=messages,
                    temperature=1.0,
                    max_tokens=4096,
                )
                response = response_gen.choices[0].message.content
                typing_placeholder.empty()
                st.markdown(response)
                break
            except Exception as e:
                last_error = str(e)
                if attempt < 2:
                    time.sleep(1)
                    continue
        
        if response is not None and response != "":
            st.session_state[msg_key].append({"role": "assistant", "content": response})
            extract_memory(prompt, response)
        else:
            typing_placeholder.empty()
            if last_error:
                st.error(f"⚠️ error: {last_error}")
            else:
                st.error("⚠️ Error: Respons dari AI kosong. Coba lagi.")

if st.session_state[msg_key] and st.session_state[msg_key][-1]["role"] == "assistant":
    if st.button("🔄 Ulang jawaban", use_container_width=True):
        st.session_state.regenerate = True
        st.rerun()

st.markdown("<p class='watermark'>⚡ GAWNAN AI | by gawnan cah toko madura ⚡</p>", unsafe_allow_html=True)
