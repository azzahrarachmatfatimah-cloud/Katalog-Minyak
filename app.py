import streamlit as st

# 1. Konfigurasi Halaman Web
st.set_page_config(page_title="Essential Oil Marketplace", page_icon="🌿", layout="wide")

# 2. Inisialisasi Session State (Database Produk & Keranjang)
if "katalog_minyak" not in st.session_state:
    st.session_state["katalog_minyak"] = [
        {
            "id": 1,
            "nama": "Pure Clove Essential Oil (Minyak Cengkeh)",
            "kategori": "Essential Oil",
            "harga": 12.0,
            "ukuran": "50ml",
            "stok": "In Stock",
            "manfaat": "Relieves toothache, natural antiseptic, warm & soothing aroma.",
            "pemakaian": "Diffuse 3-5 drops or mix with carrier oil for massage."
        },
        {
            "id": 2,
            "nama": "Citronella Grass Oil (Minyak Serai Wangi)",
            "kategori": "Essential Oil",
            "harga": 8.5,
            "ukuran": "100ml",
            "stok": "In Stock",
            "manfaat": "Natural insect repellent, stress relief, fresh citrus scent.",
            "pemakaian": "Mix with water for room spray or use in aromatherapy diffuser."
        },
        {
            "id": 3,
            "nama": "Nutmeg Essential Oil (Minyak Pala)",
            "kategori": "Spice Extract",
            "harga": 15.0,
            "ukuran": "30ml",
            "stok": "Limited",
            "manfaat": "Muscle relaxation, improves sleep quality, warm spicy blend.",
            "pemakaian": "Add 2-3 drops to warm bath water or diffuse at bedtime."
        },
        {
            "id": 4,
            "nama": "Patchouli Natural Oil (Minyak Nilam)",
            "kategori": "Essential Oil",
            "harga": 20.0,
            "ukuran": "50ml",
            "stok": "In Stock",
            "manfaat": "Skin grounding, long-lasting earthy perfume, anti-aging properties.",
            "pemakaian": "Apply diluted to skin or use in perfumery blends."
        }
    ]

if "keranjang" not in st.session_state:
    st.session_state["keranjang"] = []

# 3. Header Utama
st.title("🌿 Premium Essential Oils & Spices Catalogue")
st.write("Discover authentic Indonesian essential oils. Select your items and order via WhatsApp!")
st.markdown("---")

# 4. SIDEBAR: Search, Filter, & Shopping Cart
st.sidebar.header("🔍 Search & Filter")
kata_kunci = st.sidebar.text_input("Search Product:")

# Ambil daftar kategori unik
kategori_list = ["All Categories"] + sorted(list(set(item["kategori"] for item in st.session_state["katalog_minyak"])))
kategori_pilihan = st.sidebar.selectbox("Category Filter:", kategori_list)

st.sidebar.markdown("---")

# SIDEBAR: Keranjang Belanja
st.sidebar.header("🛒 Shopping Cart")
cart_count = len(st.session_state["keranjang"])
st.sidebar.write(f"Items in Cart: **{cart_count}**")

if cart_count > 0:
    total_harga = 0.0
    st.sidebar.write("---")
    for idx, cart_item in enumerate(st.session_state["keranjang"]):
        st.sidebar.write(f"• **{cart_item['nama']}**")
        st.sidebar.write(f"  _${cart_item['harga']} / {cart_item['ukuran']}_")
        total_harga += cart_item['harga']
    
    st.sidebar.markdown("---")
    st.sidebar.subheader(f"Total: `${total_harga:.2f}`")
    
    # Format Rekap Pesanan ke WhatsApp
    daftar_item_str = "%0A".join([f"- {item['nama']} (${item['harga']})" for item in st.session_state['keranjang']])
    pesan_wa = f"Hello,%20I%20would%20like%20to%20order%20the%20following%20items:%0A{daftar_item_str}%0A%0ATotal:%20${total_harga:.2f}"
    
    # Masukkan nomor WA seller kamu di sini (format kode negara tanpa +)
    nomor_wa = "6281234567890" 
    link_wa = f"https://wa.me/{nomor_wa}?text={pesan_wa}"
    
    st.sidebar.markdown(f"[💬 **Send Order via WhatsApp**]({link_wa})")
    
    if st.sidebar.button("🗑️ Clear Cart"):
        st.session_state["keranjang"] = []
        st.rerun()

# 5. FILTERING DATA KATALOG
produk_ditampilkan = st.session_state["katalog_minyak"]

# Filter Kategori
if kategori_pilihan != "All Categories":
    produk_ditampilkan = [p for p in produk_ditampilkan if p["kategori"] == kategori_pilihan]

# Filter Kata Kunci Search
if kata_kunci:
    produk_ditampilkan = [p for p in produk_ditampilkan if kata_kunci.lower() in p["nama"].lower()]

# 6. TAMPILAN KATALOG UTAMA (GRID 2 KOLOM)
st.subheader("📦 Products")

if not produk_ditampilkan:
    st.warning("No products found matching your search/filter.")
else:
    col1, col2 = st.columns(2)
    
    for idx, item in enumerate(produk_ditampilkan):
        target_col = col1 if idx % 2 == 0 else col2
        
        with target_col:
            st.markdown(f"### {item['nama']}")
            st.write(f"🏷️ **Category:** {item['kategori']}")
            st.write(f"💵 **Price:** `${item['harga']:.2f}` / {item['ukuran']} | 📦 **Status:** `{item['stok']}`")
            
            # Detail Informasi Manfaat & Cara Pakai
            with st.expander("📖 View Benefits & Usage"):
                st.write(f"✨ **Benefits:** {item['manfaat']}")
                st.write(f"💡 **How to Use:** {item['pemakaian']}")
            
            # Tombol Masukkan Keranjang
            if st.button(f"🛒 Add to Cart", key=f"add_{item['id']}"):
                st.session_state["keranjang"].append(item)
                st.success(f"Added {item['nama']} to cart!")
                st.rerun()
                
            st.markdown("---")
