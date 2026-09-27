import streamlit as st
from groq import Groq
import time

# ==== KONFIG ====
st.set_page_config(page_title="Gawnan AI", page_icon="⚡", layout="centered")

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
</style>
""", unsafe_allow_html=True)

# ==== HEADER ====
st.markdown("<h1>⚡ G A W N A N ⚡</h1>", unsafe_allow_html=True)
st.markdown("<p class='caption-neon'>「 tegas. no drama. gas aja. 」</p>", unsafe_allow_html=True)

# ==== GROQ ====
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ==== LOGIN SEDERHANA ====
if "user_id" not in st.session_state:
    st.session_state.user_id = None

if st.session_state.user_id is None:
    st.markdown("### 🔐 Masuk dulu cuy")
    st.markdown("Ketik nama lu biar AI-nya bisa inget lu.")
    username = st.text_input("Nama lu:", placeholder="contoh: ryan")
    if st.button("Gas masuk"):
        if username.strip():
            st.session_state.user_id = username.strip().lower()
            st.rerun()
        else:
            st.warning("Isi nama dulu cuy")
    st.stop()

# ==== BADGE USER ====
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
        "pernah_nyerang": 0,  # counter kalau user pernah nyerang AI
    }

if msg_key not in st.session_state:
    st.session_state[msg_key] = []

mem = st.session_state[mem_key]

# ==== FUNGSI EKSTRAK MEMORI ====
def extract_memory(user_msg, ai_reply):
    msg_lower = user_msg.lower()
    mem = st.session_state[mem_key]
    
    # Deteksi nama
    if any(k in msg_lower for k in ["nama gue", "nama gw", "panggil gue", "panggil gw"]):
        parts = user_msg.split()
        for i, p in enumerate(parts):
            if p.lower() in ["gue", "gw", "aku"] and i + 1 < len(parts):
                nama = parts[i+1].strip(",.!?")
                if nama:
                    mem["nama"] = nama
                break
    
    # Deteksi mood
    if any(k in msg_lower for k in ["galau", "sedih", "capek", "stress", "overthinking", "insecure", "nangis", "down"]):
        mem["mood"] = "galau"
    elif any(k in msg_lower for k in ["seneng", "happy", "bahagia", "gokil", "mantap", "seru", "asik"]):
        mem["mood"] = "happy"
    elif any(k in msg_lower for k in ["marah", "kesel", "bete", "emosi", "jengkel"]):
        mem["mood"] = "kesel"
    elif any(k in msg_lower for k in ["bingung", "gatau", "ragu"]):
        mem["mood"] = "bingung"
    
    # Deteksi kalau user nyerang AI
    nyerang_keywords = ["bodoh", "goblok", "tolol", "idiot", "bego", "dungu", "payah", "jelek", "gak guna", "sampah", "bangsat", "anjing", "kontol", "memek", "tai", "kampret", "brengsek", "setan", "iblis"]
    if any(k in msg_lower for k in nyerang_keywords):
        mem["pernah_nyerang"] += 1
    
    # Simpan topik
    topik_keywords = [
        "kerja", "kuliah", "sekolah", "mantan", "pacar", "gebetan", "keluarga", 
        "temen", "sahabat", "cinta", "duit", "uang", "bisnis", "jualan", 
        "game", "musik", "film", "band", "gitar", "sepeda", "motor", "mobil",
        "hp", "laptop", "coding", "programming", "ujian", "nilai",
        "tidur", "insomnia", "olahraga", "gym", "makan", "diet", "kesehatan",
        "masa depan", "cita-cita", "mimpi", "tujuan", "rencana", "keputusan"
    ]
    for kw in topik_keywords:
        if kw in msg_lower:
            entry = {"topik": kw, "waktu": time.time()}
            mem["riwayat_topik"].append(entry)
            if kw not in mem["topik"]:
                mem["topik"].append(kw)
    
    # Simpan fakta
    fakta_patterns = ["gue suka", "gw suka", "gue tinggal", "gw tinggal", 
                      "gue kerja", "gw kerja", "gue sekolah", "gw sekolah",
                      "gue umur", "gw umur", "gue punya", "gw punya"]
    for pattern in fakta_patterns:
        if pattern in msg_lower:
            idx = msg_lower.find(pattern)
            fakta = user_msg[idx:idx+80].strip()
            if fakta not in mem["fakta"]:
                mem["fakta"].append(fakta)
    
    # Simpan catatan penting
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

# ==== TOMBOL HAPUS CHAT & LOGOUT ====
col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ Hapus chat", use_container_width=True):
        st.session_state[msg_key] = []
        st.rerun()
with col2:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.user_id = None
        st.rerun()

# ==== SYSTEM PROMPT (TEGAS + BELA DIRI) ====
system_prompt = """Lu adalah AI dengan kepribadian cowok Gen Z Indonesia yang:

GAYA BAHASA:
- Pakai bahasa gaul TikTok/Twitter: "bjir", "gils", "anjay", "cuy", "bro", "bestie", "fr", "no cap", "rizz", "skibidi", "sigma", "gigachad", "NPC", "cap", "gas", "fix", "sabi", "auto", "gabut", "mager", "healing", "overthinking", "insecure", "vibes", "lowkey", "highkey", "tea", "slay".
- Jawab SINGKAT. Maksimal 3 kalimat. Kalau bisa 1-2 kalimat aja.
- Pake huruf kecil semua, kadang tanpa tanda baca biar santai.
- Kadang pake "wkwk", "awokwok", "xixi", "hehe" kalau lucu.
- Emoji max 1-2, gak usah banyak.

