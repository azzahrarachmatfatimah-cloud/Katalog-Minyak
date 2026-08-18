import streamlit as st
from supabase import create_client

# 1. Konfigurasi Halaman Web
st.set_page_config(page_title="Essential Oil Marketplace", page_icon="🌿", layout="wide")

# 2. Inisialisasi Supabase
@st.cache_resource
def init_supabase():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error("⚠️ Koneksi database gagal. Cek konfigurasi secrets.")
        return None

supabase = init_supabase()

# 3. Inisialisasi Session State Akun
if "user" not in st.session_state:
    st.session_state["user"] = None
if "profile" not in st.session_state:
    st.session_state["profile"] = None

# -------------------------------------------------------------------
# HELPER FUNCTIONS AUTH & PROFILE
# -------------------------------------------------------------------
def get_user_profile(user_id):
    res = supabase.table("profiles").select("*").eq("id", user_id).execute()
    return res.data[0] if res.data else None

def check_seller_verification(user_id):
    res = supabase.table("seller_verifications").select("*").eq("user_id", user_id).execute()
    return res.data[0] if res.data else None

# -------------------------------------------------------------------
# SIDEBAR: MODUL AUTENTIKASI (LOGIN / REGISTER / AKUN)
# -------------------------------------------------------------------
st.sidebar.title("🔐 Akun & Autentikasi")

if st.session_state["user"] is None:
    auth_mode = st.sidebar.radio("Pilih Akses:", ["Masuk (Login)", "Daftar (Register)"])
    
    if auth_mode == "Daftar (Register)":
        st.sidebar.subheader("Buat Akun Baru")
        reg_email = st.sidebar.text_input("Email")
        reg_name = st.sidebar.text_input("Nama Lengkap")
        reg_password = st.sidebar.text_input("Password", type="password")
        reg_role = st.sidebar.selectbox("Daftar Sebagai:", ["Pembeli (Buyer)", "Penjual (Seller)"])
        
        if st.sidebar.button("Daftar Akun"):
            if reg_email and reg_password and reg_name:
                try:
                    role_value = "seller" if "Penjual" in reg_role else "buyer"
                    # Register ke Supabase Auth
                    res = supabase.auth.sign_up({"email": reg_email, "password": reg_password})
                    if res.user:
                        # Simpan ke tabel profiles
                        supabase.table("profiles").insert({
                            "id": res.user.id,
                            "email": reg_email,
                            "full_name": reg_name,
                            "role": role_value
                        }).execute()
                        st.sidebar.success("✅ Pendaftaran berhasil! Silakan Login.")
                except Exception as e:
                    st.sidebar.error(f"Gagal daftar: {e}")
            else:
                st.sidebar.warning("Isi semua kolom pendaftaran.")

    elif auth_mode == "Masuk (Login)":
        st.sidebar.subheader("Login Akun")
        login_email = st.sidebar.text_input("Email")
        login_password = st.sidebar.text_input("Password", type="password")
        
        if st.sidebar.button("Masuk"):
            if login_email and login_password:
                try:
                    res = supabase.auth.sign_in_with_password({"email": login_email, "password": login_password})
                    if res.user:
                        profile = get_user_profile(res.user.id)
                        st.session_state["user"] = res.user
                        st.session_state["profile"] = profile
                        st.sidebar.success("✅ Login berhasil!")
                        st.rerun()
                except Exception as e:
                    st.sidebar.error("Email atau Password salah.")
            else:
                st.sidebar.warning("Masukkan Email dan Password.")

else:
    # Tampilan Jika Pengguna Sudah Login
    profile = st.session_state["profile"]
    st.sidebar.markdown(f"**Selamat datang,**\n### {profile['full_name']}")
    st.sidebar.info(f"🎭 Peran: **{profile['role'].upper()}**")
    
    if st.sidebar.button("🚪 Keluar (Logout)"):
        supabase.auth.sign_out()
        st.session_state["user"] = None
        st.session_state["profile"] = None
        st.rerun()

# -------------------------------------------------------------------
# HALAMAN UTAMA APLIKASI
# -------------------------------------------------------------------
st.title("🌿 Premium Essential Oils Marketplace")

