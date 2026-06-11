"""
app_streamlit.py  –  Ngapain di Rumah? (Streamlit Version)
Deploy ke Streamlit Cloud tanpa ubah engine.py / transaksi.py / data_wisata.py
"""

import streamlit as st

# ─── Konfigurasi halaman ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ngapain di Rumah? 🌏",
    page_icon="🗺️",
    layout="centered",
)

# ─── Inject CSS ringan ───────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Sembunyikan header/footer Streamlit default */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Bubble chat user lebih kanan */
    .stChatMessage[data-testid="stChatMessageUser"] {
        background: #e8f4fd;
        border-radius: 16px 16px 4px 16px;
    }
</style>
""", unsafe_allow_html=True)

# ─── Import engine (harus ada di folder yang sama) ───────────────────────────
try:
    from engine import proses_pesan, SALAM_AWAL
except ImportError:
    st.error("❌ File `engine.py` tidak ditemukan di folder yang sama dengan `app_streamlit.py`.")
    st.stop()

# ─── Session state ────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Sapa user pertama kali
    st.session_state.messages.append({
        "role": "assistant",
        "content": SALAM_AWAL,
    })

# ID sesi tetap selama tab browser aktif
SESSION_ID = "streamlit_user"

# ─── Judul aplikasi ───────────────────────────────────────────────────────────
st.title("🗺️ Ngapain di Rumah?")
st.caption("Chatbot wisata Indonesia — tiket, destinasi, dan keranjang dalam satu chat.")

st.divider()

# ─── Tampilkan riwayat chat ───────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        # Markdown agar bold (*teks*) dan newline tampil rapi
        st.markdown(msg["content"])

# ─── Input pengguna ───────────────────────────────────────────────────────────
if prompt := st.chat_input("Ketik pesan... (contoh: cari borobudur)"):

    # Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Proses lewat engine yang sudah ada
    with st.chat_message("assistant"):
        with st.spinner("Mencari..."):
            response = proses_pesan(prompt, SESSION_ID)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

# ─── Tombol reset di sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Pengaturan")

    if st.button("🔄 Reset Percakapan", use_container_width=True):
        st.session_state.messages = [{
            "role": "assistant",
            "content": SALAM_AWAL,
        }]
        # Reset sesi engine juga
        from engine import reset_sesi
        reset_sesi(SESSION_ID)
        st.rerun()

    st.divider()
    st.markdown("**Perintah cepat:**")
    st.code("provinsi\ncari [kota/tempat]\npesan [destinasi]\nsimpan [destinasi]\nkeranjang\nreset", language=None)

    st.divider()
    st.caption("Dibuat dengan ❤️ · Flask → Streamlit")