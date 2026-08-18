import streamlit as st
from supabase import create_client
import urllib.parse

# 1. Konfigurasi Halaman Web
st.set_page_config(page_title="Essential Oil Marketplace", page_icon="🌿", layout="wide")

# 2. Inisialisasi Supabase Database & Auth
@st.cache_resource
def init_supabase():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception:
        st.error("⚠️ Koneksi database gagal. Cek konfigurasi secrets.")
        return None

supabase = init_supabase()

# 3. Inisialisasi Session State
if "user" not in st.session_state:
    st.session_state["user"] = None
if "profile" not in st.session_state:
    st.session_state["profile"] = None
if "cart" not in st.session_state:
    st.session_state["cart"] = []

# --- Helper Functions ---
def get_user_profile(user_id):
    try:
        res = supabase.table("profiles").select("*").eq("id", user_id).execute()
        return res.data[0] if res.data else None
    except Exception:
        return None

def check_seller_verification(user_id):
    try:
        res = supabase.table("seller_verifications").select("*").eq("user_id", user_id).execute()
        return res.data[0] if res.data else None
    except Exception:
        return None

def get_all_sellers():
    try:
        res = supabase.table("profiles").select("id, full_name, email").eq("role", "seller").execute()
        return res.data if res.data else []
    except Exception:
        return []

# ===================================================================
# SCENARIO 1: TAMPILAN HALAMAN LOGIN & REGISTER (JIKA BELUM LOGIN)
# ===================================================================
if st.session_state["user"] is None:
    st.markdown("<h1 style='text-align: center;'>🌿 Premium Essential Oils</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Silakan masuk atau daftar akun untuk mengakses marketplace</p>", unsafe_allow_html=True)
    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        auth_tab1, auth_tab2 = st.tabs(["🔑 Masuk (Login)", "📝 Daftar (Register)"])
        
        # TAB LOGIN
        with auth_tab1:
            st.subheader("Login ke Akun Anda")
            login_email = st.text_input("Email", key="log_email")
            login_password = st.text_input("Password", type="password", key="log_pass")
            
            if st.button("Masuk Sekarang", key="btn_log", use_container_width=True):
                if login_email and login_password:
                    try:
                        res = supabase.auth.sign_in_with_password({"email": login_email, "password": login_password})
                        if res.user:
                            profile = get_user_profile(res.user.id)
                            st.session_state["user"] = res.user
                            st.session_state["profile"] = profile
                            st.success("✅ Login berhasil!")
                            st.rerun()
                    except Exception:
                        st.error("Email atau Password salah.")
                else:
                    st.warning("Masukkan Email dan Password.")

        # TAB REGISTER
        with auth_tab2:
            st.subheader("Buat Akun Baru")
            reg_email = st.text_input("Email", key="reg_email")
            reg_name = st.text_input("Nama Lengkap", key="reg_name")
            reg_password = st.text_input("Password", type="password", key="reg_pass")
            reg_role = st.selectbox("Daftar Sebagai:", ["Pembeli (Buyer)", "Penjual (Seller)"], key="reg_role")
            
            if st.button("Daftar Akun Baru", key="btn_reg", use_container_width=True):
                if reg_email and reg_password and reg_name:
                    try:
                        role_value = "seller" if "Penjual" in reg_role else "buyer"
                        res = supabase.auth.sign_up({"email": reg_email, "password": reg_password})
                        if res.user:
                            supabase.table("profiles").insert({
                                "id": res.user.id,
                                "email": reg_email,
                                "full_name": reg_name,
                                "role": role_value
                            }).execute()
                            st.success("✅ Pendaftaran berhasil! Silakan pindah ke tab Login.")
                    except Exception as e:
                        st.error(f"Gagal daftar: {e}")
                else:
                    st.warning("Isi semua kolom pendaftaran.")

