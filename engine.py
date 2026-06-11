# ============================================================
#  engine.py  –  Ngapain di Rumah?
#  Mesin pemrosesan pesan chatbot wisata per destinasi
# ============================================================

from data_wisata import (
    get_semua_provinsi,
    get_kota_by_provinsi,
    get_destinasi_by_kota,
    get_semua_destinasi_provinsi,
    cari_destinasi,
    format_kartu_destinasi,
    format_harga,
    DESTINASI_WISATA,
)
from transaksi import (
    mulai_transaksi, proses_transaksi,
    sedang_transaksi, teks_mulai_pesan, cek_booking,
    tambah_ke_keranjang, lihat_keranjang,
    hapus_dari_keranjang, kosongkan_keranjang,
)

# ─────────────────────────────────────────────────
#  STATE SESI PENGGUNA
# ─────────────────────────────────────────────────
sesi_pengguna: dict = {}


def get_sesi(session_id: str) -> dict:
    if session_id not in sesi_pengguna:
        sesi_pengguna[session_id] = {
            "langkah": "awal",
            "provinsi": None,
            "kota": None,
        }
    return sesi_pengguna[session_id]


def reset_sesi(session_id: str):
    sesi_pengguna[session_id] = {
        "langkah": "awal",
        "provinsi": None,
        "kota": None,
    }


# ─────────────────────────────────────────────────
#  HELPER TEKS
# ─────────────────────────────────────────────────

EMOJI_PROVINSI = {
    "jawa tengah": "🏯",
    "di yogyakarta": "👑",
    "jawa timur": "⛰️",
    "bali": "🌺",
    "dki jakarta": "🏙️",
    "nusa tenggara barat": "🏝️",
    "papua barat": "🤿",
    "sumatera utara": "🌊",
    "sulawesi selatan": "🦀",
    "kalimantan timur": "🌿",
}

SALAM_AWAL = (
    "Halo! Selamat datang di *Ngapain di Rumah?* 🌏\n\n"
    "Saya siap membantu kamu menemukan destinasi wisata di seluruh Indonesia "
    "lengkap dengan *harga tiket masuk* (dewasa & anak-anak).\n\n"
    "Ketik:\n"
    "🗺️ *provinsi*  — lihat daftar provinsi\n"
    "🔍 *cari [nama tempat/kota]*  — cari destinasi langsung\n"
    "🎫 *pesan [nama destinasi]*  — pesan tiket langsung\n"
    "🛒 *simpan [nama destinasi]*  — simpan ke keranjang wishlist\n"
    "🛒 *keranjang*  — lihat daftar simpanan\n"
    "🔄 *reset*  — mulai ulang percakapan"
)


def daftar_provinsi_teks() -> str:
    provinsi_list = get_semua_provinsi()
    baris = ["🗺️ *Pilih Provinsi Tujuan Wisatamu:*\n"]
    for i, prov in enumerate(provinsi_list, 1):
        emj = EMOJI_PROVINSI.get(prov, "📍")
        baris.append(f"{i}. {emj} {prov.title()}")
    baris.append("\n💬 Ketik nama provinsi atau nomornya.")
    return "\n".join(baris)


def daftar_kota_teks(provinsi: str) -> str:
    kota_list = get_kota_by_provinsi(provinsi)
    if not kota_list:
        return f"❌ Maaf, data kota untuk *{provinsi.title()}* belum tersedia."

    baris = [f"📍 *Kota/Kabupaten di {provinsi.title()}:*\n"]
    for i, kota in enumerate(kota_list, 1):
        dest_count = len(get_destinasi_by_kota(provinsi, kota))
        baris.append(f"{i}. 🏙️ {kota.title()}  ({dest_count} destinasi)")
    baris.append("\n💬 Ketik nama kota/kabupaten atau nomornya.")
    baris.append("⬅️ Ketik *kembali* untuk pilih provinsi lain.")
    return "\n".join(baris)


def daftar_destinasi_teks(provinsi: str, kota: str) -> str:
    destinasi_list = get_destinasi_by_kota(provinsi, kota)
    if not destinasi_list:
        return f"❌ Belum ada data destinasi untuk *{kota.title()}*."

    baris = [f"🎯 *Destinasi Wisata di {kota.title()}, {provinsi.title()}:*\n"]
    for i, dest in enumerate(destinasi_list, 1):
        kartu = format_kartu_destinasi(dest, i)
        baris.append(kartu)
        baris.append("")

    baris.append("─" * 35)
    baris.append("🎫 Ketik *pesan tiket* untuk memesan.")
    baris.append("🛒 Ketik *simpan [nama destinasi]* untuk simpan ke keranjang.")
    baris.append("⬅️ Ketik *kembali* untuk pilih kota lain.")
    baris.append("🏠 Ketik *menu* atau *provinsi* untuk mulai ulang.")
    return "\n".join(baris)


