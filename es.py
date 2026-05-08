import streamlit as st
from datetime import datetime

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Kasir UMKM",
    layout="wide"
)

# =========================
# DATA MENU
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
        "gambar": "https://images.unsplash.com/photo-1623065422902-30a2d299bbe4?q=80&w=1200&auto=format&fit=crop",
    },
]

# =========================
# SESSION
# =========================
if "keranjang" not in st.session_state:
    st.session_state.keranjang = []

if "riwayat_transaksi" not in st.session_state:
    st.session_state.riwayat_transaksi = []

if "struk" not in st.session_state:
    st.session_state.struk = ""

# =========================
# STYLE
# =========================
st.markdown(
    """
    <style>

    .main {
        background: linear-gradient(
            to bottom right,
            #ffe4e6,
            #fef9c3,
            #fed7aa
        );
    }

    h1, h2, h3 {
        color: #7c2d12;
    }

    .stButton button {
        background-color: #fb923c;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px;
        font-weight: bold;
    }

    .stButton button:hover {
        background-color: #ea580c;
        color: white;
    }

    .struk {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border: 2px dashed #999;
        color: black;
        font-family: monospace;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# TITLE
# =========================
st.title("🥥 Aplikasi Kasir Es Kelapa")

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

        st.subheader("Menu Minuman")

        for item in menu:

            with st.container(border=True):

                st.image(
                    item["gambar"],
                    use_container_width=True
                )

                st.write(f"### {item['nama']}")
                st.write(f"Harga : Rp {item['harga']:,}")

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

        st.write(f"## Total : Rp {total:,}")

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

        if uang > 0:

            if uang >= total:

                st.success(
                    f"Kembalian : Rp {kembalian:,}"
                )

            else:

                st.error(
                    "Uang pelanggan kurang"
                )

        col_hapus, col_cetak = st.columns(2)

        # =====================
        # HAPUS KERANJANG
        # =====================
        with col_hapus:

            if st.button(
                "Kosongkan Keranjang"
            ):

                st.session_state.keranjang = []
                st.rerun()

        # =====================
        # CETAK STRUK
        # =====================
        with col_cetak:

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
                    }

                    st.session_state.riwayat_transaksi.append(
                        transaksi
                    )

                    # =================
                    # STRUK
                    # =================
                    struk = f"""
TOKO ES KELAPA
========================

Tanggal:
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

------------------------
"""

                    for item in st.session_state.keranjang:

                        subtotal = (
                            item["harga"]
                            * item["qty"]
                        )

                        struk += (
                            f"{item['nama']}\n"
                            f"{item['qty']} x "
                            f"Rp {item['harga']:,}\n"
                            f"= Rp {subtotal:,}\n\n"
                        )

                    struk += (
                        "========================\n"
                        f"TOTAL : Rp {total:,}\n"
                        f"METODE : {metode}\n"
                        f"TUNAI : Rp {uang:,}\n"
                        f"KEMBALI : Rp {kembalian:,}\n"
                        "========================\n"
                        "Terima Kasih\n"
                    )

                    st.session_state.struk = struk

                    st.success(
                        "Struk berhasil dicetak"
                    )

                    st.balloons()

                    st.session_state.keranjang = []

        # =====================
        # TAMPILKAN STRUK
        # =====================
        if st.session_state.struk != "":

            st.markdown("## 🧾 Struk Pembayaran")

            st.markdown(
                f"""
                <div class="struk">
                <pre>{st.session_state.struk}</pre>
                </div>
                """,
                unsafe
