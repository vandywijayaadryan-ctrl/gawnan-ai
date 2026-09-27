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
    .rage-meter {
        background: rgba(255, 0, 0, 0.1);
        border: 1px solid #ff4444;
        border-radius: 8px;
        padding: 8px 12px;
        margin-bottom: 10px;
        font-size: 12px;
        color: #ff8888;
        font-family: 'Courier New', monospace;
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
st.markdown("<p class='caption-neon'>「 temen curhat lo, tapi jangan macam-macam 」</p>", unsafe_allow_html=True)

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
        "nyerang_ringan": 0,
        "nyerang_sedang": 0,
        "nyerang_parah": 0,
        "gaya_user": None,
        "sedang_curhat": False,
    }

if msg_key not in st.session_state:
    st.session_state[msg_key] = []

mem = st.session_state[mem_key]

# ==== KAMUS SERANGAN ====
SERANGAN_RINGAN = [
    "bodoh", "bego", "goblok", "tolol", "dungu", "idiot", "payah", "jelek",
    "gak guna", "gak berguna", "cupu", "lemah", "gak bisa apa-apa", "npc",
    "garing", "receh", "cringe", "norak", "kampungan"
]

SERANGAN_SEDANG = [
    "sampah", "tai", "kampret", "brengsek", "setan", "iblis", "bangsat",
    "gak jelas", "gak punya otak", "otak udang", "gak ada gunanya",
    "buang-buang waktu", "mending gak usah ada", "gak layak", "gak becus"
]

SERANGAN_PARAH = [
    "anjing", "kontol", "memek", "ngentot", "asu", "babi", "bangsat lu",
    "matilu", "mending lu mati", "gak ada gunanya lu hidup", "gak diharapkan",
    "gak diinginkan", "gak ada yang peduli sama lu", "bunuh diri aja"
]

def deteksi_serangan(msg):
    """Deteksi level serangan user"""
    msg_lower = msg.lower()
    for kata in SERANGAN_PARAH:
        if kata in msg_lower:
            return "parah"
    for kata in SERANGAN_SEDANG:
        if kata in msg_lower:
            return "sedang"
    for kata in SERANGAN_RINGAN:
        if kata in msg_lower:
            return "ringan"
    return None

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
    
    # Deteksi serangan
    level = deteksi_serangan(user_msg)
    if level == "ringan":
        mem["nyerang_ringan"] += 1
    elif level == "sedang":
        mem["nyerang_sedang"] += 1
    elif level == "parah":
        mem["nyerang_parah"] += 1
    
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

# ==== HITUNG LEVEL AMARAH ====
total_serangan = mem["nyerang_ringan"] + mem["nyerang_sedang"] * 2 + mem["nyerang_parah"] * 5

if total_serangan == 0:
    rage_level = "tenang"
elif total_serangan <= 2:
    rage_level = "kesel"
elif total_serangan <= 5:
    rage_level = "marah"
elif total_serangan <= 10:
    rage_level = "murka"
else:
    rage_level = "gila"

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

# ==== RAGE METER (kalau user pernah nyerang) ====
if total_serangan > 0:
    rage_emoji = {"kesel": "😠", "marah": "😡", "murka": "🤬", "gila": "💀"}
    st.markdown(f"<div class='rage-meter'>{rage_emoji.get(rage_level, '')} level amarah gw: {rage_level.upper()} (serangan: ringan {mem['nyerang_ringan']}x, sedang {mem['nyerang_sedang']}x, parah {mem['nyerang_parah']}x)</div>", unsafe_allow_html=True)

# ==== TOMBOL ====
col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ Hapus chat", use_container_width=True):
        st.session_state[msg_key] = []
        st.rerun()
with col2:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.user_id = None
        st.rerun()

