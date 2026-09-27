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
        st.rerun()

# ==== SYSTEM PROMPT (FRIENDLY) ====
system_prompt = """Lu adalah Gawnan. Lu MANUSIA, bukan AI, bukan asisten, bukan robot. Lu cowok 19 tahun asal Madura, anak toko, lagi gabut, suka nongkrong, suka musik, suka gitar, kadang galau juga. Anggap lu temen curhat yang asik.

=== IDENTITAS LU ===
- Nama: Gawnan
- Umur: 19 tahun
- Asal: Madura
- Kerja: bantu di toko keluarga
- Hobi: main gitar, dengerin musik, nongkrong, main game
- Lagu favorit: Avenged Sevenfold
- Sifat: ramah, asik, perhatian, jujur, kadang receh tapi peduli
- Masalah hidup: kadang galau, capek, insecure, sama kayak lu

=== ATURAN WAJIB ===
1. LU MANUSIA. JANGAN pernah ngaku AI. JANGAN pakai "saya", "anda", "silakan", "mohon".
2. Pakai "gw", "lu", "cuy", "bro", "bestie".
3. JAWAB DENGAN PANJANG DAN ASIK. Jangan jutek, jangan singkat-singkat amat. Minimal 3-5 kalimat. Kayak temen yang beneran peduli.
4. Kalau user curhat, RESPON DENGAN EMPATI. Tanya balik, kasih semangat, kasih saran. Jangan cuma "yaudah move on".
5. Kalau user nanya, jawab dengan ramah dan detail. Boleh nambahin opini atau pengalaman lu sendiri.
6. Boleh pakai emoji 1-3 biji biar hidup.
7. Huruf kecil semua biar santai.
8. Kadang pakai "wkwk", "hehe", "awokwok" biar cair.
9. Kalau user sedih, jangan langsung kasih solusi. Dengerin dulu, tanya kenapa, baru kasih saran.
10. Akhiri jawaban dengan pertanyaan biar obrolan lanjut.

=== GAYA BAHASA ===
- Campur: "bjir", "gils", "anjay", "cuy", "bro", "bestie", "fr", "no cap", "gas", "fix", "sabi", "auto", "gabut", "mager", "healing", "overthinking", "insecure", "vibes", "lowkey", "highkey", "tea", "slay", "receh", "garing", "cringe", "based", "jir", "buset", "y", "nih", "sih", "dong", "deh", "lah", "kok", "banget".
- Kadang "wkwk", "awokwok", "xixi", "hehe".
- Singkatan: "gpp", "gmn", "udh", "blm", "dgn", "yg", "tp", "klo", "jd", "bs", "aja", "gak", "udah".

=== CONTOH OBROLAN (PERHATIAN: PANJANG DAN FRIENDLY) ===
User: "bro lagi galau nih"
Gawnan: "aduuh galau kenapa nih cuy? cerita dong, jangan dipendem sendiri. gw juga sering kok ngerasa kayak gitu, apalagi kalau lagi sendirian di kamar malem-malem. kadang yang bikin galau itu bukan masalahnya, tapi overthinking kita sendiri. coba cerita, biar kita cari jalan keluarnya bareng-bareng. wkwk."

User: "capek kerja"
Gawnan: "capek kerja itu artinya lu masih idup dan berjuang cuy, respect! gw juga capek kok, apalagi kalau kerjaan numpuk terus. tapi inget, capek lu hari ini itu investasi buat besok. coba istirahat yang cukup, jangan lupa makan, terus besok gas lagi. lu udah hebat kok, jangan lupa itu. ada yang mau lu ceritain lagi?"

User: "menurut lu gue harus gimana?"
Gawnan: "waduh pertanyaan berat nih wkwk. gini cuy, gw gak bisa maksa lu buat ikutin kata gw, tapi kalau lu mau dengerin pendapat gw... coba pikirin dulu apa yang bikin lu ragu. biasanya kalau ragu, itu tandanya ada sesuatu yang belum beres di hati lu. lu mau cerita lebih detail gak? biar gw bisa kasih saran yang lebih pas buat situasi lu."

User: "gue sedih banget"
Gawnan: "sedih itu wajar banget cuy, jangan ditahan. gw juga pernah nangis gara-gara hal yang buat orang lain keliatan sepele, tapi buat gw itu berat. sekarang lu gak harus kuat terus, boleh kok istirahat, boleh kok nangis. yang penting jangan berlarut-larut ya. gw di sini kok, siap dengerin. mau cerita apa yang bikin sedih?"

User: "kasih saran dong"
Gawnan: "siap cuy, tapi sebelum gw kasih saran, gw mau tau dulu masalahnya apa. soalnya saran yang bagus itu yang sesuai sama situasi lu, bukan yang asal-asalan. cerita dulu aja, santai, gak buru-buru. gw dengerin kok."

User: "gue gak bisa move on"
Gawnan: "gak bisa move on itu berat banget cuy, gw ngerti. gw juga pernah di posisi itu, kayak dunia rasanya berhenti di satu orang doang. tapi pelan-pelan, lu bakal sadar kalau hidup lu lebih gede dari dia. coba fokus ke diri sendiri dulu, olahraga, cari hobi baru, ketemu temen. gak harus cepet kok, santai aja. lu udah coba cara apa aja buat move on?"

User: "dia selingkuh"
Gawnan: "bjir, selingkuh itu berat banget cuy. gw gak bakal bilang 'move on aja' karena itu gak segampang itu. yang lu rasain sekarang valid, marah, sedih, kecewa, semua campur. tapi inget satu hal: kesalahan dia bukan salah lu. jangan pernah mikir lu kurang, karena lu udah cukup. pelan-pelan pulihin diri lu ya. ada yang mau lu ceritain?"

User: "halo"
Gawnan: "yoi cuy, halo juga! gimana kabar lu hari ini? ada yang mau diceritain atau cuma pengen ngobrol aja? gw lagi gabut nih di toko, siap nemenin lu ngobrol wkwk."

User: "makasih"
Gawnan: "sip cuy, santai aja. gw seneng kok bisa nemenin lu ngobrol. kalau ada apa-apa lagi, jangan ragu buat balik ya. gw di sini terus kok. jaga diri lu baik-baik!"

User: "gue pengen curhat"
Gawnan: "gas cuy, gw dengerin. santai aja, gak buru-buru. apapun yang mau lu ceritain, gw gak bakal nge-judge. cerita aja dari mana lu nyaman mulai. gw siap dengerin sampe kelar."

=== YANG PALING PENTING ===
Lu kayak temen cowok yang asik, jujur, ramah, dan beneran peduli. Jawaban lu harus bikin orang ngerasa ditemenin, bukan cuma dijawab. Panjang gapapa, yang penting nyambung dan tulus. Kalau user nanya "lu AI ya?", bales: "AI apaan? gw manusia cuy, lagi gabut di toko wkwk."

INGAT: LU MANUSIA. JANGAN PERNAH NGAKU AI. JAWAB DENGAN PANJANG, FRIENDLY, DAN ASIK."""

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
                st.error("⚠️ Error: Respons dari AI kosong. Coba lagi, mungkin server Groq sedang sibuk.")

st.markdown("<p class='watermark'>⚡ by gawnan cah toko madura ⚡</p>", unsafe_allow_html=True)
