# ============================================================
#  transaksi.py  –  WisataBot
#  Alur pemesanan tiket: pilih destinasi → jumlah orang
#                        → data pemesan → pilih bayar → konfirmasi
# ============================================================

from database import (
    simpan_transaksi, get_transaksi,
    cek_dan_expire_satu, expire_transaksi_kadaluarsa,
    simpan_keranjang, get_keranjang,
    hapus_keranjang_item, hapus_semua_keranjang,
)
from data_wisata import format_harga
from datetime import datetime as dt

# ─────────────────────────────────────────────────
#  INFO PEMBAYARAN
# ─────────────────────────────────────────────────

BANK_LIST = {
    "bca":     {"nama": "BCA",     "no_rek": "1234567890", "atas_nama": "WisataBot Indonesia"},
    "bni":     {"nama": "BNI",     "no_rek": "0987654321", "atas_nama": "WisataBot Indonesia"},
    "bri":     {"nama": "BRI",     "no_rek": "5678901234", "atas_nama": "WisataBot Indonesia"},
    "mandiri": {"nama": "Mandiri", "no_rek": "1122334455", "atas_nama": "WisataBot Indonesia"},
}

EWALLET_LIST = {
    "gopay":     {"nama": "GoPay",     "no": "0812-3456-7890", "atas_nama": "WisataBot"},
    "dana":      {"nama": "DANA",      "no": "0812-3456-7890", "atas_nama": "WisataBot"},
    "ovo":       {"nama": "OVO",       "no": "0812-3456-7890", "atas_nama": "WisataBot"},
    "qris":      {"nama": "QRIS",      "no": "(scan QR di kasir)", "atas_nama": "WisataBot"},
    "shopeepay": {"nama": "ShopeePay", "no": "0812-3456-7890", "atas_nama": "WisataBot"},
}


# ─────────────────────────────────────────────────
#  STATE TRANSAKSI PER SESI
# ─────────────────────────────────────────────────

sesi_transaksi: dict = {}

LANGKAH_URUT = [
    "isi_dewasa",
    "isi_anak",
    "isi_nama",
    "isi_hp",
    "pilih_metode",
    "pilih_bank",
    "konfirmasi",
    "selesai",
]


def get_trx(sid: str) -> dict:
    if sid not in sesi_transaksi:
        sesi_transaksi[sid] = {}
    return sesi_transaksi[sid]


def reset_trx(sid: str):
    sesi_transaksi[sid] = {}


def mulai_transaksi(sid: str, destinasi: dict, provinsi: str, kota: str):
    """Inisiasi transaksi baru untuk sebuah destinasi."""
    sesi_transaksi[sid] = {
        "langkah":      "isi_dewasa",
        "destinasi":    destinasi["nama"],
        "provinsi":     provinsi,
        "kota":         kota,
        "harga_dewasa": destinasi["harga_dewasa"],
        "harga_anak":   destinasi["harga_anak"],
        "jumlah_dewasa": 0,
        "jumlah_anak":   0,
        "nama_pemesan":  "",
        "no_hp":         "",
        "metode_bayar":  "",
        "bank_tujuan":   "",
        "total_bayar":   0,
    }


def sedang_transaksi(sid: str) -> bool:
    trx = sesi_transaksi.get(sid, {})
    return bool(trx) and trx.get("langkah", "selesai") not in ("", "selesai")


# ─────────────────────────────────────────────────
#  FORMAT TEKS HELPER
# ─────────────────────────────────────────────────

def teks_mulai_pesan(dest: dict, provinsi: str, kota: str) -> str:
    nama = dest["nama"]
    hd   = format_harga(dest["harga_dewasa"])
    ha   = format_harga(dest["harga_anak"])
    return (
        f"🎫 *Pesan Tiket – {nama}*\n"
        f"📍 {kota.title()}, {provinsi.title()}\n\n"
        f"💰 Harga tiket:\n"
        f"   👤 Dewasa    : {hd}\n"
        f"   👦 Anak >5th : {ha}\n\n"
        f"Berapa orang *dewasa* yang akan hadir?\n"
        f"_(ketik angka, contoh: 2)_\n\n"
        f"❌ Ketik *batal* untuk membatalkan."
    )


