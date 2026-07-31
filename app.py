import streamlit as st

# Konfigurasi Tampilan
st.set_page_config(page_title="Essential Oil Marketplace", page_icon="🌿")

st.title("🌿 Essential Oils & Spices Catalogue")
st.write(
    "Explore our premium collection of pure essential oils. Contact us directly to place your order!"
)
st.markdown("---")

# Data Produk (Menggunakan List Python Biasa - Tanpa Pandas)
data_minyak = [
    {
        "nama": "nutmeg oil (Minyak Pala)",
        "kategori": "Essential Oil",
        "harga": "Rp. 600.000 / 1kg",
        "stok": "In Stock",
        "deskripsi": "100% pure organic clove oil extracted from premium clove buds.",
    },
    {
        "nama": "Citronella Grass Oil (Minyak Serai Wangi)",
        "kategori": "Essential Oil",
        "harga": "400.000 / 1kg",
        "stok": "In Stock",
        "deskripsi": "Aromatic citronella oil perfect for aromatherapy and natural mosquito repellent.",
    },
]

# Tampilkan Katalag
st.subheader("📦 Product Catalog")

for item in data_minyak:
    st.write(f"### {item['nama']}")
    st.write(f"**Category:** {item['kategori']}")
    st.write(f"**Price:** `{item['harga']}` | **Status:** `{item['stok']}`")
    st.write(f"_{item['deskripsi']}_")

    # Tombol WhatsApp
    pesan_wa = f"Hello, I am interested in buying {item['nama']} ({item['harga']}). Is it available?"
    link_wa = f"https://wa.me/6285147158294?text={pesan_wa.replace(' ', '%20')}"

    st.markdown(f"[💬 **Inquire / Buy via WhatsApp**]({link_wa})")
    st.markdown("---")

st.info(
    "💡 *Note for Client Demo: This app operates without direct money transactions. All orders are redirected to direct chat with the seller.*"
)
