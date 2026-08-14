import streamlit as st

# 1. Konfigurasi Halaman Web
st.set_page_config(page_title="Essential Oil Marketplace", page_icon="🌿", layout="wide")

# 2. DICTIONARY TRANSLASI (Bahasa Inggris & Indonesia)
TEXTS = {
    "English": {
        "title": "🌿 Premium Essential Oils & Spices Catalogue",
        "subtitle": "Discover authentic Indonesian essential oils. Select your items and order via WhatsApp!",
        "search_label": "Search Product:",
        "category_label": "Category Filter:",
        "all_categories": "All Categories",
        "cart_title": "🛒 Shopping Cart",
        "cart_items": "Items in Cart:",
        "total": "Total:",
        "send_wa": "💬 Send Order via WhatsApp",
        "clear_cart": "🗑️ Clear Cart",
        "products_title": "📦 Products",
        "no_products": "No products found matching your search/filter.",
        "category": "Category:",
        "price": "Price:",
        "status": "Status:",
        "view_details": "📖 View Benefits & Usage",
        "benefits": "Benefits:",
        "usage": "How to Use:",
        "add_to_cart": "🛒 Add to Cart",
        "added_success": "Added to cart!",
        "lang_selector": "🌐 Select Language / Pilih Bahasa:"
    },
    "Bahasa Indonesia": {
        "title": "🌿 Katalog Minyak Rempah & Atsiri Premium",
        "subtitle": "Temukan minyak atsiri asli Indonesia. Pilih produk dan pesan langsung via WhatsApp!",
        "search_label": "Cari Produk:",
        "category_label": "Filter Kategori:",
        "all_categories": "Semua Kategori",
        "cart_title": "🛒 Keranjang Belanja",
        "cart_items": "Jumlah Barang:",
        "total": "Total Harga:",
        "send_wa": "💬 Kirim Pesanan via WhatsApp",
        "clear_cart": "🗑️ Kosongkan Keranjang",
        "products_title": "📦 Daftar Produk",
        "no_products": "Tidak ada produk yang cocok dengan pencarian Anda.",
        "category": "Kategori:",
        "price": "Harga:",
        "status": "Status:",
        "view_details": "📖 Lihat Manfaat & Cara Pakai",
        "benefits": "Manfaat:",
        "usage": "Cara Penggunaan:",
        "add_to_cart": "🛒 Tambah ke Keranjang",
        "added_success": "Berhasil ditambahkan ke keranjang!",
        "lang_selector": "🌐 Pilih Bahasa / Select Language:"
    }
}

# 3. SIDEBAR: Pilihan Bahasa (Letakkan di Paling Atas Sidebar)
st.sidebar.header("⚙️ Settings / Pengaturan")
bahasa = st.sidebar.selectbox(
    "🌐 Language / Bahasa",
    ["English", "Bahasa Indonesia"]
)
t = TEXTS[bahasa] # Variabel 't' menyimpan teks sesuai bahasa terpilih

# 4. Inisialisasi Session State (Database Produk & Keranjang)
if "katalog_minyak" not in st.session_state:
    st.session_state["katalog_minyak"] = [
        {
            "id": 1,
            "nama_en": "Pure Clove Essential Oil (Minyak Cengkeh)",
            "nama_id": "Minyak Atsiri Cengkeh Murni",
            "kategori": "Essential Oil",
            "harga": 12.0,
            "ukuran": "50ml",
            "stok": "In Stock",
            "manfaat_en": "Relieves toothache, natural antiseptic, warm & soothing aroma.",
            "manfaat_id": "Meringankan sakit gigi, antiseptik alami, aroma hangat & menenangkan.",
            "pemakaian_en": "Diffuse 3-5 drops or mix with carrier oil for massage.",
            "pemakaian_id": "Teteskan 3-5 tetes ke diffuser atau campur dengan carrier oil untuk pijat."
        },
        {
            "id": 2,
            "nama_en": "Citronella Grass Oil (Minyak Serai Wangi)",
            "nama_id": "Minyak Serai Wangi Alami",
            "kategori": "Essential Oil",
            "harga": 8.5,
            "ukuran": "100ml",
            "stok": "In Stock",
            "manfaat_en": "Natural insect repellent, stress relief, fresh citrus scent.",
            "manfaat_id": "Penolak nyamuk alami, meredakan stres, aroma sitrus yang segar.",
            "pemakaian_en": "Mix with water for room spray or use in aromatherapy diffuser.",
            "pemakaian_id": "Campur dengan air untuk semprotan ruangan atau gunakan di diffuser."
        },
        {
            "id": 3,
            "nama_en": "Nutmeg Essential Oil (Minyak Pala)",
            "nama_id": "Minyak Atsiri Pala Premium",
            "kategori": "Spice Extract",
            "harga": 15.0,
            "ukuran": "30ml",
            "stok": "Limited",
            "manfaat_en": "Muscle relaxation, improves sleep quality, warm spicy blend.",
            "manfaat_id": "Relaksasi otot, meningkatkan kualitas tidur, aroma rempah hangat.",
            "pemakaian_en": "Add 2-3 drops to warm bath water or diffuse at bedtime.",
            "pemakaian_id": "Teteskan 2-3 tetes ke air mandi hangat atau gunakan diffuser sebelum tidur."
        },
        {
            "id": 4,
            "nama_en": "Patchouli Natural Oil (Minyak Nilam)",
            "nama_id": "Minyak Nilam Murni (Patchouli)",
            "kategori": "Essential Oil",
            "harga": 20.0,
            "ukuran": "50ml",
            "stok": "In Stock",
            "manfaat_en": "Skin grounding, long-lasting earthy perfume, anti-aging properties.",
            "manfaat_id": "Menutrisi kulit, aroma parfum tanah yang tahan lama, kaya antioksidan.",
            "pemakaian_en": "Apply diluted to skin or use in perfumery blends.",
            "pemakaian_id": "Oleskan secara terencerkan ke kulit atau gunakan sebagai bahan dasar parfum."
        }
    ]

