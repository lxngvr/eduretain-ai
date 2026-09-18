# IMPORT LIBRARY & DEPENDENCIES
import base64
import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st

# TENTUKAN PATH LOGO SESUAI LOKASI FOLDER
LOGO_PATH = os.path.join("image", "eduretain AI - logo.png")
if not os.path.exists(LOGO_PATH):
    possible_paths = [
        "image/eduretain AI - logo.png",
        "image/logo.png",
        "eduretain AI - logo.png",
        "logo.png"
    ]
    LOGO_PATH = next((p for p in possible_paths if os.path.exists(p)), None)

# FUNGSI ENKODING LOGO KE BASE64 (RESPONSIF DI SEMUA RESOLUSI)
def get_image_base64(path):
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

LOGO_BASE64 = get_image_base64(LOGO_PATH)

# KONFIGURASI TAMPILAN HALAMAN
st.set_page_config(
    page_title="EduRetain AI - Student Retention Early Warning System",
    page_icon=LOGO_PATH if LOGO_PATH else "🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# INJEKSI CSS GLOBAL STREAMLIT
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,300..900;1,300..900&display=swap');

    /* 1. VARIABEL WARNA & TIPOGRAFI GLOBAL */
    :root {
        --font: 'Nunito', sans-serif !important;
        --font-sans: 'Nunito', sans-serif !important;
        --primary-color: #2563EB !important;
    }

    html, body, [class*="st-"], .stApp {
        font-family: 'Nunito', sans-serif !important;
    }

    /* 2. PROTEKSI IKON STREAMLIT & FONT AWESOME */
    [data-testid*="stIcon"],
    [data-testid="stFileUploaderDropzone"] svg,
    .material-symbols-rounded,
    .material-icons {
        font-family: 'Material Symbols Rounded', 'Material Icons' !important;
    }

    .fa, .fa-solid, .fa-brands, .fa-regular {
        font-family: 'Font Awesome 6 Free' !important;
        font-weight: 900 !important;
    }

    /* 3. TOMBOL UTAMA */
    button[kind="primary"] {
        background-color: #2563EB !important;
        border-color: #2563EB !important;
        color: #FFFFFF !important;
    }
    button[kind="primary"]:hover,
    button[kind="primary"]:focus,
    button[kind="primary"]:active {
        background-color: #1D4ED8 !important;
        border-color: #1D4ED8 !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.3) !important;
    }

    /* 4. TOMBOL SEKUNDER */
    button[kind="secondary"]:hover {
        border-color: #2563EB !important;
        color: #2563EB !important;
    }

    /* 5. TAB NAVIGASI HORIZONTAL RESPONSIF */
    div[data-testid="stRadio"] > div[role="radiogroup"] {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label {
        flex: 1 1 auto;
        min-width: 160px;
        text-align: center;
        padding: 0.5rem 1rem !important;
        border-radius: 0.5rem !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        background: transparent !important;
        cursor: pointer;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label[data-checked="true"] {
        border-color: #2563EB !important;
        background-color: rgba(37, 99, 235, 0.15) !important;
        color: #60A5FA !important;
        font-weight: 700;
    }

    /* 6. INPUT FIELD FOCUS RING */
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="select"]:focus-within {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 1px #2563EB !important;
    }

    /* 7. SLIDER DAN PROGRESS BAR */
    div[data-baseweb="slider"] div[role="slider"] {
        background-color: #2563EB !important;
    }
    .stProgress > div > div > div > div {
        background-color: #2563EB !important;
    }

    /* 8. TERJEMAHKAN TOOLTIP ERROR BAWAAN STREAMLIT KE BAHASA INDONESIA */
    div[data-baseweb="popover"] div[role="tooltip"] {
        font-size: 0 !important;
    }
    div[data-baseweb="popover"] div[role="tooltip"]::before {
        content: "Peringatan: Angka di luar batas acuan data. Silakan masukkan nilai yang valid." !important;
        font-size: 0.82rem !important;
        font-family: 'Nunito', sans-serif !important;
        color: #FFFFFF !important;
        display: block;
        line-height: 1.3;
    }

    /* 9. STYLING FILE UPLOADER (TOMBOL SILANG TETAP X, HANYA TOMBOL LUAR JADI EDIT BERKAS) */
    
    /* Lindungi tombol silang (delete) di dalam preview berkas */
    [data-testid="stFileUploaderFile"] button,
    button[aria-label="Delete"] {
        display: inline-flex !important;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        color: #94A3B8 !important;
        cursor: pointer !important;
    }
    [data-testid="stFileUploaderFile"] button *,
    button[aria-label="Delete"] * {
        display: inline-block !important;
    }
    [data-testid="stFileUploaderFile"] button::before,
    [data-testid="stFileUploaderFile"] button::after,
    button[aria-label="Delete"]::before,
    button[aria-label="Delete"]::after {
        content: none !important;
    }

    /* Hanya targetkan tombol penambahan/penggantian di luar kotak berkas */
    [data-testid="stFileUploaderDropzone"] > div > button:not([aria-label="Delete"]),
    [data-testid="stFileUploaderDropzone"] button:not([data-testid*="stFileUploaderFile"] button):not([aria-label="Delete"]) {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 0.45rem !important;
        padding: 0.35rem 0.8rem !important;
        border-radius: 0.45rem !important;
        background-color: rgba(37, 99, 235, 0.12) !important;
        border: 1px solid rgba(37, 99, 235, 0.4) !important;
        cursor: pointer !important;
        transition: all 0.2s ease-in-out !important;
    }

    [data-testid="stFileUploaderDropzone"] > div > button:not([aria-label="Delete"]) *,
    [data-testid="stFileUploaderDropzone"] button:not([data-testid*="stFileUploaderFile"] button):not([aria-label="Delete"]) * {
        display: none !important;
    }

    [data-testid="stFileUploaderDropzone"] > div > button:not([aria-label="Delete"]):hover,
    [data-testid="stFileUploaderDropzone"] button:not([data-testid*="stFileUploaderFile"] button):not([aria-label="Delete"]):hover {
        background-color: rgba(37, 99, 235, 0.25) !important;
        border-color: #2563EB !important;
    }

    [data-testid="stFileUploaderDropzone"] > div > button:not([aria-label="Delete"])::before,
    [data-testid="stFileUploaderDropzone"] button:not([data-testid*="stFileUploaderFile"] button):not([aria-label="Delete"])::before {
        content: "\\f2f1" !important;
        font-family: "Font Awesome 6 Free" !important;
        font-weight: 900 !important;
        font-size: 0.8rem !important;
        color: #60A5FA !important;
        display: inline-block !important;
    }

    [data-testid="stFileUploaderDropzone"] > div > button:not([aria-label="Delete"])::after,
    [data-testid="stFileUploaderDropzone"] button:not([data-testid*="stFileUploaderFile"] button):not([aria-label="Delete"])::after {
        content: "Ubah Berkas" !important;
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        font-family: 'Nunito', sans-serif !important;
        color: #60A5FA !important;
        display: inline-block !important;
    }

    /* 10. MEDIA QUERIES RESPONSIF KHUSUS KONTEN UTAMA */
    @media (max-width: 768px) {
        section[data-testid="stMain"] [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
            margin-bottom: 0.75rem;
        }
        div[role="dialog"] {
            width: 95vw !important;
            max-width: 95vw !important;
            padding: 1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# 1. CACHING DATASET REFERENSI
@st.cache_data(show_spinner=False)
def load_reference_features():
    csv_path = 'clean_students_performance.csv'
    if os.path.exists(csv_path):
        df_clean = pd.read_csv(csv_path)
        drop_cols = [c for c in ['Status', 'Status_Binary'] if c in df_clean.columns]
        df_features = df_clean.drop(columns=drop_cols)
        return pd.DataFrame([df_features.median(numeric_only=True)]), df_features.columns.tolist()
    return None, []

# 2. PEMUATAN ARTEFAK MODEL MACHINE LEARNING
@st.cache_resource(show_spinner=False)
def load_artifacts():
    possible_models = [
        os.path.join("model", "model_random_forest.joblib"),
        os.path.join("model", "random_forest_model.joblib"),
        "model_random_forest.joblib",
        "random_forest_model.joblib"
    ]
    
    model_path = None
    for p in possible_models:
        if os.path.exists(p):
            model_path = p
            break
            
    if model_path is None:
        if os.path.exists("model") and len(os.listdir("model")) > 0:
            for f in os.listdir("model"):
                if f.endswith(".joblib") and "forest" in f:
                    model_path = os.path.join("model", f)
                    break

    if model_path is None:
        raise FileNotFoundError("Berkas model Random Forest tidak ditemukan di folder model/ atau root.")

    model = joblib.load(model_path)

    scaler_path = os.path.join("model", "scaler.joblib") if os.path.exists(os.path.join("model", "scaler.joblib")) else "scaler.joblib"
    encoder_path = os.path.join("model", "label_encoder.joblib") if os.path.exists(os.path.join("model", "label_encoder.joblib")) else "label_encoder.joblib"

    scaler = joblib.load(scaler_path) if os.path.exists(scaler_path) else None
    encoder = joblib.load(encoder_path) if os.path.exists(encoder_path) else {0: 'Graduate', 1: 'Dropout'}

    return model, scaler, encoder

# 3. SPLASH SCREEN
if "initialized" not in st.session_state:
    splash_container = st.empty()
    with splash_container.status("Menginisialisasi Sistem Cerdas...", expanded=True):
        try:
            st.write("Memuat bobot model Random Forest Classifier...")
            model, scaler, encoder = load_artifacts()
            st.write("Menyiapkan matriks baseline fitur...")
            median_sample, reference_columns = load_reference_features()
            st.session_state["initialized"] = True
        except Exception as e:
            st.error(f"Detail kesalahan: {e}")
            st.stop()
            
    splash_container.empty()
    st.toast("Sistem cerdas siap digunakan!")
else:
    model, scaler, encoder = load_artifacts()
    median_sample, reference_columns = load_reference_features()

# HELPER DECODE LABEL BINER
def decode_label(pred_val):
    if isinstance(encoder, dict):
        return encoder.get(int(pred_val), "Dropout" if pred_val == 1 else "Graduate")
    elif hasattr(encoder, "inverse_transform"):
        return encoder.inverse_transform([pred_val])[0]
    return "Dropout" if pred_val == 1 else "Graduate"

# PIPELINE INFERENSI DATA
def run_pipeline(custom_input):
    if median_sample is not None:
        sample = median_sample.copy()
        feature_cols_lower = {col.lower(): col for col in sample.columns}
    else:
        sample = pd.DataFrame([custom_input])
        feature_cols_lower = {col.lower(): col for col in custom_input.keys()}

    for k, v in custom_input.items():
        if k.lower() in feature_cols_lower:
            actual_col = feature_cols_lower[k.lower()]
            sample[actual_col] = v

    expected_cols = getattr(scaler, "feature_names_in_", getattr(model, "feature_names_in_", None))
    if expected_cols is not None:
        for c in expected_cols:
            if c not in sample.columns:
                sample[c] = 0
        sample = sample[expected_cols]

    processed = scaler.transform(sample) if scaler is not None else sample
    pred = model.predict(processed)[0]
    prob = model.predict_proba(processed)[0] if hasattr(model, "predict_proba") else None
    label = decode_label(pred)
    return label, prob

# FUNGSI RESET HASIL PREDIKSI KETIKA ADA INPUT YANG DIUBAH
def reset_prediction():
    st.session_state['has_predicted'] = False

# MODAL POP-UP 1: PROFIL MODEL
@st.dialog("Spesifikasi Teknis Model AI")
def show_model_modal():
    st.markdown("""
    <h4><i class="fa-solid fa-microchip" style="color:#2563EB;"></i> Random Forest Classifier</h4>
    """, unsafe_allow_html=True)
    st.caption("Model klasifikasi biner untuk memprediksi potensi risiko putus studi.")

    m1, m2, m3 = st.columns(3)
    m1.metric("Akurasi", "91.87%")
    m2.metric("Weighted F1", "92.00%")
    m3.metric("F1 Dropout", "89.00%")

    st.divider()
    st.markdown("##### Ringkasan Evaluasi Model")
    eval_df = pd.DataFrame({
        "Status": ["Graduate (Lulus)", "Dropout (Rawan)"],
        "Precision": ["92%", "92%"],
        "Recall": ["95%", "87%"],
        "F1-Score": ["93%", "89%"]
    })
    st.dataframe(eval_df, hide_index=True, use_container_width=True)

    if hasattr(model, "feature_importances_") and hasattr(model, "feature_names_in_"):
        st.markdown("##### Faktor Penentu Utama")
        fi_df = pd.DataFrame({
            'Fitur': model.feature_names_in_,
            'Bobot': model.feature_importances_
        }).sort_values(by='Bobot', ascending=False).head(5)
        st.bar_chart(fi_df.set_index('Fitur'))

# MODAL POP-UP 2: PROFIL PENGEMBANG
@st.dialog("Profil Pengembang Proyek")
def show_developer_modal():
    st.markdown("""
    <h3><i class="fa-solid fa-user-gear" style="color:#2563EB;"></i> Galang Dava Ramadhan</h3>
    """, unsafe_allow_html=True)
    st.caption("Applied Artificial Intelligence & Data Science")
    st.divider()
    st.markdown("""
    **Tentang Proyek:**  
    Aplikasi *Student Retention Early Warning System* ini dikembangkan sebagai purwarupa sistem preskriptif analitik untuk mendeteksi dini risiko putus studi mahasiswa.
    
    * **Fokus Riset:** *Predictive Modeling*, *Decision Support System*, dan *What-If Prescriptive Analysis*
    * **Tahun Rilis:** 2026
    """)
    st.info("Sistem mendukung pemrosesan data individu maupun berkas massal (.csv) secara terpadu.")

# MODAL POP-UP 3: VALIDASI INPUT IDENTITAS & BATAS DATA
@st.dialog("Perhatian: Data Belum Sesuai")
def show_validation_modal(errors):
    st.markdown("""
    <h4><i class="fa-solid fa-triangle-exclamation" style="color:#DC2626;"></i> Mohon Periksa Kembali Isian Anda</h4>
    """, unsafe_allow_html=True)
    st.write("Sistem mendeteksi beberapa data yang belum lengkap atau di luar batasan data acuan:")
    
    for err in errors:
        st.markdown(f"- {err}")
        
    st.write("")
    if st.button("Mengerti & Perbaiki Data", type="primary", use_container_width=True):
        st.rerun()

# MODAL POP-UP 4: VALIDASI BERKAS BATCH SCREENING (DENGAN RESET UPLOADER)
@st.dialog("Peringatan: Berkas Tidak Sesuai")
def show_batch_file_error_modal(error_messages):
    st.markdown("""
    <h4><i class="fa-solid fa-file-circle-xmark" style="color:#DC2626;"></i> Format Berkas CSV Tidak Valid</h4>
    """, unsafe_allow_html=True)
    st.write("Sistem tidak dapat memproses berkas yang diunggah karena alasan berikut:")
    for msg in error_messages:
        st.markdown(f"- {msg}")
    st.info("Pastikan berkas CSV memuat parameter akademik utama seperti kolom SKS, nilai semester, dan status pembayaran SPP.")
    
    if st.button("Tutup & Unggah Ulang Berkas", type="primary", use_container_width=True):
        st.session_state["uploader_key"] = st.session_state.get("uploader_key", 0) + 1
        st.rerun()

# PANEL SIDEBAR
with st.sidebar:
    if LOGO_BASE64:
        logo_markup = f'<img src="data:image/png;base64,{LOGO_BASE64}" style="width: 52px; height: 52px; object-fit: contain; flex-shrink: 0; border-radius: 8px;">'
    else:
        logo_markup = '<span style="font-size: 2.2rem; flex-shrink: 0; line-height: 1;">🎓</span>'

    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 12px; padding: 2px 0 8px 0;">
        {logo_markup}
        <div style="display: flex; flex-direction: column; justify-content: center; line-height: 1.15;">
            <div style="font-size: 1.25rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.3px;">
                EduRetain <span style="color: #60A5FA;">AI</span>
            </div>
            <div style="font-size: 0.78rem; color: #94A3B8; font-weight: 600; margin-top: 2px;">
                Early Warning System
            </div>
        </div>
    </div>
    <hr style="margin-top: 6px; margin-bottom: 1rem; border: none; border-top: 1px solid rgba(255, 255, 255, 0.12);">
    """, unsafe_allow_html=True)

    if st.button("Spesifikasi Model AI", icon=":material/memory:", use_container_width=True):
        show_model_modal()
        
    if st.button("Tentang Pengembang", icon=":material/badge:", use_container_width=True):
        show_developer_modal()
        
    st.markdown("""
    <hr style="margin-top: 8px; margin-bottom: 1rem; border: none; border-top: 1px solid rgba(255, 255, 255, 0.12);">
    """, unsafe_allow_html=True)
    
    st.caption("Tugas Akademik Artificial Intelligence & Machine Learning")
    st.caption("© 2026 Galang Dava Ramadhan. All rights reserved.")

# HEADER UTAMA
st.markdown("""
<h1 style="font-size: 2.1rem; font-weight: 800; margin-bottom: 0.2rem;">
    Sistem Prediksi Retensi & Intervensi Mahasiswa
</h1>
""", unsafe_allow_html=True)
st.caption("Early Warning System berbasis Machine Learning untuk mendeteksi risiko putus studi dan merumuskan intervensi preskriptif.")

# MANAJEMEN STATE TAB NAVIGASI
if "selected_tab" not in st.session_state:
    st.session_state["selected_tab"] = "Evaluasi Mahasiswa (Individual)"

selected_tab = st.radio(
    "Pilih Menu Navigasi:",
    options=["Evaluasi Mahasiswa (Individual)", "Pemindaian Angkatan (Batch Screening)"],
    horizontal=True,
    label_visibility="collapsed",
    key="selected_tab"
)

st.write("")

# ==========================================
# TAB 1: EVALUASI INDIVIDUAL + WHAT-IF
# ==========================================
if selected_tab == "Evaluasi Mahasiswa (Individual)":
    input_name = st.text_input(
        "Nama Lengkap Mahasiswa",
        value=st.session_state.get('student_name', ''),
        placeholder="contoh : Aang Acumalaka",
        help="Nama wajib diisi untuk personalisasi lembar rekomendasi.",
        key="input_name_widget",
        on_change=reset_prediction
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("##### <i class='fa-solid fa-wallet' style='color:#2563EB;'></i> Administrasi & Finansial", unsafe_allow_html=True)
            tuition = st.selectbox(
                "Status Pembayaran SPP",
                options=[1, 0],
                index=0,
                format_func=lambda x: "Lancar / Lunas" if x == 1 else "Menunggak",
                key="widget_tuition",
                on_change=reset_prediction
            )
            debtor = st.selectbox(
                "Memiliki Tunggakan Utang?",
                options=[0, 1],
                index=0,
                format_func=lambda x: "Tidak Ada" if x == 0 else "Ya (Ada Tunggakan)",
                key="widget_debtor",
                on_change=reset_prediction
            )
            scholarship = st.selectbox(
                "Penerima Beasiswa?",
                options=[0, 1],
                index=0,
                format_func=lambda x: "Bukan Penerima" if x == 0 else "Ya (Penerima)",
                key="widget_scholarship",
                on_change=reset_prediction
            )
            gender = st.selectbox(
                "Jenis Kelamin",
                options=[1, 0],
                format_func=lambda x: "Laki-laki" if x == 1 else "Perempuan",
                key="widget_gender",
                on_change=reset_prediction
            )
            age = st.number_input(
                "Usia Saat Masuk (Tahun)",
                min_value=17,
                max_value=70,
                value=20,
                step=1,
                help="Batas usia acuan: 17 sampai 70 tahun. Tombol minus (-) otomatis terkunci pada angka 17.",
                key="widget_age",
                on_change=reset_prediction
            )

    with col2:
        with st.container(border=True):
            st.markdown("##### <i class='fa-solid fa-book' style='color:#2563EB;'></i> Evaluasi Semester 1", unsafe_allow_html=True)
            admission_grade = st.number_input(
                "Nilai Ujian Masuk (0 - 200)",
                min_value=0.0,
                max_value=200.0,
                value=126.0,
                step=0.5,
                help="Skala nilai seleksi masuk: 0 sampai 200.",
                key="widget_admission_grade",
                on_change=reset_prediction
            )
            sem1_enrolled = st.number_input(
                "SKS Diambil Sem 1",
                min_value=0,
                max_value=26,
                value=6,
                step=1,
                key="widget_sem1_enrolled",
                help="Batas pengambilan: 0 sampai 26 SKS.",
                on_change=reset_prediction
            )
            sem1_approved = st.number_input(
                "SKS Lulus Sem 1",
                min_value=0,
                max_value=int(sem1_enrolled),
                value=min(5, int(sem1_enrolled)),
                step=1,
                key="widget_sem1_approved",
                help="Otomatis terkunci agar tidak melebihi SKS yang diambil.",
                on_change=reset_prediction
            )
            sem1_grade = st.number_input(
                "Rata-rata Nilai Sem 1 (0 - 20)",
                min_value=0.0,
                max_value=20.0,
                value=12.3,
                step=0.1,
                help="Skala akademik: 0 sampai 20.",
                key="widget_sem1_grade",
                on_change=reset_prediction
            )

    with col3:
        with st.container(border=True):
            st.markdown("##### <i class='fa-solid fa-book-open' style='color:#2563EB;'></i> Evaluasi Semester 2", unsafe_allow_html=True)
            sem2_enrolled = st.number_input(
                "SKS Diambil Sem 2",
                min_value=0,
                max_value=26,
                value=6,
                step=1,
                key="widget_sem2_enrolled",
                help="Batas pengambilan: 0 sampai 26 SKS.",
                on_change=reset_prediction
            )
            sem2_approved = st.number_input(
                "SKS Lulus Sem 2",
                min_value=0,
                max_value=int(sem2_enrolled),
                value=min(5, int(sem2_enrolled)),
                step=1,
                key="widget_sem2_approved",
                help="Otomatis terkunci agar tidak melebihi SKS yang diambil.",
                on_change=reset_prediction
            )
            sem2_grade = st.number_input(
                "Rata-rata Nilai Sem 2 (0 - 20)",
                min_value=0.0,
                max_value=20.0,
                value=12.2,
                step=0.1,
                help="Skala akademik: 0 sampai 20.",
                key="widget_sem2_grade",
                on_change=reset_prediction
            )

    calc_sem1_eval = int(sem1_enrolled) + max(0, (int(sem1_enrolled) - int(sem1_approved)))
    calc_sem2_eval = int(sem2_enrolled) + max(0, (int(sem2_enrolled) - int(sem2_approved)))

    st.write("")

    if st.button("Jalankan Analisis Risiko", type="primary", use_container_width=True):
        validation_errors = []

        if not input_name.strip():
            validation_errors.append("Kolom **Nama Lengkap Mahasiswa** belum diisi.")

        if age is None or age < 17 or age > 70:
            validation_errors.append(f"**Usia Saat Masuk** ({age} tahun) di luar batas acuan. Harap masukkan nilai antara **17 hingga 70 tahun**.")

        if admission_grade is None or admission_grade < 0.0 or admission_grade > 200.0:
            validation_errors.append(f"**Nilai Ujian Masuk** ({admission_grade}) di luar skala. Harap masukkan nilai antara **0 hingga 200**.")

        if sem1_enrolled is None or sem1_enrolled < 0 or sem1_enrolled > 26:
            validation_errors.append(f"**SKS Diambil Sem 1** ({sem1_enrolled}) di luar batas acuan (maksimum 26 SKS).")

        if sem1_approved is None or sem1_approved < 0 or sem1_approved > sem1_enrolled:
            validation_errors.append(f"**SKS Lulus Sem 1** ({sem1_approved} SKS) tidak boleh melebihi SKS yang diambil ({sem1_enrolled} SKS).")

        if sem1_grade is None or sem1_grade < 0.0 or sem1_grade > 20.0:
            validation_errors.append(f"**Rata-rata Nilai Sem 1** ({sem1_grade}) di luar skala (0 hingga 20).")

        if sem2_enrolled is None or sem2_enrolled < 0 or sem2_enrolled > 26:
            validation_errors.append(f"**SKS Diambil Sem 2** ({sem2_enrolled}) di luar batas acuan (maksimum 26 SKS).")

        if sem2_approved is None or sem2_approved < 0 or sem2_approved > sem2_enrolled:
            validation_errors.append(f"**SKS Lulus Sem 2** ({sem2_approved} SKS) tidak boleh melebihi SKS yang diambil ({sem2_enrolled} SKS).")

        if sem2_grade is None or sem2_grade < 0.0 or sem2_grade > 20.0:
            validation_errors.append(f"**Rata-rata Nilai Sem 2** ({sem2_grade}) di luar skala (0 hingga 20).")

        if validation_errors:
            st.session_state['has_predicted'] = False
            show_validation_modal(validation_errors)
        else:
            current_data = {
                'Admission_grade': float(admission_grade),
                'Age_at_enrollment': int(age),
                'Curricular_units_1st_sem_enrolled': int(sem1_enrolled),
                'Curricular_units_1st_sem_evaluations': int(calc_sem1_eval),
                'Curricular_units_1st_sem_approved': int(sem1_approved),
                'Curricular_units_1st_sem_grade': float(sem1_grade),
                'Curricular_units_2nd_sem_enrolled': int(sem2_enrolled),
                'Curricular_units_2nd_sem_evaluations': int(calc_sem2_eval),
                'Curricular_units_2nd_sem_approved': int(sem2_approved),
                'Curricular_units_2nd_sem_grade': float(sem2_grade),
                'Tuition_fees_up_to_date': int(tuition),
                'Scholarship_holder': int(scholarship),
                'Debtor': int(debtor),
                'Gender': int(gender)
            }

            status_result, proba = run_pipeline(current_data)
            st.session_state['student_name'] = input_name.strip()
            st.session_state['has_predicted'] = True
            st.session_state['current_data'] = current_data
            st.session_state['status_result'] = status_result
            st.session_state['proba'] = proba
            st.rerun()

    if st.session_state.get('has_predicted', False):
        display_name = st.session_state.get('student_name', 'Mahasiswa')
        current_data = st.session_state['current_data']
        status_result = st.session_state['status_result']
        proba = st.session_state['proba']

        st.divider()
        st.markdown(f"### <i class='fa-solid fa-chart-pie' style='color:#2563EB;'></i> Hasil Evaluasi: **{display_name}**", unsafe_allow_html=True)
        
        with st.container(border=True):
            res1, res2 = st.columns([1.2, 0.8])

            with res1:
                if status_result == "Dropout":
                    st.error("Status Prediksi: Dropout (Risiko Kritis)")
                    st.caption("Pola capaian mengindikasikan mahasiswa berada dalam zona rentan putus studi.")
                else:
                    st.success("Status Prediksi: Graduate (Kondisi Stabil)")
                    st.caption("Mahasiswa berada pada trajektori akademik yang positif menuju kelulusan tepat waktu.")

                if proba is not None and len(proba) >= 2:
                    risk_pct = float(proba[1])
                    st.metric(label="Probabilitas Risiko Dropout", value=f"{risk_pct * 100:.1f}%")
                    st.progress(risk_pct)

            with res2:
                if proba is not None and len(proba) >= 2:
                    st.markdown("**Distribusi Keyakinan Model AI:**")
                    prob_df = pd.DataFrame({
                        'Status': ['Graduate (Lulus)', 'Dropout (Putus Studi)'],
                        'Peluang': [f"{proba[0]*100:.2f}%", f"{proba[1]*100:.2f}%"]
                    })
                    st.dataframe(prob_df, use_container_width=True, hide_index=True)

        # SIMULASI INTERVENSI (WHAT-IF)
        st.divider()
        st.markdown("### <i class='fa-solid fa-flask-vial' style='color:#2563EB;'></i> Simulasi Tindakan Intervensi (What-If)", unsafe_allow_html=True)
        st.caption("Uji skenario mitigasi: ubah parameter berikut untuk melihat proyeksi perubahan risiko secara real-time.")
        
        with st.container(border=True):
            sim_col1, sim_col2 = st.columns(2)
            with sim_col1:
                sim_tuition = st.selectbox(
                    "Intervensi Status SPP:", 
                    options=[1, 0], 
                    index=0 if current_data['Tuition_fees_up_to_date'] == 1 else 1, 
                    format_func=lambda x: "SPP Dilunasi / Keringanan Cicilan" if x == 1 else "SPP Tetap Menunggak"
                )
                sim_debtor = st.selectbox(
                    "Intervensi Beban Tunggakan Utang:", 
                    options=[0, 1], 
                    index=0 if current_data['Debtor'] == 0 else 1, 
                    format_func=lambda x: "Bebas Tunggakan Utang" if x == 0 else "Masih Memiliki Tunggakan"
                )
            with sim_col2:
                base_approved = int(current_data['Curricular_units_2nd_sem_approved'])
                max_enrolled = max(1, int(current_data['Curricular_units_2nd_sem_enrolled']))
                sim_sem2_approved = st.slider(
                    "Target SKS Lulus Semester 2:", 
                    min_value=0, 
                    max_value=max_enrolled, 
                    value=min(base_approved, max_enrolled),
                    help="Melalui bimbingan asistensi atau kelas remedial."
                )
                base_grade = float(current_data['Curricular_units_2nd_sem_grade'])
                sim_sem2_grade = st.slider(
                    "Target Nilai Semester 2:", 
                    min_value=0.0, 
                    max_value=20.0, 
                    value=min(20.0, max(0.0, base_grade)), 
                    step=0.5
                )

            sim_sem2_eval = max_enrolled + max(0, (max_enrolled - int(sim_sem2_approved)))

            sim_data = current_data.copy()
            sim_data['Tuition_fees_up_to_date'] = int(sim_tuition)
            sim_data['Debtor'] = int(sim_debtor)
            sim_data['Curricular_units_2nd_sem_approved'] = int(sim_sem2_approved)
            sim_data['Curricular_units_2nd_sem_evaluations'] = int(sim_sem2_eval)
            sim_data['Curricular_units_2nd_sem_grade'] = float(sim_sem2_grade)
            
            sim_status, sim_proba = run_pipeline(sim_data)

            if proba is not None and sim_proba is not None and len(sim_proba) >= 2:
                old_risk = float(proba[1]) * 100
                new_risk = float(sim_proba[1]) * 100
                delta_risk = new_risk - old_risk
                
                m1, m2 = st.columns(2)
                m1.metric("Proyeksi Status Akhir", sim_status)
                m2.metric("Proyeksi Risiko Akhir", f"{new_risk:.1f}%", f"{delta_risk:+.1f}%", delta_color="inverse")

        # REKOMENDASI TINDAKAN PRESKRIPTIF DINAMIS
        st.markdown("### <i class='fa-solid fa-clipboard-list' style='color:#2563EB;'></i> Rencana Aksi Intervensi", unsafe_allow_html=True)
        
        if status_result == "Dropout" and sim_status == "Graduate":
            st.info(f"""
            **Skenario Intervensi Berhasil Memulihkan Prediksi Mahasiswa**  
            Melalui penyesuaian parameter di atas, potensi putus studi atas nama **{display_name}** berhasil ditekan ke kategori aman.
            
            **Langkah Operasional Kampus:**
            1. **Fasilitasi Finansial:** Koordinasikan skema cicilan SPP atau daftarkan ke bantuan beasiswa darurat.
            2. **Kontrak Akademik Remedial:** Daftarkan mahasiswa pada program bimbingan asistensi agar target **{sim_sem2_approved} SKS** tercapai.
            3. **Monitoring Dosen Wali:** Agendakan evaluasi dua mingguan guna memastikan capaian nilai **{sim_sem2_grade:.1f}** terpenuhi.
            """)

        elif sim_status == "Dropout":
            st.warning(f"""
            **Status Kritis: Diperlukan Penanganan Khusus**  
            Proyeksi akademik **{display_name}** masih berada di zona rawan putus studi meskipun skenario telah disimulasikan.
            
            **Langkah Penyelamatan Terpadu:**
            * **Audit Keuangan:** Koordinasikan penangguhan beban administrasi/tunggakan dengan bagian keuangan.
            * **Konseling Terjadwal:** Adakan pertemuan tatap muka bersama dosen wali dan orang tua untuk meninjau kendala non-akademis.
            * **Restrukturisasi Beban Studi:** Evaluasi kembali beban studi semester berikutnya agar sesuai kapasitas adaptasi mahasiswa.
            """)

        else:
            st.success(f"""
            **Kondisi Mahasiswa Berada dalam Status Aman**  
            Mahasiswa atas nama **{display_name}** menunjukkan ketahanan studi yang stabil.
            
            **Pengembangan Potensi:**
            * Dorong partisipasi dalam program magang industri bersertifikat (MBKM).
            * Libatkan dalam proyek penelitian atau tim perlombaan ilmiah mahasiswa.
            """)

# ==========================================
# TAB 2: BATCH SCREENING KAMPUS
# ==========================================
elif selected_tab == "Pemindaian Angkatan (Batch Screening)":
    st.markdown("""
    <h3><i class="fa-solid fa-folder-tree" style="color:#2563EB;"></i> Skrining Risiko Massal (Batch Screening)</h3>
    """, unsafe_allow_html=True)
    st.caption("Unggah berkas rekapitulasi angkatan (.csv) untuk mendeteksi kelompok mahasiswa rentan putus studi secara serempak.")

    if "uploader_key" not in st.session_state:
        st.session_state["uploader_key"] = 0

    uploaded_file = st.file_uploader(
        "Pilih Berkas CSV", 
        type=["csv"], 
        help="Format berkas CSV harus memuat data angkatan mahasiswa.",
        key=f"csv_uploader_{st.session_state['uploader_key']}"
    )

    if uploaded_file is None:
        with st.container(border=True):
            st.info("Format berkas dapat mencakup kolom identitas (`NIM`, `Nama_Mahasiswa`, `Kelas`) dan parameter akademik (`Curricular_units_...`, `Tuition_fees_up_to_date`, dll).")
    else:
        try:
            df_upload = pd.read_csv(uploaded_file)
            
            # 1. VALIDASI KESESUAIAN BERKAS DENGAN FORMAT ANALISIS
            batch_errors = []
            if df_upload.empty:
                batch_errors.append("Berkas CSV yang diunggah kosong (tidak memiliki baris data).")

            required_features = [
                'Curricular_units_1st_sem_enrolled',
                'Curricular_units_1st_sem_approved',
                'Curricular_units_1st_sem_grade',
                'Curricular_units_2nd_sem_enrolled',
                'Curricular_units_2nd_sem_approved',
                'Curricular_units_2nd_sem_grade',
                'Tuition_fees_up_to_date'
            ]
            
            missing_features = [col for col in required_features if col not in df_upload.columns]
            if missing_features:
                batch_errors.append(f"Berkas tidak memuat kolom parameter analisis wajib: `{', '.join(missing_features)}`.")

            if batch_errors:
                show_batch_file_error_modal(batch_errors)
            else:
                st.success(f"Berkas valid dan siap diproses: terdeteksi **{len(df_upload)} baris data mahasiswa**.")
                
                if 'Curricular_units_1st_sem_evaluations' not in df_upload.columns:
                    df_upload['Curricular_units_1st_sem_evaluations'] = df_upload['Curricular_units_1st_sem_enrolled'] + (df_upload['Curricular_units_1st_sem_enrolled'] - df_upload.get('Curricular_units_1st_sem_approved', 0))
                if 'Curricular_units_2nd_sem_evaluations' not in df_upload.columns:
                    df_upload['Curricular_units_2nd_sem_evaluations'] = df_upload['Curricular_units_2nd_sem_enrolled'] + (df_upload['Curricular_units_2nd_sem_enrolled'] - df_upload.get('Curricular_units_2nd_sem_approved', 0))

                if st.button("Jalankan Analisis Massal", icon=":material/rocket_launch:", type="primary"):
                    with st.spinner("Model AI sedang memproses seluruh data angkatan..."):
                        expected_cols = getattr(scaler, "feature_names_in_", getattr(model, "feature_names_in_", None))
                        
                        df_proc = df_upload.copy()
                        if expected_cols is not None:
                            for col in expected_cols:
                                if col not in df_proc.columns:
                                    df_proc[col] = 0
                            df_features_batch = df_proc[expected_cols]
                        else:
                            df_features_batch = df_proc

                        processed_batch = scaler.transform(df_features_batch) if scaler is not None else df_features_batch
                        predictions = model.predict(processed_batch)
                        probabilities = model.predict_proba(processed_batch) if hasattr(model, "predict_proba") else None

                        df_upload['Prediksi_Status'] = [decode_label(p) for p in predictions]
                        if probabilities is not None:
                            df_upload['Risiko_Dropout_Persen'] = [round(float(p[1]) * 100, 2) for p in probabilities]

                        # 2. KPI RINGKASAN EKSEKUTIF
                        total_mhs = len(df_upload)
                        total_dropout = int((df_upload['Prediksi_Status'] == 'Dropout').sum())
                        pct_dropout = float((total_dropout / total_mhs) * 100) if total_mhs > 0 else 0.0

                        if pct_dropout >= 50.0:
                            ratio_border_color = "#DC2626"
                            ratio_bg_color = "rgba(220, 38, 38, 0.08)"
                            ratio_text_color = "#F87171"
                            ratio_badge_text = "KRITIS / TINGGI"
                            ratio_badge_color = "#DC2626"
                        elif pct_dropout >= 25.0:
                            ratio_border_color = "#F59E0B"
                            ratio_bg_color = "rgba(245, 158, 11, 0.08)"
                            ratio_text_color = "#FBBF24"
                            ratio_badge_text = "WASPADA / SEDANG"
                            ratio_badge_color = "#F59E0B"
                        else:
                            ratio_border_color = "#10B981"
                            ratio_bg_color = "rgba(16, 185, 129, 0.08)"
                            ratio_text_color = "#34D399"
                            ratio_badge_text = "STABIL / TERKENDALI"
                            ratio_badge_color = "#10B981"

                        st.divider()
                        k1, k2, k3 = st.columns(3)
                        
                        with k1:
                            st.markdown(f"""
                            <div style="padding: 1.1rem; border-radius: 0.75rem; border: 1px solid rgba(37, 99, 235, 0.35); background: rgba(37, 99, 235, 0.06); margin-bottom: 0.5rem;">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <span style="font-size: 0.85rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px;">Total Mahasiswa</span>
                                    <i class="fa-solid fa-users" style="color: #60A5FA; font-size: 1.1rem;"></i>
                                </div>
                                <div style="font-size: 2.1rem; font-weight: 800; color: #FFFFFF; margin-top: 0.35rem;">
                                    {total_mhs:,}
                                </div>
                                <div style="font-size: 0.78rem; color: #64748B; margin-top: 0.15rem;">Seluruh data populasi angkatan</div>
                            </div>
                            """.replace(",", "."), unsafe_allow_html=True)
                            
                        with k2:
                            st.markdown(f"""
                            <div style="padding: 1.1rem; border-radius: 0.75rem; border: 1px solid rgba(220, 38, 38, 0.45); background: rgba(220, 38, 38, 0.08); margin-bottom: 0.5rem;">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <span style="font-size: 0.85rem; font-weight: 700; color: #FCA5A5; text-transform: uppercase; letter-spacing: 0.5px;">Potensi Dropout</span>
                                    <i class="fa-solid fa-triangle-exclamation" style="color: #EF4444; font-size: 1.1rem;"></i>
                                </div>
                                <div style="font-size: 2.1rem; font-weight: 800; color: #F87171; margin-top: 0.35rem;">
                                    {total_dropout:,}
                                </div>
                                <div style="font-size: 0.78rem; color: #FCA5A5; margin-top: 0.15rem;">Membutuhkan mitigasi akademik</div>
                            </div>
                            """.replace(",", "."), unsafe_allow_html=True)

                        with k3:
                            st.markdown(f"""
                            <div style="padding: 1.1rem; border-radius: 0.75rem; border: 1px solid {ratio_border_color}; background: {ratio_bg_color}; margin-bottom: 0.5rem;">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <span style="font-size: 0.85rem; font-weight: 700; color: {ratio_text_color}; text-transform: uppercase; letter-spacing: 0.5px;">Rasio Mahasiswa Kritis</span>
                                    <span style="font-size: 0.7rem; font-weight: 800; background-color: {ratio_badge_color}; color: #FFFFFF; padding: 2px 7px; border-radius: 9999px;">{ratio_badge_text}</span>
                                </div>
                                <div style="font-size: 2.1rem; font-weight: 800; color: {ratio_text_color}; margin-top: 0.35rem;">
                                    {pct_dropout:.1f}%
                                </div>
                                <div style="font-size: 0.78rem; color: #94A3B8; margin-top: 0.15rem;">Proporsi risiko dari populasi terdeteksi</div>
                            </div>
                            """, unsafe_allow_html=True)

                        # 3. DEKODE NILAI BINER & PENYESUAIAN NAMA KOLOM
                        st.write("")
                        st.markdown("##### <i class='fa-solid fa-table-list' style='color:#2563EB;'></i> Hasil Pemindaian & Daftar Prioritas Penanganan", unsafe_allow_html=True)
                        
                        df_display = df_upload.copy()
                        
                        if 'Tuition_fees_up_to_date' in df_display.columns:
                            df_display['Tuition_fees_up_to_date'] = df_display['Tuition_fees_up_to_date'].map({1: 'Lunas', 0: 'Menunggak'}).fillna(df_display['Tuition_fees_up_to_date'])
                        if 'Debtor' in df_display.columns:
                            df_display['Debtor'] = df_display['Debtor'].map({1: 'Ada Utang', 0: 'Bebas Utang'}).fillna(df_display['Debtor'])
                        if 'Scholarship_holder' in df_display.columns:
                            df_display['Scholarship_holder'] = df_display['Scholarship_holder'].map({1: 'Penerima', 0: 'Bukan Penerima'}).fillna(df_display['Scholarship_holder'])
                        if 'Gender' in df_display.columns:
                            df_display['Gender'] = df_display['Gender'].map({1: 'Laki-laki', 0: 'Perempuan'}).fillna(df_display['Gender'])

                        rename_dict = {
                            'NIM': 'NIM',
                            'Nama_Mahasiswa': 'Nama Mahasiswa',
                            'Kelas': 'Kelas',
                            'Prediksi_Status': 'Status Prediksi',
                            'Risiko_Dropout_Persen': 'Tingkat Risiko (%)',
                            'Admission_grade': 'Nilai Seleksi Masuk',
                            'Age_at_enrollment': 'Usia Masuk',
                            'Gender': 'Jenis Kelamin',
                            'Tuition_fees_up_to_date': 'Status SPP',
                            'Debtor': 'Beban Utang',
                            'Scholarship_holder': 'Status Beasiswa',
                            'Curricular_units_1st_sem_enrolled': 'SKS Diambil Sem 1',
                            'Curricular_units_1st_sem_evaluations': 'Evaluasi Ujian Sem 1',
                            'Curricular_units_1st_sem_approved': 'SKS Lulus Sem 1',
                            'Curricular_units_1st_sem_grade': 'Rata-rata Nilai Sem 1',
                            'Curricular_units_2nd_sem_enrolled': 'SKS Diambil Sem 2',
                            'Curricular_units_2nd_sem_evaluations': 'Evaluasi Ujian Sem 2',
                            'Curricular_units_2nd_sem_approved': 'SKS Lulus Sem 2',
                            'Curricular_units_2nd_sem_grade': 'Rata-rata Nilai Sem 2'
                        }
                        
                        df_display = df_display.rename(columns=rename_dict)

                        def highlight_risk_cells(val):
                            if isinstance(val, (int, float)):
                                if val >= 60.0:
                                    return 'background-color: rgba(220, 38, 38, 0.28); color: #FCA5A5; font-weight: 800;'
                                elif val >= 40.0:
                                    return 'background-color: rgba(245, 158, 11, 0.25); color: #FDE68A; font-weight: 700;'
                                else:
                                    return 'background-color: rgba(16, 185, 129, 0.22); color: #86EFAC; font-weight: 700;'
                            return ''

                        filter_tab1, filter_tab2 = st.tabs(["Prioritas Intervensi (Risiko > 60%)", "Seluruh Data Angkatan"])
                        
                        with filter_tab1:
                            if 'Tingkat Risiko (%)' in df_display.columns:
                                df_high_risk = df_display[df_display['Tingkat Risiko (%)'] >= 60.0].sort_values(by='Tingkat Risiko (%)', ascending=False)
                            else:
                                df_high_risk = df_display[df_display['Status Prediksi'] == 'Dropout']
                            
                            st.markdown(f"""
                            <div style="display: inline-block; padding: 4px 10px; border-radius: 6px; background-color: rgba(220, 38, 38, 0.15); border: 1px solid #DC2626; color: #FCA5A5; font-weight: 700; font-size: 0.82rem; margin-bottom: 0.5rem;">
                                <i class="fa-solid fa-triangle-exclamation"></i> Terdeteksi {len(df_high_risk)} mahasiswa dalam zona risiko tinggi (> 60%). Tindakan penyelamatan darurat diperlukan segera.
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if 'Tingkat Risiko (%)' in df_high_risk.columns:
                                styled_high = df_high_risk.style.map(highlight_risk_cells, subset=['Tingkat Risiko (%)'])
                                st.dataframe(styled_high, use_container_width=True)
                            else:
                                st.dataframe(df_high_risk, use_container_width=True)
                            
                        with filter_tab2:
                            st.caption(f"Menampilkan total rekapitulasi **{len(df_display)} mahasiswa**.")
                            if 'Tingkat Risiko (%)' in df_display.columns:
                                styled_all = df_display.style.map(highlight_risk_cells, subset=['Tingkat Risiko (%)'])
                                st.dataframe(styled_all, use_container_width=True)
                            else:
                                st.dataframe(df_display, use_container_width=True)

                        # EXPORT BUTTON
                        csv_export = df_upload.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Unduh Rekapitulasi Lengkap (.csv)",
                            icon=":material/download:",
                            data=csv_export,
                            file_name="laporan_skrining_risiko_mahasiswa.csv",
                            mime="text/csv"
                        )

                        # 4. ACTION PLAN REKOMENDASI UNTUK KAMPUS
                        st.divider()
                        st.markdown("### <i class='fa-solid fa-bullhorn' style='color:#2563EB;'></i> Rekomendasi Rencana Aksi Kampus (Institutional Action Plan)", unsafe_allow_html=True)
                        st.caption("Sistem secara otomatis merumuskan 1 rencana aksi utama berdasarkan profil sebaran risiko angkatan:")

                        if pct_dropout >= 50.0:
                            st.markdown("""
                            <div style="padding: 1.25rem; border-radius: 0.75rem; border-left: 6px solid #DC2626; background: rgba(220, 38, 38, 0.08); border-top: 1px solid rgba(220,38,38,0.25); border-right: 1px solid rgba(220,38,38,0.25); border-bottom: 1px solid rgba(220,38,38,0.25);">
                                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.5rem;">
                                    <span style="font-size: 0.75rem; font-weight: 800; background-color: #DC2626; color: #FFFFFF; padding: 2px 8px; border-radius: 4px;">PRIORITAS 1</span>
                                    <span style="font-size: 1.15rem; font-weight: 800; color: #F87171;">Tindakan Darurat: Angkatan Dalam Zona Kritis (> 50% Berisiko)</span>
                                </div>
                                <p style="color: #E2E8F0; font-size: 0.9rem; margin-bottom: 0.75rem;">
                                    Lebih dari separuh populasi angkatan terindikasi berada di ambang putus studi. Diperlukan intervensi institusional lintas unit secepatnya:
                                </p>
                                <ul style="color: #E2E8F0; font-size: 0.9rem; margin-bottom: 0; line-height: 1.6;">
                                    <li><b>Konseling Terjadwal Wajib:</b> Terbitkan surat panggilan resmi bagi mahasiswa di tab <i>Prioritas Intervensi</i> bersama Dosen Pembimbing Akademik (DPA) dan orang tua/wali dalam kurun 7 hari ke depan.</li>
                                    <li><b>Relaksasi Beban Finansial:</b> Biro Keuangan wajib membuka skema penangguhan atau cicilan khusus SPP bagi mahasiswa berstatus menunggak agar tidak terkendala administrasi ujian.</li>
                                    <li><b>Proteksi Status Akademik:</b> Kunci sementara opsi pengunduran diri sepihak di sistem informasi akademik sebelum sesi mediasi prodi terlaksana.</li>
                                    <li><b>Audit Silabus Semester Awal:</b> Gugus Penjaminan Mutu perlu meninjau tingkat kesulitan mata kuliah semester 1 dan 2 yang mencatat rasio ketidaklulusan tertinggi.</li>
                                </ul>
                            </div>
                            """, unsafe_allow_html=True)

                        elif pct_dropout >= 25.0:
                            st.markdown("""
                            <div style="padding: 1.25rem; border-radius: 0.75rem; border-left: 6px solid #F59E0B; background: rgba(245, 158, 11, 0.08); border-top: 1px solid rgba(245,158,11,0.25); border-right: 1px solid rgba(245,158,11,0.25); border-bottom: 1px solid rgba(245,158,11,0.25);">
                                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.5rem;">
                                    <span style="font-size: 0.75rem; font-weight: 800; background-color: #F59E0B; color: #000000; padding: 2px 8px; border-radius: 4px;">PRIORITAS 2</span>
                                    <span style="font-size: 1.15rem; font-weight: 800; color: #FBBF24;">Tindakan Mitigasi Terarah: Angkatan Dalam Zona Waspada (25% - 50% Berisiko)</span>
                                </div>
                                <p style="color: #E2E8F0; font-size: 0.9rem; margin-bottom: 0.75rem;">
                                    Tingkat risiko angkatan berada pada level menengah. Fokus utama diarahkan pada penguatan kompetensi akademik dan pencegahan penurunan performa:
                                </p>
                                <ul style="color: #E2E8F0; font-size: 0.9rem; margin-bottom: 0; line-height: 1.6;">
                                    <li><b>Program Belajar Sebaya (Peer Tutoring):</b> Selenggarakan kelas asistensi intensif untuk mata kuliah dasar dengan melibatkan kakak tingkat berprestasi.</li>
                                    <li><b>Restrukturisasi Kontrak SKS:</b> Batasi batas pengambilan rencana studi maksimal 18 SKS pada semester berikutnya bagi mahasiswa dengan SKS lulus rendah.</li>
                                    <li><b>Monitoring Kemajuan Berkala:</b> DPA melakukan evaluasi capaian nilai setiap pertengahan semester (pasca-UTS) sebelum nilai akhir difinalisasi.</li>
                                </ul>
                            </div>
                            """, unsafe_allow_html=True)

                        else:
                            st.markdown("""
                            <div style="padding: 1.25rem; border-radius: 0.75rem; border-left: 6px solid #10B981; background: rgba(16, 185, 129, 0.08); border-top: 1px solid rgba(16,185,129,0.25); border-right: 1px solid rgba(16,185,129,0.25); border-bottom: 1px solid rgba(16,185,129,0.25);">
                                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.5rem;">
                                    <span style="font-size: 0.75rem; font-weight: 800; background-color: #10B981; color: #FFFFFF; padding: 2px 8px; border-radius: 4px;">PRIORITAS 3</span>
                                    <span style="font-size: 1.15rem; font-weight: 800; color: #34D399;">Kondisi Prima: Angkatan Dalam Kondisi Stabil (< 25% Berisiko)</span>
                                </div>
                                <p style="color: #E2E8F0; font-size: 0.9rem; margin-bottom: 0.75rem;">
                                    Mayoritas mahasiswa berada pada trajektori kelulusan yang sehat. Kampus dapat memaksimalkan program pengembangan potensi unggulan:
                                </p>
                                <ul style="color: #E2E8F0; font-size: 0.9rem; margin-bottom: 0; line-height: 1.6;">
                                    <li><b>Akselerasi Program Unggulan:</b> Salurkan mahasiswa ke program magang bersertifikat (MBKM), riset kolaboratif dosen, dan kompetisi ilmiah nasional.</li>
                                    <li><b>Pemberian Insentif Beasiswa Prestasi:</b> Fasilitasi skema penghargaan akademik untuk mempertahankan indeks prestasi kumulatif.</li>
                                    <li><b>Pemantauan Sistem Otomatis:</b> Cukup lakukan peninjauan rutin mandiri melalui dasbor analitik akademik kampus setiap pergantian semester.</li>
                                </ul>
                            </div>
                            """, unsafe_allow_html=True)

        except Exception as err:
            show_batch_file_error_modal([f"Terjadi kesalahan teknis saat membaca berkas: {err}"])