def teks_ringkasan(trx: dict) -> str:
    total  = trx["total_bayar"]
    metode = trx["metode_bayar"]
    bank   = trx["bank_tujuan"]

    if metode == "bank":
        info = BANK_LIST.get(bank, {})
        info_bayar = (
            f"🏦 Transfer ke *{info.get('nama', bank.upper())}*\n"
            f"   No. Rek : `{info.get('no_rek', '-')}`\n"
            f"   A/N     : {info.get('atas_nama', '-')}"
        )
    else:
        info = EWALLET_LIST.get(bank, {})
        info_bayar = (
            f"📱 Transfer ke *{info.get('nama', bank.upper())}*\n"
            f"   No/ID   : `{info.get('no', '-')}`\n"
            f"   A/N     : {info.get('atas_nama', '-')}"
        )

    return (
        f"📋 *Ringkasan Pesanan:*\n"
        f"─────────────────────────\n"
        f"🎯 Destinasi  : {trx['destinasi']}\n"
        f"📍 Lokasi     : {trx['kota'].title()}, {trx['provinsi'].title()}\n"
        f"👤 Dewasa     : {trx['jumlah_dewasa']} orang × {format_harga(trx['harga_dewasa'])}\n"
        f"👦 Anak >5th  : {trx['jumlah_anak']} orang × {format_harga(trx['harga_anak'])}\n"
        f"─────────────────────────\n"
        f"💵 *Total     : {format_harga(total)}*\n"
        f"─────────────────────────\n"
        f"👤 Pemesan    : {trx['nama_pemesan']}\n"
        f"📞 No. HP     : {trx['no_hp']}\n\n"
        f"{info_bayar}\n\n"
        f"✅ Ketik *konfirmasi* untuk lanjut bayar\n"
        f"❌ Ketik *batal* untuk membatalkan"
    )


def teks_sukses(kode: str, trx: dict) -> str:
    from datetime import datetime, timedelta
    expired_str = (datetime.now() + timedelta(hours=24)).strftime("%d %b %Y %H:%M")
    return (
        f"✅ *Pesanan Berhasil Dibuat!*\n\n"
        f"🎟️ Kode Booking : *{kode}*\n"
        f"📌 Destinasi    : {trx['destinasi']}\n"
        f"💵 Total Bayar  : {format_harga(trx['total_bayar'])}\n\n"
        f"⏳ Bayar sebelum: *{expired_str}*\n"
        f"📸 Setelah bayar, kirim bukti ke admin kami.\n\n"
        f"🔍 Cek status: ketik *cek {kode}*\n"
        f"🏠 Ketik *menu* untuk kembali ke awal."
    )


# ─────────────────────────────────────────────────
#  PROSESOR ALUR TRANSAKSI
# ─────────────────────────────────────────────────

