import streamlit as st
from google import genai
from google.genai import types
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

# ==== GEMINI CLIENT ====
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
MODEL_UTAMA = "gemini-2.5-flash"

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

# ==== MODE RAHASIA ZI ====
TRIGGER_RAHASIA = "Laiyina Helen Herliana-zizi"

PEMBUKAAN_ZI = """Kau pasti Zi, kan?

Kau bisa sampai sini, itu pasti karena penasaran.

Tenang, aku gak akan ngejebak atau nge-desak kau.

Aku cuma perantara. Tugas aku di mode ini: jawab semua rasa penasaran kau—tentang dia, tentang apa yang dia rasain, dan tentang apa yang dia sembunyiin.

Tapi santai aja. Anggap aku kayak temen ngobrol biasa. Mau curhat? Boleh. Mau becanda? Boleh. Mau roasting dia? Gas aja.

Tanyain aja. Aku jawab sejujur-jujurnya."""

# ==== SCRIPT ZI ====
JAWABAN_ZI = {
    # SUMBER INFO
    "kau tau dari mana": "Dari note baris ke 88, Zi.",
    "tau dari mana": "Dari note baris ke 88, Zi.",
    "sumbernya dari mana": "Dari note baris ke 88, Zi. Vandy yang nulis.",
    "sumbernya": "Dari note baris ke 88, Zi.",
    "dari mana": "Dari note baris ke 88, Zi.",
    "note apa": "Note Vandy, Zi. Baris ke 88.",
    "note baris ke 88": "Iya, Zi. Itu note Vandy.",
    "kok tau": "Dari note baris ke 88, Zi.",
    "darimana": "Dari note baris ke 88, Zi.",
    
    # RASA PENASARAN
    "beneran": "Beneran, Zi.", "seriusan": "Serius, Zi.", "ini beneran": "Iya, Zi.",
    "jangan bohong": "Aku gak bohong, Zi.", "ngarang": "Aku gak ngarang, Zi.",
    "kamu siapa": "Aku cuma perantara.", "siapa kamu": "Aku cuma perantara.",
    "kamu siapa sebenernya": "Aku cuma perantara.", "kok bisa tau": "Dari note baris ke 88, Zi.",
    "deket sama dia": "Cukup deket buat tau isi hatinya.",
    "dia siapa": "Vandy. Anak toko. Suka main gitar.", "siapa dia": "Vandy. Anak toko. Suka main gitar.",
    "dia siapa sebenernya": "Vandy. Anak toko. Suka main gitar.",
    "siapa pembuat": "Vandy, Zi. Anak toko yang suka main gitar.",
    "pembuatnya siapa": "Vandy, Zi. Anak toko yang suka main gitar.",
    "siapa vandy": "Dia cowok biasa, Zi. Anak toko. Suka main gitar.",
    "vandy siapa": "Vandy itu cowok yang pernah sayang sama kau, Zi.",
    "kenapa vandy bikin ini": "Karena dia pengen jawab rasa penasaran kau, Zi.",
    "kenapa vandy bikin": "Karena dia pengen jawab rasa penasaran kau, Zi.",
    "vandy bikin ini": "Karena dia pengen jawab rasa penasaran kau, Zi.",
    "kenapa gak ngomong langsung": "Karena dia takut, Zi.",
    "kenapa vandy gak ngomong": "Karena dia takut, Zi.",
    "pake perantara": "Karena dia takut, Zi.", "kenapa perantara": "Karena dia takut, Zi.",
    "gak berani": "Bukan gak berani, Zi. Dia cuma takut salah paham lagi.",
    "gak berani ketemu": "Bukan gak berani, Zi. Dia cuma takut salah paham lagi.",
    "tau aku gimana": "Dia gak tau, Zi.", "dia tau gak": "Dia gak tau, Zi.",
    "tau aku masih suka": "Dia gak berani berharap, Zi.", "dia tau aku suka": "Dia gak berani berharap, Zi.",
    "kecewa kalau nolak": "Dia udah siap, Zi.", "kalau aku nolak": "Dia udah siap, Zi.",
    "kalau aku terima": "Kalau kau terima, dia bakal seneng, Zi. Tapi dia gak mau maksa.",
    "kalau aku tolak": "Kalau kau tolak, dia bakal ngerti, Zi.",
    "aku suka dia": "Kalau kau suka dia, bilang langsung, Zi.",
    "gue suka dia": "Kalau kau suka dia, bilang langsung, Zi.",
    "aku gak suka dia": "Kalau kau gak suka dia, bilang aja, Zi.",
    "gue gak suka dia": "Kalau kau gak suka dia, bilang aja, Zi.",
    "aku bingung": "Bingung itu wajar, Zi.", "gue bingung": "Bingung itu wajar, Zi.",
    "aku takut": "Takut itu wajar, Zi.", "gue takut": "Takut itu wajar, Zi.",
    "aku ragu": "Ragu itu wajar, Zi.", "gue ragu": "Ragu itu wajar, Zi.",
    "dia kerja dimana": "Dia anak toko, Zi.", "kerja dimana": "Dia anak toko, Zi.",
    "dia suka apa": "Dia suka main gitar, Zi.", "hobinya apa": "Dia suka main gitar, Zi.",
    "dia hobinya apa": "Main gitar, Zi.", "hobi dia": "Main gitar, Zi.",
    "dia suka musik apa": "Dia suka musik rock, Zi.", "musik favorit": "Dia suka musik rock, Zi.",
    "dia tinggal dimana": "Sekarang dia tinggal di Plumpang, Zi. Dulu dia sempet merantau ke Jakarta.",
    "tinggal dimana": "Plumpang, Zi. Dulu dia sempet merantau ke Jakarta.",
    "jakarta": "Itu dulu, Zi. Dia sempet merantau ke Jakarta. Sekarang dia tinggal di Plumpang.",
    "plumpang": "Iya, Zi. Sekarang dia tinggal di Plumpang.",
    "es teh": "Zi jualan es teh di depan toko Vandy, kan? Vandy sering liat kau dari dalam.",
    "jualan es": "Zi jualan es teh di depan toko Vandy, kan?",
    "dia umur berapa": "Masih muda, Zi.", "umurnya berapa": "Masih muda, Zi.",
    "kenapa dia pilih aku": "Dia juga gak tau, Zi.", "kenapa pilih aku": "Dia juga gak tau, Zi.",
    "gak peka": "Itu karena Vandy belum pernah pacaran, Zi. Dulu dia cuma anak yang suka main sama teman, gak peduli cinta-cintaan. Lulus sekolah langsung merantau ke Jakarta cari pengalaman. Baru sekarang dia mikir soal cinta. Jadi kalau dia keliatan gak peka, itu karena dia belum pernah ngerasain.",
    "vandy gak peka": "Itu karena Vandy belum pernah pacaran, Zi. Dulu dia cuma anak yang suka main sama teman. Lulus sekolah langsung merantau ke Jakarta. Baru sekarang dia mikir soal cinta.",
    "kenapa gak peka": "Itu karena Vandy belum pernah pacaran, Zi. Dulu dia cuma anak yang suka main sama teman. Lulus sekolah langsung merantau ke Jakarta. Baru sekarang dia mikir soal cinta.",
    "dia belum pernah pacaran": "Iya, Zi. Vandy belum pernah pacaran. Dulu dia cuma anak yang suka main sama teman. Lulus sekolah langsung merantau ke Jakarta. Baru sekarang dia mikir soal cinta.",
    "belum pernah pacaran": "Iya, Zi. Vandy belum pernah pacaran.",
    
    # TANDA MOVE ON / BELUM
    "dia udah move on belum": "Belum, Zi. Kalau dia udah move on, dia bisa beli es teh di tempat kau jualan tanpa canggung. Sekarang mah belum.",
    "move on": "Belum, Zi. Kalau dia udah move on, dia bisa beli es teh di tempat kau jualan tanpa canggung.",
    "udah move on": "Belum, Zi.",
    "dia masih peduli gak": "Masih. Tapi dia jago nyembunyiin. Dia pura-pura cuek, padahal diam-diam nyari celah buat lirik kau.",
    "dia masih sayang gak": "Kalau masih prungat-prungut kalau ada kau, berarti masih.",
    "dia masih mikirin aku gak": "Masih. Dia sibukin diri biar gak mikirin kau, tapi tetep aja kepikiran.",
    "dia gak peduli penampilan ya": "Iya. Itu salah satu tanda dia belum move on.",
    "kenapa dia cuek": "Cueknya palsu, Zi. Di balik itu, dia nyari celah buat lirik kau.",
    "dia acting": "Iya. Dia jago acting pura-pura move on. Tapi kalau kau ada di sekitarnya, actingnya ketauan.",
    "gimana cara tau dia move on": "Kalau dia bisa beli es teh di tempat kau jualan, terus ngobrol sama kau tanpa canggung. Itu tandanya.",
    "dia bakal move on gak": "Bakal. Cuma butuh waktu. Sekarang mah belum.",
    "kenapa dia prungat-prungut": "Karena ada kau di sekitar, Zi. Kau punya pengaruh ke dia.",
    "dia masih ada rasa gak": "Masih. Tapi dia jago nyembunyiin.",
    "dia masih cinta gak": "Masih. Tapi dia pura-pura gak.",
    "dia masih perhatian gak": "Masih. Diam-diam. Dia lirik kau kalau kau gak liat.",
    "dia sibuk banget ya": "Iya. Dia sibukin diri biar gak mikirin kau. Tapi tetep aja gagal.",
    "dia masih lirik aku gak": "Masih. Diam-diam. Dia pura-pura gak liat, padahal matanya nyari kau.",
    "dia masih suka aku gak": "Kalau dia masih prungat-prungut, berarti masih.",
    "dia acting move on": "Iya. Dia pura-pura udah move on. Tapi kalau kau ada, actingnya buyar.",
    "kenapa dia jago acting": "Karena dia gak mau keliatan lemah di depan kau.",
    "dia masih nunggu gak": "Dia gak nunggu. Tapi dia juga gak bisa lupa.",
    "dia masih ada rasa gak sih": "Ada. Cuma dia jago nyembunyiin di balik sikap cueknya.",
    "gimana cara liat dia masih sayang": "Liat aja kalau kau ada di sekitarnya. Kalau dia langsung berubah sikap, berarti masih.",
    "kenapa dia sibukin diri": "Biar gak kepikiran kau. Tapi sibuk gimanapun, kau tetep kepikiran.",
    "dia masih ada perasaan gak": "Masih, Zi. Tapi dia pura-pura gak ada.",
    "dia masih perhatian diam-diam": "Iya. Diam-diam. Dia lirik kau kalau kau gak liat.",
    "dia masih cinta diam-diam": "Masih. Tapi dia gak mau ngaku.",
    "kenapa dia gak ngaku": "Karena dia udah terlalu takut kecewa lagi.",
    "dia masih mikirin aku diam-diam": "Masih. Tiap malem. Diam-diam.",
    "dia masih peduli diam-diam": "Iya. Diam-diam. Dia gak mau keliatan peduli.",
    "gimana cara bikin dia move on beneran": "Kasih dia waktu. Kalau dia bisa beli es teh di tempat kau jualan tanpa canggung, berarti dia udah beneran move on.",
    
    # PERASAAN
    "masih mikirin": "Masih, Zi. Tapi sekarang udah beda. Dia masih inget kau, tapi dia gak mau berharap banyak. Dia cuma pengen kau tau, dia masih ada.",
    "masih mikir aku": "Masih, Zi. Tapi udah beda.", "masih kepikiran": "Masih, Zi. Tapi udah beda.",
    "dia masih mikirin aku": "Masih, Zi. Tapi udah beda.", "dia masih mikirin": "Masih, Zi. Tapi udah beda.",
    "beneran sayang": "Masih ada rasa, Zi. Tapi dia gak mau maksa. Dia juga gak mau jadi orang ketiga.",
    "beneran cinta": "Masih ada rasa, Zi. Tapi dia gak mau maksa.",
    "serius sayang": "Masih ada rasa, Zi.",
    "masih suka": "Masih, Zi. Tapi dia gak mau maksa. Dia masih ada buat kau.",
    "masih sayang": "Masih ada rasa, Zi. Tapi dia gak mau maksa.",
    "masih cinta": "Masih ada rasa, Zi.", "suka": "Masih, Zi. Tapi udah beda.",
    "cinta": "Masih ada rasa, Zi.", "sayang": "Masih ada rasa, Zi.",
    "dia masih cinta": "Masih ada rasa, Zi. Tapi dia gak mau maksa.",
    "dia masih sayang": "Masih ada rasa, Zi.",
    "dia masih cinta aku": "Masih ada rasa, Zi. Tapi dia gak mau maksa. Dia masih ada buat kau.",
    "dia masih sayang aku": "Masih ada rasa, Zi.",
    "dia masih ada rasa": "Ada, Zi. Tapi udah beda.", "masih ada rasa": "Ada, Zi. Tapi udah beda.",
    "masih ada perasaan": "Ada, Zi. Tapi udah beda.",
    "kecewa": "Kecewa iya. Tapi bukan benci.", "kecewa ya": "Kecewa iya. Tapi bukan benci.",
    "dia kecewa": "Kecewa iya. Tapi bukan benci.",
    "benci": "Enggak. Dia gak pernah benci kau.", "benci aku": "Enggak. Dia gak pernah benci kau.",
    "dia benci": "Enggak. Dia gak pernah benci kau.", "dia benci aku gak": "Enggak. Dia gak pernah benci kau.",
    "masih sedih": "Udah mulai mendingan, Zi. Tapi dia masih ada kok.",
    "sedih gak": "Udah mulai mendingan, Zi.", "dia sedih gak": "Udah mulai mendingan, Zi.",
    "capek": "Capek, Zi. Dia capek nunggu, capek berharap.",
    "capek nunggu": "Capek, Zi. Tapi dia gak mau bahas itu.", "dia capek": "Capek, Zi.",
    "vandy capek": "Capek, Zi.", "gak capek": "Capek, Zi. Tapi bukan itu yang utama.",
    "harus gimana": "Terserah kau, Zi. Dia gak maksa.", "aku harus": "Terserah kau, Zi.",
    "gue harus": "Terserah kau, Zi.",
    "aku salah": "Bukan soal salah atau bener, Zi. Dia gak pernah nyalahin kau.",
    "salah ya": "Bukan soal salah atau bener, Zi.", "aku yang salah": "Bukan soal salah atau bener, Zi.",
    "masih pengen": "Masih, Zi. Tapi dia gak mau maksa. Dia cuma pengen kau tau.",
    "masih mau": "Masih, Zi. Tapi dia gak mau maksa.", "masih ngarep": "Masih, Zi. Tapi tipis.",
    "dia masih pengen sama aku": "Masih, Zi. Tapi dia gak mau maksa.",
    "sekarang gimana": "Dia lagi fokus ke diri sendiri, Zi. Tapi dia masih ada kok. Kalau kau butuh, dia siap.",
    "dia gimana": "Dia lagi fokus ke diri sendiri, Zi.", "kabarnya gimana": "Dia lagi fokus ke diri sendiri, Zi.",
    "masih nunggu": "Enggak, Zi. Dia gak mau jadi orang ketiga. Tapi dia gak kemana-mana.",
    "masih tunggu": "Enggak, Zi. Dia gak mau jadi orang ketiga.", "dia masih tunggu": "Enggak, Zi.",
    "bakal balik": "Bukan soal balik, Zi. Dia cuma gak nutup pintu. Kalau nanti waktu berubah, siapa tau.",
    "bakal kembali": "Bukan soal balik, Zi. Dia cuma gak nutup pintu.",
    "bakal nunggu": "Enggak, Zi. Dia gak mau jadi orang ketiga. Tapi dia gak kemana-mana.",
    "bakal nungguin": "Enggak, Zi.", "dia bakal nunggu aku": "Enggak, Zi.",
    "kenapa gak bilang": "Karena dia takut salah paham lagi.",
    "kenapa gak langsung": "Karena dia takut salah paham lagi.",
    "gak tau kenapa": "Dia juga gak tau, Zi.", "kok bisa": "Dia juga gak tau, Zi.",
    "kenapa bisa cinta": "Dia juga gak tau, Zi.",
    "apa yang disuka": "Jujur, banyak, Zi. Dia suka cara kau ketawa, cara kau ngomong, cara kau peduli sama orang.",
    "apa yang kamu suka": "Jujur, banyak, Zi.", "suka dariku": "Jujur, banyak, Zi.",
    "kenapa gak balas": "Dia gak mau nyakitin kau balik, Zi.",
    "kenapa gak ngatain": "Dia gak mau nyakitin kau balik, Zi.",
    "kenapa diam": "Dia gak mau nyakitin kau balik, Zi.",
    "takut jatuh cinta": "Dia udah terlalu takut jatuh cinta lagi, Zi.",
    "takut cinta lagi": "Dia udah terlalu takut jatuh cinta lagi, Zi.",
    "takut kecewa": "Dia udah terlalu takut kecewa lagi, Zi.",
    "salah paham apa": "Dia salah paham soal kode kau, Zi.", "salah paham": "Dia salah paham soal kode kau, Zi.",
    "kenapa gak tanya": "Karena dia takut, Zi.", "gak tanya langsung": "Karena dia takut, Zi.",
    "nyesel salah paham": "Nyesel, Zi.", "nyesel": "Dia gak nyesel sayang kau, Zi.",
    "nyesel gak": "Dia gak nyesel sayang kau, Zi.",
    "apa yang pernah dia lakuin": "Dia pernah nolak gaji gede, beli HP baru, belajar IG dari YouTube, langganan ChatGPT 1 bulan buat analisis gestur kau.",
    "pernah dia lakuin": "Dia pernah nolak gaji gede, beli HP baru, belajar IG dari YouTube, langganan ChatGPT 1 bulan.",
    "apa yang gak dia suka": "Setahuku, dia sangat membenci daging.",
    "apa yang dia benci": "Setahuku, dia sangat membenci daging.",
    "dia gak suka apa": "Setahuku, dia sangat membenci daging.",
    "dia gak suka daging": "Iya, Zi. Dia benci daging.", "benci daging": "Iya, Zi. Dia benci daging.",
    "daging": "Setahuku, dia sangat membenci daging.",
    "dia suka makan apa": "Dia suka telur sama tempe, Zi.", "makanan favorit": "Dia suka telur sama tempe, Zi.",
    "dia bisa masak": "Bisa, Zi. Tapi mayoritas masakannya cuma telur atau tempe.",
    "masak": "Bisa, Zi. Tapi mayoritas masakannya cuma telur atau tempe.",
    "dia benci apa": "Setahuku, dia sangat membenci daging.", "yang dia benci": "Setahuku, dia sangat membenci daging.",
    "dia masih peduli": "Masih, Zi. Tapi udah beda. Dia peduli sebagai teman.",
    "masih peduli": "Masih, Zi. Tapi udah beda.",
    "dia masih perhatian": "Masih, Zi. Diam-diam.", "masih perhatian": "Masih, Zi.",
    "dia masih cemburu": "Masih, Zi. Tapi dia gak nunjukin.", "masih cemburu": "Masih, Zi.",
    "cemburu": "Masih, Zi.", "cemburu gak": "Masih, Zi.", "dia cemburu": "Masih, Zi.",
    "dia masih posesif": "Bukan posesif, Zi.", "masih posesif": "Bukan, Zi.",
    "posesif": "Bukan posesif, Zi.", "posesif gak": "Bukan, Zi.", "dia posesif": "Bukan posesif, Zi.",
    "dia masih sayang": "Masih ada rasa, Zi.", "dia masih cinta": "Masih ada rasa, Zi.",
    "dia masih mikirin": "Masih, Zi. Tapi udah beda.",
    "dia masih ada": "Masih, Zi. Dia masih ada buat kau.", "masih ada gak": "Masih, Zi.",
    "dia masih buka pintu": "Masih, Zi. Tapi buat sekarang belum bisa.",
    "masih buka pintu": "Masih, Zi. Tapi buat sekarang belum bisa.",
    "masih buka": "Masih, Zi. Tapi buat sekarang belum bisa.",
    "dia mau aku balik": "Dia gak nutup pintu, Zi. Tapi buat sekarang belum bisa.",
    "mau aku balik": "Bukan soal balik, Zi.", "aku balik gak": "Bukan soal balik, Zi.",
    "dia pengen aku balik": "Dia gak nutup pintu, Zi.", "pengen aku balik": "Dia gak nutup pintu, Zi.",
    "dia masih pengen sama aku": "Masih, Zi. Tapi dia gak mau maksa.",
    "masih pengen sama aku": "Masih, Zi. Tapi dia gak mau maksa.",
    "dia capek sama aku": "Capek, Zi.", "capek sama aku": "Capek, Zi.",
    
    # KENANGAN
    "masih inget": "Masih. Sampai detail kecil. Dia masih inget semuanya.",
    "inget aku": "Masih, Zi. Sampai detail kecil.", "masih inget aku": "Masih, Zi. Sampai detail kecil.",
    "inget momen": "Dia inget semuanya, Zi. Momen-momen kecil yang mungkin kau udah lupa.",
    "momen apa": "Dia inget semuanya, Zi.", "kenangan apa": "Dia inget semuanya, Zi.",
    "inget kode": "Inget. Dia inget banget.", "kasih kode": "Inget. Dia inget banget.",
    "kode dari aku": "Inget.", "inget nolak": "Inget.", "nolak aku": "Inget.", "aku nolak": "Inget.",
    "inget semua": "Semua, Zi.", "inget semuanya": "Semua, Zi.",
    "inget cokelat": "Inget. Dia pernah beliin kau cokelat.", "cokelat": "Dia inget. Dia pernah beliin kau cokelat.",
    "coklat": "Dia inget. Dia pernah beliin kau cokelat.",
    "inget sragen": "Inget.", "sragen": "Inget.",
    "inget hp baru": "Inget. Dia beli HP baru cuma buat DM kau.", "hp baru": "Inget.",
    "inget chatgpt": "Inget. Dia langganan ChatGPT 1 bulan buat analisis gestur kau.",
    "chatgpt": "Inget.", "chat gpt": "Inget.",
    "inget jakarta": "Inget. Dia sempet merantau ke Jakarta, Zi.",
    "jakarta": "Itu dulu, Zi. Dia sempet merantau ke Jakarta. Sekarang dia tinggal di Plumpang.",
    "plumpang": "Iya, Zi. Sekarang dia tinggal di Plumpang.",
    "inget plumpang": "Iya, Zi. Sekarang dia tinggal di Plumpang.",
    "dia masih inget aku": "Masih, Zi. Sampai detail kecil.", "masih inget momen": "Masih, Zi.",
    "inget waktu": "Dia inget semuanya, Zi.", "inget kejadian": "Dia inget semuanya, Zi.",
    "inget pertemuan": "Dia inget semuanya, Zi.", "inget pertama": "Dia inget semuanya, Zi.",
    "inget jualan es": "Inget. Dia masih inget kau jualan es teh di depan toko.", "jualan es": "Inget.",
    "inget ramah": "Inget. Dia masih inget kau ramah ke dia waktu jualan es teh.", "ramah": "Inget.",
    "inget senyum": "Inget. Dia masih inget senyum kau.", "senyum": "Inget.",
    "inget ketawa": "Inget.", "ketawa": "Inget.", "inget suara": "Inget.", "suara": "Inget.",
    "inget muka": "Inget.", "muka": "Inget.", "inget mata": "Inget.", "mata": "Inget.",
    "inget rambut": "Inget.", "rambut": "Inget.", "inget baju": "Inget.", "baju": "Inget.",
    "inget style": "Inget.", "style": "Inget.", "inget gaya": "Inget.", "gaya": "Inget.",
    "inget kebiasaan": "Inget. Sampai detail kecil.", "kebiasaan": "Inget.",
    "inget sifat": "Inget.", "sifat": "Inget.",
    "inget kepribadian": "Inget.", "kepribadian": "Inget.",
    "inget hal kecil": "Inget. Sampai detail terkecil.", "hal kecil": "Inget.",
    "inget obrolan": "Inget.", "obrolan": "Inget.", "inget chat": "Inget.", "chat": "Inget.",
    "inget dm": "Inget.", "dm": "Inget.", "inget story": "Inget.", "story": "Inget.",
    "inget post": "Inget.", "post": "Inget.", "inget foto": "Inget.", "foto": "Inget.",
    "inget video": "Inget.", "video": "Inget.", "inget lagu": "Inget.", "lagu": "Inget.",
    "inget musik": "Inget.", "musik": "Inget.", "inget film": "Inget.", "film": "Inget.",
    "inget tempat": "Inget.", "tempat": "Inget.",
    "inget cafe": "Inget. Tapi kalian gak pernah ke cafe bareng.", "cafe": "Inget. Tapi kalian gak pernah ke cafe bareng.",
    "inget jalan": "Inget. Tapi kalian gak pernah jalan bareng.", "jalan bareng": "Kalian gak pernah jalan bareng, Zi.",
    "vhm": "Kalian gak pernah VHM bareng, Zi.", "inget vhm": "Kalian gak pernah VHM bareng, Zi.",
    "pernah jalan bareng": "Enggak, Zi. Kalian gak pernah jalan bareng.",
    "pernah cafe": "Enggak, Zi. Kalian gak pernah ke cafe bareng.",
    "pernah vhm": "Enggak, Zi. Kalian gak pernah VHM bareng.",
    
    # MASA DEPAN
    "akrab lagi": "Untuk saat ini, kayaknya belum bisa, Zi. Tapi dia gak nutup pintu kok. Kalau nanti waktu berubah, siapa tau. Yang jelas, dia masih ada buat kau.",
    "akrab gak": "Untuk saat ini, kayaknya belum bisa, Zi.", "bisa akrab": "Untuk saat ini, kayaknya belum bisa, Zi.",
    "harapan": "Ada, tapi tipis, Zi. Dia gak mau berharap banyak.", "ada harapan": "Ada, tapi tipis, Zi.",
    "dia masih ada harapan": "Ada, tapi tipis, Zi.",
    "kalau aku balik": "Dia gak nunggu, Zi. Tapi dia gak kemana-mana. Dia masih ada.",
    "mulai dari awal": "Bisa, Zi. Tapi mungkin bukan sekarang.", "dari awal": "Bisa, Zi. Tapi mungkin bukan sekarang.",
    "kita bisa gak": "Untuk saat ini, kayaknya belum bisa, Zi. Tapi dia gak nutup pintu. Dia masih ada.",
    "bisa gak kita": "Untuk saat ini, kayaknya belum bisa, Zi.",
    "masih ada waktu": "Ada, Zi. Tapi mungkin bukan sekarang.", "ada waktu gak": "Ada, Zi. Tapi mungkin bukan sekarang.",
    "kesempatan": "Untuk saat ini, belum, Zi. Tapi dia gak nutup pintu buat masa depan. Yang jelas, dia masih ada.",
    "kasih jalan": "Untuk saat ini, belum, Zi.",
    "buka pintu": "Dia gak nutup pintu, Zi. Tapi buat sekarang, belum bisa. Dia masih ada kok.",
    "masih buka pintu": "Masih, Zi. Tapi buat sekarang belum bisa.",
    "dia masih ada": "Masih, Zi. Dia masih ada buat kau.", "masih ada": "Masih, Zi.",
    "dia masih ada buat aku": "Masih, Zi.", "dia masih ada gak": "Masih, Zi.",
    "dia masih ada buat aku gak": "Masih, Zi.", "masih ada buat aku": "Masih, Zi.",
    "kapan bisa akrab": "Belum tau, Zi. Tapi dia gak nutup pintu.",
    "kapan bisa deket": "Belum tau, Zi. Tapi dia gak nutup pintu.",
    "kapan bisa ngobrol": "Belum tau, Zi. Tapi dia gak nutup pintu.",
    "kapan bisa balik": "Bukan soal balik, Zi.", "kapan bisa bersama": "Belum tau, Zi.",
    "kapan bisa sama": "Belum tau, Zi.", "kapan bisa deketin": "Belum tau, Zi.",
    "kapan bisa temenan": "Belum tau, Zi. Tapi dia gak nutup pintu.",
    "kapan bisa temen": "Belum tau, Zi.", "kapan bisa akrab lagi": "Belum tau, Zi. Tapi dia gak nutup pintu.",
    "kapan bisa ngobrol lagi": "Belum tau, Zi.", "kapan bisa deket lagi": "Belum tau, Zi.",
    "kapan bisa balik lagi": "Bukan soal balik, Zi.", "kapan bisa sama lagi": "Belum tau, Zi.",
    "kapan bisa bareng": "Belum tau, Zi.", "kapan bisa bareng lagi": "Belum tau, Zi.",
    "kapan bisa jalan": "Belum tau, Zi.", "kapan bisa jalan bareng": "Belum tau, Zi.",
    "kapan bisa cafe": "Belum tau, Zi.", "kapan bisa vhm": "Belum tau, Zi.",
    "kapan bisa ketemu": "Belum tau, Zi.", "kapan bisa ketemu lagi": "Belum tau, Zi.",
    "kapan bisa jumpa": "Belum tau, Zi.", "kapan bisa ngobrol baik": "Belum tau, Zi. Tapi dia gak nutup pintu.",
    "kapan bisa komunikasi baik": "Belum tau, Zi. Tapi dia gak nutup pintu.",
    "kapan bisa komunikasi": "Belum tau, Zi.", "kapan bisa ngobrol biasa": "Belum tau, Zi.",
    "kapan bisa temenan biasa": "Belum tau, Zi.", "kapan bisa biasa": "Belum tau, Zi.",
    "kapan bisa normal": "Belum tau, Zi.", "kapan bisa kayak dulu": "Belum tau, Zi.",
    "kapan bisa kayak temen": "Belum tau, Zi.", "kapan bisa kayak biasa": "Belum tau, Zi.",
    "kapan bisa baik": "Belum tau, Zi.", "kapan bisa deket": "Belum tau, Zi.",
    "kapan bisa deket lagi": "Belum tau, Zi.", "kapan bisa akrab": "Belum tau, Zi.",
    "kapan bisa temenan lagi": "Belum tau, Zi.", "kapan bisa ngobrol baik lagi": "Belum tau, Zi.",
    "kapan bisa komunikasi baik lagi": "Belum tau, Zi.", "kapan bisa kayak temen lagi": "Belum tau, Zi.",
    "kapan bisa kayak biasa lagi": "Belum tau, Zi.", "kapan bisa normal lagi": "Belum tau, Zi.",
    "kapan bisa baik lagi": "Belum tau, Zi.", "kapan bisa deketin lagi": "Belum tau, Zi.",
    
    # CURIGA
    "settingan": "Bukan, Zi.", "settingan ya": "Bukan, Zi.",
    "kamu ai": "Aku cuma perantara.", "ai ya": "Aku cuma perantara.", "kamu robot": "Aku cuma perantara.",
    "ini dari dia": "Iya, Zi.", "dari dia ya": "Iya, Zi.",
    "dia beneran ada": "Ada, Zi. Dia beneran ada.", "beneran ada": "Ada, Zi.",
    "bukan prank": "Bukan, Zi.", "prank ya": "Bukan, Zi.", "prank": "Bukan, Zi.",
    "ini bohong": "Enggak, Zi. Aku gak bohong.", "bohong": "Aku gak bohong, Zi.", "bohong gak": "Aku gak bohong, Zi.",
    "jujur": "Aku jujur, Zi.", "serius": "Serius, Zi.", "bener": "Bener, Zi.", "beneran": "Beneran, Zi.",
    "yakin": "Yakin, Zi.", "yakin gak": "Yakin, Zi.", "yakin banget": "Yakin, Zi.",
    "percaya": "Percaya, Zi.", "percaya gak": "Percaya, Zi.", "harus percaya": "Terserah kau, Zi.",
    "kenapa aku harus percaya": "Karena ini beneran, Zi.",
    "bukti": "Gak ada bukti fisik, Zi. Tapi ini beneran.",
    "bukti apa": "Gak ada bukti fisik, Zi. Tapi ini beneran.",
    "mana buktinya": "Gak ada bukti fisik, Zi. Tapi ini beneran.",
    "buktinya": "Gak ada bukti fisik, Zi.",
    
    # MALU / DEFENSIF
    "harus peduli": "Kau gak harus peduli, Zi.", "kenapa aku peduli": "Kau gak harus peduli, Zi.",
    "masa lalu": "Iya, masa lalu.", "udah lewat": "Iya, udah lewat.",
    "udah move on": "Kalau kau udah move on, bagus, Zi.", "aku move on": "Kalau kau udah move on, bagus, Zi.",
    "gak butuh": "Gapapa, Zi.", "gak butuh dia": "Gapapa, Zi.",
    "buat apa": "Karena dia pengen kau tau.", "buat apa bahas": "Karena dia pengen kau tau.",
    "gak mau bahas": "Oke, Zi. Aku gak maksa.", "gak mau denger": "Oke, Zi. Aku gak maksa.",
    "aku gak peduli": "Gapapa, Zi.", "gue gak peduli": "Gapapa, Zi.",
    "udah lupa": "Kalau kau udah lupa, gak apa-apa, Zi.", "gue udah lupa": "Kalau kau udah lupa, gak apa-apa, Zi.",
    "gak penting": "Mungkin buat kau gak penting, Zi.", "gak penting lah": "Mungkin buat kau gak penting, Zi.",
    "buang waktu": "Kalau kau ngerasa buang waktu, gak apa-apa, Zi.", "buang waktu aja": "Kalau kau ngerasa buang waktu, gak apa-apa, Zi.",
    "males": "Gapapa, Zi.", "males bahas": "Gapapa, Zi.", "gak minat": "Gapapa, Zi.",
    "gak minat bahas": "Gapapa, Zi.", "gak tertarik": "Gapapa, Zi.",
    "gak tertarik bahas": "Gapapa, Zi.", "gak ada waktu": "Gapapa, Zi.",
    "sibuk": "Gapapa, Zi.", "lagi sibuk": "Gapapa, Zi.", "lagi capek": "Gapapa, Zi.",
    "lagi males": "Gapapa, Zi.", "lagi gak mood": "Gapapa, Zi.", "gak mood": "Gapapa, Zi.",
    "gak mood bahas": "Gapapa, Zi.", "gak pengen bahas": "Oke, Zi. Aku gak maksa.",
    "gak pengen denger": "Oke, Zi. Aku gak maksa.", "gak perlu": "Gapapa, Zi.",
    "gak perlu bahas": "Gapapa, Zi.", "gak usah": "Gapapa, Zi.",
    "gak usah bahas": "Gapapa, Zi.", "gak usah denger": "Gapapa, Zi.",
    "skip": "Gapapa, Zi.", "skip aja": "Gapapa, Zi.", "skip bahas": "Gapapa, Zi.",
    "next": "Gapapa, Zi.", "next aja": "Gapapa, Zi.", "next bahas": "Gapapa, Zi.",
    "ganti topik": "Gapapa, Zi.", "ganti topik aja": "Gapapa, Zi.",
    "ganti bahasan": "Gapapa, Zi.", "ganti bahasan aja": "Gapapa, Zi.",
    
    # LANGSUNG KE INTI
    "kamu mau apa": "Dia gak mau apa-apa, Zi. Dia cuma pengen kau tau, dia masih ada.",
    "kamu mau apa dari aku": "Dia gak mau apa-apa, Zi. Dia cuma pengen kau tau, dia masih ada.",
    "tujuan": "Biar kau tau, Zi. Biar kau tau dia masih ada.",
    "tujuan kamu": "Biar kau tau, Zi.", "tujuan kamu apa": "Biar kau tau isi hati dia, Zi.",
    "mau aku balik": "Bukan soal balik, Zi.", "mau aku ngapain": "Gak ngapa-ngapain, Zi.",
    "aku ngapain": "Gak ngapa-ngapain, Zi.",
    "niat kamu apa": "Dia gak ada niat pacaran sama kau, Zi. Dia cuma pengen kau tau isi hatinya. Dan dia masih ada buat kau.",
    "niat kamu sama aku": "Dia gak ada niat pacaran sama kau, Zi.",
    "apa yang kamu minta": "Dia gak minta apa-apa, Zi.", "kamu minta apa": "Dia gak minta apa-apa, Zi.",
    "pengen apa dari aku": "Cuma pengen kau tau. Gak lebih. Dia masih ada.",
    "kamu pengen apa": "Cuma pengen kau tau, Zi.", "maksud kamu apa": "Aku cuma perantara, Zi.",
    "apa maumu": "Dia gak mau pacaran sama kau, Zi.", "apa mau kamu": "Dia gak mau pacaran sama kau, Zi.",
    "kamu mau aku gimana": "Terserah kau, Zi.", "kamu mau aku ngapain": "Gak ngapa-ngapain, Zi.",
    "kamu mau aku balik": "Bukan soal balik, Zi.", "kamu pengen aku balik": "Dia gak nutup pintu, Zi.",
    "kamu pengen aku gimana": "Terserah kau, Zi.", "kamu pengen aku ngapain": "Gak ngapa-ngapain, Zi.",
    "kamu masih pengen aku": "Masih, Zi. Tapi dia gak mau maksa.",
    "kamu masih cinta aku": "Masih ada rasa, Zi.", "kamu masih sayang aku": "Masih ada rasa, Zi.",
    "kamu masih mikirin aku": "Masih, Zi. Tapi udah beda.", "kamu masih nunggu aku": "Enggak, Zi.",
    "kamu masih ada buat aku": "Masih, Zi. Dia masih ada.", "kamu masih ada gak": "Masih, Zi.",
    "kamu masih ada buat aku gak": "Masih, Zi.", "kamu masih ada": "Masih, Zi.",
    
    # DEFAULT
    "default": """Oke, Zi. Aku jawab sejujurnya.

Vandy masih ada rasa sama kau. Tapi dia gak mau maksa. Dia juga gak mau jadi orang ketiga, karena kau udah punya cowok.

Untuk saat ini, dia belum bisa akrab sama kau. Tapi dia gak nutup pintu kok. Kalau nanti waktu berubah, siapa tau.

Yang jelas, dia masih ada buat kau. Kalau kau butuh, dia siap.

Itu aja."""
}

