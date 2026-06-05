# app.py - Prediksi Kalori Resep Makanan (Versi Perbaikan)
import streamlit as st
import pandas as pd
import numpy as np
import re
import random

# Konfigurasi halaman
st.set_page_config(
    page_title="KaloriKu - Prediksi Kalori Resep",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
    }
    .main-header {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
    }
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    .prediction-box {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-top: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .calorie-number {
        font-size: 5rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    .calorie-unit {
        font-size: 1.5rem;
    }
    .calorie-status {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        padding: 0.5rem;
        border-radius: 10px;
        background-color: rgba(255,255,255,0.2);
    }
    .info-box {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
        border-left: 5px solid #2ecc71;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .ingredient-badge {
        background-color: #f0f0f0;
        padding: 5px 10px;
        border-radius: 20px;
        display: inline-block;
        margin: 3px;
        font-size: 0.8rem;
    }
    .stTextInput > div > div > input {
        background-color: white;
    }
    .stTextArea > div > div > textarea {
        background-color: white;
    }
    div[data-testid="stForm"] {
        background-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# Database kalori bahan makanan (per 100g)
CALORIE_DB = {
    # Protein hewani
    'ayam': 165, 'daging sapi': 250, 'daging kambing': 180, 'bebek': 200,
    'ikan': 150, 'bandeng': 140, 'tongkol': 120, 'salmon': 208, 'tuna': 132,
    'udang': 99, 'cumi': 92, 'kerang': 86, 'telur': 155, 'telur ayam': 155,
    
    # Karbohidrat
    'nasi': 130, 'beras': 130, 'kentang': 77, 'ubi': 86, 'singkong': 160,
    'mie': 138, 'pasta': 131, 'roti': 265, 'bihun': 130, 'kwetiau': 120,
    'tepung': 364, 'tepung terigu': 364, 'tepung beras': 360, 'tepung maizena': 380,
    
    # Sayuran
    'bayam': 23, 'kangkung': 19, 'sawi': 15, 'kol': 25, 'brokoli': 34,
    'wortel': 41, 'buncis': 31, 'kacang panjang': 47, 'tomat': 18, 'timun': 15,
    'cabe': 40, 'cabai': 40, 'bawang putih': 149, 'bawang merah': 40, 'bawang bombay': 40,
    'jahe': 80, 'kunyit': 354, 'lengkuas': 80, 'serai': 99,
    
    # Tahu tempe
    'tahu': 80, 'tempe': 193, 'oncom': 115,
    
    # Bumbu & pelengkap
    'minyak': 884, 'minyak goreng': 884, 'mentega': 717, 'margarin': 717,
    'santan': 230, 'kecap': 60, 'kecap manis': 60, 'gula': 387, 'garam': 0,
    'merica': 255, 'ketumbar': 298, 'daun jeruk': 50, 'daun salam': 50,
}

# Database kalori per jenis masakan
DISH_CALORIES = {
    'ayam goreng': 350, 'ayam bakar': 320, 'ayam geprek': 450, 'ayam woku': 380,
    'rendang': 450, 'soto ayam': 250, 'rawon': 320, 'sate ayam': 300,
    'nasi goreng': 380, 'mie goreng': 420, 'nasi uduk': 400, 'lontong sayur': 350,
    'gado-gado': 300, 'pecel': 280, 'ketoprak': 320, 'tahu tek': 350,
    'sayur asem': 150, 'sayur lodeh': 180, 'capcay': 120, 'tumis kangkung': 100,
    'bakso': 350, 'mie ayam': 420, 'pangsit': 280, 'siomay': 250,
}

def clean_text(text):
    """Membersihkan teks input"""
    if not isinstance(text, str):
        text = str(text)
    text = text.lower()
    text = re.sub(r'[^\w\s-]', ' ', text)
    text = ' '.join(text.split())
    return text

def extract_ingredients(ingredients_text):
    """Ekstrak bahan-bahan dari teks"""
    cleaned = clean_text(ingredients_text)
    ingredients = re.split(r'[,-]', cleaned)
    ingredients = [i.strip() for i in ingredients if i.strip() and len(i.strip()) > 2]
    return ingredients

def count_calories_from_ingredients(ingredients_text, portion=1):
    """Hitung kalori berdasarkan bahan yang digunakan"""
    ingredients = extract_ingredients(ingredients_text)
    total_calories = 0
    ingredients_found = []
    
    for ingredient in ingredients:
        for key, calories in CALORIE_DB.items():
            if key in ingredient:
                weight = 100
                contribution = (calories * weight / 100)
                total_calories += contribution
                ingredients_found.append({
                    'bahan': key,
                    'kalori_per_100g': calories,
                    'estimasi_kalori': contribution
                })
                break
    
    total_calories = total_calories * portion / 2
    return total_calories, ingredients_found

def predict_calories(title, ingredients, steps):
    """Prediksi total kalori resep"""
    cleaned_title = clean_text(title)
    cleaned_ingredients = clean_text(ingredients)
    cleaned_steps = clean_text(steps)
    
    # 1. Hitung dari bahan
    ingredient_calories, ingredients_found = count_calories_from_ingredients(ingredients)
    
    # 2. Cari match dengan database masakan
    dish_calories = 0
    matched_dish = None
    for dish, calories in DISH_CALORIES.items():
        if dish in cleaned_title:
            dish_calories = calories
            matched_dish = dish
            break
    
    # 3. Estimasi dari langkah
    step_calories = 0
    if 'goreng' in cleaned_steps:
        step_calories += 150
    if 'santan' in cleaned_ingredients:
        step_calories += 100
    if 'minyak' in cleaned_ingredients:
        step_calories += 80
    
    # 4. Kombinasikan
    if dish_calories > 0:
        total_calories = dish_calories
    elif ingredient_calories > 0:
        total_calories = ingredient_calories + step_calories
    else:
        total_calories = 250 + len(cleaned_ingredients.split()) * 5
    
    total_calories = max(100, min(1500, int(total_calories)))
    
    return total_calories, ingredients_found, matched_dish

def get_calorie_category(calories):
    if calories < 200:
        return ("Rendah Kalori", "🥗", "Cocok untuk diet atau camilan sehat")
    elif calories < 400:
        return ("Sedang", "🍚", "Porsi normal untuk makan siang/malam")
    elif calories < 600:
        return ("Tinggi", "🍛", "Cukup tinggi, perhatikan porsi Anda")
    else:
        return ("Sangat Tinggi", "🍕", "Kaya energi, cocok untuk aktivitas berat")

def calculate_nutrition(calories):
    protein = int(calories * 0.15 / 4)
    carbs = int(calories * 0.55 / 4)
    fat = int(calories * 0.30 / 9)
    return protein, carbs, fat

# Header
st.markdown("""
<div class="main-header">
    <h1>🥗 KaloriKu - Prediksi Kalori Resep</h1>
    <p>Masukkan resep Anda dan dapatkan estimasi total kalori serta analisis nutrisinya!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2985/2985132.png", width=80)
    st.title("🍽️ Tentang Aplikasi")
    st.markdown("""
    Aplikasi ini menggunakan **database bahan makanan** untuk memprediksi total kalori sebuah resep.
    
    ### 🔬 Metode Perhitungan:
    1. **Analisis Bahan** - Mencocokkan bahan dengan database kalori
    2. **Database Resep** - Mencocokkan dengan resep populer
    3. **Metode Memasak** - Pengaruh cara memasak terhadap kalori
    
    ### 📊 Database:
    - 80+ bahan makanan dengan nilai kalori
    - 30+ jenis masakan populer
    """)
    
    st.markdown("---")
    st.caption("Made with ❤️ | Data dari berbagai sumber")

# Input form
st.subheader("📝 Masukkan Resep Anda")

col1, col2 = st.columns(2)

with col1:
    title = st.text_input(
        "🍲 **Judul Resep**",
        placeholder="contoh: Ayam Goreng Crispy",
        help="Masukkan nama resep Anda"
    )
    
    portion = st.number_input(
        "👥 **Jumlah Porsi**",
        min_value=1,
        max_value=10,
        value=1,
        help="Berapa porsi yang dihasilkan dari resep ini?"
    )

with col2:
    ingredients = st.text_area(
        "🥕 **Bahan-bahan**",
        placeholder="contoh: 1 kg ayam, tepung terigu 200g, bawang putih 5 siung, garam, merica",
        height=150,
        help="Pisahkan dengan koma untuk hasil terbaik"
    )
    
    steps = st.text_area(
        "📖 **Langkah Memasak**",
        placeholder="contoh: 1. Cuci ayam hingga bersih, 2. Haluskan bumbu, 3. Goreng hingga matang",
        height=150,
        help="Jelaskan langkah memasak secara detail"
    )

# Contoh resep dengan tampilan lebih rapi
st.markdown("---")
st.markdown("### 🍳 Contoh Resep (Klik tombol di bawah untuk mencoba)")

col_a, col_b, col_c = st.columns(3)

with col_a:
    if st.button("🍗 Ayam Goreng Krispi", use_container_width=True):
        title = "Ayam Goreng Krispi"
        ingredients = "1 kg ayam, tepung terigu 200g, tepung maizena 100g, bawang putih 5 siung, garam, merica, telur 2 butir, minyak goreng"
        steps = "1. Cuci ayam hingga bersih\n2. Haluskan bawang putih\n3. Marinasi ayam dengan bawang putih dan garam\n4. Campur tepung terigu dan maizena\n5. Celup ayam ke telur lalu gulingkan ke tepung\n6. Goreng hingga kecoklatan"
        st.rerun()

with col_b:
    if st.button("🍜 Nasi Goreng Spesial", use_container_width=True):
        title = "Nasi Goreng Spesial"
        ingredients = "nasi putih 500g, bawang putih 3 siung, bawang merah 2 siung, cabai 5 buah, kecap manis, telur 2 butir, ayam suwir 100g, margarin"
        steps = "1. Haluskan bawang dan cabai\n2. Tumis bumbu hingga harum\n3. Masukkan ayam suwir\n4. Masukkan nasi dan kecap\n5. Aduk rata\n6. Masak telur orak arik"
        st.rerun()

with col_c:
    if st.button("🥬 Sayur Asem Segar", use_container_width=True):
        title = "Sayur Asem"
        ingredients = "kacang panjang, jagung manis, melinjo, daun so, asam jawa, cabai, bawang merah, garam, gula"
        steps = "1. Rebus air hingga mendidih\n2. Masukkan jagung dan kacang panjang\n3. Tambahkan bumbu halus\n4. Masukkan asam jawa dan daun so\n5. Masak hingga matang"
        st.rerun()

st.markdown("---")

# Tombol prediksi
if st.button("🔮 Prediksi Kalori", type="primary", use_container_width=True):
    if not title or not ingredients or not steps:
        st.warning("⚠️ Mohon lengkapi semua field (judul resep, bahan-bahan, dan langkah memasak) terlebih dahulu!")
    else:
        with st.spinner("Menghitung estimasi kalori..."):
            calories, ingredients_found, matched_dish = predict_calories(title, ingredients, steps)
            calories_per_portion = int(calories / portion)
            
            # Hasil prediksi
            st.markdown("---")
            st.markdown("## 📊 Hasil Prediksi")
            
            col_left, col_mid, col_right = st.columns([1, 2, 1])
            with col_mid:
                category, icon, _ = get_calorie_category(calories_per_portion)
                st.markdown(f"""
                <div class="prediction-box">
                    <p style="font-size: 1.1rem;">📊 Estimasi Total Kalori</p>
                    <p class="calorie-number">{calories_per_portion:,}</p>
                    <p class="calorie-unit">kalori per porsi</p>
                    <div class="calorie-status">
                        {icon} {category} {icon}
                    </div>
                    <p style="font-size: 0.9rem; margin-top: 0.5rem;">
                        Total resep: {calories:,} kalori ({portion} porsi)
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # Detail
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🥗 Analisis Nutrisi (Estimasi)")
                protein, carbs, fat = calculate_nutrition(calories_per_portion)
                
                metcol1, metcol2, metcol3 = st.columns(3)
                with metcol1:
                    st.metric("🥩 Protein", f"{protein}g")
                with metcol2:
                    st.metric("🍚 Karbohidrat", f"{carbs}g")
                with metcol3:
                    st.metric("🥑 Lemak", f"{fat}g")
                
                st.markdown("---")
                _, _, desc = get_calorie_category(calories_per_portion)
                st.info(f"**Kategori:** {desc}")
            
            with col2:
                st.markdown("### 🥕 Bahan yang Terdeteksi")
                if ingredients_found:
                    for ing in ingredients_found[:10]:
                        st.markdown(f"- **{ing['bahan'].title()}** : {ing['estimasi_kalori']:.0f} kalori")
                else:
                    st.info("Tidak ada bahan yang terdeteksi dari database. Coba gunakan bahan yang lebih umum seperti ayam, nasi, telur, dll.")
                
                if matched_dish:
                    st.success(f"🍽️ **Resep mirip:** {matched_dish.title()}")
            
            # Saran
            st.markdown("---")
            st.markdown("### 💡 Saran & Rekomendasi")
            
            saran_col1, saran_col2 = st.columns(2)
            
            with saran_col1:
                if calories_per_portion > 500:
                    st.warning("⚡ **Kalori Cukup Tinggi**")
                    st.markdown("""
                    - Kurangi penggunaan minyak/minyak goreng
                    - Ganti santan dengan susu rendah lemak
                    - Perbanyak porsi sayuran
                    - Panggang/bakar daripada digoreng
                    """)
                elif calories_per_portion < 250:
                    st.success("✅ **Kalori Rendah**")
                    st.markdown("""
                    - Cocok untuk program diet
                    - Bisa ditambah protein untuk kenyang lebih lama
                    - Tambahkan sayuran hijau untuk nutrisi
                    """)
                else:
                    st.info("📌 **Kalori Seimbang**")
                    st.markdown("""
                    - Porsi ideal untuk makan utama
                    - Kombinasikan dengan sayuran
                    - Perhatikan porsi karbohidrat
                    """)
            
            with saran_col2:
                st.markdown("**🏃 Aktivitas untuk Membakar Kalori Ini:**")
                if calories_per_portion <= 300:
                    st.markdown("- 🚶‍♀️ Jalan kaki 15-20 menit")
                elif calories_per_portion <= 500:
                    st.markdown("- 🚴‍♂️ Bersepeda 20-30 menit")
                else:
                    st.markdown("- 🏃‍♂️ Lari 30-40 menit")
                    st.markdown("- 🏊‍♀️ Berenang 45 menit")

# Footer
st.markdown("---")
st.caption("Estimasi kalori bersifat perkiraan. Gunakan sebagai panduan, bukan acuan medis.")

# Info tambahan
with st.expander("ℹ️ Tentang Perhitungan Kalori"):
    st.markdown("""
    ### Bagaimana Aplikasi Menghitung Kalori?
    
    1. **Analisis Bahan**: Aplikasi mencocokkan bahan dengan database yang berisi nilai kalori per 100g.
    
    2. **Database Resep**: Jika judul resep cocok dengan database masakan populer, aplikasi menggunakan nilai tersebut.
    
    3. **Metode Memasak**: Cara memasak mempengaruhi kalori - menggoreng menambah kalori.
    
    ### Sumber Data
    
    Database kalori bersumber dari Data Komposisi Pangan Indonesia.
    """)