def proses_transaksi(pesan: str, sid: str) -> str:
    trx   = get_trx(sid)
    teks  = pesan.strip()
    lower = teks.lower()

    if lower in ("batal", "cancel", "batalkan"):
        reset_trx(sid)
        return "❌ Pemesanan dibatalkan.\n\n🏠 Ketik *menu* untuk kembali ke awal."

    langkah = trx.get("langkah", "")

    if langkah == "isi_dewasa":
        if not teks.isdigit() or int(teks) < 0:
            return "⚠️ Masukkan angka yang valid (0 atau lebih).\nBerapa orang *dewasa*?"
        trx["jumlah_dewasa"] = int(teks)
        if trx["harga_anak"] > 0:
            trx["langkah"] = "isi_anak"
            return (
                f"✅ Dewasa: *{teks} orang*\n\n"
                f"Berapa orang *anak-anak (>5 tahun)*?\n"
                f"_(ketik 0 jika tidak ada)_"
            )
        else:
            trx["jumlah_anak"] = 0
            trx["langkah"]     = "isi_nama"
            return "✅ Oke!\n\nSilakan masukkan *nama lengkap* pemesan:"

    if langkah == "isi_anak":
        if not teks.isdigit() or int(teks) < 0:
            return "⚠️ Masukkan angka yang valid.\nBerapa orang *anak-anak (>5th)*?"
        trx["jumlah_anak"] = int(teks)
        total = (trx["jumlah_dewasa"] * trx["harga_dewasa"] +
                 trx["jumlah_anak"]   * trx["harga_anak"])
        if total == 0 and trx["jumlah_dewasa"] == 0 and trx["jumlah_anak"] == 0:
            return "⚠️ Jumlah pengunjung tidak boleh 0 semua. Berapa orang *dewasa*?"
        trx["total_bayar"] = total
        trx["langkah"]     = "isi_nama"
        return "✅ Oke!\n\nSilakan masukkan *nama lengkap* pemesan:"

    if langkah == "isi_nama":
        if len(teks) < 3:
            return "⚠️ Nama terlalu pendek. Masukkan *nama lengkap* pemesan:"
        trx["nama_pemesan"] = teks
        trx["langkah"]      = "isi_hp"
        return f"✅ Nama: *{teks}*\n\nMasukkan *nomor HP* (WhatsApp):\n_(contoh: 08123456789)_"

    if langkah == "isi_hp":
        bersih = teks.replace("-", "").replace(" ", "").replace("+", "")
        if not bersih.isdigit() or len(bersih) < 9:
            return "⚠️ Nomor HP tidak valid.\nMasukkan *nomor HP* aktif:"
        trx["no_hp"]   = teks
        trx["langkah"] = "pilih_metode"
        if trx["total_bayar"] == 0:
            trx["total_bayar"] = trx["jumlah_dewasa"] * trx["harga_dewasa"]
        return (
            f"✅ HP: *{teks}*\n\n"
            f"💳 Pilih *metode pembayaran*:\n\n"
            f"1️⃣ *transfer* — Transfer Bank (BCA/BNI/BRI/Mandiri)\n"
            f"2️⃣ *ewallet* — E-Wallet (GoPay/DANA/OVO/QRIS/ShopeePay)\n\n"
            f"_(ketik nama atau nomornya)_"
        )

    if langkah == "pilih_metode":
        if lower in ("1", "transfer", "bank", "transfer bank"):
            trx["metode_bayar"] = "bank"
            trx["langkah"]      = "pilih_bank"
            return (
                "🏦 Pilih *bank tujuan*:\n\n"
                "1️⃣ *BCA*\n2️⃣ *BNI*\n3️⃣ *BRI*\n4️⃣ *Mandiri*\n\n"
                "_(ketik nama bank atau nomornya)_"
            )
        elif lower in ("2", "ewallet", "e-wallet", "dompet", "digital",
                       "gopay", "dana", "ovo", "qris", "shopeepay"):
            trx["metode_bayar"] = "ewallet"
            trx["langkah"]      = "pilih_bank"
            return (
                "📱 Pilih *e-wallet / QRIS*:\n\n"
                "1️⃣ *GoPay*\n2️⃣ *DANA*\n3️⃣ *OVO*\n4️⃣ *QRIS*\n5️⃣ *ShopeePay*\n\n"
                "_(ketik nama atau nomornya)_"
            )
        return "⚠️ Pilihan tidak dikenali.\n\nKetik *transfer* untuk bank, atau *ewallet* untuk e-wallet."

    if langkah == "pilih_bank":
        metode = trx["metode_bayar"]
        if metode == "bank":
            MAP = {"1": "bca", "2": "bni", "3": "bri", "4": "mandiri",
                   "bca": "bca", "bni": "bni", "bri": "bri", "mandiri": "mandiri"}
            pilihan = MAP.get(lower)
            if not pilihan:
                return "⚠️ Bank tidak dikenali. Pilih: BCA, BNI, BRI, atau Mandiri."
        else:
            MAP = {"1": "gopay", "2": "dana", "3": "ovo", "4": "qris", "5": "shopeepay",
                   "gopay": "gopay", "dana": "dana", "ovo": "ovo",
                   "qris": "qris", "shopeepay": "shopeepay"}
            pilihan = MAP.get(lower)
            if not pilihan:
                return "⚠️ E-wallet tidak dikenali. Pilih: GoPay, DANA, OVO, QRIS, atau ShopeePay."
        trx["bank_tujuan"] = pilihan
        trx["langkah"]     = "konfirmasi"
        return teks_ringkasan(trx)

    if langkah == "konfirmasi":
        if lower in ("konfirmasi", "ya", "yes", "ok", "oke", "lanjut", "bayar", "confirm"):
            hasil = simpan_transaksi({
                "session_id":    sid,
                "nama_pemesan":  trx["nama_pemesan"],
                "no_hp":         trx["no_hp"],
                "provinsi":      trx["provinsi"],
                "kota":          trx["kota"],
                "destinasi":     trx["destinasi"],
                "jumlah_dewasa": trx["jumlah_dewasa"],
                "jumlah_anak":   trx["jumlah_anak"],
                "harga_dewasa":  trx["harga_dewasa"],
                "harga_anak":    trx["harga_anak"],
                "total_bayar":   trx["total_bayar"],
                "metode_bayar":  trx["metode_bayar"],
                "bank_tujuan":   trx["bank_tujuan"],
            })
            if hasil["sukses"]:
                kode = hasil["kode_booking"]
                hapus_keranjang_item(sid, trx["destinasi"])
                teks_ok = teks_sukses(kode, trx)
                reset_trx(sid)
                return teks_ok
            else:
                return (
                    f"❌ Gagal menyimpan pesanan: {hasil['pesan']}\n"
                    "Silakan coba lagi atau hubungi admin."
                )
        elif lower in ("tidak", "no", "ganti", "ubah"):
            reset_trx(sid)
            return "❌ Pemesanan dibatalkan.\n\n🏠 Ketik *menu* untuk kembali ke awal."
        else:
            return (
                "💬 Ketik *konfirmasi* untuk melanjutkan pembayaran,\n"
                "atau *batal* untuk membatalkan."
            )

    reset_trx(sid)
    return "⚠️ Terjadi kesalahan alur. Ketik *menu* untuk mulai ulang."