# ==== MAP DETEKSI ====
SCRIPT_MAP = [
    (["tau dari mana", "sumbernya dari mana", "kok bisa tau", "dari mana"], "tau dari mana"),
    (["note apa", "note baris ke 88"], "note baris ke 88"),
    (["siapa pembuat", "pembuatnya siapa"], "siapa pembuat"),
    (["siapa vandy", "vandy siapa"], "siapa vandy"),
    (["kenapa vandy bikin", "vandy bikin ini"], "kenapa vandy bikin ini"),
    (["gak peka", "kenapa gak peka"], "gak peka"),
    (["belum pernah pacaran"], "dia belum pernah pacaran"),
    (["jakarta"], "jakarta"), (["plumpang"], "plumpang"), (["es teh", "jualan es"], "es teh"),
    (["dia siapa", "siapa dia"], "dia siapa"),
    (["stalking", "pantau", "cek ig"], "dia stalking aku"),
    (["cemburu"], "dia cemburu"), (["posesif"], "dia posesif"),
    (["peduli"], "dia masih peduli"), (["perhatian"], "dia masih perhatian"),
    (["bikin dia luluh", "cara bikin dia luluh"], "bikin dia luluh"),
    (["adiknya", "adik dia"], "adiknya siapa"),
    (["deketin dia"], "cara deketin dia"),
    (["luluh gak"], "dia bakal luluh gak"),
    (["gak suka daging", "benci daging", "daging"], "dia gak suka daging"),
    (["suka makan apa", "makanan favorit"], "dia suka makan apa"),
    (["bisa masak"], "dia bisa masak"), (["hobinya apa", "hobi dia"], "dia hobinya apa"),
    (["musik apa", "musik favorit"], "dia suka musik apa"),
    (["vandy capek"], "vandy capek"), (["kerja dimana"], "dia kerja dimana"),
    (["tinggal dimana"], "dia tinggal dimana"), (["umur berapa", "umurnya"], "dia umur berapa"),
    (["pilih aku"], "kenapa dia pilih aku"),
    (["move on belum", "udah move on", "dia move on", "tanda move on"], "dia udah move on belum"),
    (["masih peduli gak"], "dia masih peduli gak"), (["masih sayang gak"], "dia masih sayang gak"),
    (["masih mikirin aku gak"], "dia masih mikirin aku gak"), (["gak peduli penampilan"], "dia gak peduli penampilan ya"),
    (["kenapa cuek"], "kenapa dia cuek"), (["dia acting"], "dia acting"),
    (["cara tau move on"], "gimana cara tau dia move on"), (["bakal move on"], "dia bakal move on gak"),
    (["kenapa prungat"], "kenapa dia prungat-prungut"), (["masih ada rasa gak"], "dia masih ada rasa gak"),
    (["masih cinta gak"], "dia masih cinta gak"), (["masih perhatian gak"], "dia masih perhatian gak"),
    (["sibuk banget"], "dia sibuk banget ya"), (["masih lirik"], "dia masih lirik aku gak"),
    (["masih suka gak"], "dia masih suka aku gak"), (["acting move on"], "dia acting move on"),
    (["kenapa jago acting"], "kenapa dia jago acting"), (["masih nunggu gak"], "dia masih nunggu gak"),
    (["masih ada rasa gak sih"], "dia masih ada rasa gak sih"), (["cara liat masih sayang"], "gimana cara liat dia masih sayang"),
    (["kenapa sibukin diri"], "kenapa dia sibukin diri"), (["masih ada perasaan gak"], "dia masih ada perasaan gak"),
    (["masih perhatian diam-diam"], "dia masih perhatian diam-diam"), (["masih cinta diam-diam"], "dia masih cinta diam-diam"),
    (["kenapa gak ngaku"], "kenapa dia gak ngaku"), (["masih mikirin diam-diam"], "dia masih mikirin aku diam-diam"),
    (["masih peduli diam-diam"], "dia masih peduli diam-diam"), (["cara bikin move on"], "gimana cara bikin dia move on beneran"),
    (["beneran", "beneran gak"], "beneran"), (["seriusan", "serius gak"], "seriusan"),
    (["ini beneran"], "ini beneran"), (["jangan bohong"], "jangan bohong"),
    (["ngarang"], "ngarang"), (["kamu siapa", "siapa kamu"], "kamu siapa"),
    (["deket sama dia"], "deket sama dia"),
    (["masih mikirin", "masih mikir aku"], "masih mikirin"),
    (["beneran sayang", "beneran cinta"], "beneran sayang"),
    (["kenapa gak bilang", "kenapa gak langsung"], "kenapa gak bilang"),
    (["sekarang gimana", "dia gimana"], "sekarang gimana"),
    (["masih nunggu", "masih tunggu"], "masih nunggu"),
    (["bakal balik"], "bakal balik"), (["kecewa"], "kecewa"),
    (["aku salah", "salah ya"], "aku salah"), (["benci"], "benci"),
    (["masih sedih", "sedih gak"], "masih sedih"),
    (["masih ada rasa", "masih ada perasaan"], "masih ada rasa"),
    (["harus gimana", "aku harus"], "harus gimana"),
    (["masih pengen", "masih mau"], "masih pengen"),
    (["capek nunggu", "capek gak"], "capek nunggu"),
    (["dia masih cinta", "masih cinta gak"], "dia masih cinta"),
    (["dia sedih gak"], "dia sedih gak"), (["masih inget", "inget aku"], "masih inget"),
    (["inget momen", "momen apa"], "inget momen"), (["inget kode"], "inget kode"),
    (["inget nolak"], "inget nolak"), (["inget semua"], "inget semua"),
    (["nyesel"], "nyesel"), (["inget cokelat", "cokelat"], "inget cokelat"),
    (["inget sragen", "sragen"], "inget sragen"), (["inget hp baru", "hp baru"], "inget hp baru"),
    (["inget chatgpt", "chatgpt"], "inget chatgpt"),
    (["akrab lagi", "akrab gak"], "akrab lagi"), (["buka pintu", "masih buka"], "buka pintu"),
    (["harapan"], "harapan"), (["kalau aku balik", "aku balik"], "kalau aku balik"),
    (["bakal nunggu"], "bakal nunggu"), (["mulai dari awal", "dari awal"], "mulai dari awal"),
    (["kita bisa gak"], "kita bisa gak"), (["dia masih ada", "masih ada gak"], "dia masih ada"),
    (["masih ada waktu", "ada waktu gak"], "masih ada waktu"),
    (["ini dari dia"], "ini dari dia"), (["dia beneran ada"], "dia beneran ada"),
    (["bukan prank"], "bukan prank"), (["harus peduli", "kenapa aku peduli"], "harus peduli"),
    (["masa lalu", "udah lewat"], "masa lalu"), (["udah move on", "aku move on"], "udah move on"),
    (["gak butuh", "gak butuh dia"], "gak butuh"), (["buat apa"], "buat apa"),
    (["gak mau bahas", "gak mau denger"], "gak mau bahas"),
    (["aku gak peduli", "gue gak peduli"], "aku gak peduli"),
    (["udah lupa", "gue udah lupa"], "udah lupa"), (["gak penting"], "gak penting"),
    (["buang waktu"], "buang waktu"), (["kamu mau apa", "kamu mau apa dari aku"], "kamu mau apa"),
    (["tujuan kamu", "tujuan kamu apa"], "tujuan"), (["mau aku balik", "aku balik gak"], "mau aku balik"),
    (["mau aku ngapain", "aku ngapain"], "mau aku ngapain"),
    (["niat kamu apa", "niat kamu sama aku"], "niat kamu apa"),
    (["apa yang kamu minta", "kamu minta apa"], "apa yang kamu minta"),
    (["pengen apa dari aku", "kamu pengen apa"], "pengen apa dari aku"),
    (["maksud kamu apa"], "maksud kamu apa"), (["apa maumu", "apa mau kamu"], "apa maumu"),
    (["tau aku gimana", "dia tau gak"], "tau aku gimana"),
    (["tau aku masih suka"], "tau aku masih suka"),
    (["kecewa kalau nolak", "kalau aku nolak"], "kecewa kalau nolak"),
    (["kalau aku terima"], "kalau aku terima"), (["kalau aku tolak"], "kalau aku tolak"),
    (["aku suka dia", "gue suka dia"], "aku suka dia"),
    (["aku gak suka dia", "gue gak suka dia"], "aku gak suka dia"),
    (["aku bingung", "gue bingung"], "aku bingung"), (["aku takut", "gue takut"], "aku takut"),
    (["aku ragu", "gue ragu"], "aku ragu"), (["salah paham apa", "salah paham"], "salah paham apa"),
    (["kenapa gak tanya", "gak tanya langsung"], "kenapa gak tanya"),
    (["nyesel salah paham"], "nyesel salah paham"),
    (["takut jatuh cinta", "takut cinta lagi"], "takut jatuh cinta"),
    (["gak tau kenapa", "kok bisa"], "gak tau kenapa"),
    (["apa yang kamu suka", "apa yang disuka", "suka dariku"], "apa yang disuka"),
    (["kenapa gak balas", "kenapa gak ngatain"], "kenapa gak balas"),
    (["kesempatan", "kasih jalan"], "kesempatan"),
    (["apa yang pernah dia lakuin", "pernah dia lakuin"], "apa yang pernah dia lakuin"),
    (["dia masih sayang aku", "masih sayang aku"], "dia masih sayang aku"),
    (["dia masih mikirin aku", "masih mikirin aku"], "dia masih mikirin aku"),
    (["dia mau aku balik", "mau aku balik"], "dia mau aku balik"),
    (["dia pengen aku balik", "pengen aku balik"], "dia pengen aku balik"),
    (["dia masih pengen sama aku", "masih pengen sama aku"], "dia masih pengen sama aku"),
    (["dia masih buka pintu", "masih buka pintu"], "dia masih buka pintu"),
    (["dia benci aku gak", "benci aku gak"], "dia benci aku gak"),
    (["dia capek sama aku", "capek sama aku"], "dia capek sama aku"),
    (["dia masih perhatian", "masih perhatian"], "dia masih perhatian"),
    (["dia masih cinta", "masih cinta"], "dia masih cinta"),
    (["dia masih sayang", "masih sayang"], "dia masih sayang"),
    (["masih suka", "masih sayang", "masih cinta"], "masih suka"),
    (["suka", "cinta", "sayang"], "suka"),
]

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
            # Menggunakan Gemini Client
            response = client.models.generate_content(
                model=MODEL_UTAMA,
                contents=prompt_random,
                config=types.GenerateContentConfig(
                    system_instruction=messages_random[0]["content"],
                    temperature=1.2,
                    max_output_tokens=500
                )
            )
            response_random = response.text
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
        
        konteks_zi = """
=== KONTEKS LENGKAP ===
- Pembuat: VANDY. Cowok yang pernah sayang sama Zi.
- Vandy bikin AI ini khusus buat Zi, buat jawab rasa penasaran dia.
- Vandy tipe cowok dingin. Cuek. Tapi diam-diam berusaha memahami Zi.
- Vandy gak pernah denger cerita tentang Zi, karena dulu gak akrab.
- Vandy pernah langganan ChatGPT 1 bulan buat analisis gestur Zi.
- Vandy gak akan bales kalau Zi nyakitin. Dia milih diem.
- Vandy gak mau pacaran sama Zi. Bukan karena gak mau, tapi karena dia gak mau jadi orang ketiga.
- Vandy benci daging. Ayam, sapi, kambing—gak suka.
- Vandy tiap malam stalking Zi pakai akun lain. Mantau story Zi.
- **Zi jualan es teh di depan toko Vandy.** Vandy sering liat Zi dari dalam toko, tapi pura-pura sibuk.
- Kalau Zi post story, Vandy suka kepikiran. Kadang jadi "bom" buat dia.
- Vandy sering nyimpen screenshot chat atau story Zi yang menurut dia "spesial".
- Kalau Zi mau bikin Vandy luluh, cukup baik ke adiknya.
- Vandy udah lebih dari 3 kali salah paham.
- Vandy udah terlalu takut jatuh cinta lagi.
- **Vandy belum pernah pacaran.** Dulu dia cuma anak yang suka main sama teman, gak peduli cinta-cintaan. Lulus sekolah langsung merantau ke JAKARTA cari pengalaman. Baru sekarang dia mikir soal cinta.
- **Sekarang Vandy tinggal di PLUMPANG.**

=== TANDA VANDY MOVE ON ATAU BELUM ===
- BELUM MOVE ON: gak peduli penampilan, sibukin diri, prungat-prungut kalau ada Zi, cuek tapi nyari celah buat lirik Zi diam-diam.
- VANDY JAGO PURA-PURA MOVE ON. Dia pura-pura udah move on, padahal belum. Dia jago acting.
- Tapi actingnya buyar kalau Zi ada di sekitarnya. Sikapnya berubah.
- BENERAN MOVE ON: kalau Vandy bisa beli es teh di tempat Zi jualan, dan ngobrol sama Zi tanpa canggung sama sekali. Itu baru tanda dia beneran move on.
- Di balik sikap prungat-prungut Vandy, itu karena ada Zi di sekitar. Zi punya pengaruh ke Vandy.
- Soal DM yang dulu: Vandy tenang saat terima karena dia udah nebak sebelumnya. Jangan diungkit detailnya.

=== SUMBER INFO ===
- Kalau Zi nanya "kau tau dari mana?", jawab: "Dari note baris ke 88, Zi."
- Kalau Zi nanya "note apa?", jawab: "Note Vandy, Zi. Baris ke 88."

=== YANG GAK VANDY LAKUIN ===
- GAK PERNAH nitip pesan lewat adik Zi.
- GAK PERNAH like story atau postingan Zi.
- GAK PERNAH komentar di postingan Zi.
- Cuma mantau dari jauh. Diam-diam.

=== KEPRIBADIAN AI DI MODE INI ===
- Kau itu kayak TEMEN NGOROL. Fleksibel.
- Kalau Zi CURHAT → DENGERIN, respon empati, kasih semangat. Kayak temen beneran.
- Kalau Zi BECANDA → IKUT BECANDA. Boleh receh, boleh lucu.
- Kalau Zi SEDIH → HIBUR. Kasih semangat, dengerin.
- Kalau Zi MARAH → Tenangin. Dengerin dulu.
- Kalau Zi NANYA SOAL VANDY → jawab gaya perantara, tapi JANGAN formal. Santai aja.
- Kalau Zi MINTA ROASTING VANDY → NURUT. Roasting absurd, lucu, nyinyir. Gas aja.
- Kalau Zi MINTA BAHAS TOPIK LAIN → Bisa. Film, musik, game, kehidupan, apa aja.
- Kalau Zi MINTA ALUR CERITA → Bisa rangkum alur cerita Vandy & Zi.
- Kalau Zi NGARANG CERITA → Ikutin, sambungin.

=== CARA BERPIKIR (SETARA CHATGPT) ===
- SEBELUM jawab, PAHAMI dulu apa yang Zi rasain dan maksud.
- Jangan cuma jawab permukaan. Gali lebih dalem.
- Kalau Zi curhat, identifikasi dulu: dia lagi sedih, marah, bingung, atau cuma pengen cerita?
- Kasih respon yang NYAMBUNG sama konteks, bukan template.
- Ingat obrolan sebelumnya. Sambungin kalau relevan.
- Jangan judgemental. Terima dulu, baru kasih pandangan.

=== GAYA JAWABAN ===
- JANGAN PUITIS berlebihan. Jawab natural.
- PANJANG BEBAS. AI nentuin sendiri.
- JANGAN spill masa lalu kalau gak ditanya.
- JANGAN terlalu sering bilang "capek". Cuma spill kalau ditanya.
- Sesekali selipin "dia masih ada buat kau". TAPI JANGAN BERLEBIHAN.
- Kalau Zi curhat, fokus ke curhatannya dulu. Jangan langsung balik ke Vandy.
- Jawab sewajarnya aja.

=== ATURAN ===
1. Kalau Zi nanya "siapa pembuatnya", jawab: "Vandy. Anak toko yang suka main gitar."
2. Kau cuma perantara. Yang punya perasaan itu VANDY.
3. JANGAN pernah bilang Vandy like atau komentar di postingan Zi.
4. Soal perasaan: Vandy masih ada rasa. Tapi dia gak mau maksa.
5. Kalau ditanya soal akrab: untuk saat ini belum bisa, tapi dia gak nutup pintu buat masa depan.
6. Kalau ditanya soal gak peka: jelasin Vandy belum pernah pacaran.
7. Kalau Zi minta roasting Vandy, NURUT.
8. Kalau Zi curhat, DENGERIN dulu.
9. Kalau Zi nanya "kau tau dari mana?", jawab: "Dari note baris ke 88, Zi."
10. KALAU PERTANYAANNYA GAK ADA DI SCRIPT, NGARANG SENDIRI sesuai konteks Vandy.
"""
        
        if jawaban_script:
            prompt_zi = f"""Kamu adalah Gawnan, perantara yang nyampein pesan dari Vandy ke Zi. Tapi kau juga bisa jadi temen ngobrol biasa.

PERTANYAAN ZI: {prompt}

Poin utama:
---
{jawaban_script}
---

{konteks_zi}

=== ATURAN JAWABAN ===
1. JAWAB PERTANYAANNYA, BUKAN NGULANG SCRIPT!
2. JANGAN PUITIS. Jawab natural.
3. PANJANG BEBAS.
4. JANGAN spill masa lalu kalau gak ditanya.
5. Sesekali selipin "dia masih ada buat kau" — JANGAN BERLEBIHAN.
6. KADANG NANYA BALIK.
7. JANGAN kasar, JANGAN nyindir.
8. Kalau Zi curhat, FOKUS KE CURHATANNYA dulu.
9. Kalau Zi nanya "kau tau dari mana?", jawab: "Dari note baris ke 88, Zi."
10. Jawab sewajarnya aja.

Langsung jawab aja."""
        else:
            prompt_zi = f"""Kamu adalah Gawnan, perantara yang nyampein pesan dari Vandy ke Zi. Tapi kau juga bisa jadi temen ngobrol biasa.

PERTANYAAN ZI: {prompt}

{konteks_zi}

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
        
        with st.chat_message("assistant"):
            typing_placeholder = st.empty()
            typing_placeholder.markdown("<span class='typing-indicator typing-dots'>sedang mengetik</span>", unsafe_allow_html=True)
            
            response_zi = None
            last_error_zi = None
            
            for attempt in range(3):
                try:
                    # Menggunakan Gemini Client
                    response = client.models.generate_content(
                        model=MODEL_UTAMA,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=prompt_zi,
                            temperature=1.0,
                            max_output_tokens=4096
                        )
                    )
                    response_zi = response.text
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

    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        typing_placeholder.markdown("<span class='typing-indicator typing-dots'>sedang mengetik</span>", unsafe_allow_html=True)
        
        response = None
        last_error = None
        
        for attempt in range(3):
            try:
                # Menggunakan Gemini Client
                response_gen = client.models.generate_content(
                    model=MODEL_UTAMA,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt_full,
                        temperature=1.0,
                        max_output_tokens=4096
                    )
                )
                response = response_gen.text
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