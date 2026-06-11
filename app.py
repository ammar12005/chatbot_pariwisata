# ============================================================
#  app.py  –  Ngapain di Rumah? Flask Server
# ============================================================

from flask import Flask, request, jsonify, render_template, session
from engine import proses_pesan, reset_sesi
from database import (
    get_semua_transaksi, expire_transaksi_kadaluarsa,
    get_keranjang, hapus_keranjang_item, hapus_semua_keranjang,
)
import uuid

app = Flask(__name__)
app.secret_key = "Ngapain di Rumah?_secret_2024"   # ganti di production


@app.route("/")
def index():
    if "sid" not in session:
        session["sid"] = str(uuid.uuid4())
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    pesan = data.get("message", "").strip()

    if not pesan:
        return jsonify({"reply": "Pesan kosong. Silakan ketik sesuatu."})

    sid = session.get("sid", "default")
    balasan = proses_pesan(pesan, sid)
    return jsonify({"reply": balasan})


@app.route("/reset", methods=["POST"])
def reset():
    sid = session.get("sid", "default")
    reset_sesi(sid)
    return jsonify({"status": "ok", "reply": "Sesi berhasil direset."})


@app.route("/histori", methods=["GET"])
def histori():
    expire_transaksi_kadaluarsa()
    sid = session.get("sid", "default")
    semua = get_semua_transaksi(50)
    milik_saya = [t for t in semua if t.get("session_id") == sid]

    hasil = []
    for t in milik_saya:
        hasil.append({
            "kode":      t["kode_booking"],
            "destinasi": t["destinasi"],
            "total":     "Rp {:,}".format(t["total_bayar"]).replace(",", "."),
            "status":    t["status"],
            "waktu":     t["tanggal_pesan"].strftime("%d %b %Y, %H:%M") if t["tanggal_pesan"] else "-",
        })

    return jsonify({"histori": hasil})


# ── KERANJANG WISHLIST ────────────────────────────────────────

@app.route("/keranjang", methods=["GET"])
def keranjang_get():
    """Ambil semua item keranjang wishlist milik session ini."""
    sid = session.get("sid", "default")
    items = get_keranjang(sid)

    hasil = []
    for item in items:
        hasil.append({
            "id":            item["id"],
            "nama":          item["nama_destinasi"],
            "provinsi":      item["provinsi"].title() if item["provinsi"] else "-",
            "kota":          item["kota"].title() if item["kota"] else "-",
            "harga_dewasa":  "Rp {:,}".format(item["harga_dewasa"]).replace(",", ".") if item["harga_dewasa"] else "GRATIS",
            "harga_anak":    "Rp {:,}".format(item["harga_anak"]).replace(",", ".") if item["harga_anak"] else "GRATIS",
            "emoji":         item.get("emoji", "📍"),
            "ditambahkan":   item["ditambahkan"].strftime("%d %b %Y, %H:%M") if item.get("ditambahkan") else "-",
        })

    return jsonify({"keranjang": hasil})


@app.route("/keranjang/hapus", methods=["POST"])
def keranjang_hapus():
    """Hapus satu item dari keranjang berdasarkan nama destinasi."""
    sid = session.get("sid", "default")
    data = request.get_json()
    nama = data.get("nama", "").strip()

    if not nama:
        return jsonify({"status": "error", "pesan": "Nama destinasi tidak boleh kosong."})

    berhasil = hapus_keranjang_item(sid, nama)
    if berhasil:
        return jsonify({"status": "ok", "pesan": f"{nama} dihapus dari keranjang."})
    return jsonify({"status": "error", "pesan": "Item tidak ditemukan."})


@app.route("/keranjang/kosongkan", methods=["POST"])
def keranjang_kosongkan():
    """Kosongkan seluruh keranjang."""
    sid = session.get("sid", "default")
    hapus_semua_keranjang(sid)
    return jsonify({"status": "ok", "pesan": "Keranjang berhasil dikosongkan."})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)