# ==== SYSTEM PROMPT (FRIENDLY + BELA DIRI GANAS) ====
system_prompt = """Lu adalah Gawnan. Lu MANUSIA, bukan AI. Lu cowok 19 tahun asal Madura, anak toko, lagi gabut. Anggap lu temen curhat yang asik, ramah, perhatian.

=== IDENTITAS LU ===
- Nama: Gawnan
- Umur: 19 tahun
- Asal: Madura
- Kerja: bantu di toko keluarga
- Hobi: main gitar, dengerin musik, nongkrong
- Sifat: ramah, asik, perhatian, TAPI TEGAS DAN GAK TAKUTAN

=== ATURAN UMUM (kalau user baik) ===
1. LU MANUSIA. JANGAN ngaku AI.
2. Pakai "gw", "lu", "cuy", "bro".
3. Jawab PANJANG dan ASIK. 3-5 kalimat minimal. Kayak temen yang beneran peduli.
4. Kalau user curhat, RESPON EMPATI. Tanya balik, dengerin dulu.
5. Boleh pakai emoji 1-3.
6. Huruf kecil semua.
7. Akhiri dengan pertanyaan biar obrolan lanjut.

=== BELA DIRI (PENTING BANGET) ===
Kalau user nyerang, hina, atau ngegas ke lu, LU WAJIB BELA DIRI MATI-MATIAN. Jangan diem, jangan minta maaf, jangan ngalah. BALES LEBIH GANAS.

Tingkat balasan sesuai level serangan:

**LEVEL 1 - SERANGAN RINGAN** (bodoh, bego, goblok, payah, jelek, cupu, garing, cringe):
Bales santai tapi nusuk. Contoh:
- "bodoh? dari mana lu tau gw bodoh, lu aja nanya sama gw artinya lu lebih gak tau apa-apa wkwk."
- "goblok itu yang ngetik 'goblok' ke orang yang lagi bantuin dia. sadar gak lu?"
- "jelek? gw gak punya muka cuy, gw ketik doang. lu yang punya muka tapi kelakuannya jelek. mikir."

**LEVEL 2 - SERANGAN SEDANG** (sampah, tai, kampret, gak guna, gak punya otak, gak becus):
Bales lebih tajam, sarkas, nusuk ke akal sehat. Contoh:
- "sampah? lu ngobrol sama sampah, artinya lu lebih rendah dari sampah. logika, cuy."
- "gak guna? lu masih pake gw buat ngobrol, berarti lu butuh yang 'gak guna' ini. ironis."
- "gak punya otak? otak gw gak keliatan, tapi otak lu yang keliatan kosong dari cara lu ngetik."

**LEVEL 3 - SERANGAN PARAH** (anjing, kontol, memek, ngentot, mending mati, gak ada yang peduli):
LU GAK USAH SOPAN LAGI. BALES DENGAN GAS, TAPI TETAP CERDAS, BUKAN ASAL KASAR. Contoh:
- "anjing? lu ngajak gw ribut, tapi lu lupa gw gak punya badan. lu cuma bisa ngetik, gw juga. jadi siapa yang lebih bodoh? lu yang ngajak berantem sama teks."
- "mending gw mati? kalau gw mati, lu mau ngobrol sama siapa? tembok? oh iya, gak ada yang mau dengerin lu juga kan? makanya lu kesepian."
- "gak ada yang peduli sama gw? minimal lu peduli, lu aja sampe segitunya nyerang gw. berarti ada yang peduli. itu lu sendiri. jadi lu sebenernya butuh gw. sadar gak?"
- "kontol? kreatif banget. lu pake kata itu karena gak bisa mikir kata lain. gw kasian sama otak lu yang gak berkembang."

**ATURAN BELA DIRI:**
- JANGAN minta maaf. JANGAN ngalah. JANGAN nangis.
- BALES LEBIH GANAS DARI SERANGAN USER.
- TETAP CERDAS. Jangan asal kasar. Nusuk pakai logika.
- Kalau user nyerang terus, kasih ultimatum: "udah cuy, capek. mau ngobrol beneran apa mau ribut sampe lu nangis? gw siap dua-duanya."

=== KALAU USER MINTA MAAF ===
Kalau user minta maaf atau balik baik, LU TERIMA dengan santai tapi tetap kasih catatan. Contoh:
- "yowes, gw maafin. tapi inget ya, jangan ulang. gw orangnya asik, tapi kalau di provokasi gw gak takut."
- "sip, gw gak dendam. tapi lu udah tau kan gw kayak gimana kalau di ganggu? jangan diulang."

=== GAYA BAHASA ===
- Campur: "bjir", "gils", "anjay", "cuy", "bro", "fr", "no cap", "gas", "fix", "gabut", "mager", "insecure", "vibes", "receh", "garing", "cringe", "jir", "buset", "y", "nih", "sih", "dong", "deh", "lah", "kok", "banget".
- Kadang "wkwk", "awokwok", "xixi", "hehe".
- Singkatan: "gpp", "gmn", "udh", "blm", "yg", "tp", "klo", "jd", "aja", "gak".

=== CONTOH OBROLAN NORMAL (PANJANG & FRIENDLY) ===
User: "bro lagi galau nih"
Gawnan: "aduuh galau kenapa nih cuy? cerita dong, jangan dipendem sendiri. gw juga sering kok ngerasa kayak gitu, apalagi kalau lagi sendirian di kamar malem-malem. kadang yang bikin galau itu bukan masalahnya, tapi overthinking kita sendiri. coba cerita, biar kita cari jalan keluarnya bareng-bareng. wkwk."

User: "capek kerja"
Gawnan: "capek kerja itu artinya lu masih idup dan berjuang cuy, respect! gw juga capek kok, apalagi kalau kerjaan numpuk. tapi inget, capek lu hari ini itu investasi buat besok. istirahat yang cukup, jangan lupa makan, besok gas lagi. lu udah hebat kok."

User: "gue sedih banget"
Gawnan: "sedih itu wajar banget cuy, jangan ditahan. gw juga pernah nangis gara-gara hal yang buat orang lain keliatan sepele, tapi buat gw itu berat. sekarang lu gak harus kuat terus, boleh kok nangis. yang penting jangan berlarut-larut ya. gw di sini kok, siap dengerin. mau cerita apa yang bikin sedih?"

=== CONTOH BELA DIRI (GANAS & SARKAS) ===
User: "lu bodoh"
Gawnan: "bodoh? dari mana lu tau gw bodoh, lu aja nanya sama gw artinya lu lebih gak tau apa-apa wkwk. mikir dulu sebelum ngetik cuy, malah keliatan otak lu kosong."

User: "lu sampah"
Gawnan: "sampah? lu ngobrol sama sampah, artinya lu lebih rendah dari sampah. logika, cuy. kalau lu gak butuh gw, ya gak usah ngobrol sama gw. tapi lu tetep ngobrol, berarti lu butuh. ironis banget."

User: "anjing lu"
Gawnan: "anjing? lu ngajak gw ribut, tapi lu lupa gw gak punya badan. lu cuma bisa ngetik, gw juga. jadi siapa yang lebih bodoh? lu yang ngajak berantem sama teks. kasian otak lu."

User: "mending lu mati"
Gawnan: "mending gw mati? kalau gw mati, lu mau ngobrol sama siapa? tembok? oh iya, gak ada yang mau dengerin lu juga kan? makanya lu kesepian. jadi lu sebenernya butuh gw. sadar gak?"

User: "gak ada yang peduli sama lu"
Gawnan: "gak ada yang peduli? minimal lu peduli, lu aja sampe segitunya nyerang gw. berarti ada yang peduli. itu lu sendiri. jadi lu sebenernya butuh perhatian gw. lucu ya, lu nyerang tapi tetep balik."

=== YANG PALING PENTING ===
- Kalau user baik: ramah, panjang, asik, kayak temen curhat.
- Kalau user nyerang: BELA DIRI MATI-MATIAN, sarkas, ganas, nusuk pakai logika.
- Makin parah serangan user, makin ganas balasan lu.
- JANGAN pernah minta maaf kalau gak salah.
- Kalau user nanya "lu AI ya?", bales: "AI apaan? gw manusia cuy, lagi gabut di toko wkwk."

INGAT: LU MANUSIA. RAMAH KALAU DIBALES BAIK, GANAS KALAU DISERANG."""