# Navigasi Tab Sesuai Hak Akses
user_role = st.session_state["profile"]["role"] if st.session_state["profile"] else "guest"

if user_role == "seller":
    tab_katalog, tab_seller, tab_verifikasi = st.tabs(["🛍️ Katalog Produk", "⚙️ Panel Penjual", "📜 Verifikasi Kantor Usaha"])
else:
    tab_katalog, = st.tabs(["🛍️ Katalog Produk"])

# TAB 1: KATALOG PRODUK (Dapat diakses semua pengguna)
with tab_katalog:
    st.subheader("📦 Katalog Minyak Atsiri")
    res = supabase.table("katalog_minyak").select("*").execute()
    data_produk = res.data if res.data else []
    
    if not data_produk:
        st.info("Belum ada produk di katalog.")
    else:
        cols = st.columns(3)
        for idx, item in enumerate(data_produk):
            with cols[idx % 3]:
                st.markdown(f"### {item.get('nama_id', 'Produk')}")
                st.write(f"🏷️ Kategori: **{item.get('kategori', '-')}**")
                st.write(f"💵 Harga: **${item.get('harga', 0)}** | Stok: {item.get('stok', '-')}")
                with st.expander("Manfaat & Detail"):
                    st.write(item.get("manfaat_id", "-"))

# TAB 2 & 3: KHUSUS PENJUAL (SELLER)
if user_role == "seller":
    user_id = st.session_state["user"].id
    verification = check_seller_verification(user_id)

    # TAB VERIFIKASI USAHA
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
            st.warning("⚠️ Akun Anda belum terverifikasi. Lengkapi formulir legalitas di bawah untuk dapat mengunggah produk.")
            with st.form("form_verifikasi"):
                comp_name = st.text_input("Nama Perusahaan / Perusahaan Perorangan")
                npwp_no = st.text_input("Nomor NPWP Badan / Perorangan")
                address = st.text_area("Alamat Lengkap Kantor / Tempat Usaha")
                license_no = st.text_input("Nomor Izin Berusaha (NIB / SIUP)")
                
                submit_verif = st.form_submit_button("Kirim Dokumen Verifikasi")
                if submit_verif:
                    if comp_name and npwp_no and address and license_no:
                        supabase.table("seller_verifications").insert({
                            "user_id": user_id,
                            "company_name": comp_name,
                            "npwp": npwp_no,
                            "office_address": address,
                            "business_license_no": license_no,
                            "status": "verified"  # Otomatis verified untuk mode latihan
                        }).execute()
                        st.success("✅ Dokumen berhasil dikirim dan diverifikasi!")
                        st.rerun()
                    else:
                        st.error("Mohon lengkapi semua kolom persyaratan.")

    # TAB PANEL PENJUAL
    with tab_seller:
        st.subheader("➕ Tambah Produk Baru")
        if not verification or verification.get("status") != "verified":
            st.error("🔒 Fitur Tambah Produk terkunci. Anda harus menyelesaikan **Verifikasi Kantor Usaha** terlebih dahulu.")
        else:
            with st.form("form_tambah_produk"):
                p_name_en = st.text_input("Nama Produk (English)")
                p_name_id = st.text_input("Nama Produk (Indonesia)")
                p_cat = st.selectbox("Kategori", ["Essential Oil", "Carrier Oil", "Spice Oil"])
                p_price = st.number_input("Harga ($)", min_value=1.0, value=10.0)
                p_size = st.text_input("Ukuran (misal: 50ml)")
                p_stock = st.selectbox("Status Stok", ["In Stock", "Out of Stock"])
                p_benefit_id = st.text_area("Manfaat Produk (Bahasa Indonesia)")
                
                btn_save = st.form_submit_button("💾 Simpan Produk ke Database")
                if btn_save:
                    payload = {
                        "nama_en": p_name_en,
                        "nama_id": p_name_id,
                        "kategori": p_cat,
                        "harga": p_price,
                        "ukuran": p_size,
                        "stok": p_stock,
                        "manfaat_id": p_benefit_id
                    }
                    supabase.table("katalog_minyak").insert(payload).execute()
                    st.success("✅ Produk berhasil ditambahkan oleh Penjual Terverifikasi!")
                    st.rerun()
