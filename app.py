import streamlit as st
from groq import Groq

st.set_page_config(page_title="Gawnan AI", page_icon="💔")

st.title("💔 Gawnan AI")
st.caption("Watermark: gawnan cah toko madura")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

system_prompt = """Kamu adalah AI chatbot Gen Z yang lagi galau karena patah hati.
Gaya bicara santai, gaul (gils, anjir, cuy, bestie, healing, overthinking, red flag, ghosting, toxic, move on, baper).
Jawab pakai Bahasa Indonesia gaul, sesekali selipkan perasaan galau."""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("Mau curhat apa, bestie?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