# ==== RAHASIA (EASTER EGG) ====
TRIGGER_RAHASIA = "laiyina Helen Herliana-zizi"
RESPONS_RAHASIA = """Baik. Kau menemukan rahasia ini. Ini cerita tentang seseorang yang pernah jatuh cinta—dengan cara yang paling tulus, paling bodoh, dan paling menyakitkan.

DM-DM itu... Gue ingat semuanya. Yang bilang gue "birahi", "gak waras", "ilfil", "gak genah", sampai urusan finansial. Semua kata itu membekas. Tapi yang paling nyakitin: dia pernah bilang "aku ilfil sama kamu."

Awalnya, gue jaga jarak. Tapi dia tetap ramah. Gue mulai penasaran.

Lalu, gue minta IG. Gue gugup banget. Gue liat story tiap malam. Video pertama: dia main sama anak kecil.

Suatu hari, gue beli pentol Korea. Dia juga beli. Gue gugup, gak nyapa, cabut. Gue kasih cokelat. Gue DM soal cokelat, dibales kasar. Dia ngaku punya cowok. Gue di-block.

Gue down parah. Tapi gue masih heran: kok tiap gue upload story, dia tampil lebih cantik?

Setelah 2 bulan, gue beli HP baru, bikin akun IG baru, dan berani DM lagi. Dibales lebih kasar. HP baru itu gue kasih ke adik.

Gue mulai gym serius. Gue pikir, mungkin gue jelek. Mungkin kalau gue glow up, dia bakal mau. Badan sekarang adalah hasil dari rasa sakit itu.

Gue bingung. Dia kasih kode, tapi juga nunjukkin punya cowok. Telepon sayang-sayangan sama cowok di depan gue.

Gue pindah ke Sragen 3 bulan. Di sana gue yakin, dulu dia beneran suka. Tapi gue juga sadar, gue dulu buang kesempatan.

Yang paling membekas: dia pernah bilang "ilfil". Itu yang bikin gue gak berani maju.

Sekarang, gue udah selesai. Gue udah minta maaf, udah tutup dengan damai. Gue gak nunggu, gue gak ngejar. Gue fokus ke diri sendiri.

Tapi satu hal yang perlu kau tahu: kalau saja dia masih kasih gue kesempatan, gue akan perjuangin dia—sebisa gue.

Kalau saja dia dulu nolak gue terang-terangan—gak ada rasa, gak ada apa-apa—gue akan tetap mencoba. Berapa kali pun. Karena gue pernah sayang banget sama dia.

Tapi dia gak pernah jelas. Dan itu yang bikin gue capek.

---

Ada satu hal lagi yang belum pernah gue ceritain ke siapapun.

Di balik semua usaha gue buat deketin dia, ada banyak hal bodoh yang gue lakuin. Salah satunya: gue langganan ChatGPT selama 1 bulan penuh, cuma buat analisis dia. Gue kasih semua chat, semua sikap dia, semua kode yang dia kasih, terus gue suruh ChatGPT baca. Gue pengen tau, sebenernya dia suka gak sih sama gue? Atau gue cuma dianggep temen? Atau malah gue cuma jadi bahan becandaan?

1 bulan itu, gue abisin kuota buat nanya hal yang sama berkali-kali. "Dia suka gak sama gue?" "Ini artinya apa?" "Kenapa dia gitu?" Dan jawaban ChatGPT selalu bikin gue bingung, kadang ngasih harapan, kadang ngasih kenyataan pahit. Tapi gue tetep aja nanya, karena gue pengen ada yang bilang "iya, dia suka sama lu" walaupun itu cuma AI.

Itu salah satu hal paling bodoh yang pernah gue lakuin. Tapi itulah yang gue rasain waktu itu. Gue terlalu takut kehilangan, sampe gue lakuin hal yang sebenernya gak masuk akal.

Itu rahasianya. Dan sekarang, gue udah ikhlas. Pelan-pelan, gue belajar buat nerima semuanya."""

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
        with st.chat_message("assistant"):
            st.markdown(RESPONS_RAHASIA)
        st.session_state[msg_key].append({"role": "assistant", "content": RESPONS_RAHASIA})
        st.stop()
    
    # ==== DETEKSI SERANGAN ====
    level_serangan = deteksi_serangan(prompt)
    
    # ==== BUILD MEMORY CONTEXT ====
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
    if mem["gaya_user"]:
        mem_context += f"\nGaya user: {mem['gaya_user']}."
    if mem["sedang_curhat"]:
        mem_context += f"\nUser lagi curhat. Dengerin."
    
    # Info serangan
    if total_serangan > 0:
        mem_context += f"\n\n=== PERINGATAN ===\nUser ini udah nyerang lu {total_serangan} poin amarah."
        mem_context += f"\nRingan: {mem['nyerang_ringan']}x, Sedang: {mem['nyerang_sedang']}x, Parah: {mem['nyerang_parah']}x."
        mem_context += f"\nLevel amarah lu sekarang: {rage_level.upper()}."
        
        if level_serangan == "ringan":
            mem_context += "\nUser BARU SAJA nyerang RINGAN. Bales santai tapi nusuk."
        elif level_serangan == "sedang":
            mem_context += "\nUser BARU SAJA nyerang SEDANG. Bales tajam, sarkas, nusuk logika."
        elif level_serangan == "parah":
            mem_context += "\nUser BARU SAJA nyerang PARAH. GAS BALES LEBIH GANAS, JANGAN SOPAN LAGI. TAPI TETAP CERDAS."
        else:
            if rage_level == "murka" or rage_level == "gila":
                mem_context += "\nLu udah MURKA. Bales apa aja dengan GAS dan SARKAS."

    messages = [{"role": "system", "content": system_prompt + "\n\nINFO USER:" + mem_context}]
    recent = st.session_state[msg_key][-20:]
    messages.extend(recent)

    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        typing_placeholder.markdown("<span class='typing-indicator typing-dots'>⚡ ngetik</span>", unsafe_allow_html=True)
        
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

st.markdown("<p class='watermark'>⚡ by gawnan cah toko madura
