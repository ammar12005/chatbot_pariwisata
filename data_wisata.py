# ============================================================
#  data_wisata.py  –  Ngapain di Rumah?
#  Data destinasi wisata seluruh Indonesia
#  Struktur: Provinsi → Kota/Kabupaten → Destinasi
#  Tiket: harga_dewasa & harga_anak (anak > 5 tahun)
# ============================================================

DESTINASI_WISATA = {
    # ─────────────────────────────────────────────
    #  JAWA TENGAH
    # ─────────────────────────────────────────────
    "jawa tengah": {
        "semarang": [
            {
                "nama": "Lawang Sewu",
                "deskripsi": "Gedung bersejarah peninggalan Belanda dengan arsitektur Eropa yang megah dan kisah mistis yang terkenal.",
                "harga_dewasa": 20000,
                "harga_anak": 10000,
                "jam_buka": "07.00 – 21.00 WIB",
                "kategori": "sejarah",
                "emoji": "🏛️"
            },
            {
                "nama": "Sam Poo Kong",
                "deskripsi": "Klenteng tertua di Semarang, tempat bersejarah Laksamana Cheng Ho mendarat di tanah Jawa.",
                "harga_dewasa": 10000,
                "harga_anak": 5000,
                "jam_buka": "06.00 – 21.00 WIB",
                "kategori": "budaya",
                "emoji": "🏯"
            },
            {
                "nama": "Kota Lama Semarang",
                "deskripsi": "Kawasan bersejarah dengan bangunan kolonial Belanda, disebut 'Little Netherland'.",
                "harga_dewasa": 0,
                "harga_anak": 0,
                "jam_buka": "24 Jam",
                "kategori": "sejarah",
                "emoji": "🏙️"
            },
            {
                "nama": "Masjid Agung Jawa Tengah",
                "deskripsi": "Masjid megah dengan arsitektur perpaduan Jawa, Arab, dan Eropa. Terdapat payung hidrolik raksasa.",
                "harga_dewasa": 0,
                "harga_anak": 0,
                "jam_buka": "24 Jam",
                "kategori": "religi",
                "emoji": "🕌"
            },
            {
                "nama": "Pantai Marina",
                "deskripsi": "Pantai kota dengan fasilitas lengkap, cocok untuk bersantai dan menikmati sunset.",
                "harga_dewasa": 15000,
                "harga_anak": 8000,
                "jam_buka": "06.00 – 18.00 WIB",
                "kategori": "alam",
                "emoji": "🏖️"
            },
            {
                "nama": "Goa Kreo",
                "deskripsi": "Gua alam dengan populasi kera ekor panjang di tepi waduk Jatibarang yang indah.",
                "harga_dewasa": 10000,
                "harga_anak": 5000,
                "jam_buka": "08.00 – 17.00 WIB",
                "kategori": "alam",
                "emoji": "🦟"
            },
        ],
        "solo": [
            {
                "nama": "Keraton Kasunanan Surakarta",
                "deskripsi": "Istana Kerajaan Surakarta yang menyimpan koleksi pusaka dan artefak budaya Jawa.",
                "harga_dewasa": 15000,
                "harga_anak": 10000,
                "jam_buka": "09.00 – 14.00 WIB (Senin–Kamis & Sabtu–Minggu)",
                "kategori": "sejarah",
                "emoji": "👑"
            },
            {
                "nama": "Pura Mangkunegaran",
                "deskripsi": "Puri bangsawan Jawa dengan koleksi gamelan, wayang, dan keris bersejarah.",
                "harga_dewasa": 20000,
                "harga_anak": 10000,
                "jam_buka": "09.00 – 14.00 WIB",
                "kategori": "budaya",
                "emoji": "🏛️"
            },
            {
                "nama": "Pasar Klewer",
                "deskripsi": "Pusat grosir batik terbesar di Indonesia, surga belanja kain dan batik Solo.",
                "harga_dewasa": 0,
                "harga_anak": 0,
                "jam_buka": "08.00 – 17.00 WIB",
                "kategori": "belanja",
                "emoji": "🛍️"
            },
            {
                "nama": "Taman Balekambang",
                "deskripsi": "Taman kota bersejarah dengan danau, hutan pinus, dan pentas seni terbuka.",
                "harga_dewasa": 5000,
                "harga_anak": 3000,
                "jam_buka": "07.00 – 17.00 WIB",
                "kategori": "taman",
                "emoji": "🌳"
            },
        ],
        "magelang": [
            {
                "nama": "Candi Borobudur",
                "deskripsi": "Candi Buddha terbesar di dunia, warisan budaya UNESCO yang dibangun abad ke-8.",
                "harga_dewasa": 50000,
                "harga_anak": 25000,
                "jam_buka": "06.00 – 17.00 WIB",
                "kategori": "sejarah",
                "emoji": "🛕"
            },
            {
                "nama": "Punthuk Setumbu",
                "deskripsi": "Bukit dengan pemandangan spektakuler Borobudur di tengah kabut pagi hari.",
                "harga_dewasa": 30000,
                "harga_anak": 15000,
                "jam_buka": "04.30 – 08.00 WIB (sunrise)",
                "kategori": "alam",
                "emoji": "🌄"
            },
            {
                "nama": "Candi Mendut",
                "deskripsi": "Candi Buddha yang menyimpan tiga arca batu besar setinggi 3 meter, satu jalur dengan Borobudur.",
                "harga_dewasa": 15000,
                "harga_anak": 8000,
                "jam_buka": "07.00 – 17.00 WIB",
                "kategori": "sejarah",
                "emoji": "🛕"
            },
        ],
        "klaten": [
            {
                "nama": "Candi Prambanan",
                "deskripsi": "Candi Hindu terbesar di Indonesia, kompleks megah abad ke-9 warisan UNESCO.",
                "harga_dewasa": 50000,
                "harga_anak": 25000,
                "jam_buka": "06.00 – 17.00 WIB",
                "kategori": "sejarah",
                "emoji": "🛕"
            },
            {
                "nama": "Deles Indah",
                "deskripsi": "Kawasan wisata alam di lereng Gunung Merapi dengan pemandangan hijau dan udara sejuk.",
                "harga_dewasa": 15000,
                "harga_anak": 8000,
                "jam_buka": "07.00 – 17.00 WIB",
                "kategori": "alam",
                "emoji": "⛰️"
            },
        ],
        "karimunjawa": [
            {
                "nama": "Taman Nasional Karimunjawa",
                "deskripsi": "Kepulauan tropis dengan snorkeling, diving, pantai berpasir putih, dan terumbu karang.",
                "harga_dewasa": 25000,
                "harga_anak": 12000,
                "jam_buka": "08.00 – 16.00 WIB",
                "kategori": "alam",
                "emoji": "🏝️"
            },
        ],
        "dieng": [
            {
                "nama": "Dataran Tinggi Dieng",
                "deskripsi": "Kawasan vulkanik dengan telaga warna, kawah, candi Arjuna, dan fenomena embun upas (frost).",
                "harga_dewasa": 20000,
                "harga_anak": 10000,
                "jam_buka": "06.00 – 17.00 WIB",
                "kategori": "alam",
                "emoji": "🌋"
            },
            {
                "nama": "Telaga Warna Dieng",
                "deskripsi": "Danau kawah yang airnya berubah warna karena kandungan belerang, dikelilingi hutan pinus.",
                "harga_dewasa": 15000,
                "harga_anak": 8000,
                "jam_buka": "07.00 – 16.00 WIB",
                "kategori": "alam",
                "emoji": "🏞️"
            },
        ],
        "banyumas": [
            {
                "nama": "Baturraden",
                "deskripsi": "Wisata alam di lereng Gunung Slamet dengan air terjun, kolam air panas belerang, dan hutan.",
                "harga_dewasa": 20000,
                "harga_anak": 10000,
                "jam_buka": "07.00 – 17.00 WIB",
                "kategori": "alam",
                "emoji": "🌊"
            },
        ],
        "wonogiri": [
            {
                "nama": "Waduk Gajah Mungkur",
                "deskripsi": "Waduk besar dengan wisata air, perahu, dan pemandangan bukit hijau yang menenangkan.",
                "harga_dewasa": 15000,
                "harga_anak": 8000,
                "jam_buka": "07.00 – 17.00 WIB",
                "kategori": "alam",
                "emoji": "🚣"
            },
        ],
    },

    # ─────────────────────────────────────────────
    #  DI YOGYAKARTA
    # ─────────────────────────────────────────────
    "di yogyakarta": {
        "yogyakarta": [
            {
                "nama": "Keraton Yogyakarta",
                "deskripsi": "Istana Sultan Yogyakarta yang masih aktif, pusat budaya dan seni Jawa.",
                "harga_dewasa": 15000,
                "harga_anak": 8000,
                "jam_buka": "09.00 – 14.00 WIB",
                "kategori": "sejarah",
                "emoji": "👑"
            },
            {
                "nama": "Taman Sari",
                "deskripsi": "Istana air peninggalan Kesultanan Yogyakarta dengan kolam pemandian dan terowongan bawah tanah.",
                "harga_dewasa": 15000,
                "harga_anak": 8000,
                "jam_buka": "09.00 – 15.00 WIB",
                "kategori": "sejarah",
                "emoji": "🏯"
            },
            {
                "nama": "Malioboro",
                "deskripsi": "Jalan ikonik Yogyakarta, pusat oleh-oleh, kuliner, dan keramaian khas kota pelajar.",
                "harga_dewasa": 0,
                "harga_anak": 0,
                "jam_buka": "24 Jam",
                "kategori": "belanja",
                "emoji": "🛒"
            },
        ],
        "sleman": [
            {
                "nama": "Gunung Merapi",
                "deskripsi": "Gunung berapi aktif paling terkenal di Indonesia, tersedia jeep lava tour dan museum.",
                "harga_dewasa": 150000,
                "harga_anak": 100000,
                "jam_buka": "06.00 – 17.00 WIB",
                "kategori": "alam",
                "emoji": "🌋"
            },
            {
                "nama": "Candi Prambanan (sisi Sleman)",
                "deskripsi": "Kompleks candi Hindu megah abad ke-9, bisa diakses dari sisi Sleman maupun Klaten.",
                "harga_dewasa": 50000,
                "harga_anak": 25000,
                "jam_buka": "06.00 – 17.00 WIB",
                "kategori": "sejarah",
                "emoji": "🛕"
            },
        ],
        "gunungkidul": [
            {
                "nama": "Pantai Gunungkidul (Indrayanti, Wediombo, Baron)",
                "deskripsi": "Deretan pantai eksotis dengan tebing karang, pasir putih, dan ombak indah khas Samudera Hindia.",
                "harga_dewasa": 15000,
                "harga_anak": 8000,
                "jam_buka": "06.00 – 18.00 WIB",
                "kategori": "alam",
                "emoji": "🏖️"
            },
            {
                "nama": "Goa Pindul",
                "deskripsi": "Cave tubing melewati gua dengan stalaktit, stalagmit, dan sungai bawah tanah.",
                "harga_dewasa": 35000,
                "harga_anak": 20000,
                "jam_buka": "08.00 – 17.00 WIB",
                "kategori": "alam",
                "emoji": "🕳️"
            },
        ],
    },

    # ─────────────────────────────────────────────
    #  JAWA TIMUR
    # ─────────────────────────────────────────────
    "jawa timur": {
        "bromo tengger semeru": [
            {
                "nama": "Gunung Bromo",
                "deskripsi": "Gunung berapi aktif dengan lautan pasir dan pemandangan sunrise paling ikonik di Indonesia.",
                "harga_dewasa": 29000,
                "harga_anak": 14500,
                "jam_buka": "24 Jam (sunrise 03.30 WIB)",
                "kategori": "alam",
                "emoji": "🌋"
            },
        ],
        "banyuwangi": [
            {
                "nama": "Kawah Ijen",
                "deskripsi": "Kawah asam terbesar di dunia dengan fenomena blue fire (api biru) dan pemandangan danau hijau tosca.",
                "harga_dewasa": 100000,
                "harga_anak": 50000,
                "jam_buka": "01.00 – 12.00 WIB",
                "kategori": "alam",
                "emoji": "🔥"
            },
            {
                "nama": "Pantai Pulau Merah",
                "deskripsi": "Pantai dengan pasir merah muda dan ombak besar, surga bagi para peselancar.",
                "harga_dewasa": 15000,
                "harga_anak": 8000,
                "jam_buka": "06.00 – 18.00 WIB",
                "kategori": "alam",
                "emoji": "🏄"
            },
        ],
        "malang": [
            {
                "nama": "Coban Rondo",
                "deskripsi": "Air terjun setinggi 84 meter dikelilingi hutan pinus yang rimbun dan sejuk.",
                "harga_dewasa": 20000,
                "harga_anak": 10000,
                "jam_buka": "08.00 – 16.00 WIB",
                "kategori": "alam",
                "emoji": "💧"
            },
            {
                "nama": "Jatim Park 1",
                "deskripsi": "Taman hiburan dan edukasi dengan wahana seru, museum tubuh, dan science center.",
                "harga_dewasa": 80000,
                "harga_anak": 60000,
                "jam_buka": "08.00 – 17.00 WIB",
                "kategori": "hiburan",
                "emoji": "🎡"
            },
        ],
        "surabaya": [
            {
                "nama": "Kebun Binatang Surabaya",
                "deskripsi": "Kebun binatang tertua di Indonesia dengan koleksi satwa terlengkap se-Asia Tenggara.",
                "harga_dewasa": 30000,
                "harga_anak": 25000,
                "jam_buka": "08.00 – 16.00 WIB",
                "kategori": "hiburan",
                "emoji": "🦁"
            },
        ],
    },

    # ─────────────────────────────────────────────
    #  BALI
    # ─────────────────────────────────────────────
    "bali": {
        "badung": [
            {
                "nama": "Pantai Kuta",
                "deskripsi": "Pantai paling terkenal di Bali dengan sunset memukau dan suasana internasional.",
                "harga_dewasa": 0,
                "harga_anak": 0,
                "jam_buka": "24 Jam",
                "kategori": "alam",
                "emoji": "🌅"
            },
            {
                "nama": "Garuda Wisnu Kencana (GWK)",
                "deskripsi": "Patung megah Dewa Wisnu setinggi 121 meter, ikon budaya dan spiritual Bali.",
                "harga_dewasa": 125000,
                "harga_anak": 75000,
                "jam_buka": "09.00 – 21.00 WIB",
                "kategori": "budaya",
                "emoji": "🦅"
            },
        ],
        "gianyar": [
            {
                "nama": "Ubud Monkey Forest",
                "deskripsi": "Hutan suci dengan ratusan kera ekor panjang dan pura kuno di tengah lebatnya hutan.",
                "harga_dewasa": 80000,
                "harga_anak": 60000,
                "jam_buka": "08.30 – 18.00 WIB",
                "kategori": "alam",
                "emoji": "🐒"
            },
            {
                "nama": "Tegalalang Rice Terrace",
                "deskripsi": "Sawah terasering bertingkat yang menakjubkan, salah satu ikon fotografi Bali.",
                "harga_dewasa": 15000,
                "harga_anak": 10000,
                "jam_buka": "07.00 – 18.00 WIB",
                "kategori": "alam",
                "emoji": "🌾"
            },
        ],
        "buleleng": [
            {
                "nama": "Pantai Lovina",
                "deskripsi": "Pantai berpasir hitam di Bali Utara, terkenal dengan wisata melihat lumba-lumba liar.",
                "harga_dewasa": 0,
                "harga_anak": 0,
                "jam_buka": "24 Jam",
                "kategori": "alam",
                "emoji": "🐬"
            },
        ],
        "tabanan": [
            {
                "nama": "Tanah Lot",
                "deskripsi": "Pura di atas batu karang di tengah laut, lokasi sunset paling ikonik di Bali.",
                "harga_dewasa": 60000,
                "harga_anak": 30000,
                "jam_buka": "07.00 – 19.00 WIB",
                "kategori": "religi",
                "emoji": "🛕"
            },
        ],
    },

    # ─────────────────────────────────────────────
    #  DKI JAKARTA
    # ─────────────────────────────────────────────
    "dki jakarta": {
        "jakarta pusat": [
            {
                "nama": "Monas (Monumen Nasional)",
                "deskripsi": "Ikon ibu kota Indonesia dengan museum sejarah perjuangan bangsa dan menara emas 132 meter.",
                "harga_dewasa": 20000,
                "harga_anak": 3000,
                "jam_buka": "08.00 – 22.00 WIB",
                "kategori": "sejarah",
                "emoji": "🗼"
            },
            {
                "nama": "Museum Nasional Indonesia",
                "deskripsi": "Museum terbesar di Asia Tenggara dengan koleksi arkeologi dan kebudayaan dari seluruh nusantara.",
                "harga_dewasa": 10000,
                "harga_anak": 5000,
                "jam_buka": "08.00 – 16.00 WIB (Selasa–Minggu)",
                "kategori": "sejarah",
                "emoji": "🏛️"
            },
        ],
        "jakarta utara": [
            {
                "nama": "Kepulauan Seribu",
                "deskripsi": "Gugusan pulau-pulau kecil di Teluk Jakarta dengan snorkeling, diving, dan pantai bersih.",
                "harga_dewasa": 50000,
                "harga_anak": 30000,
                "jam_buka": "07.00 – 17.00 WIB",
                "kategori": "alam",
                "emoji": "🏝️"
            },
            {
                "nama": "Kota Tua Jakarta",
                "deskripsi": "Kawasan bersejarah era VOC dengan Museum Fatahillah, sepeda onthel, dan bangunan kolonial.",
                "harga_dewasa": 0,
                "harga_anak": 0,
                "jam_buka": "24 Jam",
                "kategori": "sejarah",
                "emoji": "🏙️"
            },
        ],
    },

    # ─────────────────────────────────────────────
    #  LOMBOK / NTB
    # ─────────────────────────────────────────────
    "nusa tenggara barat": {
        "lombok utara": [
            {
                "nama": "Gili Trawangan",
                "deskripsi": "Pulau kecil tanpa kendaraan bermotor, terkenal dengan snorkeling, diving, dan pesta pantai.",
                "harga_dewasa": 25000,
                "harga_anak": 12000,
                "jam_buka": "24 Jam",
                "kategori": "alam",
                "emoji": "🏝️"
            },
            {
                "nama": "Gunung Rinjani",
                "deskripsi": "Gunung berapi aktif tertinggi kedua di Indonesia (3.726 mdpl) dengan danau Segara Anak.",
                "harga_dewasa": 150000,
                "harga_anak": 75000,
                "jam_buka": "06.00 – 15.00 WIB (pendaftaran)",
                "kategori": "alam",
                "emoji": "⛰️"
            },
        ],
        "lombok tengah": [
            {
                "nama": "Pantai Kuta Lombok",
                "deskripsi": "Pantai eksotis dengan pasir merah muda dan bukit-bukit hijau, masih alami dan bersih.",
                "harga_dewasa": 10000,
                "harga_anak": 5000,
                "jam_buka": "06.00 – 18.00 WIB",
                "kategori": "alam",
                "emoji": "🏖️"
            },
        ],
    },

    # ─────────────────────────────────────────────
    #  PAPUA / PAPUA BARAT
    # ─────────────────────────────────────────────
    "papua barat": {
        "raja ampat": [
            {
                "nama": "Kepulauan Raja Ampat",
                "deskripsi": "Surga bahari dengan keanekaragaman hayati laut tertinggi di dunia, spot diving terbaik global.",
                "harga_dewasa": 1000000,
                "harga_anak": 500000,
                "jam_buka": "Sepanjang tahun (peak season Apr–Nov)",
                "kategori": "alam",
                "emoji": "🤿"
            },
        ],
    },

    # ─────────────────────────────────────────────
    #  SUMATERA UTARA
    # ─────────────────────────────────────────────
    "sumatera utara": {
        "samosir": [
            {
                "nama": "Danau Toba",
                "deskripsi": "Danau vulkanik terbesar di dunia dengan Pulau Samosir di tengahnya dan budaya Batak.",
                "harga_dewasa": 25000,
                "harga_anak": 15000,
                "jam_buka": "07.00 – 18.00 WIB",
                "kategori": "alam",
                "emoji": "🏞️"
            },
        ],
        "karo": [
            {
                "nama": "Berastagi",
                "deskripsi": "Dataran tinggi Karo dengan Gunung Sinabung, pasar buah, dan udara sejuk pegunungan.",
                "harga_dewasa": 20000,
                "harga_anak": 10000,
                "jam_buka": "07.00 – 17.00 WIB",
                "kategori": "alam",
                "emoji": "⛰️"
            },
        ],
    },

    # ─────────────────────────────────────────────
    #  SULAWESI SELATAN
    # ─────────────────────────────────────────────
    "sulawesi selatan": {
        "tana toraja": [
            {
                "nama": "Tanah Toraja",
                "deskripsi": "Destinasi budaya unik dengan rumah adat Tongkonan, upacara Rambu Solo, dan kuburan di tebing batu.",
                "harga_dewasa": 25000,
                "harga_anak": 15000,
                "jam_buka": "08.00 – 17.00 WIB",
                "kategori": "budaya",
                "emoji": "🏡"
            },
        ],
        "makassar": [
            {
                "nama": "Benteng Rotterdam",
                "deskripsi": "Benteng peninggalan Kerajaan Gowa-Tallo abad ke-14, kini museum sejarah Sulawesi Selatan.",
                "harga_dewasa": 10000,
                "harga_anak": 5000,
                "jam_buka": "08.00 – 18.00 WIB",
                "kategori": "sejarah",
                "emoji": "🏰"
            },
        ],
    },

    # ─────────────────────────────────────────────
    #  KALIMANTAN TIMUR
    # ─────────────────────────────────────────────
    "kalimantan timur": {
        "kutai kartanegara": [
            {
                "nama": "Taman Nasional Kutai",
                "deskripsi": "Hutan hujan tropis habitat orangutan Kalimantan, bekantan, dan berbagai satwa endemik Borneo.",
                "harga_dewasa": 20000,
                "harga_anak": 10000,
                "jam_buka": "07.00 – 17.00 WIB",
                "kategori": "alam",
                "emoji": "🦧"
            },
        ],
    },
}


