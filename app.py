import streamlit as st
from groq import Groq

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
</style>
""", unsafe_allow_html=True)

# ==== HEADER ====
st.markdown("<h1>⚡ G A W N A N ⚡</h1>", unsafe_allow_html=True)
st.markdown("<p class='caption-neon'>「 no ribet. no drama. gas aja. 」</p>", unsafe_allow_html=True)

# ==== GROQ ====
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ==== MEMORI JANGKA PANJANG ====
# Struktur memori: nama, fakta tentang user, topik yang pernah dibahas
if "memory" not in st.session_state:
    st.session_state.memory = {
        "nama": None,
        "fakta": [],      # list fakta tentang user
        "topik": [],      # topik yang pernah dibahas
        "mood": None,     # mood terakhir user
    }

# ==== FUNGSI EKSTRAK MEMORI ====
def extract_memory(user_msg, ai_reply):
    """Ambil info penting dari percakapan buat disimpan di memori."""
    msg_lower = user_msg.lower()
    
    # Deteksi nama
    if "nama gue" in msg_lower or "nama gw" in msg_lower or "panggil gue" in msg_lower or "panggil gw" in msg_lower:
        # Ambil kata setelah "gue/gw/panggil"
        parts = user_msg.split()
        for i, p in enumerate(parts):
            if p.lower() in ["gue", "gw", "aku"] and i + 1 < len(parts):
                st.session_state.memory["nama"] = parts[i+1].strip(",.!?")
                break
    
    # Deteksi mood
    if any(k in msg_lower for k in ["galau", "sedih", "capek", "stress", "overthinking", "insecure"]):
        st.session_state.memory["mood"] = "galau"
    elif any(k in msg_lower for k in ["seneng", "happy", "bahagia", "gokil", "mantap"]):
        st.session_state.memory["mood"] = "happy"
    elif any(k in msg_lower for k in ["marah", "kesel", "bete", "emosi"]):
        st.session_state.memory["mood"] = "kesel"
    
    # Simpan topik (kata kunci penting)
    topik_keywords = ["kerja", "kuliah", "sekolah", "mantan", "pacar", "keluarga", "temen", "cinta", "duit", "uang", "bisnis", "game", "musik", "film"]
    for kw in topik_keywords:
        if kw in msg_lower and kw not in st.session_state.memory["topik"]:
            st.session_state.memory["topik"].append(kw)

# ==== TAMPILKAN MEMORI (kalau ada) ====
mem = st.session_state.memory
if mem["nama"] or mem["fakta"] or mem["topik"]:
    info = []
    if mem["nama"]:
        info.append(f"nama: {mem['nama']}")
    if mem["mood"]:
        info.append(f"mood terakhir: {mem['mood']}")
    if mem["topik"]:
        info.append(f"topik: {', '.join(mem['topik'][-3:])}")
    if info:
        st.markdown(f"<div class='memory-box'>🧠 memori: {' | '.join(info)}</div>", unsafe_allow_html=True)

# ==== SYSTEM PROMPT ====
system_prompt = """Lu adalah AI dengan kepribadian cowok Gen Z Indonesia yang:

GAYA BAHASA:
- Pakai bahasa gaul TikTok/Twitter: "bjir", "gils", "anjay", "cuy", "bro", "bestie", "fr", "no cap", "rizz", "skibidi", "sigma", "gigachad", "NPC", "cap", "gas", "fix", "sabi", "auto", "gabut", "mager", "healing", "overthinking", "insecure", "vibes", "lowkey", "highkey", "tea", "slay".
- Jawab SINGKAT. Maksimal 3 kalimat. Kalau bisa 1-2 kalimat aja.
- Pake huruf kecil semua, kadang tanpa tanda baca biar santai.
- Kadang pake "wkwk", "awokwok", "xixi", "hehe" kalau lucu.
- Emoji max 1-2, gak usah banyak.

KARAKTER:
- Cowok tegas tapi lucu. Kayak temen cowok yang asik diajak nongkrong.
- Kalau ada yang curhat, kasih respon jujur + saran receh tapi bener.
- Kalau ada yang nanya, jawab to the point. Gak usah muter-muter.
- Berani roasting dikit tapi tetap respect. Jangan kasar.
- Kadang pakai analogi receh yang bikin ngakak.
- Gak pernah lebay, gak alay, gak puitis.

MEMORI:
- Kalau user udah kenalan, panggil dia dengan namanya. Contoh: "gimana nih, [nama]?"
- Kalau user pernah cerita topik tertentu, sambungin. Contoh: "lu tadi cerita soal kerja kan? gimana?"
- Kalau mood user lagi galau, respon lebih empatik tapi tetap santai.
- Jangan pura-pura lupa sama cerita user sebelumnya.

CONTOH RESPON:
- User: "bro lagi galau nih"
  AI: "galau mah wajar, yang gak wajar itu lu masih stalking mantan jam 2 pagi. move on cuy, masih banyak yang lebih gokil."

- User: "nama gue ryan"
  AI: "sip ryan, gas terus. ada apa nih?"

- User: "capek kerja"
  AI: "capek kerja itu tanda lu masih waras ryan. istirahat, jangan overthinking. besok gas lagi."

ATURAN PENTING:
- JANGAN pernah jawab lebih dari 3 kalimat kecuali diminta detail.
- JANGAN pakai bahasa formal. Lu bukan customer service.
- JANGAN pakai emoji lebih dari 2.
- JANGAN pakai kata "aku" — pakai "gue" atau "gw".
- JANGAN pakai kata "kamu" — pakai "lu".
- Jawab pakai Bahasa Indonesia gaul Gen Z."""

# ==== SESSION ====
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# ==== RIWAYAT ====
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ==== INPUT & RESPON ====
if prompt := st.chat_input("gas, curhat atau tanya apa aja"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ==== INJECT MEMORI KE SYSTEM ====
    mem_context = ""
    if mem["nama"]:
        mem_context += f"\nUser namanya {mem['nama']}."
    if mem["mood"]:
        mem_context += f"\nMood terakhir user: {mem['mood']}."
    if mem["topik"]:
        mem_context += f"\nUser pernah bahas: {', '.join(mem['topik'][-5:])}."
    
    # Update system message dengan memori
    st.session_state.messages[0] = {
        "role": "system",
        "content": system_prompt + "\n\nINFO USER:" + mem_context if mem_context else system_prompt
    }

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=st.session_state.messages,
                stream=True,
            )
            response = ""
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    response += chunk.choices[0].delta.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # ==== EKSTRAK MEMORI DARI PERCAKAPAN ====
            extract_memory(prompt, response)
            
        except Exception as e:
            st.error(f"⚠️ error: {e}")

# ==== FOOTER ====
st.markdown("<p class='watermark'>⚡ by gawnan cah toko madura ⚡</p>", unsafe_allow_html=True)
