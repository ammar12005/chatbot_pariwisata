from enum import Enum, auto
from engine import ChatbotEngine


class State(Enum):
    IDLE         = auto()
    BROWSING     = auto()   # user sedang melihat/memilih paket wisata
    CONFIRMATION = auto()
    PAYMENT      = auto()


class TourismFSM:
    def __init__(self):
        self.state    = State.IDLE
        self.nlp      = NLPEngine()
        self.cart     = []
        self.response = ""

    # ── Helpers ────────────────────────────────────────────────────────────────

    def get_response(self):
        return self.response

    def calculate_total(self):
        return sum(item["price"] * item["qty"] for item in self.cart)

    def _add_to_cart(self, orders: list[dict]):
        """
        Merge list orders baru ke self.cart.
        Jika paket sudah ada (dari turn sebelumnya), qty-nya ditambah.
        Data price & emoji sudah tersedia dari engine.parse_orders() — tidak perlu lookup ulang.
        """
        for order in orders:
            existing = next((i for i in self.cart if i["item"] == order["item"]), None)
            if existing:
                existing["qty"] += order["qty"]
            else:
                self.cart.append(order)

    def _reduce_cart(self, item_key: str, qty: int) -> str:
        """Kurangi qty paket di cart; hapus jika qty menjadi <= 0."""
        for item in self.cart:
            if item["item"] == item_key:
                item["qty"] -= qty
                if item["qty"] <= 0:
                    self.cart.remove(item)
                    return f"❌ Paket **{item_key}** telah dihapus dari keranjang."
                return f"🔻 Paket **{item_key}** dikurangi {qty}. Sisa: {item['qty']} tiket."
        return f"⚠️ Paket **{item_key}** tidak ditemukan di keranjang."

    # ── Main FSM Step ──────────────────────────────────────────────────────────

    def step(self, user_input: str = ""):
        user_input = user_input.strip()

        # detect_intent hanya dipanggil SATU kali di sini
        intent = self.nlp.detect_intent(user_input)

        # ── GLOBAL: Reset ──────────────────────────────────────────────────────
        if intent == "RESET":
            self.__init__()
            self.response = "🔄 Sesi di-reset. Halo! Mau lihat paket wisata apa?"
            return

        # ── STATE: IDLE ────────────────────────────────────────────────────────
        if self.state == State.IDLE:
            self.state    = State.BROWSING
            self.response = (
                "Halo! Selamat datang di WisataBot 🌏\n"
                "Ketik 'paket' untuk melihat destinasi wisata kami."
            )

            # Jika user langsung kirim input bermakna (misal "2 bromo"),
            # proses ulang di state BROWSING — input tidak diabaikan.
            if user_input:
                self.step(user_input)
            return

        # ── STATE: BROWSING ────────────────────────────────────────────────────
        elif self.state == State.BROWSING:

            if intent == "ASK_MENU":
                self.response = self.nlp.format_menu()

            elif intent == "CANCEL_ALL":
                self.cart     = []
                self.response = "🗑️ Keranjang wisata dikosongkan. Mau pilih destinasi lain?"

            elif intent == "REDUCE_ITEM":
                items = self.nlp.parse_reduce(user_input)
                if items:
                    msg = self._reduce_cart(items["item"], items["qty"])
                    self.response = msg
                else:
                    self.response = (
                        "Paket mana yang ingin dikurangi?\n"
                        "Contoh: *'batalkan 1 bromo'*."
                    )

            elif intent == "CHECKOUT":
                if not self.cart:
                    self.response = "🛒 Keranjang wisata masih kosong. Pilih paket dulu ya!"
                else:
                    self.state = State.CONFIRMATION
                    receipt = self.nlp.format_receipt(self.cart)
                    self.response = (
                        f"{receipt}\n\n"
                        f"Lanjut pembayaran? (Ya/Tidak)"
                    )

            elif intent == "NO":
                self.response = (
                    "Baik, tidak ada yang dibatalkan.\n"
                    "Ketik 'paket' untuk melihat destinasi atau 'bayar' jika sudah selesai."
                )

            elif intent in ("ORDER", "UNKNOWN"):
                new_orders = self.nlp.parse_orders(user_input)
                if new_orders:
                    self._add_to_cart(new_orders)
                    items_str = ", ".join(
                        f"{o['emoji']} {o['item'].replace('_', ' ').capitalize()} x{o['qty']}"
                        for o in new_orders
                    )
                    self.response = (
                        f"✅ Ditambahkan: {items_str}.\n"
                        f"Ada paket lain? (Ketik 'bayar' untuk selesai)"
                    )
                else:
                    self.response = (
                        "Maaf, saya tidak mengerti.\n"
                        "Ketik 'paket' untuk melihat destinasi wisata kami."
                    )

            else:
                self.response = (
                    "Maaf, saya tidak mengerti.\n"
                    "Ketik 'paket' untuk melihat destinasi wisata kami."
                )

        # ── STATE: CONFIRMATION ────────────────────────────────────────────────
        elif self.state == State.CONFIRMATION:

            if intent == "YES":
                total         = self.calculate_total()
                self.cart     = []
                self.state    = State.IDLE
                self.response = (
                    f"🎉 Terima kasih! Pembayaran **Rp {total:,}** diterima.\n"
                    f"Tim kami akan menghubungi Anda dalam 1x24 jam. Selamat berwisata! 🌏"
                )

            elif intent == "NO":
                self.state    = State.BROWSING
                self.response = "Oke, silakan tambah atau ubah paket wisata Anda."

            else:
                self.response = (
                    "Jawab **'Ya'** untuk lanjut pembayaran atau "
                    "**'Tidak'** untuk kembali ke pemilihan paket."
                )

        # ── STATE: PAYMENT ─────────────────────────────────────────────────────
        # Dipertahankan sebagai safety net untuk ekstensi di masa depan.
        elif self.state == State.PAYMENT:
            total         = self.calculate_total()
            self.cart     = []
            self.state    = State.IDLE
            self.response = (
                f"🎉 Pembayaran **Rp {total:,}** diterima. "
                f"Paket wisata sedang diproses!"
            )


# ── Demo ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    bot = TourismFSM()
    bot.step("")  # mulai sesi

    print("=" * 56)
    print("  WISATABOT  (ketik 'exit' untuk keluar)")
    print("=" * 56)

    for line in bot.get_response().splitlines():
        print(f"🤖 Bot  : {line}")

    while True:
        user_input = input("👤 User : ").strip()
        if user_input.lower() == "exit":
            print("👋 Sampai jumpa dan selamat berwisata!")
            break
        bot.step(user_input)
        for line in bot.get_response().splitlines():
            print(f"🤖 Bot  : {line}")