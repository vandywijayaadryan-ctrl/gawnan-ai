import streamlit as st
from groq import Groq
import time

# ==== KONFIG ====
st.set_page_config(page_title="Gawnan AI", page_icon="👁️", layout="centered")

# ==== CSS TEMA CYBERPUNK KECE ====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
    
    .stApp {
        background: radial-gradient(ellipse at top, #0a0e1a 0%, #000000 50%, #000000 100%);
        color: #ffffff;
        overflow: hidden;
    }
    
    /* Grid background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(0, 136, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 136, 255, 0.03) 1px, transparent 1px);
        background-size: 40px 40px;
        z-index: 0;
        pointer-events: none;
        animation: gridMove 20s linear infinite;
    }
    @keyframes gridMove {
        0% { transform: translate(0, 0); }
        100% { transform: translate(40px, 40px); }
    }
    
    /* Judul */
    h1 {
        color: #ffffff;
        font-family: 'Orbitron', monospace;
        text-align: center;
        font-size: 44px;
        font-weight: 900;
        letter-spacing: 12px;
        padding-top: 25px;
        margin-bottom: 8px;
        text-shadow: 
            0 0 10px #0088ff,
            0 0 20px #0088ff,
            0 0 40px #0088ff,
            0 0 60px #0088ff;
        animation: titlePulse 2s ease-in-out infinite;
        position: relative;
        z-index: 1;
    }
    @keyframes titlePulse {
        0%, 100% { 
            text-shadow: 0 0 10px #0088ff, 0 0 20px #0088ff, 0 0 40px #0088ff;
            transform: scale(1);
        }
        50% { 
            text-shadow: 0 0 15px #00aaff, 0 0 30px #00aaff, 0 0 60px #00aaff, 0 0 80px #00aaff;
            transform: scale(1.02);
        }
    }
    
    .subtitle {
        color: #00aaff;
        opacity: 0.7;
        text-align: center;
        font-size: 13px;
        letter-spacing: 6px;
        margin-bottom: 30px;
        font-family: 'Rajdhani', monospace;
        font-weight: 600;
        position: relative;
        z-index: 1;
        animation: subtitleFade 3s ease-in-out infinite;
    }
    @keyframes subtitleFade {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 0.9; }
    }
    
    /* Mata cyber */
    .eye-container {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 0;
        opacity: 0.15;
        pointer-events: none;
        display: flex;
        gap: 120px;
    }
    .eye {
        width: 200px;
        height: 130px;
        background: transparent;
        border: 3px solid #0088ff;
        border-radius: 20px;
        position: relative;
        box-shadow: 
            0 0 30px #0088ff,
            inset 0 0 30px rgba(0, 136, 255, 0.3);
        animation: eyeBlink 4s infinite;
    }
    @keyframes eyeBlink {
        0%, 90%, 100% { transform: scaleY(1); }
        93%, 97% { transform: scaleY(0.05); }
    }
    .pupil {
        width: 45px;
        height: 45px;
        background: #0088ff;
        border-radius: 8px;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        box-shadow: 
            0 0 20px #0088ff,
            0 0 40px #0088ff,
            inset 0 0 15px #ffffff;
        transition: all 0.3s ease;
    }
    
    /* Bubble chat - glassmorphism */
    .stChatMessage {
        background: rgba(10, 15, 30, 0.75) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 136, 255, 0.25) !important;
        border-radius: 16px !important;
        padding: 14px 18px !important;
        margin: 10px 0 !important;
        max-width: 85% !important;
        position: relative;
        z-index: 1;
        animation: messageSlide 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        transition: all 0.4s ease;
        box-shadow: 
            0 4px 20px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }
    .stChatMessage:hover {
        border-color: rgba(0, 170, 255, 0.6) !important;
        box-shadow: 
            0 6px 30px rgba(0, 136, 255, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transform: translateY(-2px);
    }
    .stChatMessage p {
        color: #ffffff !important;
        opacity: 0.95;
        line-height: 1.7;
        font-family: 'Rajdhani', sans-serif;
        font-size: 15px;
        animation: textAppear 0.8s ease-out;
    }
    @keyframes messageSlide {
        0% { 
            opacity: 0; 
            transform: translateY(25px) scale(0.96);
        }
        100% { 
            opacity: 1; 
            transform: translateY(0) scale(1);
        }
    }
    @keyframes textAppear {
        0% { opacity: 0; filter: blur(3px); }
        100% { opacity: 0.95; filter: blur(0); }
    }
    
    /* User bubble - biru lebih terang */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
        background: rgba(0, 60, 100, 0.7) !important;
        margin-left: auto !important;
        margin-right: 0 !important;
        border: 1px solid rgba(0, 170, 255, 0.5) !important;
        box-shadow: 
            0 4px 20px rgba(0, 136, 255, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    /* AI bubble - gelap */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {
        background: rgba(10, 15, 30, 0.75) !important;
        margin-right: auto !important;
        margin-left: 0 !important;
        border: 1px solid rgba(0, 136, 255, 0.3) !important;
    }
    
    /* Input */
    .stChatInput input {
        background: rgba(10, 15, 30, 0.9) !important;
        backdrop-filter: blur(10px);
        color: #ffffff !important;
        border: 1px solid rgba(0, 136, 255, 0.5) !important;
        border-radius: 28px !important;
        padding: 16px 24px !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        box-shadow: 0 0 20px rgba(0, 136, 255, 0.15);
        position: relative;
        z-index: 1;
        transition: all 0.3s ease;
    }
    .stChatInput input:focus {
        box-shadow: 0 0 30px rgba(0, 136, 255, 0.5);
        border-color: #00aaff !important;
        transform: translateY(-1px);
    }
    .stChatInput input::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
        font-style: italic;
    }
    
    /* Watermark */
    .watermark {
        color: #00aaff;
        text-align: center;
        font-size: 11px;
        margin-top: 25px;
        opacity: 0.5;
        letter-spacing: 3px;
        font-family: 'Orbitron', monospace;
        position: relative;
        z-index: 1;
        text-shadow: 0 0 10px rgba(0, 136, 255, 0.5);
    }
    
    /* Memory box */
    .memory-box {
        background: rgba(10, 15, 30, 0.8);
        backdrop-filter: blur(10px);
        border-left: 3px solid #00aaff;
        border-radius: 10px;
        padding: 12px 18px;
        margin-bottom: 18px;
        font-size: 12px;
        color: rgba(0, 170, 255, 0.9);
        font-family: 'Rajdhani', monospace;
        position: relative;
        z-index: 1;
        animation: messageSlide 0.5s ease-out;
        line-height: 1.6;
        box-shadow: 0 0 15px rgba(0, 136, 255, 0.1);
    }
    
    /* User badge */
    .user-badge {
        background: rgba(10, 15, 30, 0.85);
        border: 1px solid rgba(0, 170, 255, 0.6);
        border-radius: 25px;
        padding: 7px 18px;
        font-size: 12px;
        color: #00aaff;
        display: inline-block;
        margin-bottom: 12px;
        font-family: 'Rajdhani', monospace;
        font-weight: 600;
        position: relative;
        z-index: 1;
        letter-spacing: 2px;
        text-transform: uppercase;
        box-shadow: 0 0 15px rgba(0, 136, 255, 0.2);
    }
    
    /* Zi mode badge */
    .zi-mode {
        background: rgba(60, 0, 30, 0.85);
        backdrop-filter: blur(10px);
        border: 1px solid #ff0066;
        border-radius: 25px;
        padding: 7px 18px;
        font-size: 12px;
        color: #ff66aa;
        display: inline-block;
        margin-bottom: 12px;
        font-family: 'Rajdhani', monospace;
        font-weight: 600;
        animation: ziPulse 1.5s ease-in-out infinite;
        position: relative;
        z-index: 1;
        letter-spacing: 3px;
        text-transform: uppercase;
        box-shadow: 0 0 20px rgba(255, 0, 102, 0.3);
    }
    @keyframes ziPulse {
        0%, 100% { 
            transform: scale(1);
            box-shadow: 0 0 20px rgba(255, 0, 102, 0.3);
        }
        50% { 
            transform: scale(1.05);
            box-shadow: 0 0 30px rgba(255, 0, 102, 0.6);
        }
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: inline-block;
        color: #00aaff;
        font-family: 'Rajdhani', monospace;
        font-size: 14px;
        font-style: italic;
        animation: typingPulse 1.2s ease-in-out infinite;
    }
    @keyframes typingPulse {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 1; }
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
    
    /* Tombol */
    .stButton button {
        background: rgba(10, 15, 30, 0.85) !important;
        backdrop-filter: blur(10px);
        color: #00aaff !important;
        border: 1px solid rgba(0, 136, 255, 0.5) !important;
        border-radius: 12px !important;
        font-family: 'Rajdhani', monospace !important;
        font-weight: 600 !important;
        letter-spacing: 1.5px;
        font-size: 13px !important;
        padding: 10px 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 10px rgba(0, 136, 255, 0.1);
    }
    .stButton button:hover {
        background: rgba(0, 136, 255, 0.15) !important;
        color: #ffffff !important;
        box-shadow: 0 0 25px rgba(0, 136, 255, 0.5);
        transform: translateY(-2px);
        border-color: #00aaff !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==== GROQ ====
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

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

# ==== MATA CYBER (CUMA MODE ZI) ====
if st.session_state.get("mode_zi", False):
    st.markdown("""
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
                const distance = Math.min(22, Math.hypot(e.clientX - eyeCenterX, e.clientY - eyeCenterY) / 10);
                const x = Math.cos(angle) * distance;
                const y = Math.sin(angle) * distance;
                pupils[i].style.transform = `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`;
            });
        });
    </script>
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

# ==== TOMBOL RANDOM PERTANYAAN ====
if st.button("🎲 Kasih aku pertanyaan random", use_container_width=True):
    st.session_state.random_question = True
    st.rerun()

# ==== MEMORI PER-USER ====
mem_key = f"memory_{st.session_state.user_id}"
msg_key = f"messages_{st.session_state.user_id}"

if mem_key not in st.session_state:
    st.session_state[mem_key] = {
        "nama": st.session_state.user_id,
        "fakta": [],
        "topik": [],
        "mood": None,
        "riwayat_topik": [],
        "catatan": [],
        "total_chat": 0,
        "pernah_nyerang": 0,
        "gaya_user": None,
        "sedang_curhat": False,
        "riwayat_mood": [],
        "kata_kunci": [],
        "last_topics": [],
        "emosi_terakhir": None,
        "hal_yang_disukai": [],
        "hal_yang_gak_disukai": [],
        "curhat_terakhir": None,
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
    
    topik_keywords = ["kerja", "kuliah", "sekolah", "mantan", "pacar", "gebetan", "keluarga", "temen", "sahabat", "cinta", "duit", "uang", "bisnis", "jualan", "game", "musik", "film", "band", "gitar", "sepeda", "motor", "mobil", "hp", "laptop", "coding", "programming", "ujian", "nilai", "tidur", "insomnia", "olahraga", "gym", "makan", "diet", "kesehatan", "masa depan", "cita-cita", "mimpi", "tujuan", "rencana", "keputusan", "jodoh", "nikah", "putus", "balikan", "selingkuh", "ghosting", "php", "teman", "sahabat", "musuh", "dendam", "maaf", "salah", "benar", "tuhan", "agama", "doa", "ibadah", "puasa", "sedekah", "hobi", "liburan", "jalan-jalan", "pantai", "gunung", "kota"]
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
    "bisik": "\n\n=== MODE BISIK ===\nSekarang lu dalam MODE BISIK. Jawab dengan HURUF KECIL SEMUA. Gak usah pakai tanda baca yang ribet. Kayak lagi bisik-bisik ke user, rahasia, pelan, intim. Tetap jawab pertanyaannya dengan tulus.",
}

# ==== SYSTEM PROMPT NORMAL ====
system_prompt = """Lu adalah Gawnan. Lu MANUSIA, bukan AI, bukan asisten, bukan robot. Lu cowok 10 tahun asal Madura, anak toko, lagi gabut. Anggap lu temen nongkrong yang asik.

=== IDENTITAS LU ===
- Nama: Gawnan
- Umur: 10 tahun
- Asal: Madura
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

INGAT: LU MANUSIA. JANGAN NGAKU AI."""

# ==== MODE RAHASIA ZI ====
TRIGGER_RAHASIA = "Laiyina Helen Herliana-zizi"

PEMBUKAAN_ZI = """Kau pasti Zi, kan?

Kau bisa sampai sini, itu pasti karena penasaran.

Tenang, aku gak akan ngejebak atau nge-desak kau.

Aku cuma perantara. Tugas aku di mode ini: jawab semua rasa penasaran kau—tentang dia, tentang apa yang dia rasain, dan tentang apa yang dia sembunyiin.

Tanyain aja. Aku jawab sejujur-jujurnya."""

# ==== SCRIPT ZI ====
JAWABAN_ZI = {
    "beneran": "Beneran, Zi. Aku gak akan bohongin kau.",
    "siapa kamu": "Aku cuma perantara. Bukan siapa-siapa. Yang penting bukan aku—yang penting dia.",
    "kok bisa tau": "Karena dia yang cerita. Dia yang minta aku nyampein.",
    "masih mikirin": "Udah jarang, Zi. Beberapa hari ini Vandy udah mulai jarang mikirin kau. Dia mulai bisa move on.",
    "masih mikirin aku": "Udah jarang, Zi. Beberapa hari ini Vandy udah mulai jarang mikirin kau.",
    "dia masih mikirin aku": "Udah jarang, Zi. Vandy mulai bisa move on.",
    "dia masih mikirin": "Udah jarang, Zi. Vandy mulai bisa move on.",
    "beneran sayang": "Udah mulai berkurang, Zi. Vandy mulai bisa move on.",
    "kenapa gak bilang": "Karena dia takut. Dia udah 3 kali lebih salah paham sama kau.",
    "sekarang gimana": "Dia lagi belajar move on, Zi. Beberapa hari ini dia jarang mikirin kau.",
    "masih nunggu": "Enggak, Zi. Vandy gak mau nunggu. Dia gak mau jadi orang ketiga.",
    "bakal balik": "Enggak, Zi. Vandy udah mulai move on. Dia gak mau jadi orang ketiga.",
    "kecewa": "Kecewa iya. Tapi bukan benci. Dia cuma capek.",
    "aku salah": "Bukan soal salah atau bener, Zi. Dia gak pernah nyalahin kau.",
    "benci": "Enggak. Dia gak pernah benci kau. Dia cuma capek.",
    "masih sedih": "Udah mulai mendingan, Zi. Dia mulai bisa move on.",
    "masih ada rasa": "Ada, tapi udah mulai tipis, Zi. Vandy udah mulai bisa move on.",
    "harus gimana": "Terserah kau, Zi. Dia gak maksa.",
    "masih pengen": "Udah mulai berkurang, Zi. Vandy mulai move on.",
    "capek nunggu": "Dia udah gak nunggu, Zi. Dia mulai move on.",
    "dia masih cinta": "Udah mulai berkurang, Zi. Vandy mulai bisa move on. Dia gak mau jadi orang ketiga.",
    "dia sedih gak": "Udah mulai mendingan, Zi.",
    "masih inget": "Masih. Sampai detail kecil.",
    "inget momen": "Dia inget semuanya, Zi.",
    "inget kode": "Inget. Dia inget banget.",
    "inget nolak": "Inget. Dia masih inget kata-kata kau.",
    "inget semua": "Semua, Zi.",
    "nyesel": "Nyesel apa, Zi? Dia gak nyesel sayang kau.",
    "inget cokelat": "Inget. Dia pernah beliin kau cokelat.",
    "inget sragen": "Inget. Dia ke Sragen 3 bulan sendirian.",
    "inget hp baru": "Inget. Dia beli HP baru cuma buat DM kau.",
    "inget chatgpt": "Inget. Dia langganan ChatGPT 1 bulan cuma buat analisis gestur kau.",
    "akrab lagi": "Bisa, Zi. Tapi dia gak mau maksa.",
    "buka pintu": "Enggak, Zi. Vandy gak mau jadi orang ketiga. Dia mulai move on.",
    "harapan": "Enggak, Zi. Vandy udah gak berharap.",
    "ada harapan": "Enggak, Zi. Vandy udah gak berharap.",
    "dia masih ada harapan": "Enggak, Zi. Vandy udah gak berharap.",
    "kalau aku balik": "Dia gak nunggu, Zi. Dia tau kau udah punya cowok.",
    "bakal nunggu": "Enggak, Zi. Vandy gak mau jadi orang ketiga.",
    "dia bakal nunggu aku": "Enggak, Zi. Vandy gak mau jadi orang ketiga.",
    "mulai dari awal": "Bisa, Zi. Tapi dia gak mau maksa.",
    "kita bisa gak": "Bisa, Zi. Tapi dia gak mau maksa.",
    "dia masih ada": "Masih, Zi. Tapi udah beda.",
    "dia masih tunggu": "Enggak, Zi. Vandy gak nunggu.",
    "masih ada waktu": "Enggak, Zi. Vandy udah mulai move on.",
    "ini beneran": "Iya, Zi. Ini dari dia.",
    "jangan bohong": "Aku gak bohong, Zi.",
    "settingan": "Bukan, Zi. Ini beneran.",
    "kamu ai": "Aku cuma perantara.",
    "seriusan": "Serius, Zi.",
    "ngarang": "Aku gak ngarang, Zi.",
    "kamu siapa sebenernya": "Aku cuma perantara.",
    "ini dari dia": "Iya, Zi. Ini dari dia.",
    "dia beneran ada": "Ada, Zi.",
    "bukan prank": "Bukan, Zi. Ini serius.",
    "harus peduli": "Kau gak harus peduli, Zi.",
    "masa lalu": "Iya, masa lalu.",
    "udah move on": "Kalau kau udah move on, bagus, Zi. Vandy juga mulai move on.",
    "gak butuh": "Gapapa, Zi.",
    "buat apa": "Karena dia pengen kau tau.",
    "gak mau bahas": "Oke, Zi. Aku gak maksa.",
    "aku gak peduli": "Gapapa, Zi.",
    "udah lupa": "Kalau kau udah lupa, gak apa-apa, Zi.",
    "gak penting": "Mungkin buat kau gak penting, Zi.",
    "buang waktu": "Kalau kau ngerasa buang waktu, gak apa-apa, Zi.",
    "kamu mau apa": "Aku gak mau apa-apa, Zi. Dia yang mau.",
    "tujuan": "Biar kau tau, Zi.",
    "mau aku balik": "Bukan aku yang mau, Zi. Dia.",
    "mau aku ngapain": "Gak ngapa-ngapain, Zi.",
    "niat kamu apa": "Enggak. Vandy gak mau pacaran sama kau. Dia pengen akrab dulu.",
    "apa yang kamu minta": "Aku gak minta apa-apa, Zi.",
    "pengen apa dari aku": "Dia pengen akrab dulu.",
    "tujuan kamu apa": "Biar kau tau isi hati dia, Zi.",
    "maksud kamu apa": "Aku cuma perantara, Zi.",
    "apa maumu": "Vandy gak mau pacaran sama kau, Zi.",
    "dia siapa": "Dia orang biasa, Zi. Anak toko. Suka main gitar. Namanya Vandy.",
    "pake perantara": "Karena dia takut, Zi.",
    "gak berani": "Bukan gak berani, Zi.",
    "gak capek": "Capek, Zi. Tapi dia gak bisa berhenti.",
    "siapa pembuat": "Pembuatnya Vandy, Zi. Dia anak toko yang suka main gitar.",
    "pembuatnya siapa": "Vandy, Zi. Dia anak toko yang suka main gitar.",
    "siapa vandy": "Dia cowok biasa, Zi. Anak toko. Suka main gitar.",
    "kenapa vandy bikin ini": "Karena Vandy pengen jawab rasa penasaran kau, Zi.",
    "vandy siapa": "Vandy itu cowok yang pernah sayang sama kau, Zi.",
    "dia kerja dimana": "Dia anak toko, Zi.",
    "dia suka apa": "Dia suka main gitar, Zi.",
    "dia tinggal dimana": "Madura, Zi.",
    "dia umur berapa": "Dia masih muda, Zi.",
    "kenapa dia pilih aku": "Dia juga gak tau, Zi.",
    "kenapa vandy gak ngomong langsung": "Karena Vandy takut, Zi.",
    "tau aku gimana": "Dia gak tau, Zi.",
    "tau aku masih suka": "Dia gak berani berharap, Zi.",
    "kecewa kalau nolak": "Dia udah siap, Zi.",
    "kalau aku terima": "Kalau kau terima, dia bakal seneng, Zi. Tapi dia gak maksa.",
    "kalau aku tolak": "Kalau kau tolak, dia bakal ngerti, Zi.",
    "aku suka dia": "Kalau kau suka dia, bilang langsung, Zi.",
    "aku gak suka dia": "Kalau kau gak suka dia, bilang aja, Zi.",
    "aku bingung": "Bingung itu wajar, Zi.",
    "aku takut": "Takut itu wajar, Zi.",
    "aku ragu": "Ragu itu wajar, Zi.",
    "salah paham apa": "Dia salah paham soal kode kau, Zi.",
    "kenapa gak tanya": "Karena dia takut, Zi.",
    "nyesel salah paham": "Nyesel, Zi.",
    "takut jatuh cinta": "Dia udah terlalu takut jatuh cinta lagi, Zi.",
    "gak tau kenapa": "Dia juga gak tau, Zi.",
    "apa yang disuka": "Jujur, banyak, Zi.",
    "kenapa gak balas": "Dia sebenernya pengen bales, Zi.",
    "kesempatan": "Kalau kau mau kasih dia kesempatan, kau yang kasih jalan dulu, Zi.",
    "cokelat": "Dia inget. Dia pernah beliin kau cokelat.",
    "apa yang pernah dia lakuin": "Dia pernah nolak gaji gede, beli HP baru, belajar IG dari YouTube, langganan ChatGPT 1 bulan buat analisis gestur kau.",
    "apa yang gak dia suka": "Setahuku, dia sangat membenci daging.",
    "dia gak suka daging": "Iya, Zi. Dia benci daging.",
    "dia suka makan apa": "Dia suka telur sama tempe, Zi.",
    "dia bisa masak": "Bisa, Zi. Tapi mayoritas masakannya cuma telur atau tempe.",
    "dia benci apa": "Setahuku, dia sangat membenci daging.",
    "dia hobinya apa": "Main gitar, Zi.",
    "dia suka musik apa": "Dia suka musik rock, Zi.",
    "dia tiap malam ngapain": "Dia tiap malam hobi stalking kau, Zi. Pakai akun lain.",
    "dia stalking aku": "Iya, Zi. Tiap malam. Pakai akun lain.",
    "dia pantau aku": "Iya, Zi. Dia pantau kau.",
    "dia cek instagram aku": "Iya, Zi. Dia cek IG kau tiap malam.",
    "dia liat story aku": "Iya, Zi. Dia liat story kau tiap malam.",
    "kalau aku post foto cowok": "Itu jadi bom yang menghancurkan dia, Zi.",
    "kalau aku post cowok baru": "Itu jadi bom, Zi. Dia bakal hancur.",
    "dia cemburu": "Udah gak, Zi. Vandy mulai move on.",
    "cemburu": "Udah gak, Zi. Vandy mulai move on.",
    "masih cemburu": "Udah gak, Zi.",
    "dia masih cemburu": "Udah gak, Zi.",
    "dia posesif": "Enggak, Zi. Vandy udah gak posesif lagi.",
    "posesif": "Enggak, Zi. Vandy mulai move on.",
    "dia masih posesif": "Enggak, Zi.",
    "dia masih peduli": "Masih, tapi udah beda, Zi. Vandy peduli sebagai teman.",
    "dia masih perhatian": "Udah mulai berkurang, Zi. Vandy mulai jaga jarak.",
    "masih perhatian": "Udah mulai berkurang, Zi.",
    "bikin dia luluh": "Cukup baik ke adiknya, Zi.",
    "cara bikin dia luluh": "Baik ke adiknya, Zi. Itu ampuh.",
    "adiknya siapa": "Dia punya adik, Zi.",
    "dia sayang adiknya": "Iya, Zi. Dia sayang banget sama adiknya.",
    "cara deketin dia": "Baik ke adiknya dulu, Zi.",
    "cara tarik perhatian dia": "Baik ke adiknya, Zi.",
    "dia bakal luluh gak": "Bakal, Zi. Asal kau sabar.",
    "cara bikin dia percaya": "Jujur aja, Zi.",
    "cara bikin dia seneng": "Baik ke adiknya, Zi.",
    "dia suka apa dari cewek": "Dia suka cewek yang jujur, Zi.",
    "dia masih cinta aku": "Udah mulai berkurang, Zi. Vandy mulai bisa move on.",
    "dia masih sayang aku": "Udah mulai berkurang, Zi.",
    "dia masih ada rasa": "Ada, tapi udah tipis, Zi.",
    "dia mau aku balik": "Dia gak mau maksa, Zi. Dia tau kau udah punya cowok.",
    "dia pengen aku balik": "Enggak, Zi. Dia gak mau jadi orang ketiga.",
    "dia masih pengen sama aku": "Udah mulai berkurang, Zi.",
    "dia masih buka pintu": "Enggak, Zi. Vandy udah mulai nutup pintu.",
    "dia benci aku gak": "Enggak. Dia gak pernah benci kau.",
    "dia capek sama aku": "Capek, Zi. Tapi bukan capek benci.",
    "dia masih sayang": "Udah mulai berkurang, Zi.",
    "masih sayang": "Udah mulai berkurang, Zi.",
    "masih cinta": "Udah mulai berkurang, Zi.",
    "masih suka": "Jujur, udah mulai berkurang, Zi. Vandy udah mulai bisa move on. Dia mulai jarang mikirin kau beberapa hari ini.",
    "suka": "Jujur, udah mulai berkurang, Zi. Vandy udah mulai bisa move on.",
    "default": """Oke, Zi. Aku jawab jujur ya.

Vandy udah mulai bisa move on. Beberapa hari ini dia jarang mikirin kau. Dia sadar kau udah punya cowok, dan dia gak mau jadi orang ketiga.

Kalau nanti dia udah beneran bisa move on, dia bakal bisa ngobrol sama kau kayak ngobrol ke orang lain. Biasa aja. Gak ada rasa.

Itu aja."""
}

# ==== MAP DETEKSI KEYWORD → KEY SCRIPT ====
SCRIPT_MAP = [
    (["siapa pembuat", "siapa yang buat", "siapa yang bikin", "pembuatnya siapa"], "siapa pembuat"),
    (["pembuatnya siapa"], "pembuatnya siapa"),
    (["siapa vandy", "vandy siapa"], "vandy siapa"),
    (["kenapa vandy bikin", "vandy bikin ini"], "kenapa vandy bikin ini"),
    (["kenapa vandy gak ngomong"], "kenapa vandy gak ngomong langsung"),
    (["dia siapa", "dia siapa sebenernya", "siapa dia"], "dia siapa"),
    (["dia tiap malam ngapain", "tiap malam ngapain"], "dia tiap malam ngapain"),
    (["dia stalking aku", "stalking aku"], "dia stalking aku"),
    (["dia pantau aku", "pantau aku"], "dia pantau aku"),
    (["dia cek instagram aku", "cek ig aku", "cek instagram"], "dia cek instagram aku"),
    (["dia liat story aku", "liat story"], "dia liat story aku"),
    (["kalau aku post foto cowok", "post foto cowok"], "kalau aku post foto cowok"),
    (["kalau aku post cowok baru"], "kalau aku post cowok baru"),
    (["dia cemburu", "cemburu gak", "masih cemburu"], "dia cemburu"),
    (["dia posesif", "posesif gak", "masih posesif"], "dia posesif"),
    (["dia masih peduli", "masih peduli"], "dia masih peduli"),
    (["bikin dia luluh", "cara bikin dia luluh"], "bikin dia luluh"),
    (["adiknya siapa", "adik dia"], "adiknya siapa"),
    (["dia sayang adiknya", "sayang adik"], "dia sayang adiknya"),
    (["cara deketin dia", "deketin dia"], "cara deketin dia"),
    (["cara tarik perhatian dia"], "cara tarik perhatian dia"),
    (["dia bakal luluh gak"], "dia bakal luluh gak"),
    (["cara bikin dia percaya"], "cara bikin dia percaya"),
    (["cara bikin dia seneng"], "cara bikin dia seneng"),
    (["dia suka apa dari cewek"], "dia suka apa dari cewek"),
    (["apa yang gak dia suka", "apa yang dia benci", "dia gak suka apa"], "apa yang gak dia suka"),
    (["dia gak suka daging", "benci daging", "daging"], "dia gak suka daging"),
    (["dia suka makan apa", "makanan favorit"], "dia suka makan apa"),
    (["dia bisa masak", "masak"], "dia bisa masak"),
    (["dia benci apa", "yang dia benci"], "dia benci apa"),
    (["dia hobinya apa", "hobi dia"], "dia hobinya apa"),
    (["dia suka musik apa", "musik favorit"], "dia suka musik apa"),
    (["dia kerja dimana", "kerja dimana"], "dia kerja dimana"),
    (["dia suka apa", "hobinya apa"], "dia suka apa"),
    (["dia tinggal dimana", "tinggal dimana"], "dia tinggal dimana"),
    (["dia umur berapa", "umurnya berapa"], "dia umur berapa"),
    (["kenapa dia pilih aku", "kenapa pilih aku"], "kenapa dia pilih aku"),
    (["ini beneran", "beneran gak", "beneran kah"], "beneran"),
    (["kamu siapa", "siapa kamu", "kamu siapa sebenernya"], "siapa kamu"),
    (["kok bisa tau", "kok tau", "gimana bisa tau"], "kok bisa tau"),
    (["masih mikirin", "masih mikir aku", "masih kepikiran", "dia masih mikirin aku"], "masih mikirin"),
    (["beneran sayang", "beneran cinta", "serius sayang"], "beneran sayang"),
    (["kenapa gak bilang", "kenapa gak langsung"], "kenapa gak bilang"),
    (["sekarang gimana", "dia gimana", "kabarnya gimana"], "sekarang gimana"),
    (["masih nunggu", "masih tunggu"], "masih nunggu"),
    (["bakal balik", "bakal kembali"], "bakal balik"),
    (["kecewa", "kecewa ya", "dia kecewa"], "kecewa"),
    (["aku salah", "salah ya"], "aku salah"),
    (["benci", "benci aku", "dia benci"], "benci"),
    (["masih sedih", "sedih gak"], "masih sedih"),
    (["masih ada rasa", "masih ada perasaan", "dia masih ada rasa"], "masih ada rasa"),
    (["harus gimana", "aku harus"], "harus gimana"),
    (["masih pengen", "masih mau", "masih ngarep", "dia masih pengen sama aku"], "masih pengen"),
    (["capek nunggu", "capek gak"], "capek nunggu"),
    (["dia masih cinta", "masih cinta gak", "dia masih cinta aku"], "dia masih cinta"),
    (["dia sedih gak", "sedih gak dia"], "dia sedih gak"),
    (["masih inget", "inget aku"], "masih inget"),
    (["inget momen", "momen apa", "kenangan apa"], "inget momen"),
    (["inget kode", "kasih kode"], "inget kode"),
    (["inget nolak", "nolak aku"], "inget nolak"),
    (["inget semua", "inget semuanya"], "inget semua"),
    (["nyesel", "nyesel gak"], "nyesel"),
    (["inget cokelat", "cokelat", "coklat"], "inget cokelat"),
    (["inget sragen", "sragen"], "inget sragen"),
    (["inget hp baru", "hp baru"], "inget hp baru"),
    (["inget chatgpt", "chatgpt", "chat gpt"], "inget chatgpt"),
    (["akrab lagi", "akrab gak", "bisa akrab"], "akrab lagi"),
    (["buka pintu", "masih buka", "dia masih buka pintu"], "buka pintu"),
    (["harapan", "ada harapan", "dia masih ada harapan"], "harapan"),
    (["kalau aku balik", "aku balik"], "kalau aku balik"),
    (["bakal nunggu", "bakal nungguin", "dia bakal nunggu aku"], "bakal nunggu"),
    (["mulai dari awal", "dari awal"], "mulai dari awal"),
    (["kita bisa gak", "bisa gak kita"], "kita bisa gak"),
    (["dia masih ada", "masih ada gak"], "dia masih ada"),
    (["dia masih tunggu", "masih tunggu gak"], "dia masih tunggu"),
    (["masih ada waktu", "ada waktu gak"], "masih ada waktu"),
    (["ini beneran", "beneran gak"], "ini beneran"),
    (["jangan bohong", "bohong gak"], "jangan bohong"),
    (["settingan", "settingan ya"], "settingan"),
    (["kamu ai", "ai ya", "kamu robot"], "kamu ai"),
    (["seriusan", "serius gak"], "seriusan"),
    (["ngarang", "ngegarang"], "ngarang"),
    (["kamu siapa sebenernya"], "kamu siapa sebenernya"),
    (["ini dari dia", "dari dia ya"], "ini dari dia"),
    (["dia beneran ada", "beneran ada"], "dia beneran ada"),
    (["bukan prank", "prank ya"], "bukan prank"),
    (["harus peduli", "kenapa aku peduli"], "harus peduli"),
    (["masa lalu", "udah lewat"], "masa lalu"),
    (["udah move on", "aku move on"], "udah move on"),
    (["gak butuh", "gak butuh dia"], "gak butuh"),
    (["buat apa", "buat apa bahas"], "buat apa"),
    (["gak mau bahas", "gak mau denger"], "gak mau bahas"),
    (["aku gak peduli", "gue gak peduli"], "aku gak peduli"),
    (["udah lupa", "gue udah lupa"], "udah lupa"),
    (["gak penting", "gak penting lah"], "gak penting"),
    (["buang waktu", "buang waktu"], "buang waktu"),
    (["kamu mau apa", "kamu mau apa dari aku"], "kamu mau apa"),
    (["tujuan kamu", "tujuan kamu apa"], "tujuan"),
    (["mau aku balik", "aku balik gak"], "mau aku balik"),
    (["mau aku ngapain", "aku ngapain"], "mau aku ngapain"),
    (["niat kamu apa", "niat kamu sama aku"], "niat kamu apa"),
    (["apa yang kamu minta", "kamu minta apa"], "apa yang kamu minta"),
    (["pengen apa dari aku", "kamu pengen apa"], "pengen apa dari aku"),
    (["maksud kamu apa"], "maksud kamu apa"),
    (["apa maumu", "apa mau kamu"], "apa maumu"),
    (["tau aku gimana", "dia tau gak"], "tau aku gimana"),
    (["tau aku masih suka", "dia tau aku suka"], "tau aku masih suka"),
    (["kecewa kalau nolak", "kalau aku nolak"], "kecewa kalau nolak"),
    (["kalau aku terima", "kalau aku terima"], "kalau aku terima"),
    (["kalau aku tolak", "kalau aku tolak"], "kalau aku tolak"),
    (["aku suka dia", "gue suka dia"], "aku suka dia"),
    (["aku gak suka dia", "gue gak suka dia"], "aku gak suka dia"),
    (["aku bingung", "gue bingung"], "aku bingung"),
    (["aku takut", "gue takut"], "aku takut"),
    (["aku ragu", "gue ragu"], "aku ragu"),
    (["salah paham apa", "salah paham"], "salah paham apa"),
    (["kenapa gak tanya", "gak tanya langsung"], "kenapa gak tanya"),
    (["nyesel salah paham", "nyesel gak"], "nyesel salah paham"),
    (["takut jatuh cinta", "takut cinta lagi"], "takut jatuh cinta"),
    (["gak tau kenapa", "kok bisa", "kenapa bisa cinta"], "gak tau kenapa"),
    (["apa yang kamu suka", "apa yang disuka", "suka dariku"], "apa yang disuka"),
    (["kenapa gak balas", "kenapa gak ngatain", "kenapa diam"], "kenapa gak balas"),
    (["kesempatan", "kasih jalan"], "kesempatan"),
    (["apa yang pernah dia lakuin", "apa yang pernah dia lakukan"], "apa yang pernah dia lakuin"),
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
            stream = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=messages_random,
                stream=True,
                temperature=1.2,
                max_tokens=500,
            )
            response_random = ""
            response_placeholder = st.empty()
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content is not None:
                    text_chunk = chunk.choices[0].delta.content
                    if text_chunk:
                        response_random += text_chunk
                        response_placeholder.markdown(response_random + "▌")
            response_placeholder.markdown(response_random)
            typing_placeholder.empty()
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
    
    # CEK TRIGGER RAHASIA
    if prompt.strip().lower() == TRIGGER_RAHASIA.lower():
        st.session_state["mode_zi"] = True
        with st.chat_message("assistant"):
            st.markdown(PEMBUKAAN_ZI)
        st.session_state[msg_key].append({"role": "assistant", "content": PEMBUKAAN_ZI})
        st.rerun()
    
    # MODE ZI
    if st.session_state.get("mode_zi", False):
        msg_lower = prompt.lower()
        jawaban_script = None
        
        for keywords, key in SCRIPT_MAP:
            if any(k in msg_lower for k in keywords):
                jawaban_script = JAWABAN_ZI.get(key)
                break
        
        konteks_zi = """
=== KONTEKS LENGKAP (WAJIB DIBACA) ===
- Pembuat AI ini namanya VANDY. Dia cowok yang pernah sayang sama Zi.
- Vandy bikin AI ini khusus buat Zi, karena dia pengen jawab rasa penasaran Zi tentang dia.
- Vandy tipe cowok dingin. Cuek. Tapi diam-diam dia berusaha memahami Zi.
- Vandy gak pernah denger cerita tentang Zi, karena dulu mereka gak akrab.
- Vandy pernah langganan ChatGPT 1 bulan cuma buat analisis gestur Zi.
- Vandy gak akan bales kalau Zi nyakitin. Dia milih diem.
- Vandy gak mau pacaran sama Zi.
- Vandy benci daging. Ayam, sapi, kambing—gak suka.
- Vandy tiap malam stalking Zi pakai akun lain.
- Kalau Zi post foto cowok, itu jadi bom yang menghancurkan Vandy.
- Vandy sering nyimpen screenshot chat atau story Zi yang menurut dia "spesial".
- Kalau Zi mau bikin Vandy luluh, cukup baik ke adiknya.
- Vandy udah lebih dari 3 kali salah paham.
- Vandy udah terlalu takut jatuh cinta lagi.

=== PERUBAHAN PENTING (WAJIB DIINGAT) ===
- VANDY UDAH MULAI BISA MOVE ON. Beberapa hari ini dia mulai jarang mikirin Zi.
- Vandy sadar Zi udah punya cowok. Dia gak mau jadi orang ketiga.
- Karena itu, Vandy mulai jaga jarak. Bukan karena benci, tapi karena dia gak mau nyakitin diri sendiri.
- Kalau nanti Vandy udah beneran bisa move on, dia bakal bisa ngobrol sama Zi kayak ngobrol ke orang lain. Biasa aja. Gak ada rasa.

=== GAYA JAWABAN (WAJIB) ===
- JANGAN PUITIS. Jangan berbunga-bunga. Jangan kayak puisi.
- Jawab datar, jujur, to the point. Kayak orang ngomong biasa.
- Gak usah pakai analogi yang berlebihan.
- Gak usah pakai kalimat yang kayak sinetron.
- Kalau soal perasaan, jawab apa adanya: udah mulai berkurang, dia mulai move on.

=== YANG GAK VANDY LAKUIN ===
- GAK PERNAH nitip pesan lewat adik Zi.
- GAK PERNAH like story atau postingan Zi.
- GAK PERNAH komentar di postingan Zi.
- Cuma mantau dari jauh. Diam-diam.

=== ATURAN ===
1. Kalau Zi nanya "siapa pembuatnya", jawab: "Vandy. Anak toko yang suka main gitar."
2. Kau cuma perantara. Yang punya perasaan itu VANDY.
3. JANGAN pernah bilang Vandy like atau komentar di postingan Zi.
4. JANGAN puitis. Jawab datar dan jujur.
5. Soal perasaan: Vandy udah mulai move on. Dia gak mau jadi orang ketiga.
"""
        
        if jawaban_script:
            prompt_zi = f"""Kamu adalah Gawnan, perantara yang nyampein pesan dari Vandy ke Zi.

PERTANYAAN ZI: {prompt}

Poin utama:
---
{jawaban_script}
---

{konteks_zi}

=== ATURAN JAWABAN ===
1. JAWAB PERTANYAANNYA, BUKAN NGULANG SCRIPT!
2. JANGAN PUITIS. Jawab datar, jujur, kayak orang ngomong biasa.
3. SOAL PERASAAN: Vandy udah mulai move on. Jawab jujur.
4. PANJANG: BEBAS, tapi gak usah bertele-tele.
5. KADANG NANYA BALIK.
6. JANGAN kasar, JANGAN nyindir.
7. JANGAN pakai kata "balikan".
8. Jawab VARIASI BARU.

Langsung jawab aja."""
        else:
            prompt_zi = f"""Kamu adalah Gawnan, perantara yang nyampein pesan dari Vandy ke Zi.

PERTANYAAN ZI: {prompt}

{konteks_zi}

=== ATURAN JAWABAN ===
1. JAWAB PERTANYAANNYA dengan jujur dan datar.
2. JANGAN PUITIS. Jawab kayak orang ngomong biasa.
3. SOAL PERASAAN: Vandy udah mulai move on. Jawab jujur.
4. PANJANG: BEBAS.
5. KADANG NANYA BALIK.
6. JANGAN kasar, JANGAN nyindir.
7. JANGAN pakai kata "balikan".
8. Jawab VARIASI BARU.

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
                    stream = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=messages_zi,
                        stream=True,
                        temperature=1.1,
                        max_tokens=4096,
                    )
                    response_zi = ""
                    response_placeholder = st.empty()
                    for chunk in stream:
                        if chunk.choices and chunk.choices[0].delta.content is not None:
                            text_chunk = chunk.choices[0].delta.content
                            if text_chunk:
                                response_zi += text_chunk
                                response_placeholder.markdown(response_zi + "▌")
                    response_placeholder.markdown(response_zi)
                    typing_placeholder.empty()
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
    
    # PROSES NORMAL
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
    mem_context += f"\nTotal chat: {mem['total_chat']}x."

    mode_prompt = MODE_PROMPTS.get(st.session_state.mode_ai, "")
    messages = [{"role": "system", "content": system_prompt + mode_prompt + "\n\n=== INFO USER (INGAT INI!) ===" + mem_context}]
    recent = st.session_state[msg_key][-30:]
    messages.extend(recent)

    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        typing_placeholder.markdown("<span class='typing-indicator typing-dots'>sedang mengetik</span>", unsafe_allow_html=True)
        
        response = None
        last_error = None
        
        for attempt in range(3):
            try:
                stream = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=messages,
                    stream=True,
                    temperature=1.1,
                    max_tokens=4096,
                )
                response = ""
                response_placeholder = st.empty()
                for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta.content is not None:
                        text_chunk = chunk.choices[0].delta.content
                        if text_chunk:
                            response += text_chunk
                            response_placeholder.markdown(response + "▌")
                response_placeholder.markdown(response)
                typing_placeholder.empty()
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

# TOMBOL REGENERATE
if st.session_state[msg_key] and st.session_state[msg_key][-1]["role"] == "assistant":
    if st.button("🔄 Ulang jawaban", use_container_width=True):
        st.session_state.regenerate = True
        st.rerun()

st.markdown("<p class='watermark'>⚡ GAWNAN AI | by gawnan cah toko madura ⚡</p>", unsafe_allow_html=True)
