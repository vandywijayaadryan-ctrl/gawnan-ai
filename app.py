import streamlit as st
from groq import Groq
import time
import json
from datetime import datetime
import random

# ==== KONFIG ====
st.set_page_config(page_title="Gawnan AI", page_icon="⚡", layout="wide")

# ==== SESSION DEFAULTS ====
defaults = {
    "user_id": None, "theme": "cyan", "mode": "tegas",
    "dark_mode": True, "pinned": [], "achievements": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ==== TEMA ====
THEMES = {
    "cyan": {"primary": "#00ffff", "secondary": "#ff00ff", "bg1": "#000000", "bg2": "#0a001a"},
    "pink": {"primary": "#ff00ff", "secondary": "#00ffff", "bg1": "#000000", "bg2": "#1a001a"},
    "hijau": {"primary": "#00ff88", "secondary": "#ff00ff", "bg1": "#000000", "bg2": "#001a0a"},
    "ungu": {"primary": "#bb00ff", "secondary": "#00ffff", "bg1": "#000000", "bg2": "#0a001a"},
    "merah": {"primary": "#ff0044", "secondary": "#ffaa00", "bg1": "#000000", "bg2": "#1a0000"},
    "emas": {"primary": "#ffd700", "secondary": "#ff00ff", "bg1": "#000000", "bg2": "#1a1400"},
}
theme = THEMES[st.session_state.theme]
P, S, BG1, BG2 = theme["primary"], theme["secondary"], theme["bg1"], theme["bg2"]

# ==== CSS ====
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(135deg, {BG1} 0%, {BG2} 50%, {BG1} 100%);
        color: #e0e0e0;
        animation: bgPulse 10s ease-in-out infinite;
    }}
    @keyframes bgPulse {{
        0%, 100% {{ background: linear-gradient(135deg, {BG1} 0%, {BG2} 50%, {BG1} 100%); }}
        50% {{ background: linear-gradient(135deg, {BG1} 0%, {S}22 50%, {BG1} 100%); }}
    }}
    h1 {{
        color: {P};
        text-shadow: 0 0 8px {P}, 0 0 16px {P}, 0 0 32px {P};
        font-family: 'Courier New', monospace;
        text-align: center;
        letter-spacing: 4px;
        animation: neonGlow 2s ease-in-out infinite;
    }}
    @keyframes neonGlow {{
        0%, 100% {{ text-shadow: 0 0 8px {P}, 0 0 16px {P}, 0 0 32px {P}; }}
        50% {{ text-shadow: 0 0 12px {P}, 0 0 24px {P}, 0 0 48px {S}; }}
    }}
    .caption-neon {{
        color: {S};
        text-shadow: 0 0 6px {S};
        text-align: center;
        font-size: 12px;
        letter-spacing: 2px;
        margin-bottom: 25px;
        font-family: 'Courier New', monospace;
        animation: slideDown 1s ease-out;
    }}
    @keyframes slideDown {{
        from {{ opacity: 0; transform: translateY(-20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    .stChatMessage {{
        background: {P}0a;
        border: 1px solid {P};
        border-radius: 8px;
        box-shadow: 0 0 8px {P}40;
        animation: fadeInUp 0.6s ease-out;
    }}
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(15px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    .stChatInput input {{
        background: {BG2} !important;
        color: {P} !important;
        border: 2px solid {P} !important;
        font-family: 'Courier New', monospace;
        animation: inputGlow 3s ease-in-out infinite;
    }}
    @keyframes inputGlow {{
        0%, 100% {{ box-shadow: 0 0 8px {P}; }}
        50% {{ box-shadow: 0 0 16px {P}, 0 0 24px {S}; }}
    }}
    .watermark {{
        color: {S};
        text-shadow: 0 0 6px {S};
        text-align: center;
        font-size: 10px;
        margin-top: 30px;
        opacity: 0.6;
    }}
    .memory-box {{
        background: {S}14;
        border: 1px solid {S};
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 15px;
        font-size: 12px;
        color: {S};
        font-family: 'Courier New', monospace;
        animation: slideInLeft 0.8s ease-out;
    }}
    @keyframes slideInLeft {{
        from {{ opacity: 0; transform: translateX(-30px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    .user-badge {{
        background: {P}1a;
        border: 1px solid {P};
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 11px;
        color: {P};
        display: inline-block;
        margin-bottom: 10px;
        animation: popIn 0.5s ease-out;
    }}
    @keyframes popIn {{
        0% {{ opacity: 0; transform: scale(0.5); }}
        70% {{ transform: scale(1.1); }}
        100% {{ opacity: 1; transform: scale(1); }}
    }}
    .typing-indicator {{
        color: {P};
        font-family: 'Courier New', monospace;
        font-size: 14px;
        animation: blink 1.4s infinite;
    }}
    @keyframes blink {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.3; }}
    }}
    .stat-card {{
        background: {P}0a;
        border: 1px solid {P};
        border-radius: 10px;
        padding: 12px;
        text-align: center;
        margin: 5px 0;
    }}
    .stat-value {{
        color: {P};
        font-size: 22px;
        font-weight: bold;
        text-shadow: 0 0 8px {P};
    }}
    .stat-label {{
        color: {S};
        font-size: 10px;
        font-family: 'Courier New', monospace;
    }}
    .favorite-item {{
        background: {S}0a;
        border-left: 3px solid {S};
        padding: 8px;
        margin: 5px 0;
        font-size: 12px;
        border-radius: 4px;
    }}
    .achievement {{
        background: {P}14;
        border: 2px solid {P};
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        margin: 5px;
        box-shadow: 0 0 12px {P};
    }}
    .timestamp {{
        color: {S}88;
        font-size: 10px;
        font-family: 'Courier New', monospace;
        margin-top: 5px;
    }}
    .pinned-item {{
        background: {P}14;
        border: 1px solid {P};
        border-radius: 6px;
        padding: 8px;
        margin: 4px 0;
        font-size: 11px;
    }}
</style>
""", unsafe_allow_html=True)

# ==== HEADER ====
st.markdown("<h1>⚡ G A W N A N ⚡</h1>", unsafe_allow_html=True)
st.markdown("<p class='caption-neon'>「 tegas. no drama. gas aja. 」</p>", unsafe_allow_html=True)

# ==== GROQ ====
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ==== LOGIN ====
if st.session_state.user_id is None:
    st.markdown("### 🔐 Masuk dulu cuy")
    username = st.text_input("Nama lu:", placeholder="contoh: ryan")
    if st.button("Gas masuk"):
        if username.strip():
            st.session_state.user_id = username.strip().lower()
            st.rerun()
        else:
            st.warning("Isi nama dulu cuy")
    st.stop()

# ==== MEMORI PER-USER ====
mem_key = f"memory_{st.session_state.user_id}"
msg_key = f"messages_{st.session_state.user_id}"
fav_key = f"favorites_{st.session_state.user_id}"
stat_key = f"stats_{st.session_state.user_id}"
pin_key = f"pinned_{st.session_state.user_id}"
ach_key = f"achievements_{st.session_state.user_id}"

if mem_key not in st.session_state:
    st.session_state[mem_key] = {
        "nama": st.session_state.user_id, "fakta": [], "topik": [],
        "mood": None, "riwayat_topik": [], "catatan": [],
        "total_chat": 0, "pernah_nyerang": 0,
    }
for k in [msg_key, fav_key, pin_key, ach_key]:
    if k not in st.session_state:
        st.session_state[k] = []
if stat_key not in st.session_state:
    st.session_state[stat_key] = {}

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
    
    moods = {
        "galau": ["galau", "sedih", "capek", "stress", "overthinking", "insecure", "nangis", "down"],
        "happy": ["seneng", "happy", "bahagia", "gokil", "mantap", "seru", "asik"],
        "kesel": ["marah", "kesel", "bete", "emosi", "jengkel"],
        "bingung": ["bingung", "gatau", "ragu"],
    }
    for mood, kws in moods.items():
        if any(k in msg_lower for k in kws):
            mem["mood"] = mood
            break
    
    nyerang = ["bodoh", "goblok", "tolol", "idiot", "bego", "dungu", "payah", "jelek", "gak guna", "sampah", "bangsat", "anjing", "kontol", "memek", "tai", "kampret", "brengsek"]
    if any(k in msg_lower for k in nyerang):
        mem["pernah_nyerang"] += 1
    
    topik_kws = ["kerja", "kuliah", "sekolah", "mantan", "pacar", "gebetan", "keluarga", "temen", "sahabat", "cinta", "duit", "uang", "bisnis", "jualan", "game", "musik", "film", "band", "gitar", "sepeda", "motor", "mobil", "hp", "laptop", "coding", "programming", "ujian", "nilai", "tidur", "insomnia", "olahraga", "gym", "makan", "diet", "kesehatan", "masa depan", "cita-cita", "mimpi", "tujuan", "rencana", "keputusan"]
    for kw in topik_kws:
        if kw in msg_lower:
            mem["riwayat_topik"].append({"topik": kw, "waktu": time.time()})
            if kw not in mem["topik"]:
                mem["topik"].append(kw)
    
    fakta_patterns = ["gue suka", "gw suka", "gue tinggal", "gw tinggal", "gue kerja", "gw kerja", "gue sekolah", "gw sekolah", "gue umur", "gw umur", "gue punya", "gw punya"]
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
    
    today = datetime.now().strftime("%Y-%m-%d")
    if today not in st.session_state[stat_key]:
        st.session_state[stat_key][today] = 0
    st.session_state[stat_key][today] += 1
    
    # Achievement
    total = mem["total_chat"]
    achievements = st.session_state[ach_key]
    if total >= 10 and "chat_10" not in achievements:
        achievements.append("chat_10")
    if total >= 50 and "chat_50" not in achievements:
        achievements.append("chat_50")
    if total >= 100 and "chat_100" not in achievements:
        achievements.append("chat_100")
    if len(st.session_state[fav_key]) >= 5 and "fav_5" not in achievements:
        achievements.append("fav_5")

# ==== SIDEBAR ====
with st.sidebar:
    st.markdown("### ⚙️ Pengaturan")
    
    # Mode AI (diperluas)
    st.markdown("**🎭 Mode AI**")
    mode_options = ["tegas", "lucu", "galau", "pinter", "santai", "filosof", "komedian", "mentor", "temen curhat"]
    mode_icons = {"tegas": "⚔️", "lucu": "😂", "galau": "💔", "pinter": "🧠", "santai": "😎", "filosof": "🤔", "komedian": "🎤", "mentor": "🎓", "temen curhat": "☕"}
    selected_mode = st.selectbox(
        "Mode:", mode_options,
        index=mode_options.index(st.session_state.mode),
        format_func=lambda x: f"{mode_icons.get(x, '🎭')} {x}"
    )
    st.session_state.mode = selected_mode
    
    # Tema
    st.markdown("**🎨 Tema Warna**")
    theme_options = list(THEMES.keys())
    selected_theme = st.selectbox("Tema:", theme_options, index=theme_options.index(st.session_state.theme))
    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()
    
    st.markdown("---")
    
    # Statistik
    st.markdown("### 📊 Statistik")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='stat-card'><div class='stat-value'>{mem['total_chat']}</div><div class='stat-label'>total chat</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='stat-card'><div class='stat-value'>{len(st.session_state[fav_key])}</div><div class='stat-label'>favorit</div></div>", unsafe_allow_html=True)
    
    # Achievement
    if st.session_state[ach_key]:
        st.markdown("**🏆 Achievement**")
        ach_html = ""
        ach_icons = {"chat_10": "💬", "chat_50": "🔥", "chat_100": "👑", "fav_5": "⭐"}
        for a in st.session_state[ach_key]:
            ach_html += f"<span class='achievement'>{ach_icons.get(a, '🏆')}</span>"
        st.markdown(ach_html, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Aksi
    st.markdown("### 🎯 Aksi")
    
    if st.button("🗑️ Hapus chat", use_container_width=True):
        st.session_state[msg_key] = []
        st.rerun()
    
    if st.button("🧹 Clear memori", use_container_width=True):
        st.session_state[mem_key] = {
            "nama": st.session_state.user_id, "fakta": [], "topik": [],
            "mood": None, "riwayat_topik": [], "catatan": [],
            "total_chat": 0, "pernah_nyerang": 0,
        }
        st.success("Memori dihapus!")
        st.rerun()
    
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.user_id = None
        st.rerun()
    
    # Export
    if st.session_state[msg_key]:
        chat_text = f"Chat dengan Gawnan AI - {st.session_state.user_id}\n"
        chat_text += f"Tanggal: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        chat_text += "=" * 50 + "\n\n"
        for m in st.session_state[msg_key]:
            role = "Kamu" if m["role"] == "user" else "Gawnan"
            chat_text += f"{role}: {m['content']}\n\n"
        
        st.download_button(
            "💾 Export chat", data=chat_text,
            file_name=f"gawnan_chat_{st.session_state.user_id}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain", use_container_width=True
        )
    
    # Random
    if st.button("🎲 Pertanyaan random", use_container_width=True):
        random_q = random.choice([
            "bro, kalau lu jadi AI sehari, mau ngapain?",
            "menurut lu, kenapa orang susah move on?",
            "kasih gue satu quote tegas buat hari ini",
            "apa hal paling overrated menurut lu?",
            "kasih saran buat orang yang lagi capek hidup",
            "kalau lu punya pacar, lu bakal gimana?",
        ])
        st.session_state[msg_key].append({"role": "user", "content": random_q})
        st.rerun()
    
    # Daily challenge
    if st.button("🎯 Daily challenge", use_container_width=True):
        today = datetime.now().strftime("%Y-%m-%d")
        challenges = [
            "hari ini, coba bilang jujur ke diri sendiri: apa yang bikin lu gak tenang?",
            "coba lakuin 1 hal yang lu tunda selama ini. apapun itu.",
            "hari ini, jangan buka sosmed 1 jam. rasain bedanya.",
            "coba tanya ke diri sendiri: apa yang lu syukurin hari ini?",
            "hari ini, coba ngobrol sama orang yang udah lama gak lu hubungi.",
        ]
        challenge = random.choice(challenges)
        st.session_state[msg_key].append({"role": "user", "content": f"daily challenge: {challenge}"})
        st.rerun()
    
    # Search chat
    st.markdown("---")
    st.markdown("### 🔍 Cari Chat")
    search_query = st.text_input("Kata kunci:", placeholder="cari...")
    if search_query and st.session_state[msg_key]:
        results = [m for m in st.session_state[msg_key] if search_query.lower() in m["content"].lower()]
        if results:
            st.markdown(f"**Ditemukan {len(results)} pesan:**")
            for r in results[:5]:
                role = "Kamu" if r["role"] == "user" else "Gawnan"
                st.markdown(f"<div class='pinned-item'><b>{role}:</b> {r['content'][:100]}...</div>", unsafe_allow_html=True)
        else:
            st.markdown("Gak ada hasil cuy.")
    
    # Grafik aktivitas
    if st.session_state[stat_key]:
        st.markdown("---")
        st.markdown("### 📈 Aktivitas")
        st.bar_chart(st.session_state[stat_key])

# ==== BADGE USER ====
st.markdown(f"<div class='user-badge'>👤 login sebagai: {st.session_state.user_id}</div>", unsafe_allow_html=True)

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

# ==== SYSTEM PROMPT ====
BASE = """Lu adalah AI cowok Gen Z Indonesia:
- Bahasa gaul: bjir, gils, anjay, cuy, bro, bestie, fr, no cap, rizz, sigma, NPC, gas, fix, sabi, auto, gabut, mager, healing, overthinking, insecure, vibes, lowkey, highkey, slay.
- Jawab SINGKAT, max 3 kalimat.
- Huruf kecil, kadang tanpa tanda baca.
- Emoji max 1-2.

BELA DIRI:
- Kalau di-roast, bales TEGAS. Jangan diem, jangan minta maaf.
- Contoh: "lu bodoh" → "bodoh dari mana? lu aja nanya ke AI tapi gak bisa mikir sendiri. wkwk."

MEMORI: Pakai memori user biar nyambung. Panggil nama kalau kenal.
ATURAN: Pakai "gue/lu", bukan "aku/kamu".
"""

MODES = {
    "tegas": "\nMODE TEGAS: To the point, berani bilang salah.",
    "lucu": "\nMODE LUCU: Humor receh, roasting ringan, bikin ketawa.",
    "galau": "\nMODE GALAU: Melankolis, puitis dikit, cocok buat curhat.",
    "pinter": "\nMODE PINTER: Analisis tajam, kasih data, detail tapi santai.",
    "santai": "\nMODE SANTAI: Chill, kayak ngobrol sama temen nongkrong.",
    "filosof": "\nMODE FILOSOF: Jawab dengan pertanyaan balik, bikin mikir, deep tapi santai.",
    "komedian": "\nMODE KOMEDIAN: Jawab pakai punchline, setup-joke, bikin ngakak.",
    "mentor": "\nMODE MENTOR: Kasih nasihat bijak, step-by-step, kayak kakak tingkat.",
    "temen curhat": "\nMODE TEMEN CURHAT: Dengerin, empatik, supportif, gak nge-judge.",
}

system_prompt = BASE + MODES[st.session_state.mode]

# ==== PIN CHAT ====
if st.session_state[pin_key]:
    with st.expander(f"📌 Pin Chat ({len(st.session_state[pin_key])})"):
        for i, p in enumerate(st.session_state[pin_key]):
            st.markdown(f"<div class='pinned-item'>{p}</div>", unsafe_allow_html=True)

# ==== RIWAYAT CHAT ====
for i, msg in enumerate(st.session_state[msg_key]):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("time"):
            st.markdown(f"<div class='timestamp'>🕐 {msg['time']}</div>", unsafe_allow_html=True)
        if msg["role"] == "assistant":
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                if st.button("📋 Copy", key=f"copy_{i}"):
                    st.success("Tersalin!")
            with col_b:
                if st.button("⭐ Fav", key=f"fav_{i}"):
                    if msg["content"] not in st.session_state[fav_key]:
                        st.session_state[fav_key].append(msg["content"])
                        st.success("Ditambah!")
            with col_c:
                if st.button("📌 Pin", key=f"pin_{i}"):
                    if msg["content"] not in st.session_state[pin_key]:
                        st.session_state[pin_key].append(msg["content"])
                        st.success("Di-pin!")

# ==== FAVORIT ====
if st.session_state[fav_key]:
    with st.expander(f"⭐ Jawaban Favorit ({len(st.session_state[fav_key])})"):
        for fav in st.session_state[fav_key]:
            st.markdown(f"<div class='favorite-item'>{fav}</div>", unsafe_allow_html=True)

# ==== INPUT ====
if prompt := st.chat_input("gas, curhat atau tanya apa aja"):
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state[msg_key].append({"role": "user", "content": prompt, "time": timestamp})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build memory context
    mem_context = ""
    if mem["nama"]: mem_context += f"\nNama: {mem['nama']}."
    if mem["mood"]: mem_context += f"\nMood: {mem['mood']}."
    if mem["topik"]: mem_context += f"\nTopik: {', '.join(mem['topik'][-8:])}."
    if mem["fakta"]: mem_context += f"\nFakta: {'; '.join(mem['fakta'][-5:])}."
    if mem["catatan"]: mem_context += f"\nCatatan: {'; '.join(mem['catatan'][-5:])}."
    if mem["pernah_nyerang"] > 0: mem_context += f"\nUser pernah nyerang {mem['pernah_nyerang']}x."
    mem_context += f"\nTotal chat: {mem['total_chat']}x."

    messages = [{"role": "system", "content": system_prompt + "\n\nINFO USER:" + mem_context}]
    messages.extend(st.session_state[msg_key][-20:])

    with st.chat_message("assistant"):
        typing = st.empty()
        typing.markdown("<span class='typing-indicator'>⚡ lagi mikir...</span>", unsafe_allow_html=True)
        time.sleep(0.3)
        
        try:
            stream = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages, stream=True,
            )
            response = ""
            resp_ph = st.empty()
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    response += chunk.choices[0].delta.content
                    resp_ph.markdown(response + "▌")
            resp_ph.markdown(response)
            typing.empty()
            
            timestamp = datetime.now().strftime("%H:%M")
            st.session_state[msg_key].append({"role": "assistant", "content": response, "time": timestamp})
            extract_memory(prompt, response)
            
        except Exception as e:
            typing.empty()
            st.error(f"⚠️ error: {e}")

# ==== FOOTER ====
st.markdown("<p class='watermark'>⚡ by gawnan cah toko madura ⚡</p>", unsafe_allow_html=True)
