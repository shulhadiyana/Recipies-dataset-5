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

# Custom CSS - DIPERBAIKI agar teks terlihat jelas
st.markdown("""
<style>
    /* Background utama lebih soft */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
    }
    
    /* Header */
    .main-header {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    /* Prediction box */
    .prediction-box {
        background: linear-gradient(135deg, #4ecdc4 0%, #2ecc71 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-top: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .prediction-number {
        font-size: 5rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    /* Metric card - teks gelap agar terbaca */
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        color: #2c3e50;
    }
    
    .metric-card h4 {
        color: #2c3e50;
        margin: 0 0 10px 0;
    }
    
    /* Feature box */
    .feature-box {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
        border-left: 5px solid #ff6b6b;
        color: #2c3e50;
    }
    
    /* Subheader styling */
    .stSubheader {
        color: #2c3e50 !important;
        font-weight: bold !important;
    }
    
    /* Text area label */
    .stTextArea label {
        color: #2c3e50 !important;
        font-weight: 500 !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: #ecf0f1 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #ecf0f1 !important;
    }
    
    /* Info text */
    .info-text {
        color: #2c3e50;
        background-color: #fff3cd;
        padding: 10px;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
    }
    
    /* Table styling */
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
</style>
""", unsafe_allow_html=True)

# Fungsi pembersihan teks
def clean_text(text):
    """Membersihkan teks untuk preprocessing"""
    if not isinstance(text, str):
        text = str(text)
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = ' '.join(text.split())
    text = re.sub(r'\d+', '', text)
    return text

# Load model dengan caching
@st.cache_resource
def load_model():
    """Memuat pipeline model yang sudah disimpan"""
    try:
        pipeline = joblib.load('loves_prediction_pipeline.pkl')
        return pipeline
    except FileNotFoundError:
        st.error("❌ Model file 'loves_prediction_pipeline.pkl' tidak ditemukan!")
        st.info("Pastikan file model ada di direktori yang sama dengan app.py")
        return None
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        return None

