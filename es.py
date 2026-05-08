import streamlit as st
from datetime import datetime

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Kasir Es Kelapa",
    layout="wide"
)

# =========================
# MENU
# =========================
menu = [
    {
        "id": 1,
        "nama": "Es Kelapa + Gula",
        "harga": 4000,
        "gambar": "https://images.unsplash.com/photo-1623065422902-30a2d299bbe4?q=80&w=1200&auto=format&fit=crop",
    },
    {
        "id": 2,
        "nama": "Es Kelapa + Gula + Susu",
        "harga": 5000,
        "gambar": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?q=80&w=1200&auto=format&fit=crop",
    },
    {
        "id": 3,
        "nama": "Kelapa Murni",
        "harga": 10000,
        "gambar": "https://images.unsplash.com/photo-1528825871115-3581a5387919?q=80&w=1200&auto=format&fit=crop",
    },
    {
        "id": 4,
        "nama": "Air Kelapa",
        "harga": 5000,
        "gambar": "https://images.unsplash.com/photo-1502741338009-cac2772e18bc?q=80&w=1200&auto=format&fit=crop",
    },
]

# =========================
# SESSION
# =========================
if "keranjang" not in st.session_state:
    st.session_state.keranjang = []

if "riwayat_transaksi" not in st.session_state:
    st.session_state.riwayat_transaksi = []

# =========================
# STYLE
# =========================
st.markdown(
    """
    <style>

    .stApp {
        background-image: url("https://images.unsplash.com/photo-1502741338009-cac2772e18bc?q=80&w=1600&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .main {
        background: rgba(255,255,255,0.80);
        padding: 20px;
        border-radius: 20px;
    }

    .stButton button {
        background-color: #16a34a;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px;
        font-weight: bold;
    }

    .stButton button:hover {
        background-color: #15803d;
        color: white;
    }

    h1, h2, h3 {
        color: #14532d;
    }

    [data-testid="stVerticalBlock"] > div:has(div.element-container) {
        background-color: rgba(255,255,255,0.85);
        padding: 15px;
        border-radius: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# TITLE
# =========================
st.title("🥥 Kasir Es Kelapa")

menu_tab, keuangan_tab = st.tabs(
    ["Kasir", "Keuangan"]
)

# =========================
# TAB KASIR
# =========================
with menu_tab:

    col1, col2 = st.columns(2)

    # =====================
    # MENU
    # =====================
    with col1:

        st.subheader("Menu")

        for item in menu:

            with st.container(border=True):

                st.image(
                    item["gambar"],
                    use_container_width=True
                )

                st.write(
                    f"### {item['nama']}"
                )

                st.write(
                    f"Rp {item['harga']:,}"
                )

                qty = st.number_input(
                    f"Qty {item['nama']}",
                    min_value=1,
                    value=1,
                    key=f"qty_{item['id']}"
                )

                if st.button(
                    f"Tambah {item['nama']}",
                    key=f"btn_{item['id']}"
                ):

                    found = False

                    for keranjang_item in st.session_state.keranjang:

                        if (
                            keranjang_item["nama"]
                            == item["nama"]
                        ):

                            keranjang_item["qty"] += qty
                            found = True
                            break

                    if not found:

                        st.session_state.keranjang.append({
                            "nama": item["nama"],
                            "harga": item["harga"],
                            "qty": qty,
                        })

                    st.success(
                        f"{item['nama']} ditambahkan"
                    )

    # =====================
    # KERANJANG
    # =====================
    with col2:

        st.subheader("Keranjang")

        total = 0

        if len(st.session_state.keranjang) == 0:

            st.info("Belum ada pesanan")

        else:

            for item in st.session_state.keranjang:

                subtotal = (
                    item["harga"]
                    * item["qty"]
                )

                total += subtotal

                st.write(
                    f"{item['nama']} x {item['qty']}"
                )

                st.write(
                    f"Rp {subtotal:,}"
                )

                st.divider()

        st.write(
            f"## Total: Rp {total:,}"
        )

        metode = st.selectbox(
            "Metode Pembayaran",
            [
                "Cash",
                "QRIS",
                "Transfer Bank",
                "E-Wallet"
            ]
        )

        uang = st.number_input(
            "Jumlah uang diterima",
            min_value=0
        )

        kembalian = uang - total

        # =====================
        # KEMBALIAN
        # =====================
        if uang > 0:

            if uang >= total:

                st.success(
                    f"Kembalian: Rp {kembalian:,}"
                )

            else:

                st.error(
                    "Uang pelanggan kurang"
                )

        # =====================
        # CETAK STRUK
        # =====================
        if st.button("Cetak Struk"):

            if total == 0:

                st.warning(
                    "Keranjang masih kosong"
                )

            elif uang < total:

                st.error(
                    "Pembayaran belum cukup"
                )

            else:

                total_item = sum(
                    item["qty"]
                    for item
                    in st.session_state.keranjang
                )

                transaksi = {
                    "tanggal": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "total": total,
                    "metode": metode,
                    "jumlah_item": total_item,
                    "detail": (
                        st.session_state
                        .keranjang
                        .copy()
                    )
                }

                st.session_state.riwayat_transaksi.append(
                    transaksi
                )

                # =====================
                # FORMAT STRUK
                # =====================
                struk_text = f"""
Tanggal :
{transaksi['tanggal']}

========================
"""

                for item in transaksi["detail"]:

                    subtotal = (
                        item["harga"]
                        * item["qty"]
                    )

                    struk_text += f"""
{item['nama']}
{item['qty']} x Rp {item['harga']:,}
= Rp {subtotal:,}

"""

                struk_text += f"""
========================
TOTAL      : Rp {total:,}
PEMBAYARAN : {metode}
TUNAI      : Rp {uang:,}
KEMBALIAN  : Rp {kembalian:,}
========================
"""

                st.success(
                    "Struk berhasil dicetak"
                )

                # =====================
                # TAMPILKAN STRUK
                # =====================
                st.markdown(
                    f"""
                    <div style="
                        background-color: white;
                        padding: 25px;
                        border-radius: 15px;
                        border: 2px dashed #999;
                        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
                        margin-top: 20px;
                        color: black;
                        max-width: 450px;
                        margin-left: auto;
                        margin-right: auto;
                    ">

                        <h2 style="
                            text-align: center;
                            font-family: monospace;
                            margin-bottom: 10px;
                        ">
                            🥥 TOKO ES KELAPA
                        </h2>

                        <hr>

                        <pre style="
                            font-family: monospace;
                            font-size: 15px;
                            white-space: pre-wrap;
                            line-height: 1.6;
                        ">
{struk_text}
                        </pre>

                        <hr>

                        <p style="
                            text-align: center;
                            font-weight: bold;
                            font-family: monospace;
                        ">
                            Terima Kasih 🙏
                        </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.balloons()

                # kosongkan keranjang
                st.session_state.keranjang = []

# =========================
# TAB KEUANGAN
# =========================
with keuangan_tab:

    st.subheader("Laporan Keuangan")

    total_pemasukan = sum(
        trx["total"]
        for trx
        in st.session_state.riwayat_transaksi
