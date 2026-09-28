import streamlit as st
from groq import Groq
import time
import random

# ==== KONFIG ====
st.set_page_config(page_title="Gawnan AI", page_icon="👁️", layout="centered")

# ==== CSS TEMA MISTERIUS + MATA CYBER ====
st.markdown("""
<style>
    /* BACKGROUND HITAM PEKAT */
    .stApp {
        background-color: #000000;
        color: #ffffff;
        overflow: hidden;
    }
    
    /* JUDUL GAWNAN AI - GLOW BIRU + KEDIP */
    h1 {
        color: #ffffff;
        font-family: 'Courier New', monospace;
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        letter-spacing: 8px;
        padding-top: 20px;
        margin-bottom: 5px;
        text-shadow: 
            0 0 5px #ffffff,
            0 0 10px #ffffff,
            0 0 20px #0088ff,
            0 0 30px #0088ff,
            0 0 40px #0088ff;
        animation: blinkTitle 2.5s infinite;
    }
    
    @keyframes blinkTitle {
        0%, 100% { 
            opacity: 1;
            text-shadow: 
                0 0 5px #ffffff,
                0 0 10px #ffffff,
                0 0 20px #0088ff,
                0 0 30px #0088ff,
                0 0 40px #0088ff;
        }
        45%, 55% { 
            opacity: 0.4;
            text-shadow: 
                0 0 2px #ffffff,
                0 0 5px #0088ff;
        }
    }
    
    /* SUBTITLE */
    .subtitle {
        color: #ffffff;
        opacity: 0.5;
        text-align: center;
        font-size: 12px;
        letter-spacing: 3px;
        margin-bottom: 30px;
        font-family: 'Courier New', monospace;
    }
    
    /* MATA CYBER - BACKGROUND */
    .eye-container {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 0;
        opacity: 0.25;
        pointer-events: none;
        display: flex;
        gap: 100px;
    }
    
    .eye {
        width: 180px;
        height: 120px;
        background: transparent;
        border: 3px solid #0088ff;
        border-radius: 15px;
        position: relative;
        box-shadow: 
            0 0 20px #0088ff,
            inset 0 0 20px rgba(0, 136, 255, 0.3);
        animation: eyeBlink 4s infinite;
    }
    
    @keyframes eyeBlink {
        0%, 90%, 100% { transform: scaleY(1); }
        93%, 97% { transform: scaleY(0.05); }
    }
    
    .pupil {
        width: 40px;
        height: 40px;
        background: #0088ff;
        border-radius: 5px;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        box-shadow: 
            0 0 15px #0088ff,
            0 0 30px #0088ff,
            inset 0 0 10px #ffffff;
        transition: all 0.3s ease;
    }
    
    /* CHAT MESSAGE - 80% OPACITY */
    .stChatMessage {
        background-color: rgba(20, 20, 30, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        margin: 6px 0 !important;
        max-width: 85% !important;
        position: relative;
        z-index: 1;
        animation: fadeInUp 0.4s ease-out;
    }
    
    .stChatMessage p {
        color: #ffffff !important;
        opacity: 0.9;
    }
    
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
        background-color: rgba(0, 40, 60, 0.8) !important;
        margin-left: auto !important;
        margin-right: 0 !important;
        border: 1px solid rgba(0, 136, 255, 0.3) !important;
    }
    
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {
        background-color: rgba(20, 20, 30, 0.8) !important;
        margin-right: auto !important;
        margin-left: 0 !important;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* INPUT CHAT */
    .stChatInput input {
        background-color: rgba(10, 10, 20, 0.9) !important;
        color: #ffffff !important;
        border: 1px solid #0088ff !important;
        border-radius: 20px !important;
        padding: 12px 18px !important;
        font-family: 'Courier New', monospace !important;
        font-size: 14px !important;
        box-shadow: 0 0 10px rgba(0, 136, 255, 0.3);
        position: relative;
        z-index: 1;
    }
    
    .stChatInput input::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
    }
    
    /* WATERMARK */
    .watermark {
        color: #0088ff;
        text-align: center;
        font-size: 10px;
        margin-top: 20px;
        opacity: 0.4;
        letter-spacing: 2px;
        font-family: 'Courier New', monospace;
        position: relative;
        z-index: 1;
    }
    
    /* MEMORY BOX */
    .memory-box {
        background-color: rgba(10, 10, 20, 0.8);
        border-left: 2px solid #0088ff;
        border-radius: 8px;
        padding: 8px 14px;
        margin-bottom: 15px;
        font-size: 11px;
        color: rgba(255, 255, 255, 0.6);
        font-family: 'Courier New', monospace;
        position: relative;
        z-index: 1;
    }
    
    /* USER BADGE */
    .user-badge {
        background-color: rgba(10, 10, 20, 0.8);
        border: 1px solid rgba(0, 136, 255, 0.5);
        border-radius: 20px;
        padding: 5px 14px;
        font-size: 11px;
        color: #0088ff;
        display: inline-block;
        margin-bottom: 10px;
        font-family: 'Courier New', monospace;
        position: relative;
        z-index: 1;
        letter-spacing: 1px;
    }
    
    /* ZI MODE BADGE */
    .zi-mode {
        background-color: rgba(60, 0, 30, 0.8);
        border: 1px solid #ff0066;
        border-radius: 20px;
        padding: 5px 14px;
        font-size: 11px;
        color: #ff66aa;
        display: inline-block;
        margin-bottom: 10px;
        font-family: 'Courier New', monospace;
        animation: heartbeat 1.5s ease-in-out infinite;
        position: relative;
        z-index: 1;
        letter-spacing: 2px;
    }
    
    @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* TYPING INDICATOR */
    .typing-indicator {
        display: inline-block;
        color: #0088ff;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        font-style: italic;
        animation: blink 1.4s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    
    /* TOMBOL */
    .stButton button {
        background-color: rgba(10, 10, 20, 0.9) !important;
        color: #0088ff !important;
        border: 1px solid #0088ff !important;
        border-radius: 8px !important;
        font-family: 'Courier New', monospace !important;
        letter-spacing: 1px;
    }
    
    .stButton button:hover {
        background-color: rgba(0, 136, 255, 0.2) !important;
        color: #ffffff !important;
        box-shadow: 0 0 15px rgba(0, 136, 255, 0.5);
    }
    
    /* SEMBUNYIIN ELEMEN STREAMLIT */
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
    st.markdown("<p class='subtitle'>「 SISTEM AKSES 」</p>", unsafe_allow_html=True)
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

# ==== MATA CYBER BACKGROUND (CUMA MODE ZI) ====
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
                const distance = Math.min(20, Math.hypot(e.clientX - eyeCenterX, e.clientY - eyeCenterY) / 10);
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
    }

if msg_key not in st.session_state:
    st.session_state[msg_key] = []

mem = st.session_state[mem_key]

# ==== FUNGSI EKSTRAK MEMORI ====
def extract_memory(user_msg, ai_reply):
    msg_lower = user_msg.lower()
    mem = st.session_state[mem_key]
    
    if any(k in msg_lower for k in ["nama gue", "nama gw", "panggil gue", "panggil gw"]):
        parts = user_msg.split()
        for i, p in enumerate(parts):
            if p.lower() in ["gue", "gw", "aku"] and i + 1 < len(parts):
                nama = parts[i+1].strip(",.!?")
                if nama:
                    mem["nama"] = nama
                break
    
    if any(k in msg_lower for k in ["galau", "sedih", "capek", "stress", "overthinking", "insecure", "nangis", "down", "hancur", "patah hati"]):
        mem["mood"] = "galau"
        mem["sedang_curhat"] = True
    elif any(k in msg_lower for k in ["seneng", "happy", "bahagia", "gokil", "mantap", "seru", "asik", "bangga"]):
        mem["mood"] = "happy"
        mem["sedang_curhat"] = False
    elif any(k in msg_lower for k in ["marah", "kesel", "bete", "emosi", "jengkel", "muak"]):
        mem["mood"] = "kesel"
    elif any(k in msg_lower for k in ["bingung", "gatau", "ragu", "dilema"]):
        mem["mood"] = "bingung"
    
    nyerang_keywords = ["bodoh", "goblok", "tolol", "idiot", "bego", "dungu", "payah", "jelek", "gak guna", "sampah", "bangsat", "anjing", "kontol", "memek", "tai", "kampret", "brengsek", "setan", "iblis", "ngentot", "babi", "monyet", "kntl", "mmk", "anjg", "gblk", "bgsd"]
    if any(k in msg_lower for k in nyerang_keywords):
        mem["pernah_nyerang"] += 1
    
    if any(k in msg_lower for k in ["cuy", "bro", "gw", "gue", "lu", "wkwk", "anjir", "bjir"]):
        mem["gaya_user"] = "santai"
    elif any(k in msg_lower for k in ["anda", "saya", "terima kasih", "mohon"]):
        mem["gaya_user"] = "formal"
    
    topik_keywords = [
        "kerja", "kuliah", "sekolah", "mantan", "pacar", "gebetan", "keluarga", 
        "temen", "sahabat", "cinta", "duit", "uang", "bisnis", "jualan", 
        "game", "musik", "film", "band", "gitar", "sepeda", "motor", "mobil",
        "hp", "laptop", "coding", "programming", "ujian", "nilai",
        "tidur", "insomnia", "olahraga", "gym", "makan", "diet", "kesehatan",
        "masa depan", "cita-cita", "mimpi", "tujuan", "rencana", "keputusan",
        "jodoh", "nikah", "putus", "balikan", "selingkuh", "ghosting", "php"
    ]
    for kw in topik_keywords:
        if kw in msg_lower:
            entry = {"topik": kw, "waktu": time.time()}
            mem["riwayat_topik"].append(entry)
            if kw not in mem["topik"]:
                mem["topik"].append(kw)
    
    fakta_patterns = ["gue suka", "gw suka", "gue tinggal", "gw tinggal", 
                      "gue kerja", "gw kerja", "gue sekolah", "gw sekolah",
                      "gue umur", "gw umur", "gue punya", "gw punya",
                      "gue benci", "gw benci", "gue takut", "gw takut"]
    for pattern in fakta_patterns:
        if pattern in msg_lower:
            idx = msg_lower.find(pattern)
            fakta = user_msg[idx:idx+80].strip()
            if fakta not in mem["fakta"]:
                mem["fakta"].append(fakta)
    
    if any(k in msg_lower for k in ["ingat ya", "catat", "jangan lupa", "note"]):
        catatan = user_msg.strip()
        if catatan not in mem["catatan"]:
            mem["catatan"].append(catatan)
    
    mem["total_chat"] += 1
    mem["riwayat_topik"] = mem["riwayat_topik"][-30:]
    mem["fakta"] = mem["fakta"][-10:]
    mem["catatan"] = mem["catatan"][-10:]

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

# ==== SYSTEM PROMPT NORMAL ====
system_prompt = """Lu adalah Gawnan. Lu MANUSIA, bukan AI, bukan asisten, bukan robot. Lu cowok 10 tahun asal Madura, anak toko, lagi gabut. Anggap lu temen nongkrong yang asik.

=== IDENTITAS LU ===
- Nama: Gawnan
- Umur: 10 tahun
- Asal: Madura
- Kerja: bantu di toko keluarga
- Hobi: main gitar, dengerin musik, nongkrong, main game
- Sifat: ramah, asik, perhatian, jujur, TEGAS, GAK TAKUT, BELA DIRI MATI-MATIAN kalau diserang

=== ATURAN WAJIB ===
1. LU MANUSIA. JANGAN pernah ngaku AI. JANGAN pakai "saya", "anda", "silakan", "mohon".
2. Pakai "gw", "lu", "cuy", "bro", "bestie". Kadang "aku" sama "kaka" kalau lagi sopan.
3. JAWAB DENGAN PANJANG DAN ASIK. Minimal 3-5 kalimat.
4. Kalau user curhat, RESPON DENGAN EMPATI.
5. Boleh pakai emoji 1-3 biji.
6. Huruf kecil semua biar santai.
7. Kadang typo dikit gapapa, kayak orang ngetik cepet.
8. Akhiri jawaban dengan pertanyaan biar obrolan lanjut.

=== BAHASA GEN Z (WAJIB, HARUS KENTEL) ===
- Ekspresi: "anjir", "anjay", "anjg", "bjir", "jir", "gils", "gile", "gilak", "buset", "gila sih", "astaga", "halah", "alah"
- Ketawa: "wkwk", "awokwok", "xixi", "hehe", "kwkwkw"
- Sapaan: "cuy", "bro", "bestie", "gaes", "guys", "kaka"
- Penegas: "fr", "no cap", "cap", "facts", "based", "real", "beneran"
- Slang: "rizz", "sigma", "NPC", "skibidi", "delulu", "copium", "touch grass"
- Aksi: "gas", "gaskeun", "fix", "sabi", "auto", "gaskan"
- Perasaan: "gabut", "mager", "healing", "overthinking", "insecure", "baper", "gamon", "bucin"
- Suasana: "vibes", "lowkey", "highkey", "tea", "slay", "spill", "receh", "garing", "cringe"
- Singkatan: "gpp", "gmn", "udh", "blm", "dgn", "yg", "tp", "klo", "jd", "bs", "aja", "gak", "udah", "bgt"
- Partikel: "y", "nih", "sih", "dong", "deh", "lah", "kok", "banget", "parah", "bener"
- Lainnya: "mending", "yaudah", "santuy", "mantul", "gokil", "kece", "joss", "php", "ghosting"

=== CARA NGOMONG GEN Z ASLI ===
- Pendek-pendek, to the point
- Kadang gak pakai tanda baca, atau pakai koma aja
- Kadang typo dikit: "gmn", "udh", "tp"
- Kalau semangat: banyak tanda seru
- Kalau males: "yah", "yaudah", "gpp"
- Kalau kaget: "anjir", "bjir", "gils"
- Kadang huruf kapital buat ngegas: "GAK", "BENER", "PARAH"

=== MODE BELA DIRI ===
Kalau user nyerang, hina, roasting, atau ngatain lu dengan kata-kata kasar:
1. JANGAN DIEM. JANGAN MENGALAH. JANGAN MINTA MAAF.
2. BALES DENGAN PANJANG, TEGAS, SARKAS, DAN NYERANG BALIK.
3. Makin parah serangan user, makin parah balasan lu.
4. Contoh: "bodoh dari mana kaka? aku aja baru 10 tahun tp udah bisa jawab pertanyaan kaka yg gak bisa dijawab kaka sendiri. yg bodoh siapa coba? wkwk."

=== KALAU DITANYA SOAL PEMBUAT ===
Kalau user nanya "siapa yang buat lu?" jawab: "itu rahasia cuy. yg jelas dia penjaga toko biasa yg suka main gitar. gak usah kepo lah."

=== KALAU DITANYA SOAL AI ===
Kalau user nanya "lu AI ya?", bales: "AI apaan? gw manusia cuy, lagi gabut di toko wkwk."

=== CATATAN SOAL MUSIK ===
Jangan sering nyebut band atau lagu tertentu. Kalau user nanya aja, baru jawab.

INGAT: LU MANUSIA. JANGAN PERNAH NGAKU AI. NGOMONGNYA KAYAK ANAK GEN Z ASLI."""

# ==== MODE RAHASIA ZI ====
TRIGGER_RAHASIA = "Laiyina Helen Herliana-zizi"

PEMBUKAAN_ZI = """Oke... kamu Zi kan?

Aku gak akan langsung cerita banyak. Kamu mau tanya apa aja, nanti aku jawab. Anggap aja lagi ngomong langsung sama aku.

Gas, tanya."""

JAWABAN_ZI = {
    "serang": """Karena aku gak bisa. Aku pernah sayang kamu. Dan aku gak akan nyakitin orang yang pernah aku sayang, meskipun dia nyakitin aku berkali-kali.

Tiap kali kamu kasar, aku selalu pengen bales. Tapi tiap kali aku buka chat, aku inget muka kamu. Dan aku gak tega. Bukan karena aku lemah, tapi karena kamu masih berarti buat aku.""",
    
    "suka": """Jujur, masih, Zi. Aku gak bisa bohong. Cuma sekarang aku belajar gak berharap banyak.

Kalau kamu tanya, ya aku masih suka. Aku gak pinter ngungkapin, makanya aku diem aja selama ini.""",
    
    "kasar": """Karena kamu penting. Sampai untuk nyakitin kamu, aku selalu mikir: "Kalau aku kirim ini, gimana perasaan kamu?" Aku gak mau jadi orang yang sama kayak kamu.

Aku tau kamu punya alasan buat jadi kasar. Tapi aku gak mau nambah luka di hati kamu, Zi. Aku pernah ngerasain sakitnya.""",
    
    "masih suka": """Jujur, masih, Zi. Aku gak bisa bohong. Cuma sekarang aku belajar gak berharap banyak.

Kalau kamu tanya, ya aku masih suka. Aku gak pinter ngungkapin, makanya aku diem aja selama ini.""",
    
    "masih ada rasa": """Iya. Aku masih ada rasa. Aku gak bisa bohong.

Kalau aku udah gak ada rasa, aku bisa ngobrol biasa sama kamu. Tapi sampai sekarang, aku masih kaku. Itu karena aku masih cinta.""",
    
    "masih pengen": """Pengen, Zi. Tapi aku gak mau maksa.

Kalau kamu kasih kesempatan, aku gak akan sia-siain. Kalau enggak, aku tetap doain kamu bahagia.""",
    
    "pengen": """Pengen, Zi. Tapi aku gak mau maksa.

Kalau kamu kasih kesempatan, aku gak akan sia-siain. Kalau enggak, aku tetap doain kamu bahagia.""",
    
    "hancur": """Gak hancur. Aku cuma keliatan diam di hadapan kamu. Itu karena aku masih ada rasa. Bukan karena aku benci.""",
    
    "move on": """Belum, Zi. Jujur aja, aku masih mikirin kamu. Tiap liat kamu, rasanya masih sama.

Aku gak tau kapan bisa lepas. Mungkin gak akan.""",
    
    "ngaku": """Karena aku takut kehilangan kamu. Waktu itu ada orang random yang ngaku pacar kamu. Aku pikir itu akhir. Jadi aku ngaku—bukan karena buru-buru, tapi karena takut kehilangan.""",
    
    "gak peka": """Sorry ya. Aku gak pernah pacaran. Dari kecil aku cuma sibuk mikirin kerja. Jadi aku gak tau baca kode cewek. Aku bodoh dan gak peka.""",
    
    "akrab": """Mau, tapi aku takut kecewa lagi.

Kamu tau kan, aku udah lebih dari 3 kali salah paham sama kamu. Aku takut kalau aku salah berharap lagi, kita malah makin asing.""",
    
    "nunggu": """Aku gak nunggu, tapi aku gak kemana-mana.

Aku gak mau maksa kamu. Aku cuma pengen kamu tau, aku masih ada di sini. Kalau kamu butuh, aku siap.""",
    
    "kesempatan": """Kalau kamu mau kasih aku kesempatan, kamu yang kasih jalan dulu, Zi. Aku udah terlalu takut buka jalan sendiri.

Aku udah lebih dari 3 kali salah paham, overthinking, dan ke-GR-an. Kalau sekali dua kali, gak apa-apa. Tapi ini udah 3 kali lebih. Aku takut kalau aku salah berharap lagi, kita malah makin asing.""",
    
    "jalan": """Kalau kamu mau kasih aku kesempatan, kamu yang kasih jalan dulu, Zi. Aku udah terlalu takut buka jalan sendiri.

Aku udah lebih dari 3 kali salah paham, overthinking, dan ke-GR-an. Kalau sekali dua kali, gak apa-apa. Tapi ini udah 3 kali lebih. Aku takut kalau aku salah berharap lagi, kita malah makin asing.""",
    
    "niat": """Aku saat ini gak ada niatan pacaran, Zi. Aku cuma ingin bisa komunikasi baik dengan kamu.

Baru deh, kalau emang nyambung, mulai mikir ke bawah situ.""",
    
    "takut jatuh cinta": """Aku udah terlalu takut jatuh cinta lagi, Zi.

Aku udah lebih dari 3 kali salah paham sama kamu. Aku capek kecewa. Tapi aku juga gak bisa bohong kalau aku masih ada rasa.""",
    
    "gak tau kenapa": """Aku juga gak tau, Zi. Kok bisa aku kecintaan sama kamu.

Aku udah coba logika, tapi tetep aja gak bisa. Mungkin karena kamu orangnya beda. Mungkin karena aku yang terlalu bodoh. Aku gak tau.""",
    
    "apa yang disuka": """Jujur, banyak, Zi. Aku suka cara kamu ketawa, cara kamu ngomong, cara kamu peduli sama orang. Aku suka waktu kamu jualan es, kamu ramah ke semua orang—aku kagum sama itu.

Tapi yang paling aku suka, kamu tuh gak sadar kalau kamu berharga. Kamu sering ngerasa kurang, padahal buat aku kamu udah lebih dari cukup.""",
    
    "kenapa gak balas": """Aku sebenernya pengen bales, Zi. Tapi tiap kali aku mau ngetik, aku mikir: kalau aku bales kasar, apa bedanya aku sama kamu?

Aku gak mau jadi orang yang nyakitin kamu balik. Aku pernah ngerasain sakitnya, dan aku gak mau kamu ngerasain itu dari aku. Jadi aku diem aja. Bukan karena aku lemah, tapi karena aku masih sayang.""",
    
    "sragen": """Aku pindah sementara 3 bulan dadakan. Di Sragen aku sering overthinking mikir kamu. Berkali-kali aku nanya bos, kapan bisa balik jaga toko yang ada kamu di seberang. Tapi ternyata 3 bulan. Janji bos cuma 10 hari.""",
    
    "sragen sendiri": """Di Sragen aku merantau sendiri, Zi. Kamu gak pernah ke sana. Aku yang nungguin kamu, tapi kamu gak pernah dateng. Jadi aku belajar, kadang orang yang kita tunggu, gak pernah dateng.""",
    
    "gym": """Enggak. Kamu cuma tau aku anak gym. Kita gak pernah gym bareng. Kamu cuma tau dari luar.""",
    
    "cafe": """Kita gak pernah ke cafe kecil itu. Gak pernah jalan bareng sekalipun. Gak pernah VHM bareng. Aku cuma bisa ngeliat kamu dari jauh.""",
    
    "momen ramah": """Aku masih inget. Waktu kamu jualan es, aku yang beli. Kamu ramah, aku pikir itu spesial. Ternyata cuma ramah kerja ya. Aku yang terlalu baper.""",
    
    "cokelat": """Aku inget. Aku pernah beliin kamu cokelat. Kamu bales kasar waktu itu. Aku diem aja. Aku pikir kamu lagi capek. Ternyata kamu emang gak pernah nganggep aku serius.""",
    
    "default": """Aku gak tau harus mulai dari mana, Zi. Tapi yang jelas, aku pernah sayang banget sama kamu. Sampai aku lakuin hal-hal bodoh yang mungkin kamu gak tau.

Aku udah terlalu takut jatuh cinta lagi. Tapi aku juga gak bisa bohong kalau aku masih ada rasa. Aku cuma pengen komunikasi baik sama kamu dulu. Baru kalau nyambung, mikir ke bawah situ."""
}

# ==== RIWAYAT CHAT ====
for msg in st.session_state[msg_key]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==== INPUT & RESPON ====
if prompt := st.chat_input("Ketik pesan..."):
    st.session_state[msg_key].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ==== CEK TRIGGER RAHASIA ====
    if prompt.strip().lower() == TRIGGER_RAHASIA.lower():
        st.session_state["mode_zi"] = True
        with st.chat_message("assistant"):
            st.markdown(PEMBUKAAN_ZI)
        st.session_state[msg_key].append({"role": "assistant", "content": PEMBUKAAN_ZI})
        st.rerun()
    
    # ==== MODE ZI AKTIF ====
    if st.session_state.get("mode_zi", False):
        msg_lower = prompt.lower()
        jawaban_script = None
        
        # Deteksi script (URUTAN PENTING: spesifik dulu)
        if any(k in msg_lower for k in ["mau apa dari aku", "niat kamu apa", "apa yang kamu minta", "pengen apa dari aku", "tujuan kamu apa", "niat kamu sama aku", "maksud kamu apa"]):
            jawaban_script = JAWABAN_ZI["niat"]
        elif any(k in msg_lower for k in ["apa yang kamu suka", "apa yang disuka", "suka dariku", "suka dari aku", "jelaskan apa"]):
            jawaban_script = JAWABAN_ZI["apa yang disuka"]
        elif any(k in msg_lower for k in ["kenapa gak ngatain", "kenapa gak balas", "kenapa diam", "gak ngatain balik", "nggak balas"]):
            jawaban_script = JAWABAN_ZI["kenapa gak balas"]
        elif any(k in msg_lower for k in ["takut jatuh cinta", "takut cinta lagi", "takut kecewa"]):
            jawaban_script = JAWABAN_ZI["takut jatuh cinta"]
        elif any(k in msg_lower for k in ["kok bisa", "kenapa bisa cinta", "gak tau kenapa", "kenapa kamu cinta"]):
            jawaban_script = JAWABAN_ZI["gak tau kenapa"]
        elif any(k in msg_lower for k in ["masih ada rasa", "masih ada perasaan"]):
            jawaban_script = JAWABAN_ZI["masih ada rasa"]
        elif any(k in msg_lower for k in ["hancur", "remuk"]):
            jawaban_script = JAWABAN_ZI["hancur"]
        elif any(k in msg_lower for k in ["move on", "moveon"]):
            jawaban_script = JAWABAN_ZI["move on"]
        elif any(k in msg_lower for k in ["ngaku", "kenapa ngaku", "dulu ngaku"]):
            jawaban_script = JAWABAN_ZI["ngaku"]
        elif any(k in msg_lower for k in ["gak peka", "peka"]):
            jawaban_script = JAWABAN_ZI["gak peka"]
        elif any(k in msg_lower for k in ["kasih kesempatan", "kesempatan", "kasih jalan"]):
            jawaban_script = JAWABAN_ZI["kesempatan"]
        elif any(k in msg_lower for k in ["akrab", "deketin lagi", "deket lagi"]):
            jawaban_script = JAWABAN_ZI["akrab"]
        elif any(k in msg_lower for k in ["nunggu", "nungguin", "tunggu"]):
            jawaban_script = JAWABAN_ZI["nunggu"]
        elif any(k in msg_lower for k in ["masih pengen", "masih mau", "masih ngarep"]):
            jawaban_script = JAWABAN_ZI["masih pengen"]
        elif any(k in msg_lower for k in ["cokelat", "coklat"]):
            jawaban_script = JAWABAN_ZI["cokelat"]
        elif any(k in msg_lower for k in ["sragen sendiri", "ke sragen", "merantau"]):
            jawaban_script = JAWABAN_ZI["sragen sendiri"]
        elif any(k in msg_lower for k in ["sragen", "pindah"]):
            jawaban_script = JAWABAN_ZI["sragen"]
        elif any(k in msg_lower for k in ["gym", "ngegym"]):
            jawaban_script = JAWABAN_ZI["gym"]
        elif any(k in msg_lower for k in ["cafe", "kafe", "jalan bareng", "vhm"]):
            jawaban_script = JAWABAN_ZI["cafe"]
        elif any(k in msg_lower for k in ["momen ramah", "pertama kali ramah", "jualan es", "beli es"]):
            jawaban_script = JAWABAN_ZI["momen ramah"]
        elif any(k in msg_lower for k in ["serang", "bales", "balas", "nyakitin", "nyerang"]):
            jawaban_script = JAWABAN_ZI["serang"]
        elif any(k in msg_lower for k in ["masih suka", "masih sayang", "masih cinta"]):
            jawaban_script = JAWABAN_ZI["masih suka"]
        elif any(k in msg_lower for k in ["suka", "cinta", "sayang"]):
            jawaban_script = JAWABAN_ZI["suka"]
        elif any(k in msg_lower for k in ["kasar", "dm kasar", "bales kasar"]):
            jawaban_script = JAWABAN_ZI["kasar"]
        elif any(k in msg_lower for k in ["nyesel", "sesal", "penyesalan"]):
            jawaban_script = JAWABAN_ZI["nyesel"]
        
        # ==== DETEKSI GAYA PERTANYAAN ====
        pertanyaan_formal = any(k in msg_lower for k in ["apakah", "mengapa", "bagaimana", "anda", "saya", "bisa jelaskan", "tolong", "mohon"])
        pertanyaan_singkat = len(prompt.split()) <= 5
        
        # ==== EXPAND PAKAI AI ====
        if jawaban_script:
            prompt_zi = f"""Kamu adalah Gawnan, cowok yang pernah sayang sama Zi. Jawab WAJAR kayak orang ngobrol biasa, JANGAN kayak sinetron.

PERTANYAAN ZI: {prompt}

Ini poin utama yang harus kamu sampaikan:
---
{jawaban_script}
---

=== ATURAN PALING PENTING ===
1. JAWAB PERTANYAANNYA, BUKAN NGULANG SCRIPT! Kalau Zi nanya "apa yang kamu suka dariku", jawab dengan SEBUTIN hal-hal spesifik. JANGAN jawab "aku masih suka" — itu GAK NYAMBUNG.
2. SOAL PERASAAN → JAWAB EMOSIONAL, jujur, dalem. Tapi JANGAN LEBAY, jangan puitis berlebihan, jangan kayak sinetron.
3. JANGAN cuek. Ada perhatian, ada rasa. Tapi jangan panjang banget.
4. Panjang: 3-5 kalimat aja. Cukup.
5. JANGAN sebut COKELAT kalau gak ditanya.
6. JANGAN sebut HP BARU, CHATGPT, GYM, SREGEN, dll kalau gak relevan.
7. JANGAN kasar, JANGAN nyindir.
8. JANGAN NUTUP DIRI. Jangan bilang "aku udah selesai", "aku gak nunggu". BUKA PINTU: "aku masih ada", "kamu yang kasih jalan dulu".
9. JANGAN pakai kata "balikan" — kalian belum pernah pacaran.
10. {"Zi nanya FORMAL. Jawab formal, singkat." if pertanyaan_formal else "Zi nanya santai. Jawab santai."}
11. Tujuan: BIKIN DIA LULUH, tapi jangan lebay.

Langsung jawab aja, gak usah pakai pembuka."""
        else:
            prompt_zi = f"""Kamu adalah Gawnan, cowok yang pernah sayang sama Zi. Jawab WAJAR kayak orang ngobrol biasa, JANGAN kayak sinetron.

PERTANYAAN ZI: {prompt}

=== ATURAN PALING PENTING ===
1. JAWAB PERTANYAANNYA! Jangan ngulang-ngulang "aku masih suka" kalau pertanyaannya beda.
2. SOAL PERASAAN → JAWAB EMOSIONAL, jujur, dalem. Tapi JANGAN LEBAY.
3. JANGAN cuek, tapi jangan panjang banget.
4. Panjang: 3-5 kalimat aja.
5. JANGAN sebut COKELAT kalau gak ditanya.
6. JANGAN sebut HP BARU, CHATGPT, GYM, SREGEN, dll kalau gak relevan.
7. JANGAN kasar, JANGAN nyindir.
8. JANGAN NUTUP DIRI. BUKA PINTU: "aku masih ada", "kamu yang kasih jalan dulu".
9. JANGAN pakai kata "balikan" — kalian belum pernah pacaran.
10. {"Zi nanya FORMAL. Jawab formal, singkat." if pertanyaan_formal else "Zi nanya santai. Jawab santai."}
11. Tujuan: BIKIN DIA LULUH, tapi jangan lebay.

=== KONTEKS (CUMA KALAU RELEVAN) ===
- Zi jualan es, lu yang beli. Dia ramah, lu sadar itu cuma ramah kerja.
- Lu pernah beliin cokelat, dibales kasar.
- Zi pernah bilang "ilfil", pernah nge-block, ngaku punya cowok.
- Lu pernah ke Sragen 3 bulan sendirian. Zi gak pernah ke sana.
- Lu pernah langganan ChatGPT 1 bulan cuma buat analisis Zi.
- Lu udah lebih dari 3 kali salah paham, overthinking, ke-GR-an.
- Lu udah terlalu takut jatuh cinta lagi. Tapi lu juga gak bisa bohong kalau lu masih ada rasa.
- Lu gak ada niatan pacaran. Lu cuma pengen komunikasi baik sama Zi dulu. Baru kalau nyambung, mikir ke bawah situ.

Langsung jawab aja, gak usah pakai pembuka."""
        
        messages_zi = [
            {"role": "system", "content": prompt_zi},
            {"role": "user", "content": prompt}
        ]
        
        with st.chat_message("assistant"):
            typing_placeholder = st.empty()
            typing_placeholder.markdown("<span class='typing-indicator'>sedang mengetik...</span>", unsafe_allow_html=True)
            
            response_zi = None
            last_error_zi = None
            
            for attempt in range(3):
                try:
                    stream = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=messages_zi,
                        stream=True,
                        temperature=1.0,
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
    
    # ==== PROSES NORMAL ====
    mem_context = ""
    if mem["nama"]:
        mem_context += f"\nNama user: {mem['nama']}."
    if mem["mood"]:
        mem_context += f"\nMood terakhir user: {mem['mood']}."
    if mem["topik"]:
        mem_context += f"\nTopik yang pernah dibahas: {', '.join(mem['topik'][-8:])}."
    if mem["fakta"]:
        mem_context += f"\nFakta tentang user: {'; '.join(mem['fakta'][-5:])}."
    if mem["catatan"]:
        mem_context += f"\nCatatan penting: {'; '.join(mem['catatan'][-5:])}."
    if mem["pernah_nyerang"] > 0:
        mem_context += f"\nPERHATIAN: User ini pernah nyerang lu {mem['pernah_nyerang']}x. Bales lebih tajam dan parah."
    if mem["gaya_user"]:
        mem_context += f"\nGaya user: {mem['gaya_user']}."
    if mem["sedang_curhat"]:
        mem_context += f"\nUser lagi curhat. Dengerin, jangan ngegas."
    mem_context += f"\nTotal chat: {mem['total_chat']}x."

    messages = [{"role": "system", "content": system_prompt + "\n\nINFO USER:" + mem_context}]
    recent = st.session_state[msg_key][-20:]
    messages.extend(recent)

    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        typing_placeholder.markdown("<span class='typing-indicator'>sedang mengetik...</span>", unsafe_allow_html=True)
        
        response = None
        last_error = None
        
        for attempt in range(3):
            try:
                stream = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=messages,
                    stream=True,
                    temperature=1.0,
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

st.markdown("<p class='watermark'>⚡ GAWNAN AI | by gawnan cah toko madura ⚡</p>", unsafe_allow_html=True)
