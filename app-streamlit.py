"""
app_streamlit.py  –  Ngapain di Rumah?
BRIDGE FINAL FIX: Memperbaiki pencarian DOM elemen st.chat_input di semua lini parent,
serta menangani string escaping pada tombol HTML agar tidak merusak fungsi JS `sendMsg()`.
"""

import streamlit as st
import streamlit.components.v1 as components
import os, base64, re, uuid
from datetime import datetime

st.set_page_config(
    page_title="Ngapain di Rumah? 🌏",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Import engine & Database ─────────────────────────────────────────────────
try:
    from engine import proses_pesan, SALAM_AWAL, reset_sesi
except ImportError:
    st.error("❌ File `engine.py` tidak ditemukan.")
    st.stop()

try:
    from database import (
        get_keranjang, hapus_semua_keranjang,
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
    st.session_state.sid = str(uuid.uuid4())

SESSION_ID = st.session_state.sid

# ─── Helper proses pesan ──────────────────────────────────────────────────────
def handle_prompt(prompt: str):
    prompt = prompt.strip()
    if not prompt:
        return
    pl = prompt.lower()

    if pl in ("hapus semua keranjang","kosongkan keranjang","kosongkan wishlist","clear keranjang"):
        if DB_AVAILABLE:
            hapus_semua_keranjang(SESSION_ID)
    elif pl.startswith("hapus keranjang "):
        proses_pesan(prompt, SESSION_ID)
    elif pl.startswith("simpan "):
        resp = proses_pesan(prompt, SESSION_ID)
        st.session_state.messages.append({"role": "assistant", "content": resp})
    elif pl.startswith("pesan "):
        resp = proses_pesan(prompt, SESSION_ID)
        st.session_state.messages.append({"role": "user",      "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": resp})
        if "Pesanan Berhasil Dibuat" in resp:
            st.session_state.messages = [{"role": "assistant", "content": SALAM_AWAL}]
            reset_sesi(SESSION_ID)
    else:
        resp = proses_pesan(prompt, SESSION_ID)
        st.session_state.messages.append({"role": "user",      "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": resp})
        if "Pesanan Berhasil Dibuat" in resp:
            st.session_state.messages = [{"role": "assistant", "content": SALAM_AWAL}]
            reset_sesi(SESSION_ID)

# ─── Terima input dari st.chat_input (HARUS sebelum render HTML) ──────────────
if prompt := st.chat_input("Ketik destinasi atau 'provinsi'...", key="main_input"):
    handle_prompt(prompt)
    st.rerun()

# ─── ENCODE BACKGROUND ───────────────────────────────────────────────────────
def get_base64_image(img_path):
    if os.path.exists(img_path):
        with open(img_path, "rb") as f:
            return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()
    return "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920"

bg_base64 = get_base64_image(os.path.join("static", "img", "beach.jpg"))

# ─── Sembunyikan UI Streamlit native, kecuali chat_input ─────────────────────
st.markdown(f"""
<style>
#MainMenu, footer, header {{ visibility: hidden; display: none !important; }}

/* Sembunyikan semua elemen kecuali iframe dan chat input */
[data-testid="stChatMessage"],
[data-testid="stMarkdown"],
[data-testid="stVerticalBlock"] > div:not(:has(iframe)):not(:has([data-testid="stBottom"])) {{
    display: none !important;
}}

/* Chat input disembunyikan visual tapi tetap bisa diakses JS */
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"] {{
    position: fixed !important;
    bottom: 0 !important; left: 0 !important;
    width: 100vw !important;
    opacity: 0 !important;
    z-index: 1 !important;
    pointer-events: none !important;
}}
[data-testid="stChatInput"] {{
    position: fixed !important;
    bottom: 2px !important; left: 0 !important;
    width: 100vw !important;
    opacity: 0 !important;
    z-index: 1 !important;
    pointer-events: none !important;
}}
[data-testid="stChatInput"] textarea {{
    pointer-events: all !important;
}}

/* Layout utama */
.stMain, .stApp, .block-container, [data-testid="stMain"] {{
    padding: 0 !important; margin: 0 !important;
    max-width: 100vw !important; height: 100vh !important;
    width: 100vw !important; overflow: hidden !important;
    background: transparent !important;
}}
html, body {{
    background-image: url('{bg_base64}') !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
    overflow: hidden !important;
    margin: 0 !important; padding: 0 !important;
    height: 100vh !important;
}}
[data-testid="stIframe"], [data-testid="element-container"]:has(iframe) {{
    height: 100vh !important; width: 100vw !important;
    overflow: hidden !important; margin: 0 !important; padding: 0 !important;
}}
iframe {{
    position: fixed !important; top: 0 !important; left: 0 !important;
    width: 100vw !important; height: 100vh !important;
    border: none !important; z-index: 999 !important;
}}
</style>
""", unsafe_allow_html=True)


# ─── Render helpers ───────────────────────────────────────────────────────────
def render_histori_html():
    if not DB_AVAILABLE:
        return '<div class="no-history">Database offline</div>'
    try:
        semua = get_semua_transaksi()
        milik = [t for t in semua if t.get("session_id") == SESSION_ID]
        if not milik:
            return '<div class="no-history">Belum ada transaksi</div>'
        html = ""
        for t in milik:
            dest   = t.get('destinasi', '')
            tgl    = t.get('tanggal_pesan', t.get('tanggal', ''))
            if tgl: 
                tgl = tgl.strftime("%Y-%m-%d") if hasattr(tgl, 'strftime') else str(tgl)[:10]
            kode   = t.get('kode_booking', '')
            total  = t.get('total_bayar', 0)
            harga  = f"Rp {int(total):,}".replace(",", ".") if total else ""
            status = t.get('status', 'pending')
            sc     = "#2ECC71" if status.lower() in ('selesai','confirmed','sukses','lunas') \
                     else "#E74C3C" if status.lower() in ('dibatalkan','batal','cancelled') \
                     else "#F39C12"
                     
            # Escape single quote agar aman saat dipassing ke fungsi JavaScript onclick
            kd_esc = kode.replace("'", "\\'")
            
            html += f"""<button class="history-item" onclick="sendMsg('cek booking {kd_esc}')">
                <div class="history-item-kode">🎫 {kode}</div>
                <div class="history-item-dest">{dest}</div>
                {f'<div class="history-item-harga">💰 {harga}</div>' if harga else ''}
                <div class="history-item-meta">
                    <span class="history-status-badge" style="background:{sc}22;color:{sc};">● {status}</span>
                    {f'<span class="history-item-tanggal">🗓 {tgl}</span>' if tgl else ''}
                </div></button>"""
        return html
    except Exception as e:
        return f'<div class="no-history">Gagal: {e}</div>'


def render_keranjang_html():
    if not DB_AVAILABLE:
        return '<div class="cart-empty"><div class="cart-empty-icon">⚠️</div>Database offline</div>'
    try:
        items = get_keranjang(SESSION_ID)
        if not items:
            return '<div class="cart-empty"><div class="cart-empty-icon">🗺️</div>Wishlist kosong.<br>Ketik <b>simpan [destinasi]</b>!</div>'
        html = ""
        for item in items:
            nama  = item.get('nama_destinasi', 'Destinasi')
            kota  = item.get('kota', '')
            prov  = item.get('provinsi', '')
            lok   = f"{kota}, {prov}" if kota and prov else kota or prov
            dw    = item.get('harga_dewasa', 0)
            an    = item.get('harga_anak', 0)
            emoji = item.get('emoji', '🌴')
            jam   = item.get('jam_buka', '')
            dw_f  = f"Rp {int(dw):,}".replace(",", ".") if dw else ""
            an_f  = f"Rp {int(an):,}".replace(",", ".") if an else ""
            
            # Escape nama untuk parameter Javascript onclick agar kutip tidak patah
            ns    = nama.replace("'", "\\'").replace('"', '\\"')
            
            html += f"""<div class="cart-item">
                <div class="cart-item-top">
                    <div class="cart-item-icon">{emoji}</div>
                    <div class="cart-item-info">
                        <div class="cart-item-name">{nama}</div>
                        {f'<div class="cart-item-lokasi">📍 {lok}</div>' if lok else ''}
                        {f'<div class="cart-item-harga">🎟 Dewasa: {dw_f}</div>' if dw_f else ''}
                        {f'<div class="cart-item-harga-anak">👦 Anak: {an_f}</div>' if an_f else ''}
                        {f'<div class="cart-item-jam">🕐 {jam}</div>' if jam and jam != "-" else ''}
                    </div>
                </div>
                <div class="cart-item-actions-row">
                   <button class="cart-btn-pesan" onclick="sendMsg('pesan {ns}')"><i class="fa-solid fa-ticket"></i> Pesan Tiket</button>
                    <button class="cart-action-btn btn-view" onclick="sendMsg('cari {ns}')"><i class="fa-solid fa-magnifying-glass"></i></button>
                    <button class="cart-action-btn btn-delete" onclick="sendMsg('hapus keranjang {ns}')"><i class="fa-solid fa-trash"></i></button>
                </div></div>"""
        return html
    except Exception as e:
        return f'<div class="cart-empty">Gagal: {e}</div>'


def format_bubble(teks):
    import html as hm
    s = hm.escape(teks)
    s = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\*(.*?)\*',     r'<strong>\1</strong>', s)
    return s.replace("\n", "<br>")


# ─── Kompilasi data ───────────────────────────────────────────────────────────
histori_html  = render_histori_html()
keranjang_html = render_keranjang_html()
jml = len(get_keranjang(SESSION_ID)) if DB_AVAILABLE else 0
badge = f'<span class="cart-badge">{jml}</span>' if jml > 0 else ''
cart_footer = (
    '<div class="cart-panel-footer">'
    '<button class="cart-footer-btn btn-clear" onclick="sendMsg(\'hapus semua keranjang\')">'
    '<i class="fa-solid fa-trash"></i> Kosongkan Wishlist</button></div>'
) if jml > 0 else ''

# ─── Build bubbles ────────────────────────────────────────────────────────────
bubbles = ""
for msg in st.session_state.messages:
    role  = msg["role"]
    teks  = msg["content"]
    waktu = datetime.now().strftime("%H.%M")
    if role == "assistant" and "Pesanan Berhasil Dibuat" in teks:
        km = re.search(r"Kode Booking\s*[:\-]\s*\*?([A-Z0-9\-]+)\*?", teks)
        dm = re.search(r"Destinasi\s*[:\-]\s*(.+)", teks)
        tm = re.search(r"Total Bayar\s*[:\-]\s*(.+)", teks)
        kode = km.group(1).strip() if km else "-"
        dest = dm.group(1).strip() if dm else "-"
        tot  = tm.group(1).strip() if tm else ""
        bubbles += f"""<div class="msg-row bot"><div class="bot-avatar-chat"></div>
            <div class="success-card">
                <div class="success-icon">✅🌴</div>
                <div class="success-title">Booking Berhasil!</div>
                <div class="success-detail">Pesanan untuk <b>{dest}</b> sudah tersimpan.</div>
                <div class="success-kode">{kode}</div>
                {f'<div class="success-detail">Total: <b>{tot}</b></div>' if tot else ''}
                <div class="success-cta">Lihat histori di sidebar.</div>
            </div></div>"""
        continue
    t = format_bubble(teks)
    if role == "assistant":
        bubbles += f'<div class="msg-row bot"><div class="bot-avatar-chat"></div><div class="bubble bot">{t}<small>{waktu}</small></div></div>'
    else:
        bubbles += f'<div class="msg-row user"><div class="bubble user">{t}<small>{waktu}</small></div></div>'


# ─── MASTER HTML ──────────────────────────────────────────────────────────────
full_html = f"""
<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');
*,*::before,*::after{{box-sizing:border-box!important}}
body{{margin:0;padding:0;width:100%;height:100%;background-image:url('{bg_base64}');background-size:cover;background-position:center;background-attachment:fixed;font-family:'Segoe UI',-apple-system,BlinkMacSystemFont,sans-serif;display:flex;justify-content:center;align-items:center;overflow:hidden}}
:root{{--pt:rgba(255,255,255,0.75);--pc:rgba(255,255,255,0.40);--w:#FFFFFF;--tt:#005B5C;--tm:#0D7A7B;--tl:#E4F2F1;--tg:#0F2C2C;--ts:#5F7D7D;--r:#E74C3C;--rm:#FDEAEA}}
.app-wrapper{{display:flex;justify-content:center;align-items:center;width:100%;height:100%;padding:20px}}
.container{{display:flex;width:100%;max-width:1200px;height:92vh;background:rgba(255,255,255,0.15);backdrop-filter:blur(20px);box-shadow:0 20px 50px rgba(0,0,0,0.12);border-radius:24px;overflow:hidden;border:1px solid rgba(255,255,255,0.35);position:relative}}
.sidebar{{width:280px;background:var(--pt);display:flex;flex-direction:column;padding:24px;flex-shrink:0;border-right:1px solid rgba(255,255,255,0.25);height:100%;overflow-y:auto}}
.sidebar-header{{display:flex;align-items:center;gap:12px}}
.bot-avatar-sidebar{{width:46px;height:46px;border-radius:50%;background-image:url('https://images.unsplash.com/photo-1506929562872-bb421503ef21?w=150');background-size:cover;background-position:center}}
.bot-info h2{{color:var(--tt);font-size:17px;font-weight:700;margin:0}}
.status-dot{{display:inline-block;width:8px;height:8px;background:#2ECC71;border-radius:50%;margin-right:6px}}
.bot-info small{{color:var(--ts);font-size:12px}}
.divider{{height:1px;background:rgba(0,0,0,0.06);margin:16px 0}}
.sidebar-section h4{{color:var(--ts);font-size:11px;text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;font-weight:700;margin-top:0}}
.quick-btn{{display:block;width:100%;padding:11px 16px;background:rgba(255,255,255,0.7);border:1px solid rgba(255,255,255,0.5);border-radius:12px;text-align:left;font-size:13.5px;font-weight:600;color:var(--tt);cursor:pointer;margin-bottom:8px;transition:all 0.2s}}
.quick-btn:hover{{background:var(--w);transform:translateY(-1px)}}
.history-section{{margin-top:auto;display:flex;flex-direction:column;min-height:120px;max-height:260px}}
.history-list{{display:flex;flex-direction:column;gap:6px;overflow-y:auto;padding-right:4px}}
.history-item{{font-size:12px;padding:10px 12px;background:rgba(255,255,255,0.5);border:1px solid rgba(255,255,255,0.5);border-radius:10px;display:flex;flex-direction:column;gap:3px;cursor:pointer;transition:all 0.2s;width:100%;text-align:left}}
.history-item:hover{{background:var(--tl);border-color:var(--tm);transform:translateX(3px)}}
.history-item-kode{{font-size:10px;color:var(--ts);font-family:monospace}}
.history-item-dest{{font-size:13px;color:var(--tg);font-weight:700;margin:1px 0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.history-item-harga{{font-size:11px;color:var(--tm);font-weight:600}}
.history-item-meta{{display:flex;align-items:center;gap:6px;margin-top:2px;flex-wrap:wrap}}
.history-status-badge{{font-size:10px;font-weight:700;padding:2px 8px;border-radius:20px;white-space:nowrap}}
.history-item-tanggal{{font-size:10px;color:var(--ts)}}
.no-history{{font-size:12.5px;color:var(--ts);font-style:italic}}
.chat-area{{flex:1;min-width:0;display:flex;flex-direction:column;background:var(--pc);position:relative;height:100%}}
.chat-header{{padding:20px 24px;display:flex;align-items:center;justify-content:space-between}}
.chat-header-left h3{{font-size:20px;font-weight:700;color:var(--tt);margin:0}}
.chat-header-left small{{color:var(--ts);font-size:12.5px}}
.cart-header-btn{{width:38px;height:38px;background:var(--w);border-radius:50%;display:flex;align-items:center;justify-content:center;color:var(--tt);font-size:14px;cursor:pointer;border:none;transition:all 0.2s;position:relative}}
.cart-header-btn:hover,.cart-header-btn.active{{background:var(--tt);color:white}}
.cart-badge{{position:absolute;top:-4px;right:-4px;background:var(--r);color:white;font-size:10px;font-weight:700;width:18px;height:18px;border-radius:50%;display:flex;align-items:center;justify-content:center;border:2px solid white}}
.cart-panel{{display:none;position:absolute;top:74px;right:24px;width:340px;background:var(--w);border-radius:18px;box-shadow:0 16px 40px rgba(0,0,0,0.14);z-index:1000;overflow:hidden;border:1px solid rgba(0,91,92,0.12)}}
.cart-panel.open{{display:block}}
.cart-panel-header{{padding:16px 20px;background:var(--tt);color:white;display:flex;align-items:center;justify-content:space-between}}
.cart-panel-header h4{{margin:0;font-size:15px;font-weight:700}}
.cart-close-btn{{background:rgba(255,255,255,0.2);border:none;color:white;width:28px;height:28px;border-radius:50%;cursor:pointer;font-size:13px;display:flex;align-items:center;justify-content:center}}
.cart-close-btn:hover{{background:rgba(255,255,255,0.35)}}
.cart-panel-body{{max-height:360px;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:10px}}
.cart-item{{display:flex;flex-direction:column;padding:14px;background:#F7FAFA;border-radius:14px;border:1px solid rgba(0,91,92,0.08);transition:background 0.2s}}
.cart-item:hover{{background:var(--tl)}}
.cart-item-top{{display:flex;align-items:flex-start;gap:10px}}
.cart-item-icon{{font-size:22px;width:34px;text-align:center;flex-shrink:0;margin-top:2px}}
.cart-item-info{{flex:1;min-width:0}}
.cart-item-name{{font-size:13px;font-weight:700;color:var(--tg);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.cart-item-lokasi,.cart-item-jam{{font-size:11px;color:var(--ts);margin-top:2px}}
.cart-item-harga,.cart-item-harga-anak{{font-size:11px;font-weight:700;color:var(--tm);margin-top:2px}}
.cart-item-actions-row{{display:flex;align-items:center;gap:6px;margin-top:10px}}
.cart-btn-pesan{{flex:1;padding:7px 10px;background:var(--tt);color:white;border:none;border-radius:10px;font-size:12px;font-weight:600;cursor:pointer;display:flex;align-items:center;gap:5px;justify-content:center;transition:background 0.2s}}
.cart-btn-pesan:hover{{background:var(--tm)}}
.cart-action-btn{{width:30px;height:30px;border-radius:50%;border:none;cursor:pointer;font-size:12px;display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:all 0.2s}}
.btn-view{{background:var(--tl);color:var(--tt)}}.btn-view:hover{{background:var(--tt);color:white}}
.btn-delete{{background:var(--rm);color:var(--r)}}.btn-delete:hover{{background:var(--r);color:white}}
.cart-panel-footer{{padding:12px 16px;border-top:1px solid rgba(0,0,0,0.06);display:flex;gap:8px}}
.cart-footer-btn{{flex:1;padding:10px;border-radius:12px;border:none;font-size:13px;font-weight:600;cursor:pointer;transition:all 0.2s}}
.btn-clear{{background:var(--rm);color:var(--r)}}.btn-clear:hover{{background:var(--r);color:white}}
.cart-empty{{text-align:center;padding:24px 16px;color:var(--ts);font-size:13px}}
.cart-empty-icon{{font-size:32px;margin-bottom:8px}}
.chips{{display:flex;gap:10px;padding:0 24px 12px 24px;flex-wrap:wrap}}
.chip{{padding:7px 16px;background:var(--w);border-radius:12px;font-size:13px;font-weight:600;color:var(--tg);cursor:pointer;border:none;box-shadow:0 2px 6px rgba(0,0,0,0.03)}}
.chip:hover{{background:var(--tt);color:white}}
.chat-messages{{flex:1;min-height:0;overflow-y:auto;padding:10px 24px 110px 24px;display:flex;flex-direction:column;gap:16px}}
.msg-row{{display:flex;align-items:flex-start;gap:12px}}
.msg-row.user{{justify-content:flex-end}}
.bot-avatar-chat{{width:34px;height:34px;border-radius:50%;flex-shrink:0;background-image:url('https://images.unsplash.com/photo-1506929562872-bb421503ef21?w=100');background-size:cover;background-position:center}}
.bubble{{max-width:70%;padding:14px 18px;border-radius:18px;font-size:14px;line-height:1.5;box-shadow:0 4px 12px rgba(0,0,0,0.02);word-wrap:break-word}}
.bubble.user{{background:var(--tt);color:white;border-top-right-radius:4px}}
.bubble.bot{{background:var(--w);color:var(--tg);border-top-left-radius:4px}}
.bubble small{{display:block;font-size:10px;text-align:right;margin-top:6px;opacity:.5}}
.success-card{{background:var(--w);border-radius:18px;padding:28px 24px;text-align:center;box-shadow:0 4px 12px rgba(0,0,0,0.04);max-width:70%;margin:0 auto}}
.success-icon{{font-size:40px;margin-bottom:8px}}
.success-title{{color:var(--tt);font-size:18px;font-weight:700;margin-bottom:10px}}
.success-detail{{font-size:13px;color:var(--ts);line-height:1.6;margin-bottom:8px}}
.success-kode{{display:inline-block;background:var(--tl);color:var(--tt);font-family:monospace;font-size:15px;font-weight:700;padding:6px 16px;border-radius:8px;letter-spacing:1px;margin:6px 0 10px 0}}
.success-cta{{font-size:13px;color:var(--tm);font-weight:600}}
.custom-input-container{{position:absolute;bottom:28px;left:0;right:0;display:flex;justify-content:center;padding:0 24px;z-index:9999}}
.custom-input-wrapper{{display:flex;align-items:center;width:100%;max-width:650px;background:#FFF;border-radius:30px;border:1px solid rgba(0,91,92,0.3);box-shadow:0 8px 32px rgba(0,0,0,0.15);padding:6px 8px 6px 20px}}
.custom-input-wrapper textarea{{flex:1;border:none;outline:none;background:transparent;color:#000;font-size:14.5px;font-family:inherit;resize:none;height:24px;line-height:24px}}
.custom-input-wrapper textarea::placeholder{{color:#708A8A}}
.custom-input-btn{{background:#005B5C;color:#FFF;border:none;border-radius:50%;width:38px;height:38px;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:background 0.2s}}
.custom-input-btn:hover{{background:#0D7A7B}}
::-webkit-scrollbar{{width:5px}}
::-webkit-scrollbar-thumb{{background:rgba(0,91,92,0.2);border-radius:10px}}
.cart-overlay{{display:none;position:fixed;inset:0;z-index:999}}
.cart-overlay.open{{display:block}}
</style>

<div class="cart-overlay" id="cartOverlay" onclick="tutupKeranjang()"></div>
<div class="app-wrapper">
  <div class="container">
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="bot-avatar-sidebar"></div>
        <div class="bot-info"><h2>Ngapain di Rumah?</h2><small><span class="status-dot"></span>Online</small></div>
      </div>
      <div class="divider"></div>
      <div class="sidebar-section">
        <h4>Jelajah Cepat</h4>
        <button class="quick-btn" onclick="sendMsg('provinsi')">🗺️ Semua Provinsi</button>
        <button class="quick-btn" onclick="sendMsg('cari semarang')">🏯 Semarang</button>
        <button class="quick-btn" onclick="sendMsg('cari bali')">🌺 Bali</button>
        <button class="quick-btn" onclick="sendMsg('cari bromo')">🌋 Bromo</button>
      </div>
      <div class="sidebar-section history-section">
        <div class="divider"></div>
        <h4>Histori Pesanan</h4>
        <div class="history-list" id="historyList">{histori_html}</div>
      </div>
    </aside>
    <main class="chat-area">
      <div class="chat-header">
        <div class="chat-header-left">
          <h3>Ngapain di Rumah?</h3>
          <small>Asisten Perjalanan Virtual Indonesia 🇮🇩</small>
        </div>
        <button class="cart-header-btn" id="cartBtn" onclick="toggleKeranjang()">
          <i class="fa-solid fa-basket-shopping"></i>{badge}
        </button>
      </div>
      <div class="cart-panel" id="cartPanel">
        <div class="cart-panel-header">
          <h4>🗺️ Wishlist Destinasi</h4>
          <button class="cart-close-btn" onclick="tutupKeranjang()"><i class="fa-solid fa-xmark"></i></button>
        </div>
        <div class="cart-panel-body">{keranjang_html}</div>
        {cart_footer}
      </div>
      <div class="chips">
        <button class="chip" onclick="sendMsg('provinsi')">🗺️ Provinsi</button>
        <button class="chip" onclick="sendMsg('cari bali')">🌺 Bali</button>
        <button class="chip" onclick="toggleKeranjang()">🛒 Wishlist</button>
        <button class="chip" onclick="sendMsg('keranjang')">📋 Keranjang</button>
        <button class="chip" onclick="sendMsg('reset')">🔄 Reset</button>
      </div>
      <div class="chat-messages" id="chatMessages">{bubbles}</div>
      <div class="custom-input-container">
        <div class="custom-input-wrapper">
          <textarea id="uiInput" placeholder="Ketik destinasi atau 'provinsi'..." onkeydown="checkEnter(event)"></textarea>
          <button class="custom-input-btn" onclick="submitChat()"><i class="fa-solid fa-arrow-up"></i></button>
        </div>
      </div>
    </main>
  </div>
</div>

<script>
// AMANKAN UTAMA: Buat fallback global checkEnter agar onkeydown tidak melempar ReferenceError
window.checkEnter = function(e) {{
    if (e.key === 'Enter' && !e.shiftKey) {{
        e.preventDefault();
        submitChat();
    }}
}};

// Panel Control Wishlist UI
function toggleKeranjang() {{
    document.getElementById('cartPanel').classList.toggle('open');
    document.getElementById('cartOverlay').classList.toggle('open');
}}
function tutupKeranjang() {{
    document.getElementById('cartPanel').classList.remove('open');
    document.getElementById('cartOverlay').classList.remove('open');
}}

function findChatInput() {{
    var docs = [document];
    try {{ if (window.parent && window.parent.document) docs.push(window.parent.document); }} catch(e) {{}}
    try {{ if (window.top && window.top.document) docs.push(window.top.document); }} catch(e) {{}}

    if (window.parent) {{
        try {{
            var allIframes = window.parent.document.querySelectorAll('iframe');
            for (var i = 0; i < allIframes.length; i++) {{
                try {{
                    var d = allIframes[i].contentDocument || allIframes[i].contentWindow.document;
                    if (d && docs.indexOf(d) === -1) docs.push(d);
                }} catch(e) {{}}
            }}
        }} catch(e) {{}}
    }}

    var selectors = [
        'textarea[data-testid="stChatInputTextArea"]',
        '[data-testid="stChatInput"] textarea',
        'textarea[placeholder*="Ketik destinasi"]',
        '.stChatInput textarea',
        'textarea'
    ];

    for (var d = 0; d < docs.length; d++) {{
        for (var s = 0; s < selectors.length; s++) {{
            try {{
                var el = docs[d].querySelector(selectors[s]);
                if (el && el.id !== 'uiInput') return el;
            }} catch(e) {{}}
        }}
    }}
    return null;
}}

// JANTUNG INJEKSI: Mengisi text murni bypass Virtual DOM React dan Trigger Klik Tombol Submit Streamlit
function fireToInput(text) {{
    if (!text) return;
    var el = findChatInput();
    if (!el) {{
        console.error("Input Streamlit native tidak ditemukan.");
        return;
    }}
    
    try {{
        var proto = el.ownerDocument.defaultView.HTMLTextAreaElement.prototype;
        var setter = Object.getOwnPropertyDescriptor(proto, 'value');
        if (setter && setter.set) {{
            setter.set.call(el, text);
        }} else {{
            el.value = text;
        }}
    }} catch(e) {{
        el.value = text;
    }}
    
    el.dispatchEvent(new Event('input',  {{ bubbles: true, composed: true }}));
    el.dispatchEvent(new Event('change', {{ bubbles: true, composed: true }}));
    
    setTimeout(function() {{
        try {{
            var form = el.closest('form') || el.form;
            var submitBtn = form ? (form.querySelector('button[data-testid="stChatInputSubmitButton"]') || form.querySelector('button')) : null;
            if (submitBtn) {{
                submitBtn.disabled = false;
                submitBtn.click();
            }} else {{
                // Fallback kirim event enter jika tombol disembunyikan total
                var enterEvent = new KeyboardEvent('keydown', {{
                    key: 'Enter', keyCode: 13, code: 'Enter', which: 13, bubbles: true, cancelable: true, composed: true
                }});
                el.dispatchEvent(enterEvent);
            }}
        }} catch(e) {{
            console.error("Gagal submit form:", e);
        }}
    }}, 100);
}}

// Fungsi utama pemicu dari tombol menu cepat & wishlist item
function sendMsg(text) {{
    fireToInput(text);
}}

// Fungsi kirim dari custom textarea input bawah (uiInput)
function submitChat() {{
    var uiInp = document.getElementById('uiInput');
    if (!uiInp) return;
    var text = uiInp.value.strip ? uiInp.value.strip() : uiInp.value.trim();
    if (!text) return;
    
    fireToInput(text);
    uiInp.value = ''; // Kosongkan kembali wadah input visual custom
}}

// Auto scroll down area pesan chat dan riwayat
var c = document.getElementById('chatMessages'); if(c) c.scrollTop = c.scrollHeight;
var h = document.getElementById('historyList');  if(h) h.scrollTop = h.scrollHeight;
</script>
"""

# ─── RENDER UTAMA STREAMLIT COMPONENT ────────────────────────────────────────
components.html(full_html, height=1000, scrolling=False)