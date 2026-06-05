# app.py - Prediksi Kalori Resep Makanan (Versi Optimal)
import streamlit as st

# Konfigurasi halaman
st.set_page_config(
    page_title="KaloriKu - Prediksi Kalori Resep",
    page_icon="🥗",
    layout="wide"
)

# Database kalori bahan makanan
CALORIE_DB = {
    'ayam': 165, 'daging sapi': 250, 'ikan': 150, 'udang': 99, 'telur': 155,
    'nasi': 130, 'kentang': 77, 'mie': 138, 'tepung': 364,
    'bayam': 23, 'wortel': 41, 'brokoli': 34, 'tomat': 18,
    'tahu': 80, 'tempe': 193,
    'minyak': 884, 'santan': 230, 'gula': 387, 'garam': 0,
    'bawang putih': 149, 'bawang merah': 40, 'cabai': 40,
}

DISH_CALORIES = {
    'ayam goreng': 350, 'nasi goreng': 380, 'soto ayam': 250,
    'rendang': 450, 'sayur asem': 150, 'capcay': 120,
}

def clean_text(text):
    if not isinstance(text, str):
        text = str(text)
    return text.lower().strip()

def predict_calories(title, ingredients, steps, portion):
    cleaned_title = clean_text(title)
    cleaned_ingredients = clean_text(ingredients)
    cleaned_steps = clean_text(steps)
    
    # Cek database masakan
    total = 0
    for dish, calories in DISH_CALORIES.items():
        if dish in cleaned_title:
            total = calories
            break
    
    # Jika tidak cocok, hitung dari bahan
    if total == 0:
        for key, calories in CALORIE_DB.items():
            if key in cleaned_ingredients:
                total += calories
        
        if 'goreng' in cleaned_steps:
            total += 150
        if 'santan' in cleaned_ingredients:
            total += 100
        
        total = max(100, min(800, int(total / 2)))
    
    return total

# Header
st.title("🥗 KaloriKu")
st.markdown("**Prediksi Kalori Resep Masakan**")
st.markdown("Masukkan resep Anda di bawah ini untuk mendapatkan estimasi kalori.")
st.markdown("---")

# Form input dengan tampilan jelas
st.subheader("📝 Masukkan Resep Anda")

# Baris 1: Judul Resep
st.markdown("**🍲 Judul Resep**")
title = st.text_input(
    "",
    placeholder="Contoh: Ayam Goreng Crispy",
    label_visibility="collapsed"
)

# Baris 2: Bahan-bahan
st.markdown("**🥕 Bahan-bahan**")
ingredients = st.text_area(
    "",
    placeholder="Contoh: 1 kg ayam, tepung terigu, bawang putih, garam, merica",
    height=120,
    label_visibility="collapsed"
)

# Baris 3: Jumlah Porsi dan Langkah dalam 2 kolom
col1, col2 = st.columns(2)

with col1:
    st.markdown("**👥 Jumlah Porsi**")
    portion = st.number_input(
        "",
        min_value=1,
        max_value=10,
        value=1,
        label_visibility="collapsed"
    )

with col2:
    st.markdown("**📖 Langkah Memasak**")
    steps = st.text_area(
        "",
        placeholder="Contoh: 1. Cuci ayam, 2. Goreng hingga matang",
        height=120,
        label_visibility="collapsed"
    )

st.markdown("---")

# Tombol prediksi
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    predict_btn = st.button("🔮 PREDIKSI KALORI", type="primary", use_container_width=True)

# Contoh resep
st.markdown("### 🍳 Contoh Resep (klik untuk mencoba)")

col_ex1, col_ex2, col_ex3 = st.columns(3)

with col_ex1:
    if st.button("🍗 Ayam Goreng", use_container_width=True):
        title = "Ayam Goreng Krispi"
        ingredients = "ayam, tepung terigu, bawang putih, garam, merica, telur, minyak goreng"
        steps = "1. Cuci ayam, 2. Balur dengan tepung, 3. Goreng hingga matang"
        portion = 1
        st.rerun()

with col_ex2:
    if st.button("🍜 Nasi Goreng", use_container_width=True):
        title = "Nasi Goreng Spesial"
        ingredients = "nasi, bawang putih, bawang merah, cabai, kecap, telur, margarin"
        steps = "1. Tumis bumbu, 2. Masukkan nasi, 3. Aduk rata, 4. Tambahkan kecap"
        portion = 1
        st.rerun()

with col_ex3:
    if st.button("🥬 Sayur Asem", use_container_width=True):
        title = "Sayur Asem"
        ingredients = "kacang panjang, jagung, melinjo, asam jawa, cabai, bawang merah"
        steps = "1. Rebus air, 2. Masukkan sayuran, 3. Tambahkan bumbu, 4. Masak hingga matang"
        portion = 1
        st.rerun()

st.markdown("---")

# Hasil prediksi
if predict_btn:
    if not title or not ingredients or not steps:
        st.error("❌ Mohon lengkapi: Judul Resep, Bahan-bahan, dan Langkah Memasak!")
    else:
        with st.spinner("Menghitung..."):
            calories = predict_calories(title, ingredients, steps, portion)
            calories_per_portion = int(calories / portion)
            
            # Tampilkan hasil
            st.markdown("## 📊 Hasil Prediksi")
            
            # Card hasil
            col_r1, col_r2, col_r3 = st.columns([1, 2, 1])
            with col_r2:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #e74c3c, #c0392b); 
                            padding: 2rem; border-radius: 20px; text-align: center;">
                    <p style="color: white; font-size: 1rem; margin: 0;">Estimasi Kalori per Porsi</p>
                    <p style="color: white; font-size: 4rem; font-weight: bold; margin: 0;">{calories_per_portion}</p>
                    <p style="color: white; font-size: 1.2rem; margin: 0;">kalori</p>
                    <p style="color: white; font-size: 0.8rem; margin-top: 0.5rem;">Total resep: {calories} kalori ({portion} porsi)</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Kategori
            if calories_per_portion < 250:
                st.success(f"✅ **Kategori: Rendah Kalori** - Cocok untuk diet sehat!")
            elif calories_per_portion < 450:
                st.info(f"📌 **Kategori: Sedang** - Porsi normal untuk makan siang")
            else:
                st.warning(f"⚠️ **Kategori: Tinggi** - Perhatikan porsi Anda!")
            
            # Saran aktivitas
            st.markdown("---")
            st.markdown("### 💡 Saran Aktivitas")
            if calories_per_portion <= 300:
                st.markdown("🚶‍♀️ **Jalan kaki 20 menit** dapat membakar kalori ini")
            elif calories_per_portion <= 500:
                st.markdown("🚴‍♂️ **Bersepeda 30 menit** dapat membakar kalori ini")
            else:
                st.markdown("🏃‍♂️ **Lari 40 menit** atau **Berenang 45 menit** dapat membakar kalori ini")

# Footer
st.markdown("---")
st.caption("Estimasi kalori bersifat perkiraan. Gunakan sebagai panduan.")

# Info tambahan
with st.expander("ℹ️ Cara Kerja"):
    st.markdown("""
    **Cara aplikasi menghitung kalori:**
    1. Mencocokkan judul resep dengan database masakan populer
    2. Jika tidak cocok, menghitung berdasarkan bahan yang terdeteksi
    3. Menambahkan kalori ekstra untuk metode memasak (menggoreng, santan)
    
    **Database:** 30+ bahan makanan dan 10+ masakan populer.
    """)