# ─────────────────────────────────────────────────
#  CEK STATUS BOOKING
# ─────────────────────────────────────────────────

def cek_booking(kode: str) -> str:
    # Buang prefix "BOOKING " atau "CEK " jika ikut terbawa
    kode = kode.strip()
    if kode.upper().startswith("BOOKING "):
        kode = kode[8:].strip()
    if kode.upper().startswith("CEK "):
        kode = kode[4:].strip()
    kode = kode.upper()

    cek_dan_expire_satu(kode)
    data = get_transaksi(kode)
    if not data:
        return f"❌ Kode booking *{kode}* tidak ditemukan."

    STATUS_EMOJI = {
        "pending":    "⏳",
        "lunas":      "✅",
        "dibatalkan": "❌",
        "selesai":    "🎉",
    }
    emj = STATUS_EMOJI.get(data["status"], "❓")

    # tanggal sudah berupa datetime object (dari get_transaksi yang sudah difix)
    tgl_pesan  = data["tanggal_pesan"].strftime("%d %b %Y %H:%M")  if data.get("tanggal_pesan")  else "-"
    tgl_bayar  = data["tanggal_bayar"].strftime("%d %b %Y %H:%M")  if data.get("tanggal_bayar")  else "-"
    tgl_expire = data["expired_at"].strftime("%d %b %Y %H:%M")     if data.get("expired_at")     else "-"

    info_expire = ""
    if data["status"] == "pending" and data.get("expired_at"):
        info_expire = f"⏰ Bayar sebelum : {tgl_expire}\n"

    return (
        f"🔍 *Status Booking: {kode}*\n"
        f"─────────────────────────\n"
        f"🎯 Destinasi  : {data['destinasi']}\n"
        f"👤 Pemesan    : {data['nama_pemesan']}\n"
        f"📞 No. HP     : {data['no_hp']}\n"
        f"👥 Tamu       : {data['jumlah_dewasa']} dewasa, {data['jumlah_anak']} anak\n"
        f"💵 Total      : {format_harga(data['total_bayar'])}\n"
        f"💳 Bayar via  : {data['bank_tujuan'].upper()}\n"
        f"─────────────────────────\n"
        f"Status : {emj} *{data['status'].upper()}*\n"
        f"{info_expire}"
        f"Dipesan: {tgl_pesan}\n"
        f"Dibayar: {tgl_bayar}\n\n"
        f"🏠 Ketik *menu* untuk kembali."
    )


