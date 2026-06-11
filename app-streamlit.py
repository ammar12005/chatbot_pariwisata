"""
app_streamlit.py  –  Ngapain di Rumah? (Streamlit Version)
Tampilan menyerupai versi Flask/HTML asli dengan CSS injection penuh.
"""

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Ngapain di Rumah? 🌏",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Import engine ────────────────────────────────────────────────────────────
try:
    from engine import proses_pesan, SALAM_AWAL, reset_sesi
except ImportError:
    st.error("❌ File `engine.py` tidak ditemukan.")
    st.stop()

try:
    from database import (
        get_keranjang, hapus_keranjang_item, hapus_semua_keranjang,
        get_semua_transaksi, setup_tabel
    )
    setup_tabel()
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False

# ─── Session state ────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": SALAM_AWAL}]
if "sid" not in st.session_state:
    import uuid
    st.session_state.sid = str(uuid.uuid4())
if "quick_input" not in st.session_state:
    st.session_state.quick_input = None

SESSION_ID = st.session_state.sid

# ─── Handle quick input dari chip/sidebar ────────────────────────────────────
if st.session_state.quick_input:
    prompt = st.session_state.quick_input
    st.session_state.quick_input = None
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = proses_pesan(prompt, SESSION_ID)
    st.session_state.messages.append({"role": "assistant", "content": response})

# ─── CSS Injeksi Penuh ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');

/* ── RESET STREAMLIT ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
.stApp { background: transparent; }
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #006B6B 0%, #004E4F 40%, #003838 100%);
    min-height: 100vh;
}
[data-testid="stSidebar"] { display: none; }
section.main > div { padding: 0 !important; }

/* ── CSS VARIABLES ── */
:root {
    --putih-transparan-sidebar: rgba(244,249,249,0.88);
    --putih-transparan-chat: rgba(255,255,255,0.55);
    --putih-murni: #FFFFFF;
    --tosca-tua: #005B5C;
    --tosca-medium: #0D7A7B;
    --tosca-muda: #E4F2F1;
    --teks-gelap: #0F2C2C;
    --teks-secondary: #5F7D7D;
    --merah-notif: #FF5252;
}

/* ── LAYOUT UTAMA ── */
.app-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
}

.container {
    display: flex;
    width: 100%;
    max-width: 1200px;
    height: 90vh;
    max-height: 850px;
    min-height: 600px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.25);
    border-radius: 20px;
    overflow: hidden;
}

/* ── SIDEBAR ── */
.sidebar {
    width: 290px;
    background: var(--putih-transparan-sidebar);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    display: flex;
    flex-direction: column;
    padding: 24px 20px;
    gap: 20px;
    flex-shrink: 0;
    border-right: 1px solid rgba(255,255,255,0.45);
    overflow-y: auto;
}

.sidebar-header { display: flex; align-items: center; gap: 12px; }