def hasil_cari_teks(keyword: str, hasil: list) -> str:
    if not hasil:
        return (
            f"😔 Destinasi *'{keyword}'* tidak ditemukan.\n\n"
            "Coba cari dengan:\n"
            "• Nama kota: *cari semarang*\n"
            "• Nama provinsi: *cari bali*\n"
            "• Nama tempat: *cari borobudur*"
        )

    baris = [f"🔍 *Hasil pencarian '{keyword}':*\n"]
    for i, dest in enumerate(hasil[:10], 1):
        kartu = format_kartu_destinasi(dest, i)
        baris.append(kartu)
        baris.append("")

    if len(hasil) > 10:
        baris.append(f"_...dan {len(hasil)-10} destinasi lainnya. Coba lebih spesifik._\n")

    baris.append("─" * 35)
    baris.append("🎫 Ketik *pesan [nama destinasi]* untuk memesan tiket.")
    baris.append("🛒 Ketik *simpan [nama destinasi]* untuk simpan ke keranjang.")
    baris.append("🏠 Ketik *provinsi* untuk jelajah per wilayah.")
    return "\n".join(baris)


# ─────────────────────────────────────────────────
#  DETEKSI INPUT PROVINSI & KOTA
# ─────────────────────────────────────────────────

def cocokkan_provinsi(teks: str) -> str | None:
    t = teks.lower().strip()
    provinsi_list = get_semua_provinsi()
    if t.isdigit():
        idx = int(t) - 1
        if 0 <= idx < len(provinsi_list):
            return provinsi_list[idx]
    for prov in provinsi_list:
        if t in prov or prov in t:
            return prov
    return None


def cocokkan_kota(provinsi: str, teks: str) -> str | None:
    t = teks.lower().strip()
    kota_list = get_kota_by_provinsi(provinsi)
    if t.isdigit():
        idx = int(t) - 1
        if 0 <= idx < len(kota_list):
            return kota_list[idx]
    for kota in kota_list:
        if t in kota or kota in t:
            return kota
    return None


def cari_dest_dari_semua(keyword: str):
    """Cari destinasi dari seluruh data, kembalikan (dest, provinsi, kota) atau None."""
    keyword_lower = keyword.lower()
    for provinsi, kota_dict in DESTINASI_WISATA.items():
        for kota, dest_list in kota_dict.items():
            for dest in dest_list:
                if keyword_lower in dest["nama"].lower():
                    return dest, provinsi, kota
    return None, None, None


# ─────────────────────────────────────────────────
#  PEMROSESAN PESAN UTAMA
# ─────────────────────────────────────────────────

