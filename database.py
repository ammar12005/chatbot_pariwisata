# ============================================================
#  database.py  –  Ngapain di Rumah? (SQLite Version)
#  FIX: get_transaksi parse TEXT → datetime object
# ============================================================

import os
import sqlite3
import random
import string
from datetime import datetime, timedelta
from contextlib import contextmanager

# ── PATH DATABASE ─────────────────────────────────────────────
if os.getenv("STREAMLIT_SHARING_MODE") or os.getenv("HOME") == "/home/appuser":
    DB_PATH = "/tmp/chatbot_pariwisata.db"
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), "chatbot_pariwisata.db")


# ── KONEKSI ───────────────────────────────────────────────────
@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


# ── SETUP TABEL ───────────────────────────────────────────────
def setup_tabel():
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS transaksi (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                kode_booking    TEXT NOT NULL UNIQUE,
                session_id      TEXT,
                nama_pemesan    TEXT,
                no_hp           TEXT,
                provinsi        TEXT,
                kota            TEXT,
                destinasi       TEXT,
                jumlah_dewasa   INTEGER DEFAULT 0,
                jumlah_anak     INTEGER DEFAULT 0,
                harga_dewasa    INTEGER DEFAULT 0,
                harga_anak      INTEGER DEFAULT 0,
                total_bayar     INTEGER DEFAULT 0,
                metode_bayar    TEXT,
                bank_tujuan     TEXT,
                status          TEXT DEFAULT 'pending',
                tanggal_pesan   TEXT DEFAULT (datetime('now','localtime')),
                tanggal_bayar   TEXT,
                expired_at      TEXT,
                catatan         TEXT
            );

            CREATE TABLE IF NOT EXISTS keranjang (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id      TEXT NOT NULL,
                provinsi        TEXT,
                kota            TEXT,
                nama_destinasi  TEXT,
                harga_dewasa    INTEGER DEFAULT 0,
                harga_anak      INTEGER DEFAULT 0,
                emoji           TEXT,
                deskripsi       TEXT,
                jam_buka        TEXT,
                ditambahkan     TEXT DEFAULT (datetime('now','localtime'))
            );
        """)
    print(f"[DB] SQLite siap → {DB_PATH}")
    return True


# ── HELPER: parse string tanggal ke datetime ──────────────────
def _parse_dt(val):
    """Konversi string tanggal SQLite ke datetime object. Return None jika gagal."""
    if val is None:
        return None
    if isinstance(val, datetime):
        return val
    if isinstance(val, str):
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
            try:
                return datetime.strptime(val, fmt)
            except ValueError:
                continue
    return None


# ── GENERATE KODE BOOKING ─────────────────────────────────────
def generate_kode_booking() -> str:
    huruf = ''.join(random.choices(string.ascii_uppercase, k=2))
    angka = ''.join(random.choices(string.digits, k=2))
    kode  = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    tahun = datetime.now().strftime("%y%m")
    return f"WB-{huruf}{angka}{kode}-{tahun}"


# ── SIMPAN TRANSAKSI ──────────────────────────────────────────
def simpan_transaksi(data: dict) -> dict:
    kode       = generate_kode_booking()
    expired_at = (datetime.now() + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
    try:
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO transaksi
                  (kode_booking, session_id, nama_pemesan, no_hp,
                   provinsi, kota, destinasi,
                   jumlah_dewasa, jumlah_anak,
                   harga_dewasa, harga_anak, total_bayar,
                   metode_bayar, bank_tujuan, status, expired_at)
                VALUES (?,?,?,?, ?,?,?, ?,?, ?,?,?, ?,?,'pending',?)
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
        return {"sukses": True, "kode_booking": kode, "pesan": "Transaksi berhasil disimpan."}
    except Exception as e:
        return {"sukses": False, "pesan": str(e)}


# ── AMBIL TRANSAKSI BY KODE ───────────────────────────────────
def get_transaksi(kode_booking: str) -> dict | None:
    """
    Ambil satu transaksi berdasarkan kode booking.
    FIX: field tanggal diparse dari TEXT ke datetime object
    agar bisa dipanggil .strftime() di transaksi.py.
    """
    try:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM transaksi WHERE kode_booking = ?", (kode_booking,)
            ).fetchone()
            if not row:
                return None
            data = dict(row)
            # Parse semua field tanggal ke datetime object
            for field in ("tanggal_pesan", "tanggal_bayar", "expired_at"):
                data[field] = _parse_dt(data.get(field))
            return data
    except Exception:
        return None


# ── UPDATE STATUS TRANSAKSI ───────────────────────────────────
def update_status(kode_booking: str, status: str) -> bool:
    tgl = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if status == "lunas" else None
    try:
        with get_connection() as conn:
            conn.execute(
                "UPDATE transaksi SET status=?, tanggal_bayar=? WHERE kode_booking=?",
                (status, tgl, kode_booking)
            )
        return True
    except Exception:
        return False


# ── AUTO EXPIRE SEMUA ─────────────────────────────────────────
def expire_transaksi_kadaluarsa() -> int:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with get_connection() as conn:
            cur = conn.execute("""
                UPDATE transaksi
                SET status = 'dibatalkan'
                WHERE status = 'pending'
                  AND expired_at IS NOT NULL
                  AND expired_at < ?
            """, (now,))
            return cur.rowcount
    except Exception as e:
        print(f"[DB ERROR] expire_transaksi_kadaluarsa: {e}")
        return 0


# ── CEK DAN EXPIRE SATU TRANSAKSI ────────────────────────────
def cek_dan_expire_satu(kode_booking: str) -> bool:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with get_connection() as conn:
            cur = conn.execute("""
                UPDATE transaksi
                SET status = 'dibatalkan'
                WHERE kode_booking = ?
                  AND status = 'pending'
                  AND expired_at IS NOT NULL
                  AND expired_at < ?
            """, (kode_booking, now))
            return cur.rowcount > 0
    except Exception:
        return False


# ── AMBIL SEMUA TRANSAKSI ─────────────────────────────────────
def get_semua_transaksi(limit: int = 50) -> list:
    """
    Ambil semua transaksi. Field tanggal dikembalikan sebagai string
    agar render_histori_html di app-streamlit.py bisa memformatnya sendiri.
    """
    try:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM transaksi ORDER BY tanggal_pesan DESC LIMIT ?",
                (limit,)
            ).fetchall()
            return [dict(r) for r in rows]
    except Exception:
        return []


# ═══════════════════════════════════════════════════════════
#  FUNGSI KERANJANG (WISHLIST)
# ═══════════════════════════════════════════════════════════

def simpan_keranjang(session_id: str, destinasi: dict, provinsi: str, kota: str) -> dict:
    try:
        with get_connection() as conn:
            ada = conn.execute("""
                SELECT id FROM keranjang
                WHERE session_id = ? AND nama_destinasi = ?
            """, (session_id, destinasi["nama"])).fetchone()

            if ada:
                return {"sukses": False, "pesan": "sudah_ada"}

            conn.execute("""
                INSERT INTO keranjang
                  (session_id, provinsi, kota, nama_destinasi,
                   harga_dewasa, harga_anak, emoji, deskripsi, jam_buka)
                VALUES (?,?,?,?,?,?,?,?,?)
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
        return {"sukses": True, "pesan": "Destinasi berhasil disimpan ke keranjang."}
    except Exception as e:
        return {"sukses": False, "pesan": str(e)}


def get_keranjang(session_id: str) -> list:
    try:
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM keranjang
                WHERE session_id = ?
                ORDER BY ditambahkan DESC
            """, (session_id,)).fetchall()
            return [dict(r) for r in rows]
    except Exception:
        return []


def hapus_keranjang_item(session_id: str, nama_destinasi: str) -> bool:
    try:
        with get_connection() as conn:
            cur = conn.execute("""
                DELETE FROM keranjang
                WHERE session_id = ? AND nama_destinasi = ?
            """, (session_id, nama_destinasi))
            return cur.rowcount > 0
    except Exception:
        return False


def hapus_semua_keranjang(session_id: str) -> bool:
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM keranjang WHERE session_id = ?", (session_id,))
        return True
    except Exception:
        return False


# ── Auto setup saat pertama kali diimport ─────────────────────
setup_tabel()


if __name__ == "__main__":
    print(f"Database path: {DB_PATH}")
    print("Setup selesai!")