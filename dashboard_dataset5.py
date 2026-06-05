# app.py - Prediksi Popularitas Resep dengan Model XGBoost
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import re
import string
import warnings
warnings.filterwarnings('ignore')

# Konfigurasi halaman
st.set_page_config(
    page_title="Prediksi Popularitas Resep",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS - DIPERBAIKI TOTAL ====================
st.markdown("""
<style>
    /* Hapus background gradient, gunakan warna solid terang */
    .stApp {
        background-color: #f8f9fa !important;
    }
    
    /* Header dengan teks kontras */
    .main-header {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        color: white !important;
        margin: 0;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9) !important;
        margin: 10px 0 0 0;
    }
    
    /* Prediction box dengan warna solid */
    .prediction-box {
        background: linear-gradient(135deg, #4ecdc4 0%, #2ecc71 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-top: 2rem;
    }
    
    .prediction-box p, .prediction-box div {
        color: white !important;
    }
    
    .prediction-number {
        font-size: 5rem;
        font-weight: bold;
        margin: 0;
        color: white !important;
    }
    
    /* Metric card - background putih, teks hitam */
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .metric-card h4 {
        color: #2c3e50 !important;
        margin: 0 0 10px 0;
    }
    
    .metric-card p {
        color: #2c3e50 !important;
    }
    
    /* Sidebar - latar gelap teks putih */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c3e50 0%, #1a252f 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown p {
        color: #ecf0f1 !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: white !important;
    }
    
    /* Main content text - warna gelap agar terbaca */
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #2c3e50 !important;
    }
    
    /* Label input */
    .stTextArea label, .stTextInput label {
        color: #2c3e50 !important;
        font-weight: 500 !important;
    }
    
    /* Tabel */
    table {
        background-color: white;
        border-radius: 10px;
        overflow: hidden;
    }
    
    th {
        background-color: #ff6b6b;
        color: white !important;
        padding: 10px;
    }
    
    td {
        color: #2c3e50 !important;
        padding: 8px;
    }
    
    /* Footer */
    .footer-text {
        text-align: center;
        color: #7f8c8d;
        font-size: 0.8rem;
        padding: 20px;
    }
    
    /* Subheader */
    .subheader-text {
        color: #2c3e50;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 10px;
    }
    
    /* Info box */
    .info-box {
        background-color: #d4edda;
        padding: 10px;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        color: #155724;
    }
</style>
""", unsafe_allow_html=True)

# ==================== FUNGSI ====================
def clean_text(text):
    """Membersihkan teks untuk preprocessing"""
    if not isinstance(text, str):
        text = str(text)
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = ' '.join(text.split())
    text = re.sub(r'\d+', '', text)
    return text

@st.cache_resource
def load_model():
    """Memuat pipeline model yang sudah disimpan"""
    try:
        pipeline = joblib.load('loves_prediction_pipeline.pkl')
        return pipeline
    except FileNotFoundError:
        st.error("❌ Model file 'loves_prediction_pipeline.pkl' tidak ditemukan!")
        return None
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        return None

# ==================== HEADER ====================
st.markdown("""
<div class="main-header">
    <h1>🔥 Prediksi Popularitas Resep</h1>
    <p>Machine Learning memprediksi seberapa populer resep Anda! 🍳</p>
</div>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2330/2330881.png", width=80)
    st.markdown("## 📊 Tentang Model")
    st.markdown("""
    **Model Machine Learning**
    
    Aplikasi ini menggunakan **XGBoost Regressor** yang dilatih dengan **14.945 resep**.
    
    **📈 Performa Model**
    
    - MAE: **9.90** loves
    - RMSE: 17.99 loves
    - R² Score: 0.03
    
    **🎯 Target:** MAE ≤ 10 loves ✅
    
    **💡 Interpretasi**
    
    - 0-5 loves: 🔵 Kurang populer
    - 6-15 loves: 🟢 Cukup populer
    - 16-30 loves: 🟡 Populer
    - >30 loves: 🔴 Sangat populer!
    """)
    st.markdown("---")
    st.markdown("Made with ❤️ using XGBoost")

# ==================== MAIN CONTENT ====================
st.markdown('<p style="color:#2c3e50; font-size:1.2rem; font-weight:bold;">📝 Masukkan Resep Anda</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<p style="color:#2c3e50; font-weight:500;">📝 Judul Resep</p>', unsafe_allow_html=True)
    title = st.text_area(
        "",
        placeholder="Contoh: Ayam Goreng Crispy Pedas",
        height=80,
        label_visibility="collapsed"
    )
    
    st.markdown('<p style="color:#2c3e50; font-weight:500;">🥕 Bahan-bahan</p>', unsafe_allow_html=True)
    ingredients = st.text_area(
        "",
        placeholder="Contoh: 1 kg ayam--tepung terigu--bawang putih--garam",
        height=150,
        label_visibility="collapsed"
    )

with col2:
    st.markdown('<p style="color:#2c3e50; font-weight:500;">📖 Langkah Memasak</p>', unsafe_allow_html=True)
    steps = st.text_area(
        "",
        placeholder="Contoh: 1. Cuci ayam--2. Goreng hingga matang",
        height=220,
        label_visibility="collapsed"
    )
    
    st.markdown('<p style="color:#2c3e50; font-weight:500;">🍳 Contoh Resep</p>', unsafe_allow_html=True)
    example_options = {
        "Pilih contoh resep...": "",
        "Ayam Goreng Crispy": "ayam goreng crispy|1 kg ayam--tepung--bawang putih--garam--telur|cuci ayam--campur tepung--goreng hingga kecoklatan",
        "Soto Ayam": "soto ayam|1 ekor ayam--bawang--kunyit--jahe--serai|rebus ayam--haluskan bumbu--masak hingga empuk",
        "Nasi Goreng": "nasi goreng|nasi--bawang--cabai--kecap--telur|tumis bumbu--masukkan nasi--aduk rata"
    }
    
    selected_example = st.selectbox("", list(example_options.keys()), label_visibility="collapsed")
    if selected_example != "Pilih contoh resep...":
        example_data = example_options[selected_example].split('|')
        if len(example_data) == 3:
            title = example_data[0]
            ingredients = example_data[1]
            steps = example_data[2]
            st.success(f"✅ Contoh '{selected_example}' telah diisi!")

# Tombol prediksi
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    predict_button = st.button("🔮 Prediksi Popularitas", use_container_width=True, type="primary")

# ==================== PREDIKSI ====================
model_pipeline = load_model()

if predict_button:
    if not title or not ingredients or not steps:
        st.warning("⚠️ Mohon lengkapi semua field (judul, bahan, dan langkah) terlebih dahulu!")
    elif model_pipeline is None:
        st.error("❌ Model tidak dapat dimuat. Pastikan file 'loves_prediction_pipeline.pkl' tersedia.")
    else:
        with st.spinner("Menganalisis resep..."):
            try:
                cleaned_title = clean_text(title)
                cleaned_ingredients = clean_text(ingredients)
                cleaned_steps = clean_text(steps)
                combined_text = f"{cleaned_title} {cleaned_ingredients} {cleaned_steps}"
                
                tfidf = model_pipeline['tfidf']
                text_tfidf = tfidf.transform([combined_text])
                
                model = model_pipeline['model']
                prediction = model.predict(text_tfidf)[0]
                
                st.markdown("---")
                st.markdown('<p style="color:#2c3e50; font-size:1.2rem; font-weight:bold; text-align:center;">📊 Hasil Prediksi</p>', unsafe_allow_html=True)
                
                # Tentukan kategori
                if prediction <= 5:
                    emoji = "🔵"
                    category = "Kurang Populer"
                    advice = "Coba gunakan judul yang lebih menarik atau bahan yang lebih populer!"
                elif prediction <= 15:
                    emoji = "🟢"
                    category = "Cukup Populer"
                    advice = "Resep ini memiliki potensi yang baik!"
                elif prediction <= 30:
                    emoji = "🟡"
                    category = "Populer"
                    advice = "Wah! Resep ini diprediksi akan disukai banyak orang!"
                else:
                    emoji = "🔴"
                    category = "Sangat Populer"
                    advice = "🔥 Luar biasa! Resep ini akan menjadi favorit!"
                
                # Hasil prediksi
                col_left, col_mid, col_right = st.columns([1, 2, 1])
                with col_mid:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #4ecdc4 0%, #2ecc71 100%); padding: 2rem; border-radius: 20px; text-align: center; margin-top: 1rem;">
                        <div style="font-size: 2rem;">{emoji}❤️{emoji}</div>
                        <p style="font-size: 1.2rem; margin: 0; color:white;">Prediksi Jumlah Likes</p>
                        <p style="font-size: 5rem; font-weight: bold; margin: 0; color:white;">{prediction:.0f}</p>
                        <p style="font-size: 1.1rem; color:white;">loves</p>
                        <div style="background-color: rgba(255,255,255,0.2); border-radius: 10px; padding: 8px; color:white;">
                            {category}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Saran
                st.markdown(f"""
                <div style="background-color: white; padding: 1rem; border-radius: 10px; margin-top: 1rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h4 style="color: #2c3e50; margin: 0 0 10px 0;">💡 Saran</h4>
                    <p style="color: #2c3e50;">{advice}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Detail preprocessing
                with st.expander("🔍 Lihat Detail Preprocessing"):
                    st.code(combined_text[:500] + ("..." if len(combined_text) > 500 else ""), language="text")
                
            except Exception as e:
                st.error(f"Terjadi kesalahan: {str(e)}")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div class="footer-text">
    Aplikasi ini menggunakan model XGBoost yang dilatih dengan 14.945 resep.<br>
    Hasil prediksi bersifat estimasi berdasarkan analisis teks judul, bahan, dan langkah memasak.
</div>
""", unsafe_allow_html=True)

# ==================== EXPANDER ====================
with st.expander("🏆 Kata/Fitur yang Mempengaruhi Popularitas"):
    st.markdown("""
    <table style="width:100%; border-collapse: collapse;">
        <tr>
            <th style="background-color:#ff6b6b; color:white; padding:10px;">Pengaruh Positif ⬆️</th>
            <th style="background-color:#ff6b6b; color:white; padding:10px;">Pengaruh Negatif ⬇️</th>
        </tr>
        <tr><td style="color:#2c3e50;">ayam</td><td style="color:#2c3e50;">diet</td></tr>
        <tr><td style="color:#2c3e50;">goreng</td><td style="color:#2c3e50;">sayur</td></tr>
        <tr><td style="color:#2c3e50;">crispy</td><td style="color:#2c3e50;">rebus</td></tr>
        <tr><td style="color:#2c3e50;">pedas</td><td style="color:#2c3e50;">plain</td></tr>
        <tr><td style="color:#2c3e50;">saus</td><td style="color:#2c3e50;">tanpa bumbu</td></tr>
        <tr><td style="color:#2c3e50;">sambal</td><td style="color:#2c3e50;">organik</td></tr>
        <tr><td style="color:#2c3e50;">bawang</td><td style="color:#2c3e50;">simple</td></tr>
        <tr><td style="color:#2c3e50;">tepung</td><td style="color:#2c3e50;">praktis</td></tr>
    </table>
    """, unsafe_allow_html=True)

with st.expander("🤖 Tentang Model Machine Learning"):
    st.markdown("""
    <div style="color:#2c3e50;">
    <b>Algoritma:</b> XGBoost Regressor<br><br>
    <b>Hyperparameter terbaik:</b>
    <ul>
        <li>n_estimators: 50</li>
        <li>max_depth: 5</li>
        <li>learning_rate: 0.05</li>
    </ul>
    <b>Dataset:</b> 14,945 resep | Rata-rata loves: 11.86
    </div>
    """, unsafe_allow_html=True)