.bot-avatar-sidebar {
    width: 52px; height: 52px;
    border-radius: 50%;
    background: linear-gradient(135deg, #005B5C, #0D7A7B);
    box-shadow: 0 2px 8px rgba(0,0,0,0.12);
    display: flex; align-items: center; justify-content: center;
    font-size: 24px; flex-shrink: 0;
}

.bot-info h2 { color: var(--tosca-tua); font-size: 16px; font-weight: 700; margin: 0; }
.status-dot {
    display: inline-block; width: 8px; height: 8px;
    background: #2ECC71; border-radius: 50%; margin-right: 5px;
}
.bot-info small { color: var(--teks-secondary); font-size: 12px; }

.divider { height: 1px; background: rgba(0,0,0,0.06); }

.sidebar-section h4 {
    color: var(--teks-secondary); font-size: 11px;
    text-transform: uppercase; letter-spacing: 1.2px;
    margin-bottom: 12px; font-weight: 700; margin-top: 0;
}

.quick-btn {
    display: block; width: 100%; padding: 11px 14px;
    background: rgba(255,255,255,0.52);
    border: 1px solid rgba(255,255,255,0.65);
    border-radius: 12px; color: var(--tosca-tua);
    font-size: 13.5px; font-weight: 600; text-align: left;
    cursor: pointer; margin-bottom: 9px;
    transition: all .2s ease; text-decoration: none;
}
.quick-btn:hover { background: #D5ECEB; }

/* ── HISTORI SIDEBAR ── */
.history-section { margin-top: auto; }
.history-list { display: flex; flex-direction: column; gap: 8px; max-height: 220px; overflow-y: auto; }

.history-item {
    font-size: 13px; color: var(--teks-gelap);
    padding: 10px 12px;
    background: rgba(255,255,255,0.42);
    border: 1px solid rgba(255,255,255,0.55);
    border-radius: 10px;
    display: flex; flex-direction: column; gap: 4px;
    font-weight: 600; cursor: default;
    transition: background .2s;
}
.history-item:hover { background: rgba(212,236,235,0.72); }
.history-item-header { display: flex; align-items: center; gap: 8px; color: var(--tosca-tua); font-size: 12px; }
.history-item-dest { font-size: 13px; color: var(--teks-gelap); font-weight: 700; padding-left: 20px; }
.history-item-total { font-size: 11px; color: var(--teks-secondary); font-weight: 500; padding-left: 20px; }
.no-history { font-size: 12px; color: var(--teks-secondary); font-style: italic; }

.st-badge {
    display: inline-block; font-size: 10px; padding: 1px 7px;
    border-radius: 20px; font-weight: 600; margin-left: 20px;
    margin-top: 2px; width: fit-content;
}
.st-pending { background: #FFF3CD; color: #856404; }
.st-lunas   { background: #D1FAE5; color: #065F46; }
.st-dibatalkan { background: #FEE2E2; color: #991B1B; }

/* ── CHAT AREA ── */
.chat-area {
    flex: 1; min-width: 0;
    display: flex; flex-direction: column;
    background: var(--putih-transparan-chat);
    backdrop-filter: blur(5px);
    overflow: hidden;
}

.chat-header {
    padding: 18px 24px;
    display: flex; align-items: center; justify-content: space-between;
    background: rgba(255,255,255,0.18);
    flex-shrink: 0;
    border-bottom: 1px solid rgba(255,255,255,0.3);
}
.chat-header-left h3 { font-size: 20px; font-weight: 700; color: var(--tosca-tua); margin: 0; }
.chat-header-left small { color: var(--teks-secondary); font-size: 13px; }

/* ── CHIPS ── */
.chips {
    display: flex; gap: 10px; flex-wrap: wrap;
    padding: 12px 24px; flex-shrink: 0;
    background: rgba(255,255,255,0.1);
}
.chip {
    padding: 7px 16px;
    background: var(--putih-murni);
    border-radius: 20px; font-size: 13px; font-weight: 600;
    cursor: pointer; transition: all .2s;
    border: none; box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}
.chip:hover { background: var(--tosca-muda); color: var(--tosca-tua); }

/* ── CHAT MESSAGES ── */
.chat-messages {
    flex: 1; min-height: 0; overflow-y: auto;
    padding: 20px 24px;
    display: flex; flex-direction: column; gap: 14px;
}

.msg-row { display: flex; align-items: flex-end; gap: 10px; animation: fadeIn .3s ease; }
.msg-row.user { justify-content: flex-end; }

.bot-avatar-chat {
    width: 34px; height: 34px; border-radius: 50%; flex-shrink: 0;
    background: linear-gradient(135deg, #005B5C, #0D7A7B);
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
}

.bubble {
    max-width: 72%; padding: 12px 16px;
    border-radius: 18px; font-size: 14.5px; line-height: 1.6;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    word-wrap: break-word;
}
.bubble.user {
    background: var(--tosca-tua); color: white;
    border-bottom-right-radius: 4px;
}
.bubble.bot {
    background: var(--putih-murni); color: var(--teks-gelap);
    border-bottom-left-radius: 4px;
}
.bubble small { display: block; font-size: 10px; text-align: right; margin-top: 5px; opacity: .5; }

/* ── INPUT AREA ── */
.chat-input-wrap { padding: 14px 24px 20px; flex-shrink: 0; }
.chat-input-area {
    background: var(--putih-murni); padding: 7px 9px 7px 20px;
    border-radius: 30px; display: flex; gap: 10px; align-items: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

/* ── STREAMLIT CHAT INPUT OVERRIDE ── */
[data-testid="stChatInput"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
[data-testid="stChatInput"] > div {
    background: white !important;
    border-radius: 30px !important;
    border: none !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08) !important;
    padding: 4px 8px 4px 16px !important;
}
[data-testid="stChatInput"] textarea {
    font-size: 15px !important;
    color: var(--teks-gelap) !important;
}
[data-testid="stChatInput"] button {
    background: var(--tosca-tua) !important;
    border-radius: 50% !important;
    color: white !important;
}

/* ── ANIMASI ── */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── SCROLLBAR ── */
.chat-messages::-webkit-scrollbar { width: 4px; }
.chat-messages::-webkit-scrollbar-track { background: transparent; }
.chat-messages::-webkit-scrollbar-thumb { background: rgba(0,91,92,0.2); border-radius: 4px; }

/* ── STREAMLIT CHAT MESSAGE OVERRIDE ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    gap: 0 !important;
}
[data-testid="stChatMessageContent"] { padding: 0 !important; }

/* Hide streamlit avatar and use custom */
[data-testid="stChatMessage"] [data-testid="chatAvatarIcon-assistant"],
[data-testid="stChatMessage"] [data-testid="chatAvatarIcon-user"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Helper render histori ────────────────────────────────────────────────────
def render_histori_html():
    if not DB_AVAILABLE:
        return '<div class="no-history">Database tidak tersedia</div>'
    try:
        semua = get_semua_transaksi()
        milik = [t for t in semua if t.get("session_id") == SESSION_ID]
        if not milik:
            return '<div class="no-history">Belum ada transaksi</div>'
        html = ""
        for t in milik[-5:][::-1]:
            status = t.get("status", "pending")
            label  = "✅ Lunas" if status == "lunas" else ("❌ Batal" if status == "dibatalkan" else "⏳ Pending")
            klass  = f"st-{status}"
            html += f"""
            <div class="history-item">
                <div class="history-item-header">🕐 {t.get('kode_booking','')}</div>
                <div class="history-item-dest">{t.get('destinasi','')}</div>
                <div class="history-item-total">Rp {t.get('total_bayar',0):,}</div>
                <span class="st-badge {klass}">{label}</span>
            </div>"""
        return html
    except:
        return '<div class="no-history">Gagal memuat</div>'

# ─── Helper: format pesan jadi HTML bubble ────────────────────────────────────
def format_bubble(teks, asal):
    import html
    safe = html.escape(teks)
    safe = safe.replace("**", "<b>", 1)
    # simple bold/italic
    import re
    safe = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', safe)
    safe = re.sub(r'\*(.*?)\*', r'<strong>\1</strong>', safe)
    safe = safe.replace("\n", "<br>")
    return safe

# ─── Build HTML UI ────────────────────────────────────────────────────────────
histori_html = render_histori_html()

# Build chat bubbles
bubbles_html = ""
for msg in st.session_state.messages:
    asal = msg["role"]
    teks = format_bubble(msg["content"], asal)
    if asal == "assistant":
        bubbles_html += f"""
        <div class="msg-row bot">
            <div class="bot-avatar-chat">🗺️</div>
            <div class="bubble bot">{teks}</div>
        </div>"""
    else:
        bubbles_html += f"""
        <div class="msg-row user">
            <div class="bubble user">{teks}</div>
        </div>"""

full_html = f"""
<div class="app-wrapper">
  <div class="container">

    <!-- SIDEBAR -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="bot-avatar-sidebar">🗺️</div>
        <div class="bot-info">
          <h2>Ngapain di Rumah?</h2>
          <small><span class="status-dot"></span>Online</small>
        </div>
      </div>
      <div class="divider"></div>
      <div class="sidebar-section">
        <h4>Jelajah Cepat</h4>
        <button class="quick-btn" onclick="sendMsg('provinsi')">🗺️ Semua Provinsi</button>
        <button class="quick-btn" onclick="sendMsg('cari semarang')">🏯 Semarang</button>
        <button class="quick-btn" onclick="sendMsg('cari bali')">🌺 Bali</button>
        <button class="quick-btn" onclick="sendMsg('cari bromo')">🌋 Bromo</button>
      </div>
      <div class="divider"></div>
      <div class="sidebar-section history-section">
        <h4>Histori Pesanan</h4>
        <div class="history-list">{histori_html}</div>
      </div>
    </aside>

    <!-- CHAT AREA -->
    <main class="chat-area">
      <div class="chat-header">
        <div class="chat-header-left">
          <h3>Ngapain di Rumah?</h3>
          <small>Asisten Perjalanan Virtual Indonesia 🇮🇩</small>
        </div>
      </div>
      <div class="chips">
        <button class="chip" onclick="sendMsg('provinsi')">🗺️ Provinsi</button>
        <button class="chip" onclick="sendMsg('cari bali')">🌺 Bali</button>
        <button class="chip" onclick="sendMsg('keranjang')">🛒 Keranjang</button>
        <button class="chip" onclick="sendMsg('reset')">🔄 Reset</button>
      </div>
      <div class="chat-messages" id="chatMessages">
        {bubbles_html}
      </div>
    </main>

  </div>
</div>

<script>
function sendMsg(text) {{
    // Kirim via Streamlit query param trick
    const input = window.parent.document.querySelector('[data-testid="stChatInput"] textarea');
    if (input) {{
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
        nativeInputValueSetter.call(input, text);
        input.dispatchEvent(new Event('input', {{ bubbles: true }}));
        setTimeout(() => {{
            const btn = window.parent.document.querySelector('[data-testid="stChatInput"] button[kind="primaryFormSubmit"]');
            if (btn) btn.click();
        }}, 100);
    }}
}}

// Auto scroll ke bawah
const chat = document.getElementById('chatMessages');
if (chat) chat.scrollTop = chat.scrollHeight;
</script>
"""

# ─── Render HTML custom ───────────────────────────────────────────────────────
components.html(full_html, height=900, scrolling=False)

# ─── Input tersembunyi di bawah (Streamlit chat input) ───────────────────────
st.markdown("""
<style>
/* Posisikan chat input di bawah layar tapi tetap visible */
[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 30px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: min(680px, 90vw) !important;
    z-index: 999 !important;
}
[data-testid="stChatInput"] > div {
    background: white !important;
    border-radius: 30px !important;
    border: none !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.15) !important;
    padding: 6px 8px 6px 20px !important;
}
[data-testid="stChatInput"] button {
    background: #005B5C !important;
    border-radius: 50% !important;
    width: 42px !important; height: 42px !important;
}
</style>
""", unsafe_allow_html=True)

if prompt := st.chat_input("Ketik destinasi atau 'provinsi'..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = proses_pesan(prompt, SESSION_ID)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()