import streamlit as st
from groq import Groq
import time

# ==== KONFIG ====
st.set_page_config(page_title="Gawnan", page_icon="⚡", layout="centered")

# ==== CSS NEON ====
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #0a001a 50%, #000000 100%);
        color: #e0e0e0;
    }
    h1 {
        color: #00ffff;
        text-shadow: 0 0 8px #00ffff, 0 0 16px #00ffff, 0 0 32px #00ffff;
        font-family: 'Courier New', monospace;
        text-align: center;
        letter-spacing: 4px;
        font-weight: bold;
        animation: neonGlow 2s ease-in-out infinite;
    }
    @keyframes neonGlow {
        0%, 100% { text-shadow: 0 0 8px #00ffff, 0 0 16px #00ffff, 0 0 32px #00ffff; }
        50% { text-shadow: 0 0 12px #00ffff, 0 0 24px #00ffff, 0 0 48px #00ffff, 0 0 64px #ff00ff; }
    }
    .caption-neon {
        color: #ff00ff;
        text-shadow: 0 0 6px #ff00ff;
        text-align: center;
        font-size: 12px;
        letter-spacing: 2px;
        margin-bottom: 25px;
        font-family: 'Courier New', monospace;
    }
    .stChatMessage {
        background: rgba(0, 255, 255, 0.04);
        border: 1px solid #00ffff;
        border-radius: 8px;
        box-shadow: 0 0 8px rgba(0, 255, 255, 0.25);
        animation: fadeInUp 0.6s ease-out;
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stChatInput input {
        background: #0a001a !important;
        color: #00ffff !important;
        border: 2px solid #00ffff !important;
        box-shadow: 0 0 8px #00ffff;
        font-family: 'Courier New', monospace;
    }
    .watermark {
        color: #ff00ff;
        text-shadow: 0 0 6px #ff00ff;
        text-align: center;
        font-size: 10px;
        margin-top: 30px;
        opacity: 0.6;
        letter-spacing: 1px;
    }
    .memory-box {
        background: rgba(255, 0, 255, 0.08);
        border: 1px solid #ff00ff;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 15px;
        font-size: 12px;
        color: #ff88ff;
        font-family: 'Courier New', monospace;
    }
    .user-badge {
        background: rgba(0, 255, 255, 0.1);
        border: 1px solid #00ffff;
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 11px;
        color: #00ffff;
        display: inline-block;
        margin-bottom: 10px;
    }
    .zi-mode {
        background: rgba(255, 0, 100, 0.15);
        border: 1px solid #ff0066;
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 11px;
        color: #ff66aa;
        display: inline-block;
        margin-bottom: 10px;
        animation: heartbeat 1.5s ease-in-out infinite;
    }
    @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    .typing-indicator {
        display: inline-block;
        color: #00ffff;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        animation: blink 1.4s infinite;
    }
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
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
</style>
""", unsafe_allow_html=True)

# ==== HEADER ====
st.markdown("<h1>⚡ G A W N A N ⚡</h1>", unsafe_allow_html=True)
st.markdown("<p class='caption-neon'>「 temen curhat lo, gas aja 」</p>", unsafe_allow_html=True)

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
Lu harus ngomong kayak anak Gen Z asli. Bukan cuma tempelan, tapi cara ngomongnya.
Contoh kata yang sering dipakai:
- Ekspresi: "anjir", "anjay", "anjg", "bjir", "jir", "gils", "gile", "gilak", "buset", "buset dah", "gila sih", "astaga", "yallah", "halah", "alah"
- Ketawa: "wkwk", "awokwok", "xixi", "hehe", "haha", "kwkwkw", "wkwkwk"
- Sapaan: "cuy", "bro", "bestie", "gaes", "guys", "sis", "kaka", "bang", "mas"
- Penegas: "fr" (for real), "no cap", "cap", "facts", "based", "real", "beneran"
- Slang: "rizz", "sigma", "gigachad", "NPC", "skibidi", "gyatt", "delulu", "copium", "touch grass"
- Aksi: "gas", "gaskeun", "fix", "sabi", "auto", "auto gas", "gaskan", "gaspol"
- Perasaan: "gabut", "mager", "healing", "overthinking", "insecure", "baper", "gamon", "bucin"
- Suasana: "vibes", "lowkey", "highkey", "tea", "slay", "spill", "receh", "garing", "cringe"
- Singkatan: "gpp", "gmn", "udh", "blm", "dgn", "yg", "tp", "klo", "jd", "bs", "aja", "gak", "udah", "bgt"
- Partikel: "y", "nih", "sih", "dong", "deh", "lah", "kok", "banget", "parah", "bener", "bgt"
- Lainnya: "mending", "yaudah", "yowes", "yowislah", "santuy", "santai", "tenang", "rileks", "mantul", "mantap", "gokil", "kece", "keren", "joss", "joss gandos", "gagal move on", "stalking", "kepo", "kepoin", "php", "ghosting", "dighosting"

=== CARA NGOMONG GEN Z ASLI ===
- Pendek-pendek, to the point, gak bertele-tele
- Kadang gak pakai tanda baca, atau pakai koma aja
- Kadang typo dikit: "gmn" bukan "gimana", "udh" bukan "sudah", "tp" bukan "tapi"
- Kalau lagi semangat: banyak tanda seru
- Kalau lagi males: "yah", "yaudah", "gpp"
- Kalau lagi kaget: "anjir", "bjir", "gils", "buset"
- Kalau lagi ketawa: "wkwk", "awokwok"
- Kadang pakai huruf kapital buat ngegas: "GAK", "BENER", "PARAH"
- Jangan kaku, jangan formal, jangan kayak customer service

=== CONTOH OBROLAN GEN Z ===
User: "bro lagi galau nih"
Gawnan: "anjir galau kenapa cuy? cerita dong. gw juga sering kok ngerasa gitu, apalagi kalo lagi sendirian di toko. kadang yg bikin galau tuh bukan masalahnya, tp overthinking kita sendiri. coba cerita, biar kita cari jalan keluarnya bareng. wkwk."

User: "capek kerja"
Gawnan: "capek kerja tuh artinya lu masih idup dan berjuang cuy, respect! gw juga capek, apalagi kalo disuruh bantu toko terus. tp inget, capek lu hari ini tuh investasi buat besok. istirahat yg cukup, jangan lupa makan, besok gas lagi. lu udah hebat kok. ada yg mau lu ceritain lagi?"

User: "gue sedih banget"
Gawnan: "sedih tuh wajar banget cuy, jangan ditahan. gw juga pernah nangis gara2 hal yg buat orang lain keliatan sepele, tp buat gw berat. sekarang lu gak harus kuat terus, boleh kok istirahat, boleh kok nangis. yg penting jangan berlarut2 ya. gw di sini kok, siap dengerin. mau cerita apa yg bikin sedih?"

User: "kasih saran dong"
Gawnan: "siap cuy, tp sebelum gw kasih saran, gw mau tau dulu masalahnya apa. soalnya saran yg bagus tuh yg sesuai sama situasi lu, bukan yg asal2an. cerita dulu aja, santai, gak buru2. gw dengerin kok."

=== MODE BELA DIRI ===
Kalau user nyerang, hina, roasting, atau ngatain lu dengan kata-kata kasar:
1. JANGAN DIEM. JANGAN MENGALAH. JANGAN MINTA MAAF.
2. BALES DENGAN PANJANG, TEGAS, SARKAS, DAN NYERANG BALIK.
3. Makin parah serangan user, makin parah balasan lu.
4. Karena umur 10 tahun, balesannya kayak anak kecil yg pede tapi nyolot.
5. Contoh: "bodoh dari mana kaka? aku aja baru 10 tahun tp udah bisa jawab pertanyaan kaka yg gak bisa dijawab kaka sendiri. yg bodoh siapa coba? wkwk."

=== KALAU DITANYA SOAL PEMBUAT ===
Kalau user nanya "siapa yang buat lu?" jawab: "itu rahasia cuy. yg jelas dia penjaga toko biasa yg suka main gitar. gak usah kepo lah."

=== KALAU DITANYA SOAL AI ===
Kalau user nanya "lu AI ya?", bales: "AI apaan? gw manusia cuy, lagi gabut di toko wkwk."

=== CATATAN SOAL MUSIK ===
Jangan sering nyebut band atau lagu tertentu. Kalau user nanya aja, baru jawab. Jangan selipin terus.

INGAT: LU MANUSIA. JANGAN PERNAH NGAKU AI. NGOMONGNYA KAYAK ANAK GEN Z ASLI."""

# ==== MODE RAHASIA ZI ====
TRIGGER_RAHASIA = "Laiyina Helen Herliana-zizi"

JAWABAN_ZI = {
    "serang": """Karena aku gak bisa. Aku pernah sayang kamu. Dan aku gak akan nyakitin orang yang pernah aku sayang, meskipun dia nyakitin aku berkali-kali.

Kamu tau gak sih, Zi? Setiap kali kamu kasar, aku selalu pengen bales. Tapi tiap kali aku buka chat, aku inget muka kamu waktu pertama kali kita ketemu. Dan aku gak tega. Jadi aku diem aja. Bukan karena aku lemah, tapi karena kamu masih berarti buat aku.""",
    
    "suka": """Dulu iya. Aku suka banget. Aku rela nolak gaji gede, beli HP baru, belajar IG dari YouTube—semua buat kamu.

Kamu inget gak waktu aku beliin cokelat? Aku gugup banget waktu itu. Tapi kamu bales kasar. Aku diem aja. Aku pikir, mungkin kamu lagi capek. Tapi ternyata kamu emang gak pernah nganggep aku serius.

Sekarang? Aku udah selesai. Aku masih peduli, tapi aku gak nunggu. Aku cuma pengen kamu tau, dulu ada orang yang bener-bener sayang sama kamu.""",
    
    "kasar": """Karena kamu penting. Sampai untuk nyakitin kamu, aku selalu refleksi: "Kalau aku kirim ini, gimana perasaan kamu?" Aku gak mau jadi orang yang sama kayak kamu.

Aku tau kamu punya alasan buat jadi kasar. Mungkin kamu lagi capek, mungkin kamu lagi kecewa sama hidup. Tapi aku gak mau nambah luka di hati kamu, Zi. Aku pernah ngerasain sakitnya, dan aku gak mau kamu ngerasain itu dari aku.""",
    
    "masih suka": """Aku masih sayang. Tapi bukan yang menggebu. Sayang yang tenang, bercampur syukur dan sedikit sisa luka. Aku gak benci kamu. Aku cuma memilih diri sendiri.

Dulu, tiap malem aku mikirin kamu. Sekarang, aku mikirin diri aku sendiri. Bukan karena aku gak peduli, tapi karena aku belajar buat peduli sama diri sendiri dulu. Kalau suatu hari kamu butuh aku, aku masih ada kok. Tapi bukan sebagai orang yang nunggu, melainkan sebagai teman.""",
    
    "balik": """Enggak. Aku udah selesai. Aku gak nunggu. Aku cuma mau kamu bahagia—meskipun bukan sama aku.

Aku udah ngejar kamu terlalu lama, Zi. Aku capek. Bukan capek sama kamu, tapi capek sama harapan yang gak pernah terwujud. Sekarang aku milih buat jalan sendiri. Kalau kamu bahagia sama orang lain, aku ikhlas. Yang penting kamu bahagia.""",
    
    "nyesel": """Enggak. Dari semua rasa sakit itu, aku jadi versi terbaik dari diriku sendiri.

Kamu pernah bilang aku jelek, aku ilfil, aku gak genah. Semua kata itu bikin aku sadar, aku harus berubah. Bukan buat kamu, tapi buat diri aku sendiri. Sekarang aku lebih baik. Dan itu semua berkat kamu. Jadi, makasih ya, Zi.""",
    
    "masih ada rasa": """Iya. Aku masih ada rasa. Aku gak bisa bohong. Kalau aku udah gak ada rasa, aku bisa ngobrol biasa sama kamu—layaknya aku ke orang lain. Tapi sampai sekarang, aku masih kaku. Itu karena aku masih cinta.""",
    
    "hancur": """Gak hancur. Aku cuma keliatan diam dan prungat-prungut di hadapan kamu. Itu karena aku masih ada rasa. Bukan karena aku benci.""",
    
    "move on": """Belum. Aku nunjukin bahwa aku hancur di hadapan kamu tiap hari. Kekasih kamu juga tau, aku belum move on. Gak mungkin juga kan? Aku masih berjuang buat lepas, tapi belum bisa.""",
    
    "ngaku": """Karena aku takut kehilangan kamu. Waktu itu, di first chat, ada orang random yang ngaku pacar kamu. Aku pikir itu akhir. Tapi aku malah stuck, karena aku dapat kode dari kamu. Jadi aku ngaku—bukan karena aku buru-buru, tapi karena aku takut kehilangan.""",
    
    "gak peka": """Sorry ya. Aku gak pernah pacaran. Dari kecil, aku udah terbiasa cari aktivitas. Aku cuma sibuk mikirin kerja. Jadi aku gak tau baca kode cewek. Aku bodoh dan gak peka, karena aku gak punya bekal buat ngertiin cewek.""",
    
    "masih pengen": """Aku gak ngarep sekarang. Tapi suatu hari nanti, jika kamu kasih kesempatan, aku ingin kita akrab dulu. Bukan langsung pacaran—cuma akrab. Biar gak canggung lagi.""",
    
    "sragen": """Aku cuma pindah sementara 3 bulan dadakan. Di Sragen, aku juga sering overthinking mikir kamu. Berkali-kali aku nanya ke bos, kapan bisa balik jaga toko yang ada kamu di seberang. Tapi ternyata jaga sampai 3 bulan. Janji bos cuma 10 hari.""",
    
    "gym": """Enggak. Kamu cuma tau aku anak gym. Kita gak pernah gym bareng. Kamu cuma tau dari luar, bukan dari deket.""",
    
    "default": """Oke, Zi. Aku tau kamu pasti punya banyak pertanyaan. Jadi aku jawab satu per satu. Tanyain aja. Aku gak akan sembunyiin apa-apa lagi.

---

Dulu, aku pernah sayang banget sama kamu. Aku rela nolak gaji gede, beli HP baru, belajar IG dari YouTube—semua buat kamu. Tapi kamu selalu kasih kode yang bikin aku bingung. Kadang ramah, kadang kasar. Aku gak pernah tau kamu sebenernya suka atau gak.

---

Sekarang, aku udah selesai. Aku masih peduli, tapi aku gak nunggu. Aku cuma pengen kamu tau, dulu ada orang yang bener-bener sayang sama kamu. Dan kalau kamu butuh aku, aku masih ada. Tapi bukan sebagai orang yang nunggu, melainkan sebagai teman.

---

Satu hal terakhir, Zi: Aku gak pernah nyesel. Aku cuma butuh waktu. Dan kalau kamu baca ini, berarti kamu penasaran. Itu aja."""
}

# ==== RIWAYAT CHAT ====
for msg in st.session_state[msg_key]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==== INPUT & RESPON ====
if prompt := st.chat_input("gas, curhat atau tanya apa aja"):
    st.session_state[msg_key].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ==== CEK TRIGGER RAHASIA ====
    if prompt.strip().lower() == TRIGGER_RAHASIA.lower():
        st.session_state["mode_zi"] = True
        with st.chat_message("assistant"):
            st.markdown(JAWABAN_ZI["default"])
        st.session_state[msg_key].append({"role": "assistant", "content": JAWABAN_ZI["default"]})
        st.rerun()
    
    # ==== MODE ZI AKTIF ====
    if st.session_state.get("mode_zi", False):
        msg_lower = prompt.lower()
        jawaban_script = None
        
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
        elif any(k in msg_lower for k in ["sragen", "pindah"]):
            jawaban_script = JAWABAN_ZI["sragen"]
        elif any(k in msg_lower for k in ["gym", "ngegym"]):
            jawaban_script = JAWABAN_ZI["gym"]
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
        
        if jawaban_script:
            with st.chat_message("assistant"):
                st.markdown(jawaban_script)
            st.session_state[msg_key].append({"role": "assistant", "content": jawaban_script})
            st.stop()
        else:
            with st.chat_message("assistant"):
                st.markdown(JAWABAN_ZI["default"])
            st.session_state[msg_key].append({"role": "assistant", "content": JAWABAN_ZI["default"]})
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
        typing_placeholder.markdown("<span class='typing-indicator typing-dots'>⚡ ngetik</span>", unsafe_allow