if "keranjang" not in st.session_state:
    st.session_state["keranjang"] = []

# 5. Header Utama Dinamis Sesuai Bahasa
st.title(t["title"])
st.write(t["subtitle"])
st.markdown("---")

# 6. SIDEBAR: Search & Filter Dinamis
st.sidebar.header("🔍 " + t["search_label"].replace(":", ""))
kata_kunci = st.sidebar.text_input(t["search_label"])

kategori_list = [t["all_categories"]] + sorted(list(set(item["kategori"] for item in st.session_state["katalog_minyak"])))
kategori_pilihan = st.sidebar.selectbox(t["category_label"], kategori_list)

st.sidebar.markdown("---")

# SIDEBAR: Keranjang Belanja Dinamis
st.sidebar.header(t["cart_title"])
cart_count = len(st.session_state["keranjang"])
st.sidebar.write(f"{t['cart_items']} **{cart_count}**")

if cart_count > 0:
    total_harga = 0.0
    st.sidebar.write("---")
    for idx, cart_item in enumerate(st.session_state["keranjang"]):
        nama_produk_cart = cart_item["nama_en"] if bahasa == "English" else cart_item["nama_id"]
        st.sidebar.write(f"• **{nama_produk_cart}**")
        st.sidebar.write(f"  _${cart_item['harga']} / {cart_item['ukuran']}_")
        total_harga += cart_item['harga']
    
    st.sidebar.markdown("---")
    st.sidebar.subheader(f"{t['total']} `${total_harga:.2f}`")
    
    # Rekap WA
    daftar_item_str = "%0A".join([
        f"- {item['nama_en'] if bahasa == 'English' else item['nama_id']} (${item['harga']})" 
        for item in st.session_state['keranjang']
    ])
    pesan_wa = f"Hello,%20I%20would%20like%20to%20order:%0A{daftar_item_str}%0A%0ATotal:%20${total_harga:.2f}"
    nomor_wa = "6281234567890" 
    link_wa = f"https://wa.me/{nomor_wa}?text={pesan_wa}"
    
    st.sidebar.markdown(f"[{t['send_wa']}]({link_wa})")
    
    if st.sidebar.button(t["clear_cart"]):
        st.session_state["keranjang"] = []
        st.rerun()

# 7. FILTERING DATA KATALOG
produk_ditampilkan = st.session_state["katalog_minyak"]

if kategori_pilihan != t["all_categories"]:
    produk_ditampilkan = [p for p in produk_ditampilkan if p["kategori"] == kategori_pilihan]

if kata_kunci:
    produk_ditampilkan = [
        p for p in produk_ditampilkan 
        if kata_kunci.lower() in p["nama_en"].lower() or kata_kunci.lower() in p["nama_id"].lower()
    ]

# 8. TAMPILAN KATALOG UTAMA
st.subheader(t["products_title"])

if not produk_ditampilkan:
    st.warning(t["no_products"])
else:
    col1, col2 = st.columns(2)
    
    for idx, item in enumerate(produk_ditampilkan):
        target_col = col1 if idx % 2 == 0 else col2
        
        # Penentuan Bahasa Produk
        nama_p = item["nama_en"] if bahasa == "English" else item["nama_id"]
        manfaat_p = item["manfaat_en"] if bahasa == "English" else item["manfaat_id"]
        pemakaian_p = item["pemakaian_en"] if bahasa == "English" else item["pemakaian_id"]
        
        with target_col:
            st.markdown(f"### {nama_p}")
            st.write(f"🏷️ **{t['category']}** {item['kategori']}")
            st.write(f"💵 **{t['price']}** `${item['harga']:.2f}` / {item['ukuran']} | 📦 **{t['status']}** `{item['stok']}`")
            
            with st.expander(t["view_details"]):
                st.write(f"✨ **{t['benefits']}** {manfaat_p}")
                st.write(f"💡 **{t['usage']}** {pemakaian_p}")
            
            if st.button(t["add_to_cart"], key=f"add_{item['id']}"):
                st.session_state["keranjang"].append(item)
                st.success(t["added_success"])
                st.rerun()
                
            st.markdown("---")
