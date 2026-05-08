export default function KasirApp() {
  const menu = [
    {
      id: 1,
      nama: "Es Kelapa",
      harga: 12000,
      gambar:
        "https://images.unsplash.com/photo-1497534446932-c925b458314e",
    },
    {
      id: 2,
      nama: "Mie Pedas",
      harga: 18000,
      gambar:
        "https://images.unsplash.com/photo-1550547660-d9450f859349",
    },
    {
      id: 3,
      nama: "Ayam Geprek",
      harga: 22000,
      gambar:
        "https://images.unsplash.com/photo-1600891964599-f61ba0e24092",
    },
  ];

  const transaksiDummy = [
    {
      tanggal: "2026-05-08",
      pemasukan: 450000,
      pengeluaran: 120000,
      transaksi: 18,
    },
    {
      tanggal: "2026-05-07",
      pemasukan: 390000,
      pengeluaran: 90000,
      transaksi: 14,
    },
  ];

  const [keranjang, setKeranjang] = React.useState([]);
  const [uang, setUang] = React.useState(0);
  const [metode, setMetode] = React.useState("Cash");
  const [tab, setTab] = React.useState("kasir");

  const tambahKeranjang = (item) => {
    const cek = keranjang.find((i) => i.id === item.id);

    if (cek) {
      setKeranjang(
        keranjang.map((i) =>
          i.id === item.id ? { ...i, qty: i.qty + 1 } : i
        )
      );
    } else {
      setKeranjang([...keranjang, { ...item, qty: 1 }]);
    }
  };

  const ubahQty = (id, qty) => {
    setKeranjang(
      keranjang.map((item) =>
        item.id === id ? { ...item, qty: Number(qty) } : item
      )
    );
  };

  const total = keranjang.reduce(
    (a, b) => a + b.harga * b.qty,
    0
  );

  const kembalian = uang - total;

  const cetakStruk = () => {
    window.print();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-100 via-yellow-50 to-orange-100 p-4 relative overflow-hidden">
      <div className="absolute top-5 left-5 text-5xl opacity-20">🍔</div>
      <div className="absolute top-20 right-10 text-6xl opacity-20">🍟</div>
      <div className="absolute bottom-10 left-10 text-5xl opacity-20">🧋</div>
      <div className="absolute bottom-20 right-20 text-6xl opacity-20">🍕</div>
      <div className="absolute top-1/2 left-1/3 text-5xl opacity-10">🍩</div>
      <div className="absolute top-1/3 right-1/4 text-5xl opacity-10">🌮</div>
      <h1 className="text-3xl font-bold mb-4 text-center">
        Aplikasi Kasir & Keuangan
      </h1>

      <div className="flex justify-center gap-4 mb-6">
        <button
          onClick={() => setTab("kasir")}
          className={`px-4 py-2 rounded-xl ${
            tab === "kasir"
              ? "bg-black text-white"
              : "bg-white"
          }`}
        >
          Kasir
        </button>

        <button
          onClick={() => setTab("keuangan")}
          className={`px-4 py-2 rounded-xl ${
            tab === "keuangan"
              ? "bg-black text-white"
              : "bg-white"
          }`}
        >
          Keuangan
        </button>
      </div>

      {tab === "kasir" && (
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h2 className="text-xl font-semibold mb-4">
              Menu
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {menu.map((item) => (
                <div
                  key={item.id}
                  className="bg-white rounded-2xl shadow p-3"
                >
                  <img
                    src={item.gambar}
                    alt={item.nama}
                    className="h-40 w-full object-cover rounded-xl"
                  />

                  <h3 className="font-bold mt-2">
                    {item.nama}
                  </h3>

                  <p>
                    Rp {item.harga.toLocaleString("id-ID")}
                  </p>

                  <button
                    onClick={() => tambahKeranjang(item)}
                    className="mt-3 bg-black text-white px-3 py-2 rounded-xl w-full"
                  >
                    Tambah ke Keranjang
                  </button>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white p-4 rounded-2xl shadow">
            <h2 className="text-xl font-semibold mb-4">
              Keranjang
            </h2>

            {keranjang.length === 0 && (
              <p>Belum ada pesanan</p>
            )}

            {keranjang.map((item) => (
              <div
                key={item.id}
                className="border-b py-3"
              >
                <div className="flex justify-between">
                  <div>
                    <h3 className="font-semibold">
                      {item.nama}
                    </h3>
                    <p>
                      Rp {item.harga.toLocaleString("id-ID")}
                    </p>
                  </div>

                  <input
                    type="number"
                    min="1"
                    value={item.qty}
                    onChange={(e) =>
                      ubahQty(item.id, e.target.value)
                    }
                    className="border rounded-lg w-20 p-2"
                  />
                </div>
              </div>
            ))}

            <div className="mt-4 space-y-3">
              <div className="flex justify-between font-bold text-lg">
                <span>Total</span>
                <span>
                  Rp {total.toLocaleString("id-ID")}
                </span>
              </div>

              <select
                value={metode}
                onChange={(e) => setMetode(e.target.value)}
                className="w-full border rounded-xl p-2"
              >
                <option>Cash</option>
                <option>QRIS</option>
                <option>Transfer Bank</option>
                <option>E-Wallet</option>
              </select>

              <input
                type="number"
                placeholder="Jumlah uang diterima"
                onChange={(e) => setUang(Number(e.target.value))}
                className="w-full border rounded-xl p-2"
              />

              <div className="bg-gray-100 p-3 rounded-xl">
                <p>
                  Metode Pembayaran: {metode}
                </p>
                <p>
                  Uang Diterima: Rp {uang.toLocaleString("id-ID")}
                </p>
                <p>
                  Kembalian: Rp {kembalian.toLocaleString("id-ID")}
                </p>
              </div>

              <div className="bg-yellow-100 p-3 rounded-xl">
                <p className="font-semibold mb-2">
                  Scan Barcode
                </p>

                <input
                  type="text"
                  placeholder="Scan barcode produk"
                  className="w-full border rounded-xl p-2"
                />
              </div>

              <button
                onClick={cetakStruk}
                className="bg-green-600 text-white w-full py-3 rounded-xl font-semibold"
              >
                Cetak Struk
              </button>
            </div>
          </div>
        </div>
      )}

      {tab === "keuangan" && (
        <div className="bg-white rounded-2xl shadow p-5">
          <div className="flex gap-3 mb-5 flex-wrap">
            <button className="bg-black text-white px-4 py-2 rounded-xl">
              Hari Ini
            </button>

            <button className="bg-gray-200 px-4 py-2 rounded-xl">
              7 Hari
            </button>

            <button className="bg-gray-200 px-4 py-2 rounded-xl">
              30 Hari
            </button>

            <button className="bg-gray-200 px-4 py-2 rounded-xl">
              Kustom
            </button>
          </div>

          <div className="grid md:grid-cols-3 gap-4 mb-6">
            <div className="bg-green-100 p-4 rounded-2xl">
              <h3 className="font-semibold">
                Pemasukan
              </h3>
              <p className="text-2xl font-bold">
                Rp 840.000
              </p>
            </div>

            <div className="bg-red-100 p-4 rounded-2xl">
              <h3 className="font-semibold">
                Pengeluaran
              </h3>
              <p className="text-2xl font-bold">
                Rp 210.000
              </p>
            </div>

            <div className="bg-blue-100 p-4 rounded-2xl">
              <h3 className="font-semibold">
                Laba Bersih
              </h3>
              <p className="text-2xl font-bold">
                Rp 630.000
              </p>
            </div>
          </div>

          <div className="overflow-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="bg-gray-200">
                  <th className="border p-2">Tanggal</th>
                  <th className="border p-2">Pemasukan</th>
                  <th className="border p-2">Pengeluaran</th>
                  <th className="border p-2">Transaksi</th>
                  <th className="border p-2">Laba Bersih</th>
                </tr>
              </thead>

              <tbody>
                {transaksiDummy.map((item, index) => (
                  <tr key={index}>
                    <td className="border p-2">
                      {item.tanggal}
                    </td>

                    <td className="border p-2">
                      Rp {item.pemasukan.toLocaleString("id-ID")}
                    </td>

                    <td className="border p-2">
                      Rp {item.pengeluaran.toLocaleString("id-ID")}
                    </td>

                    <td className="border p-2 text-center">
                      {item.transaksi}
                    </td>

                    <td className="border p-2">
                      Rp {(item.pemasukan - item.pengeluaran).toLocaleString("id-ID")}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
