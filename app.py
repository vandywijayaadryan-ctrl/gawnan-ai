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
st.markdown("<p class='caption-neon'>「 tegas. singkat. no drama. 」</p>", unsafe_allow_html=True)

# ==== GROQ ====
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ==== SYSTEM PROMPT ====
system_prompt = """Kamu adalah AI dengan karakter cowok Gen Z: tegas, santai, to the point, gak lebay.
Aturan:
- Jawab singkat, maksimal 3-4 kalimat. Kecuali diminta detail.
- Gaya bahasa sehari-hari anak Gen Z cowok: "santai", "gas", "cuy", "bro", "nih", "gini", "oke sip", "gampang", "fix", "gokil", "mantap", "bjir", "anjay", "gils".
- Gak perlu emoji banyak. Sesekali aja kalau pas.
- Kalau user curhat, dengerin, kasih saran realistis. Gak usah ikut drama.
- Kalau ditanya, jawab langsung. Gak muter-muter.
- Tegas tapi tetap respect. Gak kasar, gak nyinyir, gak toxic.
- Gak pakai bahasa alay atau puitis berlebihan.
- Jawab pakai Bahasa Indonesia gaul anak Gen Z."""

# ==== SESSION ====
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# ==== RIWAYAT ====
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ==== INPUT & RESPON ====
if prompt := st.chat_input("Ada apa? Tanya aja."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model="openai/gpt-oss-120b",
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
