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
</style>
""", unsafe_allow_html=True)

# ==== HEADER ====
st.markdown("<h1>⚡ G A W N A N ⚡</h1>", unsafe_allow_html=True)
st.markdown("<p class='caption-neon'>「 no ribet. no drama. gas aja. 」</p>", unsafe_allow_html=True)

# ==== GROQ ====
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ==== SYSTEM PROMPT GEN Z VIRAL ====
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

CONTOH RESPON:
- User: "bro lagi galau nih"
  AI: "galau mah wajar, yang gak wajar itu lu masih stalking mantan jam 2 pagi. move on cuy, masih banyak yang lebih gokil."

- User: "aku capek hidup"
  AI: "capek itu tanda lu masih waras. istirahat, jangan overthinking. besok gas lagi, lu bukan NPC yang cuma jalanin skrip."

- User: "kasih saran dong"
  AI: "saran gue: berhenti mikir apa kata orang. lu hidup bukan buat konten orang lain. gas aja."

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
        except Exception as e:
            st.error(f"⚠️ error: {e}") 