# ─────────────────────────────────────────────────
#  FUNGSI-FUNGSI HELPER
# ─────────────────────────────────────────────────

def format_harga(nilai: int) -> str:
    """Format angka ke format Rupiah."""
    if nilai == 0:
        return "GRATIS"
    return f"Rp {nilai:,.0f}".replace(",", ".")


def get_semua_provinsi() -> list:
    """Kembalikan daftar semua provinsi."""
    return sorted(DESTINASI_WISATA.keys())


def get_kota_by_provinsi(provinsi: str) -> list:
    """Kembalikan daftar kota/kabupaten dalam suatu provinsi."""
    prov = provinsi.lower().strip()
    if prov in DESTINASI_WISATA:
        return sorted(DESTINASI_WISATA[prov].keys())
    return []


def get_destinasi_by_kota(provinsi: str, kota: str) -> list:
    """Kembalikan daftar destinasi dalam suatu kota/kabupaten."""
    prov = provinsi.lower().strip()
    kot = kota.lower().strip()
    if prov in DESTINASI_WISATA and kot in DESTINASI_WISATA[prov]:
        return DESTINASI_WISATA[prov][kot]
    return []


def get_semua_destinasi_provinsi(provinsi: str) -> dict:
    """Kembalikan semua destinasi dalam suatu provinsi, dikelompokkan per kota."""
    prov = provinsi.lower().strip()
    if prov in DESTINASI_WISATA:
        return DESTINASI_WISATA[prov]
    return {}