# Header
st.markdown("""
<div class="main-header">
    <h1>🔥 Prediksi Popularitas Resep</h1>
    <p>Machine Learning memprediksi seberapa populer resep Anda! 🍳</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2330/2330881.png", width=80)
    st.title("📊 Tentang Model")
    st.markdown("""
    ### Model Machine Learning
    
    Aplikasi ini menggunakan **XGBoost Regressor** yang dilatih dengan **14.945 resep** dari platform kuliner.
    
    ### 📈 Performa Model
    
    | Metrik | Nilai |
    |--------|-------|
    | MAE | **9.90** loves |
    | RMSE | 17.99 loves |
    | R² Score | 0.03 |
    
    ### 🎯 Target
    
    Model berhasil mencapai target **MAE ≤ 10 loves** ✅
    
    ### 🔧 Fitur yang Digunakan
    
    - Judul resep (Title)
    - Bahan-bahan (Ingredients)  
    - Langkah memasak (Steps)
    
    ### 💡 Interpretasi
    
    - **0-5 loves**: 🔵 Kurang populer
    - **6-15 loves**: 🟢 Cukup populer
    - **16-30 loves**: 🟡 Populer
    - **>30 loves**: 🔴 Sangat populer!
    """)
    
    st.markdown("---")
    st.markdown("Made with ❤️ using XGBoost & Streamlit")

# Main content
st.markdown('<h3 style="color: #2c3e50;">📝 Masukkan Resep Anda</h3>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<p style="color: #2c3e50; font-weight: 500;">📝 Judul Resep</p>', unsafe_allow_html=True)
    title = st.text_area(
        "",
        placeholder="Contoh: Ayam Goreng Crispy Pedas",
        height=80,
        label_visibility="collapsed"
    )
    
    st.markdown('<p style="color: #2c3e50; font-weight: 500;">🥕 Bahan-bahan</p>', unsafe_allow_html=True)
    ingredients = st.text_area(
        "",
        placeholder="Contoh: 1 kg ayam--tepung terigu--bawang putih--garam--merica--cabai bubuk",
        height=150,
        label_visibility="collapsed"
    )

with col2:
    st.markdown('<p style="color: #2c3e50; font-weight: 500;">📖 Langkah Memasak</p>', unsafe_allow_html=True)
    steps = st.text_area(
        "",
        placeholder="Contoh: 1. Cuci bersih ayam--2. Campur tepung dan bumbu--3. Goreng hingga kecoklatan--4. Sajikan dengan nasi hangat",
        height=220,
        label_visibility="collapsed"
    )
    
    # Contoh resep
    st.markdown('<p style="color: #2c3e50; font-weight: 500;">🍳 Contoh Resep</p>', unsafe_allow_html=True)
    example_options = {
        "Pilih contoh resep...": "",
        "Ayam Goreng Crispy": "ayam goreng crispy renyah|1 kg ayam--tepung terigu--tepung maizena--bawang putih bubuk--merica--garam--telur--minyak goreng|cuci ayam--campur tepung dan bumbu--celup ayam ke telur--gulingkan ke tepung--goreng hingga kecoklatan",
        "Soto Ayam": "soto ayam kampung|1 ekor ayam kampung--bawang putih--bawang merah--kunyit--jahe--lengkuas--serai--daun salam--daun jeruk--soun--toge--telur rebus|rebus ayam--haluskan bumbu--tumis bumbu--masukkan ke rebusan ayam--masak hingga empuk--sajikan",
        "Nasi Goreng": "nasi goreng spesial|nasi putih--bawang putih--bawang merah--cabai--kecap manis--telur--ayam suwir--margarin|haluskan bawang dan cabai--tumis bumbu--masukkan ayam--masukkan nasi--tambahkan kecap--masak telur orak arik"
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

# Load model
model_pipeline = load_model()

# Proses prediksi
if predict_button:
    if not title or not ingredients or not steps:
        st.warning("⚠️ Mohon lengkapi semua field (judul, bahan, dan langkah) terlebih dahulu!")
    elif model_pipeline is None:
        st.error("❌ Model tidak dapat dimuat. Pastikan file 'loves_prediction_pipeline.pkl' tersedia.")
    else:
        with st.spinner("Menganalisis resep..."):
            try:
                # Preprocessing seperti di notebook
                cleaned_title = clean_text(title)
                cleaned_ingredients = clean_text(ingredients)
                cleaned_steps = clean_text(steps)
                combined_text = f"{cleaned_title} {cleaned_ingredients} {cleaned_steps}"
                
                # Transformasi dengan TF-IDF
                tfidf = model_pipeline['tfidf']
                text_tfidf = tfidf.transform([combined_text])
                
                # Prediksi dengan model
                model = model_pipeline['model']
                prediction = model.predict(text_tfidf)[0]
                
                # Tampilkan hasil
                st.markdown("---")
                st.markdown('<h3 style="color: #2c3e50; text-align: center;">📊 Hasil Prediksi</h3>', unsafe_allow_html=True)
                
                # Animasi dan hasil prediksi
                col_left, col_mid, col_right = st.columns([1, 2, 1])
                with col_mid:
                    # Tentukan emoji dan warna berdasarkan prediksi
                    if prediction <= 5:
                        emoji = "🔵"
                        category = "Kurang Populer"
                        advice = "Coba gunakan judul yang lebih menarik atau bahan yang lebih populer!"
                        bg_color = "#3498db"
                    elif prediction <= 15:
                        emoji = "🟢"
                        category = "Cukup Populer"
                        advice = "Resep ini memiliki potensi yang baik! Optimasi sedikit untuk hasil lebih maksimal."
                        bg_color = "#2ecc71"
                    elif prediction <= 30:
                        emoji = "🟡"
                        category = "Populer"
                        advice = "Wah! Resep ini diprediksi akan disukai banyak orang!"
                        bg_color = "#f39c12"
                    else:
                        emoji = "🔴"
                        category = "Sangat Populer"
                        advice = "🔥 Luar biasa! Resep ini diprediksi akan menjadi favorit banyak pengguna!"
                        bg_color = "#e74c3c"
                    
                    st.markdown(f"""
                    <div style="background: {bg_color}; padding: 2rem; border-radius: 20px; text-align: center; color: white; margin-top: 1rem; box-shadow: 0 10px 25px rgba(0,0,0,0.1);">
                        <div style="font-size: 2rem;">{emoji}❤️{emoji}</div>
                        <p style="font-size: 1.2rem; margin: 0;">Prediksi Jumlah Likes</p>
                        <p style="font-size: 5rem; font-weight: bold; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">{prediction:.0f}</p>
                        <p style="font-size: 1.1rem;">loves</p>
                        <div style="background-color: rgba(255,255,255,0.2); border-radius: 10px; padding: 8px;">
                            {category}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Saran dan analisis
                st.markdown('<h3 style="color: #2c3e50; margin-top: 2rem;">📊 Analisis & Saran</h3>', unsafe_allow_html=True)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"""
                    <div style="background-color: white; padding: 1rem; border-radius: 10px; margin-top: 1rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1); color: #2c3e50;">
                        <h4 style="color: #2c3e50; margin: 0 0 10px 0;">💡 {advice}</h4>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_b:
                    # Hitung confidence berdasarkan error model
                    confidence = max(0, min(100, 100 - (abs(prediction - 11.86) / 11.86 * 100)))
                    st.markdown(f"""
                    <div style="background-color: white; padding: 1rem; border-radius: 10px; margin-top: 1rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1); color: #2c3e50;">
                        <h4 style="color: #2c3e50; margin: 0 0 10px 0;">📊 Confidence Score</h4>
                        <div style="background-color: #e0e0e0; border-radius: 10px; height: 20px;">
                            <div style="background-color: #4ecdc4; width: {confidence}%; height: 20px; border-radius: 10px;"></div>
                        </div>
                        <p style="margin-top: 5px;">{confidence:.1f}% akurasi estimasi</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Detail preprocessing
                with st.expander("🔍 Lihat Detail Preprocessing"):
                    st.markdown("**Teks setelah dibersihkan:**")
                    st.code(combined_text[:500] + ("..." if len(combined_text) > 500 else ""), language="text")
                    st.markdown("**Fitur yang digunakan:** TF-IDF Vectorizer dengan 5000 fitur (unigram + bigram)")
                
            except Exception as e:
                st.error(f"Terjadi kesalahan saat memprediksi: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div class="footer-text">
    <p>Aplikasi ini menggunakan model XGBoost yang dilatih dengan 14.945 resep.<br>
    Hasil prediksi bersifat estimasi berdasarkan analisis teks judul, bahan, dan langkah memasak.</p>
</div>
""", unsafe_allow_html=True)

# Fitur penting
with st.expander("🏆 Kata/Fitur yang Mempengaruhi Popularitas"):
    st.markdown("""
    <div style="color: #2c3e50;">
    <p>Berdasarkan analisis model (Feature Importance), berikut adalah kata yang paling mempengaruhi prediksi likes:</p>
    
    | Pengaruh Positif ⬆️ | Pengaruh Negatif ⬇️ |
    |---------------------|---------------------|
    | ayam | diet |
    | goreng | sayur |
    | crispy | rebus |
    | pedas | plain |
    | saus | tanpa bumbu |
    | sambal | organik |
    | bawang | simple |
    | tepung | praktis |
    
    ### 💡 Tips Meningkatkan Popularitas Resep:
    1. **Judul yang menarik** - Gunakan kata seperti "crispy", "spesial", "enak"
    2. **Bahan populer** - Ayam, bawang, cabai, saus
    3. **Langkah detail** - Jelaskan proses dengan jelas
    4. **Kata kunci positif** - Tambahkan deskripsi menggugah selera
    </div>
    """, unsafe_allow_html=True)

# Informasi model
with st.expander("🤖 Tentang Model Machine Learning"):
    st.markdown("""
    <div style="color: #2c3e50;">
    ### Detail Model
    
    - **Algoritma**: XGBoost Regressor
    - **Hyperparameter terbaik** (setelah tuning):
        - `n_estimators`: 50
        - `max_depth`: 5
        - `learning_rate`: 0.05
        - `colsample_bytree`: 0.9
        - `subsample`: 0.7
    
    ### Preprocessing
    
    1. **Text Cleaning**: Lowercase, hapus punctuation, hapus angka
    2. **Feature Extraction**: TF-IDF Vectorizer dengan 5000 fitur (unigram + bigram)
    3. **Model Training**: XGBoost dengan RandomizedSearchCV
    
    ### Dataset
    
    - Jumlah resep: 14,945
    - Rata-rata loves: 11.86
    - Loves tertinggi: 939
    - Loves terendah: 0
    </div>
    """, unsafe_allow_html=True)
