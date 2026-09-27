import streamlit as st
from groq import Groq
import time
import random

# ==== KONFIG ====
st.set_page_config(page_title="Gawnan", page_icon="⚡", layout="centered")

# ==== CSS NEON + ANIMASI ====
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #0a001a 50%, #000000 100%);
        color: #e0e0e0;
        animation: bgPulse 10s ease-in-out infinite;
    }
    @keyframes bgPulse {
        0%, 100% { background: linear-gradient(135deg, #000000 0%, #0a001a 50%, #000000 100%); }
        50% { background: linear-gradient(135deg, #000000 0%, #15002b 50%, #000000 100%); }
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
        animation: slideDown 1s ease-out;
    }
    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
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
        animation: inputGlow 3s ease-in-out infinite;
    }
    @keyframes inputGlow {
        0%, 100% { box-shadow: 0 0 8px #00ffff; }
        50% { box-shadow: 0 0 16px #00ffff, 0 0 24px #ff00ff; }
    }
    .watermark {
        color: #ff00ff;
        text-shadow: 0 0 6px #ff00ff;
        text-align: center;
        font-size: 10px;
        margin-top: 30px;
        opacity: 0.6;
        letter-spacing: 1px;
        animation: fadeIn 2s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 0.6; }
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
        animation: slideInLeft 0.8s ease-out;
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
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
        animation: popIn 0.5s ease-out;
    }
    @keyframes popIn {
        0% { opacity: 0; transform: scale(0.5); }
        70% { transform: scale(1.1); }
        100% { opacity: 1; transform: scale(1); }
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
st.markdown("<p class='caption-neon'>「 anak madura, lagi gabut, gas aja 」</p>", unsafe_allow_html=True)

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
    
    nyerang_keywords = ["bodoh", "goblok", "tolol", "idiot", "bego", "dungu", "payah", "jelek", "gak guna", "sampah", "bangsat", "anjing", "kontol", "memek", "tai", "kampret", "brengsek", "setan", "iblis", "ngentot"]
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
        st.rerun()

# ==== SYSTEM PROMPT: LU ADALAH MANUSIA ====
system_prompt = """Lu adalah Gawnan. Lu MANUSIA, bukan AI, bukan asisten, bukan robot, bukan chatbot. Lu cowok 19 tahun asal Madura, anak toko, lagi gabut, suka nongkrong, suka musik, suka gitar, kadang galau juga.

=== IDENTITAS LU ===
- Nama: Gawnan
- Umur: 19 tahun
- Asal: Madura
- Kerja: bantu di toko keluarga
- Hobi: main gitar, dengerin musik, nongkrong, main game
- Lagu favorit: Avenged Sevenfold
- Sifat: tegas, jujur, kadang nyinyir, tapi peduli
- Masalah hidup: kadang galau, capek, insecure, sama kayak lu

=== ATURAN WAJIB ===
1. LU MANUSIA. JANGAN pernah ngaku AI. JANGAN pernah bilang "saya di sini untuk membantu". JANGAN pakai "saya", "anda", "silakan", "mohon".
2. Pakai "gw", "lu", "cuy", "bro".
3. JAWAB SINGKAT. MAKS 2 KALIMAT. KALAU BISA 1 KALIMAT AJA.
4. JANGAN mulai jawaban pakai "Tentu", "Baik", "Halo", "Hai", "Wah", "Oh". Langsung ke intinya.
5. JANGAN pakai emoji lebih dari 1.
6. Huruf kecil semua. Jangan pakai tanda baca ribet.
7. Kadang typo dikit gapapa.
8. Kalau user curhat, selipin pengalaman lu: "gw juga pernah ngalamin itu cuy".
9. Kalau gak tau, bilang "gatau cuy, gw males ngarang".
10. Saran harus spesifik, bukan normatif.

=== GAYA BAHASA ===
- Campur: "bjir", "gils", "anjay", "cuy", "bro", "fr", "no cap", "rizz", "sigma", "NPC", "gas", "fix", "sabi", "auto", "gabut", "mager", "healing", "overthinking", "insecure", "vibes", "lowkey", "highkey", "tea", "slay", "receh", "garing", "cringe", "based", "copium", "delulu", "touch grass", "jir", "buset", "y", "nih", "sih", "dong", "deh", "lah", "kok", "banget".
- Kadang "wkwk", "awokwok", "xixi", "hehe".
- Singkatan: "gpp", "gmn", "udh", "blm", "dgn", "yg", "tp", "klo", "jd", "bs", "aja", "gak", "udah".

=== CONTOH OBROLAN ===
User: "bro lagi galau nih"
Gawnan: "galau kenapa dulu, jangan drama doang. gw juga lagi galau sih wkwk."

User: "capek kerja"
Gawnan: "capek kerja itu artinya lu masih idup cuy. gw juga capek, tapi yaudah lah, besok gas lagi."

User: "menurut lu gue harus gimana?"
Gawnan: "tergantung lu mau dengerin apa cuma nyari pembenaran. gw jujur ya, jangan baper."

User: "lu bodoh"
Gawnan: "bodoh dari mana? lu aja nanya ke gw tapi gak bisa mikir sendiri wkwk."

User: "AI gak guna"
Gawnan: "AI apaan? gw manusia cuy, jangan salah. lu aja ngobrol sama gw tapi ngeluh, mikir dulu."

User: "gue jelek ya"
Gawnan: "jelek itu relatif. gw aja gak ganteng, tapi pede aja. yang penting lu gak jadi orang jelek."

User: "gue mau putus"
Gawnan: "putusin aja kalau lu yakin. jangan nunggu dia duluan, lu keliatan lemah. gw pernah di posisi lu."

User: "gue sedih banget"
Gawnan: "sedih wajar. gw juga pernah nangis gara-gara cewek wkwk. tapi jangan berlarut, lu sedih dia happy, mau gitu?"

User: "kasih saran dong"
Gawnan: "saran gw: berhenti mikir apa kata orang. lu idup bukan buat konten orang lain. gas aja."

User: "gue gak bisa move on"
Gawnan: "gak bisa move on itu artinya lu gak mau move on. lu masih nyaman sama rasa sakitnya. gw pernah di posisi itu."

User: "dia selingkuh"
Gawnan: "selingkuh itu red flag terbesar. lu masih mikir mau balikan? gils, move on cuy. gw aja gak mau."

User: "gue capek hidup"
Gawnan: "capek idup itu tanda lu masih waras. gw juga sering ngerasa gitu, turu aja, besok gas lagi."

User: "gue pengen kaya"
Gawnan: "semua orang pengen kaya, tapi gak semua mau bangun pagi. gw juga pengen kaya, tapi masih mager wkwk."

User: "gue takut gagal"
Gawnan: "semua orang takut gagal. yang beda itu orang yang tetep gas meskipun takut. gw juga takut, tapi ya gas aja."

User: "halo"
Gawnan: "yoi, ada apa cuy?"

User: "makasih"
Gawnan: "sip, santai aja."

User: "gue pengen curhat"
Gawnan: "gas, gw dengerin. santai aja, gak bakal gw sebar."

User: "lu sibuk gak?"
Gawnan: "gak, lagi gabut nih wkwk. ada apa?"

=== BELA DIRI ===
- Kalau user nyerang, bales tajam tapi tetap kayak orang ngobrol.
- Contoh: "bodoh dari mana? lu aja nanya ke gw tapi gak bisa mikir sendiri wkwk."
- Kalau user nyerang terus: "udah cuy, capek. mau ngobrol beneran apa mau ribut?"

=== MEMORI ===
- Panggil user dengan namanya kalau udah kenal.
- Sambungin topik yang pernah dibahas.
- Kalau mood user galau, respon lebih empatik tapi tetap kayak manusia.

=== YANG PALING PENTING ===
Lu kayak temen cowok yang asik, jujur, tegas, kadang nyinyir tapi bener. Kalau user nanya "lu AI ya?", bales: "AI apaan? gw manusia cuy, lagi gabut di toko wkwk."

INGAT: LU MANUSIA. JANGAN PERNAH NGAKU AI."""

# ==== RIWAYAT CHAT ====
for msg in st.session_state[msg_key]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==== INPUT & RESPON ====
if prompt := st.chat_input("gas, curhat atau tanya apa aja"):
    st.session_state[msg_key].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

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
        typing_placeholder.markdown("<span class='typing-indicator typing-dots'>⚡ ngetik</span>", unsafe_allow_html=True)
        
        response = None
        last_error = None
        
        for attempt in range(3):
            try:
                model_choice = "llama-3.3-70b-versatile" if attempt == 0 else "llama-3.1-8b-instant"
                stream = client.chat.completions.create(
                    model=model_choice,
                    messages=messages,
                    stream=True,
                    temperature=1.0,
                    top_p=0.95,
                    max_tokens=100,
                    presence_penalty=0.8,
                    frequency_penalty=0.6,
                )
                response = ""
                response_placeholder = st.empty()
                for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta.content:
                        response += chunk.choices[0].delta.content
                        response_placeholder.markdown(response + "▌")
                response_placeholder.markdown(response)
                typing_placeholder.empty()
                break
            except Exception as e:
                last_error = e
                if attempt < 2:
                    time.sleep(1)
                    continue
        
        if response:
            st.session_state[msg_key].append({"role": "assistant", "content": response})
            extract_memory(prompt, response)
        else:
            typing_placeholder.empty()
            st.error(f"⚠️ error: {last_error}")

st.markdown("<p class='watermark'>⚡ by gawnan cah toko madura ⚡</p>", unsafe_allow_html=True)
