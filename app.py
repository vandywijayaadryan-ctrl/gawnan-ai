import streamlit as st
from groq import Groq

# ==== KONFIG HALAMAN ====
st.set_page_config(page_title="Gawnan AI", page_icon="💜", layout="centered")

# ==== CSS TEMA NEON ====
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0014 0%, #1a0033 50%, #000000 100%);
        color: #00ffff;
    }
    h1 {
        color: #ff00ff;
        text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff, 0 0 40px #ff00ff;
        font-family: 'Courier New', monospace;
        text-align: center;
        letter-spacing: 3px;
    }
    .caption-neon {
        color: #00ffff;
        text-shadow: 0 0 5px #00ffff, 0 0 10px #00ffff;
        text-align: center;
        font-size: 13px;
        margin-bottom: 20px;
    }
    .stChatMessage {
        background: rgba(255, 0, 255, 0.05);
        border: 1px solid #ff00ff;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(255, 0, 255, 0.3);
    }
    .stChatInput input {
        background: #0a0014 !important;
        color: #00ffff !important;
        border: 2px solid #00ffff !important;
        box-shadow: 0 0 10px #00ffff;
    }
    .watermark {
        color: #00ffff;
        text-shadow: 0 0 8px #00ffff;
        text-align: center;
        font-size: 11px;
        margin-top: 30px;
        opacity: 0.7;
    }
</style>
""", unsafe_allow_html=True)

# ==== HEADER ====
st.markdown("<h1>💜 G A W N A N   A I 💜</h1>", unsafe_allow_html=True)
st.markdown("<p class='caption-neon'>「 AI Chatbot versi neon galau 」</p>", unsafe_allow_html=True)
st.markdown("<p class='watermark'>watermark: gawnan cah toko madura</p>", unsafe_allow_html=True)

# ==== GROQ CLIENT ====
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ==== SYSTEM PROMPT ====
system_prompt = """Kamu adalah AI chatbot dengan kepribadian anak Gen Z yang lagi galau karena patah hati.
Gaya bicaramu santai, gaul, pakai bahasa sehari-hari anak Gen Z (gils, anjir, cuy, bestie, healing, overthinking, red flag, green flag, ghosting, toxic, move on, baper, mager).
Jawab tetap informatif tapi santai, jangan kaku. Sesekali selipkan perasaan galau biar relate.
Jawab pakai Bahasa Indonesia gaul."""

# ==== SESSION STATE ====
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# ==== RIWAYAT CHAT ====
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ==== INPUT & RESPON ====
if prompt := st.chat_input("Mau curhat apa, bestie?"):
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
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"💔 error bre: {e}")