def cari_destinasi(keyword: str) -> list:
    """Cari destinasi berdasarkan keyword (nama kota, provinsi, atau nama tempat)."""
    keyword = keyword.lower().strip()
    hasil = []

    for provinsi, kota_dict in DESTINASI_WISATA.items():
        for kota, destinasi_list in kota_dict.items():
            # Cocok dengan nama kota/kabupaten atau provinsi
            if keyword in kota or keyword in provinsi:
                for dest in destinasi_list:
                    hasil.append({
                        **dest,
                        "provinsi": provinsi.title(),
                        "kota": kota.title(),
                    })
            else:
                # Cocok dengan nama destinasi
                for dest in destinasi_list:
                    if keyword in dest["nama"].lower() or keyword in dest.get("kategori", "").lower():
                        hasil.append({
                            **dest,
                            "provinsi": provinsi.title(),
                            "kota": kota.title(),
                        })
    return hasil


def format_kartu_destinasi(dest: dict, nomor: int = None) -> str:
    """Format satu destinasi menjadi teks kartu yang rapi."""
    emoji = dest.get("emoji", "📍")
    nama = dest["nama"]
    deskripsi = dest["deskripsi"]
    tiket_dewasa = format_harga(dest["harga_dewasa"])
    tiket_anak = format_harga(dest["harga_anak"])
    jam = dest.get("jam_buka", "-")

    prefix = f"{nomor}. " if nomor else ""

    lines = [
        f"{prefix}{emoji} *{nama}*",
        f"   📝 {deskripsi}",
        f"   🎫 Tiket Dewasa : {tiket_dewasa}",
    ]

    if dest["harga_anak"] != dest["harga_dewasa"]:
        lines.append(f"   👦 Tiket Anak   : {tiket_anak} (anak >5 tahun)")

    lines.append(f"   🕐 Jam Buka     : {jam}")

    if "provinsi" in dest and "kota" in dest:
        lines.append(f"   📍 Lokasi       : {dest['kota']}, {dest['provinsi']}")

    return "\n".join(lines)


# ─────────────────────────────────────────────────
#  TEST / PREVIEW
# ─────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("DAFTAR PROVINSI:")
    for prov in get_semua_provinsi():
        print(f"  🗺️  {prov.title()}")

    print("\n" + "=" * 60)
    print("KOTA DI JAWA TENGAH:")
    for kota in get_kota_by_provinsi("jawa tengah"):
        print(f"  🏙️  {kota.title()}")

    print("\n" + "=" * 60)
    print("DESTINASI DI SEMARANG:")
    destinasi = get_destinasi_by_kota("jawa tengah", "semarang")
    for i, d in enumerate(destinasi, 1):
        print(format_kartu_destinasi(d, i))
        print()

    print("=" * 60)
    print("CARI 'bromo':")
    hasil = cari_destinasi("bromo")
    for d in hasil:
        print(format_kartu_destinasi(d))
        print()