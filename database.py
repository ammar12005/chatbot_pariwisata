# ============================================================
#  database.py  –  Ngapain di Rumah?
#  Koneksi MySQL & setup tabel transaksi + keranjang
# ============================================================

import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import random
import string

# ── KONFIGURASI DATABASE ─────────────────────────────────────
DB_CONFIG = {
    "host": "localhost",
    "user": "root",          # sesuaikan
    "password": "",          # sesuaikan
    "database": "chatbot_pariwisata",
    "charset": "utf8mb4",
}

# ── KONEKSI ──────────────────────────────────────────────────
def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"[DB ERROR] Gagal konek: {e}")
        return None


# ── SETUP TABEL (jalankan sekali) ────────────────────────────
def setup_tabel():
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()

        # Tabel transaksi utama
        cur.execute("""
            CREATE TABLE IF NOT EXISTS transaksi (
                id              INT AUTO_INCREMENT PRIMARY KEY,
                kode_booking    VARCHAR(20) NOT NULL UNIQUE,
                session_id      VARCHAR(100),
                nama_pemesan    VARCHAR(100),
                no_hp           VARCHAR(20),
                provinsi        VARCHAR(100),
                kota            VARCHAR(100),
                destinasi       VARCHAR(200),
                jumlah_dewasa   INT DEFAULT 0,
                jumlah_anak     INT DEFAULT 0,
                harga_dewasa    INT DEFAULT 0,
                harga_anak      INT DEFAULT 0,
                total_bayar     INT DEFAULT 0,
                metode_bayar    VARCHAR(50),
                bank_tujuan     VARCHAR(50),
                status          ENUM('pending','lunas','dibatalkan') DEFAULT 'pending',
                tanggal_pesan   DATETIME DEFAULT CURRENT_TIMESTAMP,
                tanggal_bayar   DATETIME NULL,
                expired_at      DATETIME NULL,
                catatan         TEXT
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        # Tambah kolom expired_at jika tabel sudah ada tapi kolom belum ada
        try:
            cur.execute("""
                ALTER TABLE transaksi
                ADD COLUMN IF NOT EXISTS expired_at DATETIME NULL
                AFTER tanggal_bayar;
            """)
        except Error:
            pass  # kolom sudah ada, abaikan

        # ── Tabel keranjang (wishlist destinasi yang disimpan) ──
        cur.execute("""
            CREATE TABLE IF NOT EXISTS keranjang (
                id            INT AUTO_INCREMENT PRIMARY KEY,
                session_id    VARCHAR(100) NOT NULL,
                provinsi      VARCHAR(100),
                kota          VARCHAR(100),
                nama_destinasi VARCHAR(200),
                harga_dewasa  INT DEFAULT 0,
                harga_anak    INT DEFAULT 0,
                emoji         VARCHAR(10),
                deskripsi     TEXT,
                jam_buka      VARCHAR(100),
                ditambahkan   DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        conn.commit()
        print("[DB] Tabel 'transaksi' dan 'keranjang' siap.")
        return True
    except Error as e:
        print(f"[DB ERROR] setup_tabel: {e}")
        return False
    finally:
        cur.close()
        conn.close()


# ── GENERATE KODE BOOKING ─────────────────────────────────────
def generate_kode_booking() -> str:
    """Hasilkan kode booking unik, contoh: WB-A3X9-2024"""
    huruf = ''.join(random.choices(string.ascii_uppercase, k=2))
    angka = ''.join(random.choices(string.digits, k=2))
    kode  = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    tahun = datetime.now().strftime("%y%m")
    return f"WB-{huruf}{angka}{kode}-{tahun}"


# ── SIMPAN TRANSAKSI ─────────────────────────────────────────
def simpan_transaksi(data: dict) -> dict:
    conn = get_connection()
    if not conn:
        return {"sukses": False, "pesan": "Koneksi database gagal."}

    kode       = generate_kode_booking()
    expired_at = datetime.now() + timedelta(hours=24)

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO transaksi
              (kode_booking, session_id, nama_pemesan, no_hp,
               provinsi, kota, destinasi,
               jumlah_dewasa, jumlah_anak,
               harga_dewasa, harga_anak, total_bayar,
               metode_bayar, bank_tujuan, status, expired_at)
            VALUES
              (%s,%s,%s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s,'pending',%s)
        """, (
            kode,
            data.get("session_id", ""),
            data.get("nama_pemesan", ""),
            data.get("no_hp", ""),
            data.get("provinsi", ""),
            data.get("kota", ""),
            data.get("destinasi", ""),
            data.get("jumlah_dewasa", 0),
            data.get("jumlah_anak", 0),
            data.get("harga_dewasa", 0),
            data.get("harga_anak", 0),
            data.get("total_bayar", 0),
            data.get("metode_bayar", ""),
            data.get("bank_tujuan", ""),
            expired_at,
        ))
        conn.commit()
        return {"sukses": True, "kode_booking": kode, "pesan": "Transaksi berhasil disimpan."}
    except Error as e:
        conn.rollback()
        return {"sukses": False, "pesan": str(e)}
    finally:
        cur.close()
        conn.close()


# ── AMBIL TRANSAKSI BY KODE ───────────────────────────────────
def get_transaksi(kode_booking: str) -> dict | None:
    conn = get_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM transaksi WHERE kode_booking = %s", (kode_booking,))
        return cur.fetchone()
    except Error:
        return None
    finally:
        cur.close()
        conn.close()


# ── UPDATE STATUS TRANSAKSI ───────────────────────────────────
def update_status(kode_booking: str, status: str) -> bool:
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        tgl = datetime.now() if status == "lunas" else None
        cur.execute(
            "UPDATE transaksi SET status=%s, tanggal_bayar=%s WHERE kode_booking=%s",
            (status, tgl, kode_booking)
        )
        conn.commit()
        return True
    except Error:
        return False
    finally:
        cur.close()
        conn.close()


# ── AUTO EXPIRE ───────────────────────────────────────────────
def expire_transaksi_kadaluarsa() -> int:
    conn = get_connection()
    if not conn:
        return 0
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE transaksi
            SET status = 'dibatalkan'
            WHERE status = 'pending'
              AND expired_at IS NOT NULL
              AND expired_at < NOW()
        """)
        conn.commit()
        return cur.rowcount
    except Error as e:
        print(f"[DB ERROR] expire_transaksi_kadaluarsa: {e}")
        return 0
    finally:
        cur.close()
        conn.close()


# ── CEK DAN EXPIRE SATU TRANSAKSI ────────────────────────────
def cek_dan_expire_satu(kode_booking: str) -> bool:
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE transaksi
            SET status = 'dibatalkan'
            WHERE kode_booking = %s
              AND status = 'pending'
              AND expired_at IS NOT NULL
              AND expired_at < NOW()
        """, (kode_booking,))
        conn.commit()
        return cur.rowcount > 0
    except Error as e:
        print(f"[DB ERROR] cek_dan_expire_satu: {e}")
        return False
    finally:
        cur.close()
        conn.close()


# ── AMBIL SEMUA TRANSAKSI ─────────────────────────────────────
def get_semua_transaksi(limit: int = 50) -> list:
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT * FROM transaksi ORDER BY tanggal_pesan DESC LIMIT %s",
            (limit,)
        )
        return cur.fetchall()
    except Error:
        return []
    finally:
        cur.close()
        conn.close()


# ═══════════════════════════════════════════════════════════
#  FUNGSI KERANJANG (WISHLIST)
# ═══════════════════════════════════════════════════════════

def simpan_keranjang(session_id: str, destinasi: dict, provinsi: str, kota: str) -> dict:
    """
    Simpan satu destinasi ke tabel keranjang milik session ini.
    Cek duplikat — jika sudah ada, kembalikan pesan sudah tersimpan.
    """
    conn = get_connection()
    if not conn:
        return {"sukses": False, "pesan": "Koneksi database gagal."}
    try:
        cur = conn.cursor(dictionary=True)

        # Cek duplikat
        cur.execute("""
            SELECT id FROM keranjang
            WHERE session_id = %s AND nama_destinasi = %s
        """, (session_id, destinasi["nama"]))
        if cur.fetchone():
            return {"sukses": False, "pesan": "sudah_ada"}

        cur.execute("""
            INSERT INTO keranjang
              (session_id, provinsi, kota, nama_destinasi,
               harga_dewasa, harga_anak, emoji, deskripsi, jam_buka)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            session_id,
            provinsi,
            kota,
            destinasi["nama"],
            destinasi.get("harga_dewasa", 0),
            destinasi.get("harga_anak", 0),
            destinasi.get("emoji", "📍"),
            destinasi.get("deskripsi", ""),
            destinasi.get("jam_buka", "-"),
        ))
        conn.commit()
        return {"sukses": True, "pesan": "Destinasi berhasil disimpan ke keranjang."}
    except Error as e:
        conn.rollback()
        return {"sukses": False, "pesan": str(e)}
    finally:
        cur.close()
        conn.close()


def get_keranjang(session_id: str) -> list:
    """Ambil semua item keranjang milik session ini."""
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT * FROM keranjang
            WHERE session_id = %s
            ORDER BY ditambahkan DESC
        """, (session_id,))
        return cur.fetchall()
    except Error:
        return []
    finally:
        cur.close()
        conn.close()


def hapus_keranjang_item(session_id: str, nama_destinasi: str) -> bool:
    """Hapus satu item dari keranjang berdasarkan nama destinasi."""
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM keranjang
            WHERE session_id = %s AND nama_destinasi = %s
        """, (session_id, nama_destinasi))
        conn.commit()
        return cur.rowcount > 0
    except Error:
        return False
    finally:
        cur.close()
        conn.close()


def hapus_semua_keranjang(session_id: str) -> bool:
    """Kosongkan seluruh keranjang milik session ini."""
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM keranjang WHERE session_id = %s", (session_id,))
        conn.commit()
        return True
    except Error:
        return False
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    setup_tabel()