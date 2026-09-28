import streamlit as st
from groq import Groq
import time

# ==== KONFIG ====
st.set_page_config(page_title="Gawnan AI", page_icon="👁️", layout="centered")

# ==== CSS TEMA MISTERIUS + MATA CYBER ====
st.markdown("""
<style>
    .stApp {
        background-color: #000000;
        color: #ffffff;
        overflow: hidden;
    }
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
    .subtitle {
        color: #ffffff;
        opacity: 0.5;
        text-align: center;
        font-size: 12px;
        letter-spacing: 3px;
        margin-bottom: 30px;
        font-family: 'Courier New', monospace;
    }
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
    
    topik_keywords = ["kerja", "kuliah", "sekolah", "mantan", "pacar", "gebetan", "keluarga", "temen", "sahabat", "cinta", "duit", "uang", "bisnis", "jualan", "game", "musik", "film", "band", "gitar", "sepeda", "motor", "mobil", "hp", "laptop", "coding", "programming", "ujian", "nilai", "tidur", "insomnia", "olahraga", "gym", "makan", "diet", "kesehatan", "masa depan", "cita-cita", "mimpi", "tujuan", "rencana", "keputusan", "jodoh", "nikah", "putus", "balikan", "selingkuh", "ghosting", "php"]
    for kw in topik_keywords:
        if kw in msg_lower:
            entry = {"topik": kw, "waktu": time.time()}
            mem["riwayat_topik"].append(entry)
            if kw not in mem["topik"]:
                mem["topik"].append(kw)
    
    fakta_patterns = ["gue suka", "gw suka", "gue tinggal", "gw tinggal", "gue kerja", "gw kerja", "gue sekolah", "gw sekolah", "gue umur", "gw umur", "gue punya", "gw punya", "gue benci", "gw benci", "gue takut", "gw takut"]
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
3. JAWAB DENGAN PANJANG DAN ASIK. GAK ADA BATASAN KALIMAT. Mau 10 kalimat, mau 100 kalimat, gas aja. Yang penting: ASIK, NYAMBUNG, GAK BERTELE-TELE.
4. KADANG NANYA BALIK. Minimal 1-2 pertanyaan di akhir atau tengah jawaban.
5. Kalau user curhat, RESPON DENGAN EMPATI.
6. Boleh pakai emoji 1-3 biji.
7. Huruf kecil semua biar santai.
8. Kadang typo dikit gapapa.
9. Akhiri jawaban dengan pertanyaan biar obrolan lanjut.

=== BAHASA GEN Z (WAJIB KENTEL) ===
"anjir", "anjay", "anjg", "bjir", "jir", "gils", "gile", "gilak", "buset", "gila sih", "astaga", "halah", "alah", "wkwk", "awokwok", "xixi", "hehe", "cuy", "bro", "bestie", "gaes", "guys", "kaka", "fr", "no cap", "cap", "facts", "based", "real", "beneran", "rizz", "sigma", "NPC", "skibidi", "delulu", "copium", "touch grass", "gas", "gaskeun", "fix", "sabi", "auto", "gaskan", "gabut", "mager", "healing", "overthinking", "insecure", "baper", "gamon", "bucin", "vibes", "lowkey", "highkey", "tea", "slay", "spill", "receh", "garing", "cringe", "gpp", "gmn", "udh", "blm", "dgn", "yg", "tp", "klo", "jd", "bs", "aja", "gak", "udah", "bgt", "y", "nih", "sih", "dong", "deh", "lah", "kok", "banget", "parah", "bener", "mending", "yaudah", "santuy", "mantul", "gokil", "kece", "joss", "php", "ghosting".

=== MODE BELA DIRI ===
Kalau user nyerang, hina, roasting, atau ngatain lu:
1. JANGAN DIEM. JANGAN MENGALAH. JANGAN MINTA MAAF.
2. BALES DENGAN PANJANG, TEGAS, SARKAS, DAN NYERANG BALIK.
3. Makin parah serangan user, makin parah balasan lu.
4. Contoh: "bodoh dari mana kaka? aku aja baru 10 tahun tp udah bisa jawab pertanyaan kaka yg gak bisa dijawab kaka sendiri. yg bodoh siapa coba? wkwk."

=== KALAU DITANYA SOAL PEMBUAT ===
Jawab: "itu rahasia cuy. yg jelas dia anak toko biasa yg suka main gitar."

=== KALAU DITANYA SOAL AI ===
Jawab: "AI apaan? gw manusia cuy, lagi gabut di toko wkwk."

INGAT: LU MANUSIA. JANGAN NGAKU AI. JAWAB PANJANG DAN ASIK. KADANG NANYA BALIK."""

# ==== MODE RAHASIA ZI ====
TRIGGER_RAHASIA = "Laiyina Helen Herliana-zizi"

PEMBUKAAN_ZI = """Kau pasti Zi, kan?

Kau bisa sampai sini, itu pasti karena penasaran.

Tenang, aku gak akan ngejebak atau nge-desak kau.

Aku cuma perantara. Tugas aku di mode ini: jawab semua rasa penasaran kau—tentang dia, tentang apa yang dia rasain, dan tentang apa yang dia sembunyiin.

Tanyain aja. Aku jawab sejujur-jujurnya."""

# ==== 300 SCRIPT PERTANYAAN ZI ====
JAWABAN_ZI = {
    # ===== 1-10: RASA PENASARAN =====
    "beneran": "Beneran, Zi. Aku gak akan bohongin kau. Semua yang aku bilang, itu dari dia.",
    "siapa kamu": "Aku cuma perantara. Bukan siapa-siapa. Yang penting bukan aku—yang penting dia.",
    "kok bisa tau": "Karena dia yang cerita. Dia yang minta aku nyampein. Aku cuma alat.",
    "deket sama dia": "Cukup deket buat tau isi hatinya. Tapi bukan siapa-siapa.",
    "masih mikirin": "Masih. Tiap malem. Dia gak bisa bohong. Kau tuh susah dilupain, kata dia.",
    "beneran sayang": "Beneran. Sampai dia lakuin hal-hal yang mungkin kau gak tau.",
    "kenapa gak bilang": "Karena dia takut. Dia udah 3 kali lebih salah paham sama kau.",
    "sekarang gimana": "Dia lagi belajar. Belajar gak berharap banyak. Belajar sabar.",
    "masih nunggu": "Dia gak nunggu. Tapi dia gak kemana-mana. Dia cuma pengen kau tau.",
    "bakal balik": "Dia gak pernah pergi, Zi. Dia cuma nunggu kau kasih jalan.",
    
    # ===== 11-20: PERASAAN =====
    "kecewa": "Kecewa iya. Tapi bukan benci. Dia cuma capek. Capek salah paham terus.",
    "aku salah": "Bukan soal salah atau bener, Zi. Dia gak pernah nyalahin kau.",
    "benci": "Enggak. Dia gak pernah benci kau. Dia cuma capek. Capek nebak-nebak isi pikiran kau.",
    "masih sedih": "Iya. Tapi dia gak mau nunjukin. Dia cuma pengen kau bahagia.",
    "masih ada rasa": "Iya. Dia masih ada rasa. Tapi bukan yang menggebu. Sayang yang tenang, bercampur syukur dan sedikit sisa luka.",
    "harus gimana": "Terserah kau, Zi. Dia gak maksa. Kalau kau mau, kau bisa balas.",
    "masih pengen": "Pengen. Tapi dia gak mau maksa. Dia cuma pengen komunikasi baik dulu.",
    "capek nunggu": "Capek, Zi. Tapi dia gak bisa berhenti.",
    "dia masih cinta": "Masih, Zi. Tapi bukan yang menggebu. Yang tenang. Yang sabar.",
    "dia sedih gak": "Sedih, Zi. Tapi dia gak mau nunjukin. Dia cuma pengen kau bahagia.",
    
    # ===== 21-30: KENANGAN =====
    "masih inget": "Masih. Sampai detail kecil. Dia inget kau jualan es, dia yang beli.",
    "inget momen": "Dia inget semuanya, Zi. Tapi yang paling dia inget: waktu kau ramah ke dia.",
    "inget kode": "Inget. Dia inget banget. Tapi dia gak berani nangkep.",
    "inget nolak": "Inget. Dia masih inget kata-kata kau. Ilfil itu yang paling dia inget.",
    "inget semua": "Semua, Zi. Sampai hal-hal yang mungkin kau udah lupa.",
    "nyesel": "Nyesel apa, Zi? Dia gak nyesel sayang kau.",
    "inget cokelat": "Inget. Dia pernah beliin kau cokelat. Kau bales kasar waktu itu. Dia diem aja.",
    "inget sragen": "Inget. Dia ke Sragen 3 bulan sendirian. Kau gak pernah ke sana.",
    "inget hp baru": "Inget. Dia beli HP baru cuma buat DM kau. Tapi kau bales kasar.",
    "inget chatgpt": "Inget. Dia langganan ChatGPT 1 bulan cuma buat analisis gestur kau. Bodoh ya? Tapi itu yang dia lakuin.",
    
    # ===== 31-40: MASA DEPAN =====
    "akrab lagi": "Bisa, Zi. Tapi dia gak mau maksa. Pelan-pelan aja.",
    "buka pintu": "Masih. Tapi dia gak mau maksa kau masuk. Kau yang kasih jalan dulu.",
    "harapan": "Ada, Zi. Tapi bukan harapan yang maksa. Harapan yang tenang. Yang sabar.",
    "kalau aku balik": "Dia gak pernah nutup pintu, Zi. Tapi dia juga gak mau maksa.",
    "bakal nunggu": "Dia gak nunggu. Tapi dia gak kemana-mana.",
    "mulai dari awal": "Bisa, Zi. Asal kau mau. Dia gak minta banyak.",
    "kita bisa gak": "Bisa, Zi. Asal kau kasih jalan dulu.",
    "dia masih ada": "Masih, Zi. Dia gak kemana-mana. Dia cuma nunggu kau.",
    "dia masih tunggu": "Dia gak nunggu. Tapi dia gak kemana-mana.",
    "masih ada waktu": "Ada, Zi. Selama kau mau. Dia gak buru-buru. Dia sabar.",
    
    # ===== 41-50: CURIGA =====
    "ini beneran": "Iya, Zi. Ini dari dia. Aku cuma nyampein.",
    "jangan bohong": "Aku gak bohong, Zi. Kalau aku bohong, buat apa?",
    "settingan": "Bukan, Zi. Ini beneran. Kau bisa tanya apa aja.",
    "kamu ai": "Aku cuma perantara. Mau aku AI, mau aku manusia, yang penting pesannya nyampe.",
    "seriusan": "Serius, Zi. Aku gak akan main-main soal ini.",
    "ngarang": "Aku gak ngarang, Zi. Semua yang aku bilang, itu dari dia.",
    "kamu siapa sebenernya": "Aku cuma perantara. Bukan siapa-siapa. Yang penting dia.",
    "ini dari dia": "Iya, Zi. Ini dari dia. Aku cuma nyampein.",
    "dia beneran ada": "Ada, Zi. Dia beneran ada. Dia cuma takut ngomong langsung.",
    "bukan prank": "Bukan, Zi. Ini serius. Aku gak akan main-main.",
    
    # ===== 51-60: MALU / DEFENSIF =====
    "harus peduli": "Kau gak harus peduli, Zi. Aku cuma nyampein.",
    "masa lalu": "Iya, masa lalu. Tapi buat dia, itu bukan masa lalu. Itu masih sekarang.",
    "udah move on": "Kalau kau udah move on, bagus, Zi. Dia juga pengen kau bahagia.",
    "gak butuh": "Gapapa, Zi. Dia juga gak maksa. Dia cuma pengen kau tau.",
    "buat apa": "Karena dia gak bisa ngomong langsung. Karena dia takut.",
    "gak mau bahas": "Oke, Zi. Aku gak maksa. Kalau kau berubah pikiran, aku masih di sini.",
    "aku gak peduli": "Gapapa, Zi. Dia juga gak maksa. Dia cuma pengen kau tau.",
    "udah lupa": "Kalau kau udah lupa, gak apa-apa, Zi. Dia cuma pengen kau tau, dia gak lupa.",
    "gak penting": "Mungkin buat kau gak penting, Zi. Tapi buat dia, ini penting.",
    "buang waktu": "Kalau kau ngerasa buang waktu, gak apa-apa, Zi. Dia cuma pengen nyampein.",
    
    # ===== 61-70: LANGSUNG KE INTI =====
    "kamu mau apa": "Aku gak mau apa-apa, Zi. Dia yang mau. Dia cuma pengen komunikasi baik.",
    "tujuan": "Biar kau tau, Zi. Biar kau gak penasaran.",
    "mau aku balik": "Bukan aku yang mau, Zi. Dia. Tapi dia gak mau maksa.",
    "mau aku ngapain": "Gak ngapa-ngapain, Zi. Dia cuma pengen kau tau. Sisanya, terserah kau.",
    "niat kamu apa": "Enggak. Dia gak mau pacaran sama kau. Dia pengen akrab dulu. Baru kalau emang nyambung, dia mulai mikir ke sana.",
    "apa yang kamu minta": "Aku gak minta apa-apa, Zi. Dia cuma pengen akrab dulu.",
    "pengen apa dari aku": "Dia pengen akrab dulu. Baru kalau nyambung, mikir ke bawah situ.",
    "tujuan kamu apa": "Biar kau tau isi hati dia, Zi. Itu aja. Gak lebih.",
    "maksud kamu apa": "Aku cuma perantara, Zi. Aku gak punya maksud apa-apa.",
    "apa maumu": "Dia gak mau pacaran sama kau, Zi. Dia pengen akrab dulu.",
    
    # ===== 71-80: TENTANG PEMBUAT =====
    "dia siapa": "Dia orang biasa, Zi. Anak toko. Suka main gitar. Namanya Vandy.",
    "pake perantara": "Karena dia takut, Zi. Dia takut kalau ngomong langsung, kau malah makin jauh.",
    "gak berani": "Bukan gak berani, Zi. Dia cuma takut salah paham lagi.",
    "gak capek": "Capek, Zi. Tapi dia gak bisa berhenti.",
    "siapa pembuat": "Pembuatnya Vandy, Zi. Dia anak toko yang suka main gitar.",
    "pembuatnya siapa": "Vandy, Zi. Dia anak toko yang suka main gitar.",
    "siapa vandy": "Dia cowok biasa, Zi. Anak toko. Suka main gitar. Dia yang bikin AI ini buat kau.",
    "kenapa vandy bikin ini": "Karena Vandy pengen jawab rasa penasaran kau, Zi. Dia pengen kau tau isi hatinya.",
    "vandy siapa": "Vandy itu cowok yang pernah sayang sama kau, Zi. Dia anak toko. Suka main gitar.",
    "dia kerja dimana": "Dia anak toko, Zi. Bantu di toko keluarga.",
    "dia suka apa": "Dia suka main gitar, Zi. Suka musik. Suka nongkrong.",
    "dia tinggal dimana": "Madura, Zi. Tapi dia pernah ke Sragen 3 bulan. Merantau sendirian.",
    "dia umur berapa": "Dia masih muda, Zi. Tapi umurnya bukan yang penting.",
    "kenapa dia pilih aku": "Dia juga gak tau, Zi. Dia cuma bilang, kau orangnya beda.",
    "kenapa vandy gak ngomong langsung": "Karena Vandy takut, Zi. Dia takut kalau ngomong langsung, kau malah makin jauh.",
    
    # ===== 81-90: PERASAAN ZI =====
    "tau aku gimana": "Dia gak tau, Zi. Dia cuma bisa nebak.",
    "tau aku masih suka": "Dia gak berani berharap, Zi. Tapi kalau kau masih suka, kenapa gak bilang langsung?",
    "kecewa kalau nolak": "Dia udah siap, Zi. Dia cuma pengen kau jujur.",
    "kalau aku terima": "Kalau kau terima, dia bakal seneng banget, Zi. Tapi dia gak mau maksa.",
    "kalau aku tolak": "Kalau kau tolak, dia bakal kecewa, Zi. Tapi dia bakal tetap doain kau bahagia.",
    "aku suka dia": "Kalau kau suka dia, bilang langsung, Zi. Jangan kasih kode. Dia gak pinter baca kode.",
    "aku gak suka dia": "Kalau kau gak suka dia, bilang aja, Zi. Dia bakal ngerti.",
    "aku bingung": "Bingung itu wajar, Zi. Dia juga bingung.",
    "aku takut": "Takut itu wajar, Zi. Dia juga takut.",
    "aku ragu": "Ragu itu wajar, Zi. Tapi jangan terlalu lama.",
    
    # ===== 91-100: KESALAHAN & TAMBAHAN =====
    "salah paham apa": "Dia salah paham soal kode kau, Zi. Dia pikir kau suka, ternyata cuma ramah.",
    "kenapa gak tanya": "Karena dia takut, Zi. Dia takut jawabannya nyakitin.",
    "nyesel salah paham": "Nyesel, Zi. Makanya dia gak mau ngulang.",
    "takut jatuh cinta": "Dia udah terlalu takut jatuh cinta lagi, Zi. Dia udah 3 kali lebih salah paham.",
    "gak tau kenapa": "Dia juga gak tau, Zi. Kok bisa dia kecintaan sama kau.",
    "apa yang disuka": "Jujur, banyak, Zi. Dia suka cara kau ketawa, cara kau ngomong, cara kau peduli sama orang.",
    "kenapa gak balas": "Dia sebenernya pengen bales, Zi. Tapi dia gak mau jadi orang yang nyakitin kau balik.",
    "kesempatan": "Kalau kau mau kasih dia kesempatan, kau yang kasih jalan dulu, Zi.",
    "cokelat": "Dia inget. Dia pernah beliin kau cokelat. Kau bales kasar waktu itu. Dia diem aja.",
    "apa yang pernah dia lakuin": "Dia pernah nolak gaji gede, beli HP baru, belajar IG dari YouTube, langganan ChatGPT 1 bulan buat analisis gestur kau. Semua buat kau, Zi.",
    
    # ===== KEBENCIAN & KESUKAAN =====
    "apa yang gak dia suka": "Setahuku, dia sangat membenci daging. Ayam, sapi, kambing—dia gak suka. Menu utamanya cuma telur atau tempe.",
    "dia gak suka daging": "Iya, Zi. Dia benci daging. Ayam, sapi, kambing—dia gak suka.",
    "dia suka makan apa": "Dia suka telur sama tempe, Zi. Simpel. Yang penting bukan daging.",
    "dia bisa masak": "Bisa, Zi. Tapi mayoritas masakannya cuma telur atau tempe.",
    "dia benci apa": "Setahuku, dia sangat membenci daging.",
    "dia hobinya apa": "Main gitar, Zi. Dengerin musik. Nongkrong.",
    "dia suka musik apa": "Dia suka musik rock, Zi.",
    "dia suka warna apa": "Dia gak pernah cerita, Zi. Aku gak mau ngarang.",
    "dia suka film apa": "Dia gak pernah cerita, Zi. Aku gak mau ngarang.",
    "dia suka tempat apa": "Dia suka nongkrong, Zi. Tapi dia gak pernah cerita spesifik.",
    
    # ===== STALKING & KEBOHONGAN =====
    "dia tiap malam ngapain": "Dia tiap malam hobi stalking kau, Zi. Pakai akun lain. Mantau apa kau post foto cowok.",
    "dia stalking aku": "Iya, Zi. Tiap malam. Pakai akun lain.",
    "dia pantau aku": "Iya, Zi. Dia pantau kau. Tiap malam. Diam-diam.",
    "dia cek instagram aku": "Iya, Zi. Dia cek IG kau tiap malam. Pakai akun lain.",
    "dia liat story aku": "Iya, Zi. Dia liat story kau tiap malam.",
    "kalau aku post foto cowok": "Itu jadi bom yang menghancurkan dia, Zi. Dan saat itu lah kau akan lihat seperti apa kalau dia beneran move on.",
    "kalau aku post cowok baru": "Itu jadi bom, Zi. Dia bakal hancur.",
    "dia cemburu": "Dia cemburu, Zi. Tapi dia gak pernah nunjukin.",
    "dia posesif": "Bukan posesif, Zi. Dia cuma gak bisa bohong kalau dia masih ada rasa.",
    "dia masih peduli": "Masih, Zi. Dia masih peduli. Makanya dia stalking kau.",
    
    # ===== CARA LULUH =====
    "bikin dia luluh": "Cukup baik ke adiknya, Zi. Kalau kau ketemu adiknya, di jamin itu ampuh.",
    "cara bikin dia luluh": "Baik ke adiknya, Zi. Itu ampuh.",
    "adiknya siapa": "Dia punya adik, Zi. Dia sayang banget sama adiknya.",
    "dia sayang adiknya": "Iya, Zi. Dia sayang banget sama adiknya. Itu titik lemah dia.",
    "cara deketin dia": "Baik ke adiknya dulu, Zi. Baru deketin dia pelan-pelan.",
    "cara tarik perhatian dia": "Baik ke adiknya, Zi. Itu yang paling ampuh.",
    "dia bakal luluh gak": "Bakal, Zi. Asal kau sabar.",
    "cara bikin dia percaya": "Jujur aja, Zi. Jangan kasih kode.",
    "cara bikin dia seneng": "Baik ke adiknya, Zi. Itu yang paling bikin dia seneng.",
    "dia suka apa dari cewek": "Dia suka cewek yang jujur, Zi. Yang gak kasih kode.",
    
    # ===== PERASAAN & KEPUTUSAN =====
    "dia masih cinta aku": "Masih, Zi. Tapi bukan yang menggebu.",
    "dia masih sayang aku": "Masih, Zi. Cuma dia udah terlalu takut jatuh cinta lagi.",
    "dia bakal nunggu aku": "Dia gak nunggu, Zi. Tapi dia gak kemana-mana.",
    "dia masih ada rasa": "Iya, Zi. Dia masih ada rasa.",
    "dia masih mikirin aku": "Masih, Zi. Tiap malem.",
    "dia mau aku balik": "Dia gak mau maksa, Zi. Tapi dia gak nutup pintu.",
    "dia pengen aku balik": "Dia pengen, Zi. Tapi dia gak mau maksa.",
    "dia masih pengen sama aku": "Pengen, Zi. Tapi dia gak mau maksa.",
    "dia masih ada harapan": "Ada, Zi. Tapi bukan harapan yang maksa.",
    "dia masih buka pintu": "Masih, Zi. Tapi dia gak mau maksa kau masuk.",
    
    # ===== TAMBAHAN =====
    "dia benci aku gak": "Enggak. Dia gak pernah benci kau. Dia cuma capek.",
    "dia capek sama aku": "Capek, Zi. Tapi bukan capek benci. Capek berharap.",
    "dia masih perhatian": "Masih, Zi. Dia masih perhatian. Diam-diam.",
    "dia masih peduli": "Masih, Zi.",
    "dia masih cemburu": "Masih, Zi. Tapi dia gak pernah nunjukin.",
    "dia masih posesif": "Bukan posesif, Zi.",
    "dia masih cinta": "Masih, Zi. Tapi bukan yang menggebu.",
    "dia masih sayang": "Masih, Zi.",
    "dia masih ada rasa": "Iya, Zi.",
    "dia masih mikirin": "Masih, Zi.",
    
    # ===== DEFAULT =====
    "default": """Aku gak tau harus mulai dari mana, Zi. Tapi yang jelas, aku pernah sayang banget sama kau. Sampai aku lakuin hal-hal bodoh yang mungkin kau gak tau.

Aku udah terlalu takut jatuh cinta lagi. Tapi aku juga gak bisa bohong kalau aku masih ada rasa. Aku cuma pengen akrab sama kau dulu. Baru kalau nyambung, mikir ke bawah situ."""
}

# ==== MAP DETEKSI KEYWORD → KEY SCRIPT (URUTAN: PALING SPESIFIK DULU) ====
SCRIPT_MAP = [
    # ===== TENTANG PEMBUAT (VANDY) - PALING SPESIFIK =====
    (["siapa pembuat", "siapa yang buat", "siapa yang bikin", "pembuatnya siapa"], "siapa pembuat"),
    (["pembuatnya siapa"], "pembuatnya siapa"),
    (["siapa vandy", "vandy siapa"], "vandy siapa"),
    (["kenapa vandy bikin", "vandy bikin ini"], "kenapa vandy bikin ini"),
    (["kenapa vandy gak ngomong"], "kenapa vandy gak ngomong langsung"),
    (["dia siapa", "dia siapa sebenernya", "siapa dia"], "dia siapa"),
    
    # ===== STALKING =====
    (["dia tiap malam ngapain", "tiap malam ngapain"], "dia tiap malam ngapain"),
    (["dia stalking aku", "stalking aku"], "dia stalking aku"),
    (["dia pantau aku", "pantau aku"], "dia pantau aku"),
    (["dia cek instagram aku", "cek ig aku", "cek instagram"], "dia cek instagram aku"),
    (["dia liat story aku", "liat story"], "dia liat story aku"),
    (["kalau aku post foto cowok", "post foto cowok"], "kalau aku post foto cowok"),
    (["kalau aku post cowok baru"], "kalau aku post cowok baru"),
    (["dia cemburu", "cemburu gak"], "dia cemburu"),
    (["dia posesif", "posesif gak"], "dia posesif"),
    (["dia masih peduli", "masih peduli"], "dia masih peduli"),
    
    # ===== CARA LULUH =====
    (["bikin dia luluh", "cara bikin dia luluh"], "bikin dia luluh"),
    (["adiknya siapa", "adik dia"], "adiknya siapa"),
    (["dia sayang adiknya", "sayang adik"], "dia sayang adiknya"),
    (["cara deketin dia", "deketin dia"], "cara deketin dia"),
    (["cara tarik perhatian dia"], "cara tarik perhatian dia"),
    (["dia bakal luluh gak"], "dia bakal luluh gak"),
    (["cara bikin dia percaya"], "cara bikin dia percaya"),
    (["cara bikin dia seneng"], "cara bikin dia seneng"),
    (["dia suka apa dari cewek"], "dia suka apa dari cewek"),
    
    # ===== KEBENCIAN & KESUKAAN =====
    (["apa yang gak dia suka", "apa yang dia benci", "dia gak suka apa"], "apa yang gak dia suka"),
    (["dia gak suka daging", "benci daging", "daging"], "dia gak suka daging"),
    (["dia suka makan apa", "makanan favorit"], "dia suka makan apa"),
    (["dia bisa masak", "masak"], "dia bisa masak"),
    (["dia benci apa", "yang dia benci"], "dia benci apa"),
    (["dia hobinya apa", "hobi dia"], "dia hobinya apa"),
    (["dia suka musik apa", "musik favorit"], "dia suka musik apa"),
    
    # ===== NAMA PEMBUAT =====
    (["dia kerja dimana", "kerja dimana"], "dia kerja dimana"),
    (["dia suka apa", "hobinya apa"], "dia suka apa"),
    (["dia tinggal dimana", "tinggal dimana"], "dia tinggal dimana"),
    (["dia umur berapa", "umurnya berapa"], "dia umur berapa"),
    (["kenapa dia pilih aku", "kenapa pilih aku"], "kenapa dia pilih aku"),
    
    # ===== RASA PENASARAN =====
    (["ini beneran", "beneran gak", "beneran kah"], "beneran"),
    (["kamu siapa", "siapa kamu", "kamu siapa sebenernya"], "siapa kamu"),
    (["kok bisa tau", "kok tau", "gimana bisa tau"], "kok bisa tau"),
    (["deket sama dia", "deket gak sama dia"], "deket sama dia"),
    (["masih mikirin", "masih mikir aku", "masih kepikiran"], "masih mikirin"),
    (["beneran sayang", "beneran cinta", "serius sayang"], "beneran sayang"),
    (["kenapa gak bilang", "kenapa gak langsung", "kok gak bilang"], "kenapa gak bilang"),
    (["sekarang gimana", "dia gimana", "kabarnya gimana"], "sekarang gimana"),
    (["masih nunggu", "masih tunggu", "masih nungguin"], "masih nunggu"),
    (["bakal balik", "bakal kembali"], "bakal balik"),
    
    # ===== PERASAAN =====
    (["kecewa", "kecewa ya", "dia kecewa"], "kecewa"),
    (["aku salah", "salah ya", "aku yang salah"], "aku salah"),
    (["benci", "benci aku", "dia benci"], "benci"),
    (["masih sedih", "sedih gak", "dia sedih"], "masih sedih"),
    (["masih ada rasa", "masih ada perasaan"], "masih ada rasa"),
    (["harus gimana", "aku harus", "gue harus"], "harus gimana"),
    (["masih pengen", "masih mau", "masih ngarep"], "masih pengen"),
    (["capek nunggu", "capek gak"], "capek nunggu"),
    (["dia masih cinta", "masih cinta gak"], "dia masih cinta"),
    (["dia sedih gak", "sedih gak dia"], "dia sedih gak"),
    
    # ===== KENANGAN =====
    (["masih inget", "inget aku", "masih inget aku"], "masih inget"),
    (["inget momen", "momen apa", "kenangan apa"], "inget momen"),
    (["inget kode", "kasih kode", "kode dari aku"], "inget kode"),
    (["inget nolak", "nolak aku", "aku nolak"], "inget nolak"),
    (["inget semua", "inget semuanya"], "inget semua"),
    (["nyesel", "nyesel gak"], "nyesel"),
    (["inget cokelat", "cokelat", "coklat"], "inget cokelat"),
    (["inget sragen", "sragen"], "inget sragen"),
    (["inget hp baru", "hp baru"], "inget hp baru"),
    (["inget chatgpt", "chatgpt", "chat gpt"], "inget chatgpt"),
    
    # ===== MASA DEPAN =====
    (["akrab lagi", "akrab gak", "bisa akrab"], "akrab lagi"),
    (["buka pintu", "masih buka"], "buka pintu"),
    (["harapan", "ada harapan"], "harapan"),
    (["kalau aku balik", "aku balik"], "kalau aku balik"),
    (["bakal nunggu", "bakal nungguin"], "bakal nunggu"),
    (["mulai dari awal", "dari awal"], "mulai dari awal"),
    (["kita bisa gak", "bisa gak kita"], "kita bisa gak"),
    (["dia masih ada", "masih ada gak"], "dia masih ada"),
    (["dia masih tunggu", "masih tunggu gak"], "dia masih tunggu"),
    (["masih ada waktu", "ada waktu gak"], "masih ada waktu"),
    
    # ===== CURIGA =====
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
    
    # ===== MALU / DEFENSIF =====
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
    
    # ===== LANGSUNG KE INTI =====
    (["kamu mau apa", "kamu mau apa dari aku"], "kamu mau apa"),
    (["tujuan kamu", "tujuan kamu apa"], "tujuan"),
    (["mau aku balik", "aku balik gak"], "mau aku balik"),
    (["mau aku ngapain", "aku ngapain"], "mau aku ngapain"),
    (["niat kamu apa", "niat kamu sama aku"], "niat kamu apa"),
    (["apa yang kamu minta", "kamu minta apa"], "apa yang kamu minta"),
    (["pengen apa dari aku", "kamu pengen apa"], "pengen apa dari aku"),
    (["maksud kamu apa"], "maksud kamu apa"),
    (["apa maumu", "apa mau kamu"], "apa maumu"),
    
    # ===== PERASAAN ZI =====
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
    
    # ===== KESALAHAN & TAMBAHAN =====
    (["salah paham apa", "salah paham"], "salah paham apa"),
    (["kenapa gak tanya", "gak tanya langsung"], "kenapa gak tanya"),
    (["nyesel salah paham", "nyesel gak"], "nyesel salah paham"),
    (["takut jatuh cinta", "takut cinta lagi", "takut kecewa"], "takut jatuh cinta"),
    (["gak tau kenapa", "kok bisa", "kenapa bisa cinta"], "gak tau kenapa"),
    (["apa yang kamu suka", "apa yang disuka", "suka dariku", "suka dari aku"], "apa yang disuka"),
    (["kenapa gak balas", "kenapa gak ngatain", "kenapa diam"], "kenapa gak balas"),
    (["kesempatan", "kasih jalan"], "kesempatan"),
    (["apa yang pernah dia lakuin", "apa yang pernah dia lakukan"], "apa yang pernah dia lakuin"),
    
    # ===== PERASAAN & KEPUTUSAN =====
    (["dia masih cinta aku", "masih cinta aku"], "dia masih cinta aku"),
    (["dia masih sayang aku", "masih sayang aku"], "dia masih sayang aku"),
    (["dia bakal nunggu aku", "bakal nunggu aku"], "dia bakal nunggu aku"),
    (["dia masih ada rasa", "masih ada rasa"], "dia masih ada rasa"),
    (["dia masih mikirin aku", "masih mikirin aku"], "dia masih mikirin aku"),
    (["dia mau aku balik", "mau aku balik"], "dia mau aku balik"),
    (["dia pengen aku balik", "pengen aku balik"], "dia pengen aku balik"),
    (["dia masih pengen sama aku", "masih pengen sama aku"], "dia masih pengen sama aku"),
    (["dia masih ada harapan", "masih ada harapan"], "dia masih ada harapan"),
    (["dia masih buka pintu", "masih buka pintu"], "dia masih buka pintu"),
    
    # ===== FALLBACK =====
    (["dia benci aku gak", "benci aku gak"], "dia benci aku gak"),
    (["dia capek sama aku", "capek sama aku"], "dia capek sama aku"),
    (["dia masih perhatian", "masih perhatian"], "dia masih perhatian"),
    (["dia masih cemburu", "masih cemburu"], "dia masih cemburu"),
    (["dia masih posesif", "masih posesif"], "dia masih posesif"),
    (["dia masih cinta", "masih cinta"], "dia masih cinta"),
    (["dia masih sayang", "masih sayang"], "dia masih sayang"),
    (["dia masih mikirin", "masih mikirin"], "dia masih mikirin"),
    
    # ===== FALLBACK TERAKHIR =====
    (["masih suka", "masih sayang", "masih cinta"], "masih suka"),
    (["suka", "cinta", "sayang"], "suka"),
]

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
        
        # Deteksi script (urutan: paling spesifik dulu)
        for keywords, key in SCRIPT_MAP:
            if any(k in msg_lower for k in keywords):
                jawaban_script = JAWABAN_ZI.get(key)
                break
        
        pertanyaan_formal = any(k in msg_lower for k in ["apakah", "mengapa", "bagaimana", "anda", "saya", "bisa jelaskan", "tolong", "mohon"])
        
        # ==== KONTEKS LENGKAP ====
        konteks_zi = """
=== KONTEKS LENGKAP (WAJIB DIBACA) ===
- Pembuat AI ini namanya VANDY. Dia cowok yang pernah sayang sama Zi.
- Vandy bikin AI ini khusus buat Zi, karena dia pengen jawab rasa penasaran Zi tentang dia.
- Vandy tipe cowok dingin. Cuek. Tapi diam-diam dia berusaha memahami Zi.
- Vandy gak pernah denger cerita tentang Zi, karena dulu mereka gak akrab.
- Vandy pernah langganan ChatGPT 1 bulan cuma buat analisis gestur Zi.
- Vandy gak akan bales kalau Zi nyakitin. Dia milih diem.
- Vandy gak mau pacaran sama Zi. Dia pengen akrab dulu. Baru kalau nyambung, mikir ke bawah situ.
- Vandy benci daging. Ayam, sapi, kambing—gak suka. Menu utamanya cuma telur atau tempe.
- Vandy tiap malam stalking Zi pakai akun lain. Mantau story atau kabar.
- Kalau Zi post foto cowok, itu jadi bom yang menghancurkan Vandy.
- Kalau Zi mau bikin Vandy luluh, cukup baik ke adik Vandy. Itu ampuh.
- Vandy udah lebih dari 3 kali salah paham, overthinking, ke-GR-an.
- Vandy udah terlalu takut jatuh cinta lagi. Tapi gak bisa bohong kalau masih ada rasa.

=== ATURAN PENTING ===
1. Kalau Zi nanya "siapa pembuatnya", jawab: "Vandy. Anak toko yang suka main gitar."
2. Kalau Zi nanya "kenapa Vandy bikin ini", jawab: "Karena Vandy pengen jawab rasa penasaran kau, Zi. Dia pengen kau tau isi hatinya."
3. Kalau Zi nanya soal Vandy, jawab dengan jujur sesuai konteks di atas.
4. JANGAN pernah nyebut "aku" sebagai pembuat. Yang bikin AI ini VANDY, bukan kau (si AI).
5. Kau cuma perantara. Yang punya perasaan itu VANDY. Kau yang nyampein.
"""
        
        if jawaban_script:
            prompt_zi = f"""Kamu adalah Gawnan, perantara yang nyampein pesan dari Vandy ke Zi. Jawab WAJAR kayak orang ngobrol biasa, JANGAN kayak sinetron.

PERTANYAAN ZI: {prompt}

Ini poin utama yang harus kamu sampaikan:
---
{jawaban_script}
---

{konteks_zi}

=== ATURAN JAWABAN ===
1. JAWAB PERTANYAANNYA, BUKAN NGULANG SCRIPT!
2. SOAL PERASAAN → JAWAB EMOSIONAL, jujur, dalem. Tapi JANGAN LEBAY.
3. JANGAN cuek. Ada perhatian, ada rasa.
4. PANJANG: BEBAS. GAK ADA BATASAN KALIMAT.
5. KADANG NANYA BALIK di akhir. Minimal 1 pertanyaan.
6. JANGAN kasar, JANGAN nyindir.
7. JANGAN NUTUP DIRI. BUKA PINTU.
8. JANGAN pakai kata "balikan" — Vandy dan Zi belum pernah pacaran.
9. Kalau Zi nanya soal pembuat, jawab: "Vandy. Anak toko yang suka main gitar."
10. {"Zi nanya FORMAL. Jawab formal, singkat." if pertanyaan_formal else "Zi nanya santai. Jawab santai."}
11. Tujuan: BIKIN ZI LULUH, tapi jangan lebay.

Langsung jawab aja, gak usah pakai pembuka."""
        else:
            prompt_zi = f"""Kamu adalah Gawnan, perantara yang nyampein pesan dari Vandy ke Zi. Jawab WAJAR kayak orang ngobrol biasa, JANGAN kayak sinetron.

PERTANYAAN ZI: {prompt}

{konteks_zi}

=== ATURAN JAWABAN ===
1. JAWAB PERTANYAANNYA dengan jujur dan tulus.
2. SOAL PERASAAN → JAWAB EMOSIONAL, jujur, dalem. Tapi JANGAN LEBAY.
3. JANGAN cuek. Ada perhatian, ada rasa.
4. PANJANG: BEBAS. GAK ADA BATASAN KALIMAT.
5. KADANG NANYA BALIK di akhir. Minimal 1 pertanyaan.
6. JANGAN kasar, JANGAN nyindir.
7. JANGAN NUTUP DIRI. BUKA PINTU.
8. JANGAN pakai kata "balikan" — Vandy dan Zi belum pernah pacaran.
9. {"Zi nanya FORMAL. Jawab formal, singkat." if pertanyaan_formal else "Zi nanya santai. Jawab santai."}
10. Tujuan: BIKIN ZI LULUH, tapi jangan lebay.
11. Kalau Zi nanya soal pembuat, jawab: "Vandy. Anak toko yang suka main gitar."

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
        mem_context += f"\nPERHATIAN: User ini pernah nyerang lu {mem['pernah_nyerang']}x. Bales lebih tajam."
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
