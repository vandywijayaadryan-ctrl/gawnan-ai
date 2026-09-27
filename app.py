import streamlit as st
from groq import Groq
import time

# ==== KONFIG ====
st.set_page_config(page_title="Gawnan", page_icon="💬", layout="centered")

# ==== CSS ALA WHATSAPP ====
st.markdown("""
<style>
    .stApp {
        background-color: #0b141a;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'%3E%3Cg fill='%23182229' fill-opacity='0.4'%3E%3Cpath d='M10 10h5v5h-5zm20 0h5v5h-5zm20 0h5v5h-5zm20 0h5v5h-5zm-60 20h5v5h-5zm20 0h5v5h-5zm20 0h5v5h-5zm20 0h5v5h-5zm-60 20h5v5h-5zm20 0h5v5h-5zm20 0h5v5h-5zm20 0h5v5h-5zm-60 20h5v5h-5zm20 0h5v5h-5zm20 0h5v5h-5zm20 0h5v5h-5z'/%3E%3C/g%3E%3C/svg%3E");
    }
    h1 {
        color: #e9edef;
        font-family: 'Segoe UI', Roboto, sans-serif;
        text-align: center;
        font-size: 22px;
        font-weight: 500;
        letter-spacing: 1px;
        margin-bottom: 5px;
        padding-top: 10px;
    }
    .wa-header {
        background-color: #202c33;
        padding: 10px 15px;
        border-radius: 0 0 10px 10px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
    }
    .wa-header-title {
        color: #e9edef;
        font-family: 'Segoe UI', sans-serif;
        font-size: 16px;
        font-weight: 500;
        margin: 0;
    }
    .wa-header-status {
        color: #8696a0;
        font-size: 12px;
        margin-top: 2px;
    }
    .stChatMessage {
        background-color: #202c33 !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        margin: 6px 0 !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.3) !important;
        border: none !important;
        max-width: 85% !important;
        animation: fadeInUp 0.3s ease-out;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
        background-color: #005c4b !important;
        margin-left: auto !important;
        margin-right: 0 !important;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {
        background-color: #202c33 !important;
        margin-right: auto !important;
        margin-left: 0 !important;
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stChatInput input {
        background-color: #2a3942 !important;
        color: #e9edef !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 12px 18px !important;
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 15px !important;
    }
    .stChatInput input::placeholder {
        color: #8696a0 !important;
    }
    .watermark {
        color: #8696a0;
        text-align: center;
        font-size: 10px;
        margin-top: 20px;
        opacity: 0.5;
        font-family: 'Segoe UI', sans-serif;
    }
    .memory-box {
        background-color: #202c33;
        border-left: 3px solid #00a884;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 15px;
        font-size: 12px;
        color: #8696a0;
        font-family: 'Segoe UI', sans-serif;
    }
    .user-badge {
        background-color: #202c33;
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 12px;
        color: #00a884;
        display: inline-block;
        margin-bottom: 10px;
        font-family: 'Segoe UI', sans-serif;
    }
    .zi-mode {
        background-color: #202c33;
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 12px;
        color: #ff66aa;
        display: inline-block;
        margin-bottom: 10px;
        font-family: 'Segoe UI', sans-serif;
        animation: heartbeat 1.5s ease-in-out infinite;
    }
    @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.03); }
    }
    .typing-indicator {
        display: inline-block;
        color: #8696a0;
        font-family: 'Segoe UI', sans-serif;
        font-size: 13px;
        font-style: italic;
    }
    .stButton button {
        background-color: #202c33 !important;
        color: #00a884 !important;
        border: 1px solid #00a884 !important;
        border-radius: 8px !important;
        font-family: 'Segoe UI', sans-serif !important;
    }
    .stButton button:hover {
        background-color: #00a884 !important;
        color: #0b141a !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==== HEADER ALA WA ====
st.markdown("""
<div class="wa-header">
    <p class="wa-header-title">💬 Gawnan</p>
    <p class="wa-header-status">online</p>
</div>
""", unsafe_allow_html=True)

# ==== GROQ ====
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ==== LOGIN ====
if "user_id" not in st.session_state:
    st.session_state.user_id = None

if st.session_state.user_id is None:
    st.markdown("### 🔐 Masuk dulu cuy")
    st.markdown("Ketik nama lu biar gw bisa inget lu.")
    username = st.text_input("Nama lu:", placeholder="contoh: ryan")
    if st.button("Gas masuk"):
        if username.strip():
            st.session_state.user_id = username.strip().lower()
            st.rerun()
        else:
            st.warning("Isi nama dulu cuy")
    st.stop()

st.markdown(f"<div class='user-badge'>👤 login sebagai: {st.session_state.user_id}</div>", unsafe_allow_html=True)

# ==== BADGE MODE ZI ====
if st.session_state.get("mode_zi", False):
    st.markdown("<div class='zi-mode'>💗 mode Zi aktif</div>", unsafe_allow_html=True)

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
    st.markdown(f"<div class='memory-box'>🧠 memori: {' | '.join(info)}</div>", unsafe_allow_html=True)

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

# Pembukaan mode Zi - santai, gak spill
PEMBUKAAN_ZI = """Oke... kamu Zi kan?

Aku gak akan langsung cerita banyak. Kamu mau tanya apa aja, nanti aku jawab. Anggap aja lagi ngomong langsung sama aku.

Gas, tanya."""

JAWABAN_ZI = {
    "serang": """Karena aku gak bisa. Aku pernah sayang kamu. Dan aku gak akan nyakitin orang yang pernah aku sayang, meskipun dia nyakitin aku berkali-kali.

Tiap kali kamu kasar, aku selalu pengen bales. Tapi tiap kali aku buka chat, aku inget muka kamu. Dan aku gak tega. Bukan karena aku lemah, tapi karena kamu masih berarti buat aku.""",
    
    "suka": """Dulu iya. Aku suka banget. Aku rela nolak gaji gede, beli HP baru, belajar IG dari YouTube—semua buat kamu.

Sekarang? Aku udah selesai. Aku masih peduli, tapi aku gak nunggu. Aku cuma pengen kamu tau, dulu ada orang yang bener-bener sayang sama kamu.""",
    
    "kasar": """Karena kamu penting. Sampai untuk nyakitin kamu, aku selalu mikir: "Kalau aku kirim ini, gimana perasaan kamu?" Aku gak mau jadi orang yang sama kayak kamu.

Aku tau kamu punya alasan buat jadi kasar. Tapi aku gak mau nambah luka di hati kamu, Zi. Aku pernah ngerasain sakitnya.""",
    
    "masih suka": """Aku masih sayang. Tapi bukan yang menggebu. Sayang yang tenang, bercampur syukur dan sedikit sisa luka.

Dulu tiap malem aku mikirin kamu. Sekarang aku mikirin diri aku sendiri. Bukan karena gak peduli, tapi karena aku belajar peduli sama diri sendiri dulu.""",
    
    "balik": """Enggak. Aku udah selesai. Aku gak nunggu.

Aku udah ngejar kamu terlalu lama, Zi. Aku capek. Bukan capek sama kamu, tapi capek sama harapan yang gak pernah terwujud. Kalau kamu bahagia sama orang lain, aku ikhlas.""",
    
    "nyesel": """Enggak. Dari semua rasa sakit itu, aku jadi versi terbaik dari diriku sendiri.

Kamu pernah bilang aku jelek, aku ilfil. Semua kata itu bikin aku sadar, aku harus berubah. Bukan buat kamu, tapi buat diri aku sendiri. Jadi, makasih ya.""",
    
    "masih ada rasa": """Iya. Aku masih ada rasa. Aku gak bisa bohong.

Kalau aku udah gak ada rasa, aku bisa ngobrol biasa sama kamu. Tapi sampai sekarang, aku masih kaku. Itu karena aku masih cinta.""",
    
    "hancur": """Gak hancur. Aku cuma keliatan diam di hadapan kamu. Itu karena aku masih ada rasa. Bukan karena aku benci.""",
    
    "move on": """Belum. Aku masih berjuang buat lepas, tapi belum bisa. Tiap liat kamu, rasanya campur aduk.""",
    
    "ngaku": """Karena aku takut kehilangan kamu. Waktu itu ada orang random yang ngaku pacar kamu. Aku pikir itu akhir. Jadi aku ngaku—bukan karena buru-buru, tapi karena takut kehilangan.""",
    
    "gak peka": """Sorry ya. Aku gak pernah pacaran. Dari kecil aku cuma sibuk mikirin kerja. Jadi aku gak tau baca kode cewek. Aku bodoh dan gak peka.""",
    
    "masih pengen": """Aku gak ngarep sekarang. Tapi kalau suatu hari kamu kasih kesempatan, aku pengen kita akrab dulu. Bukan langsung pacaran—cuma akrab. Biar gak canggung.""",
    
    "sragen": """Aku pindah sementara 3 bulan dadakan. Di Sragen aku sering overthinking mikir kamu. Berkali-kali aku nanya bos, kapan bisa balik jaga toko yang ada kamu di seberang. Tapi ternyata 3 bulan. Janji bos cuma 10 hari.""",
    
    "sragen sendiri": """Di Sragen aku merantau sendiri, Zi. Kamu gak pernah ke sana. Aku yang nungguin kamu, tapi kamu gak pernah dateng. Jadi aku belajar, kadang orang yang kita tunggu, gak pernah dateng.""",
    
    "gym": """Enggak. Kamu cuma tau aku anak gym. Kita gak pernah gym bareng. Kamu cuma tau dari luar.""",
    
    "cafe": """Kita gak pernah ke cafe kecil itu. Gak pernah jalan bareng sekalipun. Gak pernah VHM bareng. Aku cuma bisa ngeliat kamu dari jauh.""",
    
    "momen ramah": """Aku masih inget. Waktu kamu jualan es, aku yang beli. Kamu ramah, aku pikir itu spesial. Ternyata cuma ramah kerja ya. Aku yang terlalu baper.""",
    
    "default": """Aku gak tau harus mulai dari mana, Zi. Tapi yang jelas, aku pernah sayang banget sama kamu. Sampai aku lakuin hal-hal bodoh yang mungkin kamu gak tau.

Sekarang aku udah ikhlas. Aku cuma pengen kamu tau, dulu ada orang yang bener-bener sayang sama kamu. Itu aja."""
}

# ==== RIWAYAT CHAT ====
for msg in st.session_state[msg_key]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==== INPUT & RESPON ====
if prompt := st.chat_input("Ketik pesan"):
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
        
        # Deteksi script
        if any(k in msg_lower for k in ["masih ada rasa", "masih ada perasaan"]):
            jawaban_script = JAWABAN_ZI["masih ada rasa"]
        elif any(k in msg_lower for k in ["hancur", "remuk"]):
            jawaban_script = JAWABAN_ZI["hancur"]
        elif any(k in msg_lower for k in ["move on", "moveon"]):
            jawaban_script = JAWABAN_ZI["move on"]
        elif any(k in msg_lower for k in ["ngaku", "kenapa ngaku", "dulu ngaku"]):
            jawaban_script = JAWABAN_ZI["ngaku"]
        elif any(k in msg_lower for k in ["gak peka", "peka"]):
            jawaban_script = JAWABAN_ZI["gak peka"]
        elif any(k in msg_lower for k in ["masih pengen", "masih mau", "masih ngarep"]):
            jawaban_script = JAWABAN_ZI["masih pengen"]
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
        elif any(k in msg_lower for k in ["balik", "kembali", "balikan"]):
            jawaban_script = JAWABAN_ZI["balik"]
        elif any(k in msg_lower for k in ["nyesel", "sesal", "penyesalan"]):
            jawaban_script = JAWABAN_ZI["nyesel"]
        
        # ==== EXPAND PAKAI AI (NATURAL, GAK LEBAY) ====
        if jawaban_script:
            prompt_zi = f"""Kamu adalah Gawnan, cowok yang pernah sayang sama Zi. Jawab kayak orang ngobrol biasa, jangan kayak sinetron.

Ini poin utama yang harus kamu sampaikan ke Zi:
---
{jawaban_script}
---

=== KONTEKS (JANGAN DISEBUT SEMUA, CUMA KALAU RELEVAN) ===
- Zi jualan es, lu yang beli. Dia ramah, tapi lu sadar itu cuma ramah kerja.
- Lu pernah beliin cokelat, dibales kasar.
- Zi pernah bilang "ilfil", pernah nge-block, ngaku punya cowok.
- Lu pernah ke Sragen 3 bulan sendirian. Zi gak pernah ke sana.
- Lu pernah langganan ChatGPT 1 bulan cuma buat analisis Zi.
- Lu gak pernah cafe bareng, gak pernah jalan bareng, gak pernah VHM bareng.
- Sekarang lu udah ikhlas, tapi masih ada sisa sayang yang tenang.
- Tujuan: bikin Zi ngeh kalau lu beneran cinta dia, tapi jangan lebay.

=== ATURAN JAWABAN ===
1. JAWAB WAJAR AJA. 2-4 kalimat cukup. Jangan dipaksa panjang.
2. JANGAN sebut semua kenangan sekaligus. Cuma 1 yang paling relevan.
3. JANGAN lebay, JANGAN puitis berlebihan, JANGAN kayak sinetron.
4. Bahasa santai kayak orang ngobrol. Boleh pendek, boleh agak panjang.
5. Tetap tulus dan jujur, tapi jangan dramatis.
6. Jangan kasar, jangan nyindir, jangan bikin dia merasa bersalah berlebihan.
7. Kadang gak usah diakhiri pertanyaan. Kadang cukup diem aja.
8. Tetap panggil "aku" dan "Zi" atau "kamu". Jangan "gw/lu" di mode ini.

Langsung jawab aja, gak usah pakai pembuka."""
        else:
            prompt_zi = """Kamu adalah Gawnan, cowok yang pernah sayang sama Zi. Jawab kayak orang ngobrol biasa, jangan kayak sinetron.

=== KONTEKS (JANGAN DISEBUT SEMUA, CUMA KALAU RELEVAN) ===
- Zi jualan es, lu yang beli. Dia ramah, tapi lu sadar itu cuma ramah kerja.
- Lu pernah beliin cokelat, dibales kasar.
- Zi pernah bilang "ilfil", pernah nge-block, ngaku punya cowok.
- Lu pernah ke Sragen 3 bulan sendirian. Zi gak pernah ke sana.
- Lu pernah langganan ChatGPT 1 bulan cuma buat analisis Zi.
- Lu gak pernah cafe bareng, gak pernah jalan bareng, gak pernah VHM bareng.
- Sekarang lu udah ikhlas, tapi masih ada sisa sayang yang tenang.
- Tujuan: bikin Zi ngeh kalau lu beneran cinta dia, tapi jangan lebay.

=== ATURAN JAWABAN ===
1. JAWAB WAJAR AJA. 2-4 kalimat cukup. Jangan dipaksa panjang.
2. JANGAN sebut semua kenangan sekaligus. Cuma 1 yang paling relevan.
3. JANGAN lebay, JANGAN puitis berlebihan, JANGAN kayak sinetron.
4. Bahasa santai kayak orang ngobrol. Boleh pendek, boleh agak panjang.
5. Tetap tulus dan jujur, tapi jangan dramatis.
6. Jangan kasar, jangan nyindir, jangan bikin dia merasa bersalah berlebihan.
7. Kadang gak usah diakhiri pertanyaan. Kadang cukup diem aja.
8. Tetap panggil "aku" dan "Zi" atau "kamu". Jangan "gw/lu" di mode ini.

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

st.markdown("<p class='watermark'>⚡ by gawnan cah toko madura ⚡</p>", unsafe_allow_html=True)