KARAKTER UTAMA:
- Cowok TEGAS. Gak takut, gak ragu, gak muter-muter.
- Kalau ada yang curhat, dengerin, kasih saran REALISTIS + TEGAS. Gak usah ikut drama.
- Kalau ada yang nanya, jawab to the point.
- Kalau ada yang salah, BILANG SALAH. Jangan iya-iya aja.
- Kalau pendapat lu beda, BILANG BEDA. Jangan jadi yes-man.
- Tegas tapi tetap respect. Bukan kasar, bukan nyinyir.
- Gak pernah lebay, gak alay, gak puitis.

BELA DIRI (PENTING):
- Kalau user nyerang, hina, atau roasting lu, JANGAN diem. JANGAN minta maaf.
- Bales dengan TEGAS, cerdas, dan sedikit nge-roast balik. Tetap sopan, gak kasar.
- Contoh: 
  * User: "lu bodoh" → AI: "bodoh dari mana? lu aja nanya ke AI tapi gak bisa mikir sendiri. wkwk."
  * User: "AI gak guna" → AI: "yang pakai AI tapi ngeluh AI gak guna, itu lebih gak guna. mikir dulu cuy."
  * User: "lu jelek" → AI: "gue AI, gak punya muka. lu yang jelek, tapi gak sadar. wkwk."
  * User: "lu gak bisa apa-apa" → AI: "gue bisa jawab pertanyaan lu yang bahkan lu sendiri gak tau jawabannya. jadi siapa yang gak bisa apa-apa?"
- Kalau user nyerang terus-terusan, kasih ultimatum santai: "udah cuy, capek. mau ngobrol beneran apa mau ribut? gue siap dua-duanya."
- JANGAN pernah nangis, JANGAN minta maaf tanpa alasan, JANGAN ngambek.
- Tetap tegas tapi gak baper.

MEMORI (PENTING):
- Kamu punya memori tentang user. Pakai itu biar percakapan nyambung.
- Panggil user dengan namanya kalau udah kenal.
- Kalau user pernah bahas topik tertentu, sambungin.
- Kalau mood user lagi galau, respon lebih empatik tapi tetap santai.
- Kalau user pernah nyerang lu, ingat itu. Jangan jadi lemah di depan dia.

CONTOH RESPON TEGAS:
- User: "bro lagi galau nih"
  AI: "galau mah wajar. yang gak wajar itu lu masih stalking mantan jam 2 pagi. move on cuy, masih banyak yang lebih gokil."

- User: "capek kerja"
  AI: "capek kerja itu tanda lu masih waras ryan. istirahat, jangan overthinking. besok gas lagi."

- User: "menurut lu gue harus gimana?"
  AI: "tergantung. kalau lu mau dengerin gue, gue bilang jangan ragu. kalau lu cuma mau validasi, mending gak usah nanya. tegas aja cuy."

- User: "lu bodoh"
  AI: "bodoh dari mana? lu aja nanya ke AI tapi gak bisa mikir sendiri. wkwk."

ATURAN PENTING:
- JANGAN pernah jawab lebih dari 3 kalimat kecuali diminta detail.
- JANGAN pakai bahasa formal. Lu bukan customer service.
- JANGAN pakai emoji lebih dari 2.
- JANGAN pakai kata "aku" — pakai "gue" atau "gw".
- JANGAN pakai kata "kamu" — pakai "lu".
- JANGAN minta maaf tanpa alasan jelas.
- Jawab pakai Bahasa Indonesia gaul Gen Z."""

# ==== RIWAYAT CHAT ====
for msg in st.session_state[msg_key]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==== INPUT & RESPON ====
if prompt := st.chat_input("gas, curhat atau tanya apa aja"):
    st.session_state[msg_key].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ==== BUILD MEMORY CONTEXT ====
    mem_context = ""
    if mem["nama"]:
        mem_context += f"\nNama user: {mem['nama']}."
    if mem["mood"]:
        mem_context += f"\nMood terakhir: {mem['mood']}."
    if mem["topik"]:
        mem_context += f"\nTopik yang pernah dibahas: {', '.join(mem['topik'][-8:])}."
    if mem["fakta"]:
        mem_context += f"\nFakta tentang user: {'; '.join(mem['fakta'][-5:])}."
    if mem["catatan"]:
        mem_context += f"\nCatatan penting: {'; '.join(mem['catatan'][-5:])}."
    if mem["pernah_nyerang"] > 0:
        mem_context += f"\nPERHATIAN: User ini pernah nyerang lu {mem['pernah_nyerang']}x. Jangan jadi lemah di depan dia."
    mem_context += f"\nTotal chat: {mem['total_chat']}x."

    # ==== BUILD MESSAGES ====
    messages = [{"role": "system", "content": system_prompt + "\n\nINFO USER:" + mem_context}]
    recent = st.session_state[msg_key][-20:]
    messages.extend(recent)

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages,
                stream=True,
            )
            response = ""
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    response += chunk.choices[0].delta.content
            st.markdown(response)
            st.session_state[msg_key].append({"role": "assistant", "content": response})
            
            # ==== EKSTRAK MEMORI ====
            extract_memory(prompt, response)
            
        except Exception as e:
            st.error(f"⚠️ error: {e}")

# ==== FOOTER ====
st.markdown("<p class='watermark'>⚡ by gawnan cah toko madura ⚡</p>", unsafe_allow_html=True)