def proses_pesan(pesan: str, session_id: str = "default") -> str:
    sesi = get_sesi(session_id)
    teks = pesan.strip()
    teks_lower = teks.lower()

    # ── CEK TRANSAKSI BERJALAN (prioritas tertinggi) ─────────────
    if sedang_transaksi(session_id):
        return proses_transaksi(pesan, session_id)

    # ── CEK STATUS BOOKING (dengan atau tanpa kata "booking") ────
    # Format: "cek booking WB-XXXXX" atau "cek WB-XXXXX"
    if teks_lower.startswith("cek booking "):
        kode = teks.split(" ", 2)[2].strip()
        # Buang prefix "booking" jika ikut terbawa (jaga-jaga)
        if kode.lower().startswith("booking "):
            kode = kode.split(" ", 1)[1].strip()
        return cek_booking(kode)

    if teks_lower.startswith("cek "):
        kode = teks.split(" ", 1)[1].strip()
        # Buang prefix "booking" jika ada
        if kode.lower().startswith("booking "):
            kode = kode.split(" ", 1)[1].strip()
        # Pastikan yang dimaksud adalah kode booking (bukan nama destinasi)
        if "-" in kode or kode.upper() == kode:
            return cek_booking(kode)

    # ── KERANJANG: LIHAT ─────────────────────────────────────────
    if teks_lower in ("keranjang", "wishlist", "simpanan", "cart",
                      "lihat keranjang", "cek keranjang"):
        return lihat_keranjang(session_id)

    # ── KERANJANG: KOSONGKAN ─────────────────────────────────────
    if teks_lower in ("kosongkan keranjang", "hapus semua keranjang",
                      "clear keranjang", "bersihkan keranjang"):
        return kosongkan_keranjang(session_id)

    # ── KERANJANG: HAPUS SATU ITEM ───────────────────────────────
    if teks_lower.startswith("hapus keranjang "):
        nama = teks.split(" ", 2)[2].strip()
        return hapus_dari_keranjang(session_id, nama)

    # ── KERANJANG: SIMPAN DESTINASI ──────────────────────────────
    if teks_lower.startswith("simpan "):
        keyword = teks.split(" ", 1)[1].strip()
        
        # --- PROSES PEMBERSIHAN KEYWORD (Kunci Perbaikan) ---
        keyword_clean = keyword.lower()
        # Buang kata-kata sampah/pelengkap yang sering ikut terbawa input UI
        kata_pelengkap = ["tiket", "taman wisata nasional", "wisata taman nasional", "wisata", "taman", "destinasi"]
        for kata in kata_pelengkap:
            if keyword_clean.startswith(kata + " "):
                keyword_clean = keyword_clean.replace(kata + " ", "", 1).strip()
            elif keyword_clean.startswith(kata):
                keyword_clean = keyword_clean.replace(kata, "", 1).strip()
        # ----------------------------------------------------

        if keyword.lower() not in ("keranjang", "menu", "semua") and keyword_clean != "":
            # Gunakan keyword_clean yang sudah murni nama tempatnya saja untuk pencarian
            dest, provinsi, kota = cari_dest_dari_semua(keyword_clean)
            if dest:
                return tambah_ke_keranjang(session_id, dest, provinsi, kota)
                
            # Coba cari dari konteks sesi saat ini menggunakan keyword_clean
            if sesi.get("provinsi") and sesi.get("kota"):
                dest_list = get_destinasi_by_kota(sesi["provinsi"], sesi["kota"])
                for d in dest_list:
                    if keyword_clean in d["nama"].lower():
                        return tambah_ke_keranjang(session_id, d, sesi["provinsi"], sesi["kota"])
                        
            return (
                f"😔 Destinasi *'{keyword}'* tidak ditemukan.\n\n"
                f"Coba: *cari {keyword_clean}* untuk menemukan destinasinya dulu."
            )

     # ── PESAN TIKET LANGSUNG ─────────────────────────────────────
    # ── PESAN TIKET LANGSUNG ─────────────────────────────────────
    if teks_lower.startswith("pesan "):
        keyword = teks.split(" ", 1)[1].strip()
        
        # --- PROSES PEMBERSIHAN KEYWORD (Agar Pesan Tiket Juga Lancar) ---
        keyword_clean = keyword.lower()
        kata_pelengkap = ["tiket", "taman wisata nasional", "wisata taman nasional", "wisata", "taman", "destinasi"]
        for kata in kata_pelengkap:
            if keyword_clean.startswith(kata + " "):
                keyword_clean = keyword_clean.replace(kata + " ", "", 1).strip()
            elif keyword_clean.startswith(kata):
                keyword_clean = keyword_clean.replace(kata, "", 1).strip()
        # -----------------------------------------------------------------

        if keyword.lower() not in ("tiket", "menu", "provinsi") and keyword_clean != "":
            # Gunakan keyword_clean hasil filter untuk mencari destinasi
            dest, provinsi, kota = cari_dest_dari_semua(keyword_clean)
            if dest:
                mulai_transaksi(session_id, dest, provinsi, kota)
                return teks_mulai_pesan(dest, provinsi, kota)
            
            # Coba cari dari konteks sesi saat ini jika pencarian global meleset
            if sesi.get("provinsi") and sesi.get("kota"):
                dest_list = get_destinasi_by_kota(sesi["provinsi"], sesi["kota"])
                for d in dest_list:
                    if keyword_clean in d["nama"].lower():
                        mulai_transaksi(session_id, d, sesi["provinsi"], sesi["kota"])
                        return teks_mulai_pesan(d, sesi["provinsi"], sesi["kota"])
        else:
            return SALAM_AWAL

    # ── ALUR BERDASARKAN LANGKAH ──────────────────────────────────

    if sesi["langkah"] == "awal":
        prov = cocokkan_provinsi(teks_lower)
        if prov:
            sesi["provinsi"] = prov
            sesi["langkah"] = "pilih_kota"
            return daftar_kota_teks(prov)
        hasil = cari_destinasi(teks_lower)
        if hasil:
            return hasil_cari_teks(teks, hasil)
        return (
            "👋 Halo! Ketik *provinsi* untuk mulai jelajah wisata,\n"
            "atau *cari [nama tempat/kota]* untuk pencarian cepat.\n\n"
            "Contoh: *cari semarang* atau *cari borobudur*"
        )

    if sesi["langkah"] == "pilih_provinsi":
        prov = cocokkan_provinsi(teks_lower)
        if prov:
            sesi["provinsi"] = prov
            sesi["langkah"] = "pilih_kota"
            return daftar_kota_teks(prov)
        return f"❓ Provinsi *'{teks}'* tidak ditemukan.\n\n" + daftar_provinsi_teks()

    if sesi["langkah"] == "pilih_kota":
        kota = cocokkan_kota(sesi["provinsi"], teks_lower)
        if kota:
            sesi["kota"] = kota
            sesi["langkah"] = "lihat_destinasi"
            return daftar_destinasi_teks(sesi["provinsi"], kota)
        prov = cocokkan_provinsi(teks_lower)
        if prov:
            sesi["provinsi"] = prov
            return daftar_kota_teks(prov)
        return (
            f"❓ Kota *'{teks}'* tidak ditemukan di *{sesi['provinsi'].title()}*.\n\n"
            + daftar_kota_teks(sesi["provinsi"])
        )

    if sesi["langkah"] == "lihat_destinasi":

        # Pilih destinasi pakai angka
        if teks.isdigit():
            dest_list = get_destinasi_by_kota(sesi["provinsi"], sesi["kota"])
            idx = int(teks) - 1
            if 0 <= idx < len(dest_list):
                dest = dest_list[idx]
                mulai_transaksi(session_id, dest, sesi["provinsi"], sesi["kota"])
                return teks_mulai_pesan(dest, sesi["provinsi"], sesi["kota"])
            else:
                return f"❓ Nomor *{teks}* tidak valid. Pilih antara 1–{len(dest_list)}."

        # Simpan ke keranjang dari halaman destinasi
        if any(k in teks_lower for k in ("simpan", "wishlist", "save")):
            dest_list = get_destinasi_by_kota(sesi["provinsi"], sesi["kota"])
            dest = None
            for d in dest_list:
                if d["nama"].lower() in teks_lower or any(
                    w in d["nama"].lower() for w in teks_lower.split()
                    if len(w) > 3
                ):
                    dest = d
                    break
            if not dest and len(dest_list) == 1:
                dest = dest_list[0]
            if dest:
                return tambah_ke_keranjang(session_id, dest, sesi["provinsi"], sesi["kota"])
            nama_list = ", ".join(f"*{d['nama']}*" for d in dest_list)
            return f"🛒 Mau simpan destinasi yang mana?\n\n{nama_list}\n\n_(ketik: simpan [nama])_"

        # Trigger pesan tiket
        if any(k in teks_lower for k in ("pesan", "tiket", "beli", "booking", "order")):
            dest_list = get_destinasi_by_kota(sesi["provinsi"], sesi["kota"])
            dest = None
            for d in dest_list:
                if d["nama"].lower() in teks_lower or any(
                    w in d["nama"].lower() for w in teks_lower.split()
                ):
                    dest = d
                    break
            if not dest and len(dest_list) == 1:
                dest = dest_list[0]
            if dest:
                mulai_transaksi(session_id, dest, sesi["provinsi"], sesi["kota"])
                return teks_mulai_pesan(dest, sesi["provinsi"], sesi["kota"])
            else:
                nama_list = ", ".join(f"*{d['nama']}*" for d in dest_list)
                return f"🎫 Mau pesan tiket yang mana?\n\n{nama_list}\n\n_(ketik nama destinasinya)_"

        kota = cocokkan_kota(sesi["provinsi"], teks_lower)
        if kota:
            sesi["kota"] = kota
            return daftar_destinasi_teks(sesi["provinsi"], kota)

        prov = cocokkan_provinsi(teks_lower)
        if prov:
            sesi["provinsi"] = prov
            sesi["kota"] = None
            sesi["langkah"] = "pilih_kota"
            return daftar_kota_teks(prov)

        hasil = cari_destinasi(teks_lower)
        if hasil:
            return hasil_cari_teks(teks, hasil)

        return (
            "💬 Ketik nomor destinasi untuk memesan,\n"
            "*pesan tiket* atau nama destinasi untuk booking,\n"
            "*simpan [nama]* untuk simpan ke keranjang,\n"
            "*kembali* untuk pilih kota lain,\n"
            "*provinsi* untuk jelajah wilayah lain."
        )

    return SALAM_AWAL


# ─────────────────────────────────────────────────
#  TEST MANDIRI
# ─────────────────────────────────────────────────
if __name__ == "__main__":
    test_sesi = "test_001"
    print(proses_pesan("halo", test_sesi))
    print("\n" + "=" * 60 + "\n")
    print(proses_pesan("simpan Goa Kreo", test_sesi))
    print("\n" + "=" * 60 + "\n")
    print(proses_pesan("keranjang", test_sesi))