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
        "add_product_title": "➕ Seller Panel: Add New Product",
        "name_en_label": "Product Name (English):",
        "name_id_label": "Product Name (Indonesia):",
        "category_input_label": "Category:",
        "price_label": "Price ($):",
        "size_label": "Size (e.g. 50ml):",
        "benefits_en_label": "Benefits (English):",
        "benefits_id_label": "Benefits (Indonesia):",
        "usage_en_label": "Usage (English):",
        "usage_id_label": "Usage (Indonesia):",
        "save_btn": "💾 Save Product",
        "save_success": "New product successfully added to catalogue!",
        "fill_all_error": "Please fill in all product details!"
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
        "add_product_title": "➕ Panel Penjual: Tambah Produk Baru",
        "name_en_label": "Nama Produk (Inggris):",
        "name_id_label": "Nama Produk (Indonesia):",
        "category_input_label": "Kategori:",
        "price_label": "Harga ($):",
        "size_label": "Ukuran (misal: 50ml):",
        "benefits_en_label": "Manfaat (Inggris):",
        "benefits_id_label": "Manfaat (Indonesia):",
        "usage_en_label": "Cara Pakai (Inggris):",
        "usage_id_label": "Cara Pakai (Indonesia):",
        "save_btn": "💾 Simpan Produk",
        "save_success": "Produk baru berhasil ditambahkan ke katalog!",
        "fill_all_error": "Harap isi semua informasi produk!"
    }
}

# 3. SIDEBAR: Pilihan Bahasa & Filter
st.sidebar.header("⚙️ Settings / Pengaturan")
bahasa = st.sidebar.selectbox("🌐 Language / Bahasa", ["English", "Bahasa Indonesia"])
t = TEXTS[bahasa]

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

# 7. TAB NAVIGASI: KATALOG vs PANEL PENJUAL
tab1, tab2 = st.tabs([f"🛍️ {t['products_title']}", f"⚙️ {t['add_product_title']}"])

# ================= TAB 1: KATALOG PRODUK =================
with tab1:
    # FILTERING DATA KATALOG
    produk_ditampilkan = st.session_state["katalog_minyak"]

    if kategori_pilihan != t["all_categories"]:
        produk_ditampilkan = [p for p in produk_ditampilkan if p["kategori"] == kategori_pilihan]

    if kata_kunci:
        produk_ditampilkan = [
            p for p in produk_ditampilkan 
            if kata_kunci.lower() in p["nama_en"].lower() or kata_kunci.lower() in p["nama_id"].lower()
        ]

    if not produk_ditampilkan:
        st.warning(t["no_products"])
    else:
        col1, col2 = st.columns(2)
        
        for idx, item in enumerate(produk_ditampilkan):
            target_col = col1 if idx % 2 == 0 else col2
            
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

# ================= TAB 2: FORM TAMBAH PRODUK BARU =================
with tab2:
    st.subheader(t["add_product_title"])
    
    with st.form("form_tambah_minyak"):
        col_a, col_b = st.columns(2)
        
        with col_a:
            nama_en_input = st.text_input(t["name_en_label"])
            kategori_input = st.selectbox(t["category_input_label"], ["Essential Oil", "Spice Extract", "Carrier Oil", "Custom Blend"])
            harga_input = st.number_input(t["price_label"], min_value=1.0, value=10.0, step=0.5)
            manfaat_en_input = st.text_area(t["benefits_en_label"])
            usage_en_input = st.text_area(t["usage_en_label"])
            
        with col_b:
            nama_id_input = st.text_input(t["name_id_label"])
            ukuran_input = st.text_input(t["size_label"], value="50ml")
            stok_input = st.selectbox("Status:", ["In Stock", "Limited", "Out of Stock"])
            manfaat_id_input = st.text_area(t["benefits_id_label"])
            usage_id_input = st.text_area(t["usage_id_label"])
            
        submit_button = st.form_submit_button(t["save_btn"])
        
        if submit_button:
            if nama_en_input and nama_id_input and manfaat_en_input and manfaat_id_input:
                new_id = len(st.session_state["katalog_minyak"]) + 1
                new_product = {
                    "id": new_id,
                    "nama_en": nama_en_input,
                    "nama_id": nama_id_input,
                    "kategori": kategori_input,
                    "harga": float(harga_input),
                    "ukuran": ukuran_input,
                    "stok": stok_input,
                    "manfaat_en": manfaat_en_input,
                    "manfaat_id": manfaat_id_input,
                    "pemakaian_en": usage_en_input,
                    "pemakaian_id": usage_id_input
                }
                
                st.session_state["katalog_minyak"].append(new_product)
                st.success(t["save_success"])
                st.rerun()
            else:
                st.error(t["fill_all_error"])
