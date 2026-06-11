import streamlit as st
import uuid
from engine import proses_pesan, reset_sesi
from database import (
    get_keranjang, hapus_keranjang_item, hapus_semua_keranjang, 
    get_semua_transaksi, setup_tabel
)

# Inisialisasi Database (Jalankan sekali)
setup_tabel()

# 1. Setup Session State
if "sid" not in st.session_state:
    st.session_state.sid = str(uuid.uuid4())

# 2. Sidebar Navigasi
page = st.sidebar.radio("Menu", ["Chatbot", "Wishlist", "Histori Pesanan"])

# 3. Halaman Chat
if page == "Chatbot":
    st.title("Ngapain di Rumah? 🏖️")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Tanya destinasi..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        reply = proses_pesan(prompt, st.session_state.sid)
        
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    if st.sidebar.button("Reset Sesi"):
        reset_sesi(st.session_state.sid)
        st.session_state.messages = []
        st.rerun()

# 4. Halaman Wishlist
elif page == "Wishlist":
    st.title("Wishlist Destinasi Anda ✨")
    items = get_keranjang(st.session_state.sid)

    if not items:
        st.info("Wishlist masih kosong.")
    else:
        for item in items:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                col1.write(f"**{item['nama_destinasi']}** ({item['kota']}, {item['provinsi']})")
                col1.caption(f"Harga: {item['harga_dewasa']}")
                if col2.button("Hapus", key=f"del_{item['id']}"):
                    hapus_keranjang_item(st.session_state.sid, item['nama_destinasi'])
                    st.rerun()
        
        if st.button("Kosongkan Semua Wishlist"):
            hapus_semua_keranjang(st.session_state.sid)
            st.rerun()

# 5. Halaman Histori Pesanan
elif page == "Histori Pesanan":
    st.title("Riwayat Pesanan 📋")
    transaksi = get_semua_transaksi()
    # Filter hanya untuk session ini
    milik_saya = [t for t in transaksi if t.get("session_id") == st.session_state.sid]
    
    if not milik_saya:
        st.warning("Belum ada transaksi yang dilakukan.")
    else:
        for t in milik_saya:
            st.write(f"**Kode: {t['kode_booking']}** | Status: {t['status'].upper()}")
            st.write(f"Destinasi: {t['destinasi']} - Total: Rp {t['total_bayar']:,}")
            st.divider()