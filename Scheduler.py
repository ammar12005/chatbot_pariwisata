# ============================================================
#  scheduler.py  –  Ngapain di Rumah?
#  Background thread: auto-expire transaksi pending tiap 15 menit
# ============================================================

import threading
import time
from database import expire_transaksi_kadaluarsa

INTERVAL_DETIK = 15 * 60  # cek tiap 15 menit


def jalankan_scheduler():
    def loop():
        while True:
            try:
                jumlah = expire_transaksi_kadaluarsa()
                if jumlah > 0:
                    print(f"[SCHEDULER] {jumlah} transaksi diexpire otomatis.")
            except Exception as e:
                print(f"[SCHEDULER ERROR] {e}")
            time.sleep(INTERVAL_DETIK)

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()
    print("[SCHEDULER] Auto-expire aktif, cek tiap 15 menit.")