import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Kasir UMKM", layout="wide")

# =========================
# DATA MENU
# =========================
menu = [
    {
        "id": 1,
        "nama": "Es Kelapa + Gula",
        "harga": 4000,
        "gambar": "assets/kelapa1.jpg",
    },
    {
        "id": 2,
        "nama": "Es Kelapa + Gula + Susu",
        "harga": 5000,
        "gambar": "assets/kelapa2.jpg",
    },
    {
        "id": 3,
        "nama": "Kelapa Murni",
        "harga": 10000,
        "gambar": "assets/kelapa3.jpg",
    },
    {
        "id": 4,
        "nama": "Air Kelapa",
        "harga": 5000,
        "gambar": "assets/kelapa4.jpg",
    },
]

# =========================
# SESSION STATE
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
    .main {
        background: linear-gradient(to bottom right, #ffe4e6, #fef9c3, #fed7aa);
    }

    h1, h2, h3 {
        color: #7c2d12;
    }

    .stButton button {
        background-color: #fb923c;
        color: white;
        border-radius: 10px;
        border: none;
    }

    .stButton button:hover {
        background-color: #ea580c;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# TITLE
# =========================
st.title("🥥 Aplikasi Kasir Es Kelapa")

menu_tab, keuangan_tab = st.tabs(["Kasir", "Keuangan"])

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

                st.write(f"### {item['nama']}")
                st.write(f"Rp {item['harga']:,}")

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

                        if keranjang_item["nama"] == item["nama"]:
                            keranjang_item["qty"] += qty
                            found = True
                            break

                    if not found:
                        st.session_state.keranjang.append({
                            "nama": item["nama"],
                            "harga": item["harga"],
                            "qty": qty,
                        })

                    st.success(f"{item['nama']} ditambahkan")

    # =====================
    # KERANJANG
    # =====================
    with col2:

        st.subheader("Keranjang")

        total = 0

        if len(st.session_state.keranjang) == 0:
            st.info("Belum ada pesanan")

        for item in st.session_state.keranjang:

            subtotal = item["harga"] * item["qty"]
            total += subtotal

            st.write(f"{item['nama']} x {item['qty']}")
            st.write(f"Rp {subtotal:,}")
            st.divider()

        st.write(f"## Total: Rp {total:,}")

        metode = st.selectbox(
            "Metode Pembayaran",
            ["Cash", "QRIS", "Transfer Bank", "E-Wallet"]
        )

        uang = st.number_input(
            "Jumlah uang diterima",
            min_value=0
        )

        kembalian = uang - total

        if uang > 0:

            if uang >= total:
                st.success(f"Kembalian: Rp {kembalian:,}")
            else:
                st.error("Uang pelanggan kurang")

        col_hapus, col_cetak = st.columns(2)

        # =====================
        # KOSONGKAN
        # =====================
        with col_hapus:

            if st.button("Kosongkan Keranjang"):

                st.session_state.keranjang = []
                st.rerun()

        # =====================
        # CETAK STRUK
        # =====================
        with col_cetak:

            if st.button("Cetak Struk"):

                if total == 0:

                    st.warning("Keranjang masih kosong")

                elif uang < total:

                    st.error("Pembayaran belum cukup")

                else:

                    # SIMPAN TRANSAKSI
                    transaksi = {
                        "tanggal": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "total": total,
                        "metode": metode,
                        "jumlah_item": len(
                            st.session_state.keranjang
                        ),
                    }

                    st.session_state.riwayat_transaksi.append(
                        transaksi
                    )

                    st.balloons()

                    st.success("Struk berhasil dicetak")

                    st.write("### Ringkasan Pesanan")

                    for item in st.session_state.keranjang:

                        st.write(
                            f"- {item['nama']} x {item['qty']}"
                        )

                    st.write(f"Total Bayar: Rp {total:,}")
                    st.write(f"Metode: {metode}")
                    st.write(f"Uang Diterima: Rp {uang:,}")
                    st.write(f"Kembalian: Rp {kembalian:,}")

                    # RESET KERANJANG
                    st.session_state.keranjang = []

# =========================
# TAB KEUANGAN
# =========================
with keuangan_tab:

    st.subheader("Laporan Keuangan")

    total_pemasukan = sum(
        item["total"]
        for item in st.session_state.riwayat_transaksi
    )

    total_transaksi = len(
        st.session_state.riwayat_transaksi
    )

    pengeluaran = 0
    laba_bersih = total_pemasukan - pengeluaran

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Pemasukan",
            f"Rp {total_pemasukan:,}"
        )

    with col2:
        st.metric(
            "Jumlah Transaksi",
            total_transaksi
        )

    with col3:
        st.metric(
            "Laba Bersih",
            f"Rp {laba_bersih:,}"
        )

    st.divider()

    if len(st.session_state.riwayat_transaksi) == 0:

        st.info("Belum ada transaksi")

    else:

        for item in reversed(
            st.session_state.riwayat_transaksi
        ):

            with st.container(border=True):

                st.write(
                    f"Tanggal: {item['tanggal']}"
                )

                st.write(
                    f"Total: Rp {item['total']:,}"
                )

                st.write(
                    f"Metode Pembayaran: {item['metode']}"
                )

                st.write(
                    f"Jumlah Item: {item['jumlah_item']}"
                )
