import streamlit as st

st.set_page_config(page_title="Kasir UMKM", layout="wide")

menu = [
    {
        "id": 1,
        "nama": "Es Kelapa + Gula",
        "harga": 4000,
        "gambar": "https://images.unsplash.com/photo-1623065422902-30a2d299bbe4",
    },
    {
        "id": 2,
        "nama": "Es Kelapa + Gula + Susu",
        "harga": 5000,
        "gambar": "https://images.unsplash.com/photo-1623065422902-30a2d299bbe4",
    },
    {
        "id": 3,
        "nama": "Kelapa Murni",
        "harga": 10000,
        "gambar": "https://images.unsplash.com/photo-1623065422902-30a2d299bbe4",
    },
    {
        "id": 4,
        "nama": "Air Kelapa",
        "harga": 5000,
        "gambar": "https://images.unsplash.com/photo-1623065422902-30a2d299bbe4",
    },
]

transaksiDummy = [
    {
        "tanggal": "2026-05-08",
        "pemasukan": 450000,
        "pengeluaran": 120000,
        "transaksi": 18,
    },
    {
        "tanggal": "2026-05-07",
        "pemasukan": 390000,
        "pengeluaran": 90000,
        "transaksi": 14,
    },
]

if "keranjang" not in st.session_state:
    st.session_state.keranjang = []

st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(to bottom right, #ffe4e6, #fef9c3, #fed7aa);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🍔 Aplikasi Kasir & Keuangan")

menu_tab, keuangan_tab = st.tabs(["Kasir", "Keuangan"])

with menu_tab:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Menu")

        for item in menu:
            with st.container(border=True):
                st.image(item["gambar"], use_container_width=True)
                st.write(f"### {item['nama']}")
                st.write(f"Rp {item['harga']:,}")

                qty = st.number_input(
                    f"Qty {item['nama']}",
                    min_value=1,
                    value=1,
                    key=f"qty_{item['id']}"
                )

                if st.button(f"Tambah {item['nama']}"):
                    st.session_state.keranjang.append({
                        "nama": item["nama"],
                        "harga": item["harga"],
                        "qty": qty,
                    })

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

        uang = st.number_input("Jumlah uang diterima", min_value=0)

        kembalian = uang - total

        st.success(f"Kembalian: Rp {kembalian:,}")

        st.text_input("Scan Barcode Produk")

        if st.button("Cetak Struk"):
            st.balloons()

            st.markdown("## 🧾 Struk Pembayaran")
            st.write("========================")

            for item in st.session_state.keranjang:
                subtotal = item["harga"] * item["qty"]
                st.write(f"{item['nama']} x {item['qty']}")
                st.write(f"Rp {subtotal:,}")

            st.write("------------------------")
            st.write(f"Total: Rp {total:,}")
            st.write(f"Metode: {metode}")
            st.write(f"Uang Diterima: Rp {uang:,}")
            st.write(f"Kembalian: Rp {kembalian:,}")
            st.write("========================")
            st.success("Terima kasih sudah membeli ✨")

with keuangan_tab:
    st.subheader("Laporan Keuangan")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Pemasukan", "Rp 840.000")

    with col2:
        st.metric("Pengeluaran", "Rp 210.000")

    with col3:
        st.metric("Laba Bersih", "Rp 630.000")

    st.divider()

    for item in transaksiDummy:
        laba = item["pemasukan"] - item["pengeluaran"]

        with st.container(border=True):
            st.write(f"Tanggal: {item['tanggal']}")
            st.write(f"Pemasukan: Rp {item['pemasukan']:,}")
            st.write(f"Pengeluaran: Rp {item['pengeluaran']:,}")
            st.write(f"Transaksi: {item['transaksi']}")
            st.write(f"Laba Bersih: Rp {laba:,}")
```