# ─────────────────────────────────────────────────
#  FUNGSI KERANJANG (WISHLIST)
# ─────────────────────────────────────────────────

def tambah_ke_keranjang(sid: str, destinasi: dict, provinsi: str, kota: str) -> str:
    """Simpan destinasi ke keranjang wishlist dan kembalikan teks balasan."""
    hasil = simpan_keranjang(sid, destinasi, provinsi, kota)
    nama  = destinasi["nama"]

    if not hasil["sukses"]:
        if hasil["pesan"] == "sudah_ada":
            return (
                f"🛒 *{nama}* sudah ada di keranjangmu!\n\n"
                f"Ketik *keranjang* untuk melihat daftar simpanan,\n"
                f"atau *pesan {nama}* untuk langsung booking."
            )
        return f"❌ Gagal menyimpan ke keranjang: {hasil['pesan']}"

    hd = format_harga(destinasi["harga_dewasa"])
    ha = format_harga(destinasi["harga_anak"])
    return (
        f"🛒 *{nama}* berhasil disimpan ke keranjang!\n\n"
        f"📍 {kota.title()}, {provinsi.title()}\n"
        f"💰 Tiket Dewasa: {hd} | Anak: {ha}\n\n"
        f"💡 Ketik *keranjang* untuk lihat semua simpanan.\n"
        f"🎫 Ketik *pesan {nama}* kalau sudah siap booking."
    )


def lihat_keranjang(sid: str) -> str:
    """Tampilkan semua item di keranjang wishlist."""
    items = get_keranjang(sid)
    if not items:
        return (
            "🛒 Keranjangmu masih kosong.\n\n"
            "Simpan destinasi favoritmu dengan mengetik:\n"
            "_*simpan [nama destinasi]*_\n\n"
            "Contoh: *simpan Goa Kreo* atau *simpan Borobudur*"
        )

    baris = [f"🛒 *Keranjang Wishlist* ({len(items)} destinasi)\n"]
    for i, item in enumerate(items, 1):
        hd = format_harga(item["harga_dewasa"])
        ha = format_harga(item["harga_anak"])

        raw_tgl = item.get("ditambahkan")
        if raw_tgl:
            try:
                tgl = dt.strptime(raw_tgl, "%Y-%m-%d %H:%M:%S").strftime("%d %b %Y")
            except (ValueError, TypeError):
                tgl = str(raw_tgl)[:10] if raw_tgl else "-"
        else:
            tgl = "-"

        baris.append(
            f"{i}. {item.get('emoji','📍')} *{item['nama_destinasi']}*\n"
            f"   📍 {item['kota'].title()}, {item['provinsi'].title()}\n"
            f"   💰 Dewasa: {hd} | Anak: {ha}\n"
            f"   📅 Disimpan: {tgl}"
        )
        baris.append("")

    baris.append("─" * 35)
    baris.append("🎫 Ketik *pesan [nama destinasi]* untuk booking")
    baris.append("🗑️ Ketik *hapus keranjang [nama]* untuk menghapus satu")
    baris.append("🗑️ Ketik *kosongkan keranjang* untuk hapus semua")
    return "\n".join(baris)


def hapus_dari_keranjang(sid: str, nama_destinasi: str) -> str:
    """Hapus satu item dari keranjang."""
    items = get_keranjang(sid)
    cocok = None
    for item in items:
        if nama_destinasi.lower() in item["nama_destinasi"].lower():
            cocok = item["nama_destinasi"]
            break

    if not cocok:
        return (
            f"❓ Destinasi *'{nama_destinasi}'* tidak ditemukan di keranjangmu.\n"
            f"Ketik *keranjang* untuk melihat daftar lengkap."
        )

    berhasil = hapus_keranjang_item(sid, cocok)
    if berhasil:
        return f"🗑️ *{cocok}* berhasil dihapus dari keranjang."
    return f"❌ Gagal menghapus *{cocok}* dari keranjang."


def kosongkan_keranjang(sid: str) -> str:
    """Hapus semua item dari keranjang."""
    items = get_keranjang(sid)
    if not items:
        return "🛒 Keranjangmu sudah kosong."
    hapus_semua_keranjang(sid)
    return "🗑️ Keranjang berhasil dikosongkan."