# ===================================================================
# SCENARIO 2: TAMPILAN HALAMAN UTAMA MARKETPLACE (JIKA SUDAH LOGIN)
# ===================================================================
else:
    profile = st.session_state["profile"]
    full_name = profile["full_name"] if profile else "Pengguna"
    role_name = profile["role"].upper() if profile else "GUEST"
    user_role = profile["role"] if profile else "guest"
    cart_count = sum(item["qty"] for item in st.session_state["cart"])

    # SIDEBAR UTAMA
    st.sidebar.title("👤 Profil Pengguna")
    st.sidebar.markdown(f"Selamat datang,\n### **{full_name}**")
    st.sidebar.info(f"🎭 Peran: **{role_name}**")
    st.sidebar.markdown(f"🛒 **Keranjang:** `{cart_count} Produk`")
    st.sidebar.divider()
    
    if st.sidebar.button("🚪 Keluar (Logout)", key="btn_logout", use_container_width=True):
        supabase.auth.sign_out()
        st.session_state["user"] = None
        st.session_state["profile"] = None
        st.session_state["cart"] = []
        st.rerun()

    # DASHBOARD MARKETPLACE
    st.title("🌿 Premium Essential Oils Marketplace")

    # Dynamic Tabs berdasarkan Role
    if user_role == "seller":
        tab_katalog, tab_cart, tab_seller, tab_verifikasi = st.tabs([
            "🛍️ Katalog Produk", f"🛒 Keranjang ({cart_count})", "⚙️ Panel Penjual", "📜 Verifikasi Kantor"
        ])
    else:
        tab_katalog, tab_cart = st.tabs(["🛍️ Katalog Produk", f"🛒 Keranjang ({cart_count})"])

    # ---------------------------------------------------------------
    # TAB 1: KATALOG PRODUK
    # ---------------------------------------------------------------
    with tab_katalog:
        st.subheader("📦 Katalog Minyak Atsiri")
        try:
            res_prod = supabase.table("katalog_minyak").select("*, profiles(full_name)").execute()
            data_produk = res_prod.data if res_prod.data else []
        except Exception:
            data_produk = []
        
        if not data_produk:
            st.info("Belum ada produk di katalog.")
        else:
            cols = st.columns(3)
            for idx, item in enumerate(data_produk):
                with cols[idx % 3]:
                    st.markdown(f"### {item.get('nama_id', 'Produk')}")
                    
                    # Menampilkan nama Toko / Penjual pemilik produk
                    seller_info = item.get("profiles")
                    seller_name = seller_info.get("full_name") if seller_info else "Toko Resmi"
                    st.caption(f"🏪 Toko: **{seller_name}**")
                    
                    st.write(f"🏷️ Kategori: **{item.get('kategori', '-')}**")
                    st.write(f"💵 Harga: **${item.get('harga', 0)}** | Stok: {item.get('stok', '-')}")
                    
                    with st.expander("Manfaat & Detail"):
                        st.write(item.get("manfaat_id", "-"))
                    
                    if st.button(f"🛒 Tambah ke Keranjang", key=f"add_{item.get('id', idx)}"):
                        existing_item = next((c for c in st.session_state["cart"] if c["id"] == item["id"]), None)
                        if existing_item:
                            existing_item["qty"] += 1
                        else:
                            st.session_state["cart"].append({
                                "id": item["id"],
                                "nama": item.get("nama_id", "Produk"),
                                "harga": float(item.get("harga", 0)),
                                "seller_id": item.get("seller_id"),
                                "seller_name": seller_name,
                                "qty": 1
                            })
                        st.toast(f"✅ {item.get('nama_id')} berhasil ditambahkan!", icon="🛒")
                        st.rerun()

    # ---------------------------------------------------------------
    # TAB 2: KERANJANG & FITUR PILIH PENJUAL DIRECT ORDER
    # ---------------------------------------------------------------
    with tab_cart:
        st.subheader("🛒 Ringkasan Keranjang Belanja")
        
        if not st.session_state["cart"]:
            st.info("Keranjang belanja kamu masih kosong. Pilih produk terlebih dahulu di tab Katalog.")
        else:
            total_belanja = 0.0
            
            for idx, item in enumerate(st.session_state["cart"]):
                c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
                with c1:
                    st.write(f"**{item['nama']}**")
                    st.caption(f"Toko asal: {item.get('seller_name', 'Toko Resmi')}")
                with c2:
                    st.write(f"${item['harga']} / unit")
                with c3:
                    st.write(f"Jumlah: **{item['qty']}**")
                with c4:
                    if st.button("❌", key=f"del_{idx}"):
                        st.session_state["cart"].pop(idx)
                        st.rerun()
                total_belanja += item["harga"] * item["qty"]
            
            st.divider()
            st.markdown(f"### Total Tagihan: **${total_belanja:.2f}**")
            
            st.subheader("🏬 Pilih Toko / Penjual Tujuan Pesanan")
            
            # Mendapatkan daftar Penjual terdaftar
            sellers = get_all_sellers()
            seller_options = {f"{s['full_name']} ({s['email']})": s for s in sellers}
            
            selected_seller_label = st.selectbox(
                "Pilih Penjual yang ingin Anda hubungi untuk transaksi ini:",
                options=list(seller_options.keys()) if seller_options else ["Belum ada Penjual Terdaftar"]
            )
            
            st.caption("🔒 Pembayaran dilakukan secara aman via P2P Direct Transfer langsung ke rekening Penjual.")
            
            # Form Data Checkout
            with st.form("form_checkout"):
                buyer_name = st.text_input("Nama Penerima", value=full_name)
                buyer_phone = st.text_input("Nomor Telepon / WhatsApp Pembeli", placeholder="628123456789")
                buyer_address = st.text_area("Alamat Pengiriman Lengkap")
                seller_phone = st.text_input("Nomor WhatsApp Penjual (Tujuan Pesanan)", placeholder="628123456789")
                
                checkout_platform = st.selectbox("Pilih Platform Pemesanan Direct:", [
                    "WhatsApp Direct Order",
                    "Telegram Direct Order",
                    "Email Order Format"
                ])
                
                submit_order = st.form_submit_button("🚀 Buat Pesanan & Kirim Pesan")
                
                if submit_order:
                    if buyer_name and buyer_phone and buyer_address and seller_phone:
                        # 1. Simpan Pesanan ke Supabase
                        try:
                            supabase.table("orders").insert({
                                "buyer_id": st.session_state["user"].id,
                                "items": st.session_state["cart"],
                                "total_price": total_belanja,
                                "status": "pending"
                            }).execute()
                        except Exception:
                            pass
                        
                        # 2. Format Teks Invoice Pesanan
                        selected_seller_name = selected_seller_label.split(" (")[0]
                        item_text = "\n".join([f"- {i['nama']} ({i['qty']}x) : ${i['harga']*i['qty']:.2f}" for i in st.session_state["cart"]])
                        
                        message_template = (
                            f"Halo Toko/Penjual ({selected_seller_name}), saya ingin memesan produk berikut:\n\n"
                            f"{item_text}\n\n"
                            f"*Total Tagihan:* ${total_belanja:.2f}\n\n"
                            f"*Data Pembeli:*\n"
                            f"- Nama: {buyer_name}\n"
                            f"- No HP: {buyer_phone}\n"
                            f"- Alamat: {buyer_address}\n\n"
                            f"Mohon infokan instruksi pembayaran P2P. Terima kasih!"
                        )
                        
                        # 3. Redirect / Generator Link Direct Order
                        encoded_msg = urllib.parse.quote(message_template)
                        
                        if checkout_platform == "WhatsApp Direct Order":
                            target_wa = seller_phone.replace("+", "").replace(" ", "").replace("-", "")
                            wa_url = f"https://wa.me/{target_wa}?text={encoded_msg}"
                            st.success("✅ Pesanan berhasil dibuat!")
                            st.markdown(f"[👉 **Klik Di Sini untuk Mengirim Pesanan via WhatsApp ke {selected_seller_name}**]({wa_url})", unsafe_allow_html=True)
                            
                        elif checkout_platform == "Telegram Direct Order":
                            tg_url = f"https://t.me/share/url?url=&text={encoded_msg}"
                            st.success("✅ Pesanan berhasil dibuat!")
                            st.markdown(f"[👉 **Klik Di Sini untuk Mengirim Pesanan via Telegram**]({tg_url})", unsafe_allow_html=True)
                            
                        elif checkout_platform == "Email Order Format":
                            st.code(message_template, language="text")
                            st.info("Silakan salin draf teks pesanan di atas dan kirimkan langsung ke email Penjual.")
                        
                        # Reset Keranjang
                        st.session_state["cart"] = []
                    else:
                        st.error("Lengkapi nama, nomor telepon pembeli, alamat pengiriman, dan nomor WhatsApp penjual.")

    # ---------------------------------------------------------------
    # TAB 3 & 4: FITUR PENJUAL (SELLER ONLY)
    # ---------------------------------------------------------------
    if user_role == "seller":
        user_id = st.session_state["user"].id
        verification = check_seller_verification(user_id)

        with tab_verifikasi:
            st.subheader("🏢 Verifikasi Identitas Kantor & Legalitas Penjual")
            if verification:
                st.success(f"📌 Status Verifikasi Saat Ini: **{verification['status'].upper()}**")
                st.json({
                    "Nama Perusahaan/Usaha": verification["company_name"],
                    "NPWP": verification["npwp"],
                    "Alamat Kantor": verification["office_address"],
                    "Nomor Izin Usaha (NIB/SIUP)": verification["business_license_no"]
                })
            else:
                st.warning("⚠️ Isi formulir verifikasi usaha terlebih dahulu.")
                with st.form("form_verifikasi"):
                    comp_name = st.text_input("Nama Perusahaan / Usaha")
                    npwp_no = st.text_input("Nomor NPWP")
                    address = st.text_area("Alamat Kantor")
                    license_no = st.text_input("Nomor NIB / SIUP")
                    if st.form_submit_button("Kirim Dokumen Verifikasi"):
                        if comp_name and npwp_no and address and license_no:
                            supabase.table("seller_verifications").insert({
                                "user_id": user_id,
                                "company_name": comp_name,
                                "npwp": npwp_no,
                                "office_address": address,
                                "business_license_no": license_no,
                                "status": "verified"
                            }).execute()
                            st.success("✅ Terverifikasi!")
                            st.rerun()

        with tab_seller:
            st.subheader("➕ Panel Penjual (Tambah Produk)")
            if not verification or verification.get("status") != "verified":
                st.error("🔒 Fitur terkunci. Selesaikan Verifikasi Kantor Usaha terlebih dahulu.")
            else:
                with st.form("form_tambah_produk"):
                    p_name_en = st.text_input("Nama Produk (English)")
                    p_name_id = st.text_input("Nama Produk (Indonesia)")
                    p_cat = st.selectbox("Kategori", ["Essential Oil", "Carrier Oil", "Spice Oil"])
                    p_price = st.number_input("Harga ($)", min_value=1.0, value=10.0)
                    p_size = st.text_input("Ukuran (misal: 50ml)")
                    p_stock = st.selectbox("Status Stok", ["In Stock", "Out of Stock"])
                    p_benefit_id = st.text_area("Manfaat Produk")
                    
                    if st.form_submit_button("💾 Simpan Produk"):
                        supabase.table("katalog_minyak").insert({
                            "seller_id": user_id,
                            "nama_en": p_name_en,
                            "nama_id": p_name_id,
                            "kategori": p_cat,
                            "harga": p_price,
                            "ukuran": p_size,
                            "stok": p_stock,
                            "manfaat_id": p_benefit_id
                        }).execute()
                        st.success("✅ Produk berhasil ditambahkan!")
                        st.rerun()
