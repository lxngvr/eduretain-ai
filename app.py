# IMPORT LIBRARY & DEPENDENCIES
import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st

# TENTUKAN PATH LOGO SESUAI LOKASI FOLDER
LOGO_PATH = os.path.join("image", "eduretain AI - logo.png")
if not os.path.exists(LOGO_PATH):
    # Cadangan jika berkas berada di direktori root atau format lain
    possible_paths = [
        "image/eduretain AI - logo.png",
        "image/logo.png",
        "eduretain AI - logo.png",
        "logo.png"
    ]
    LOGO_PATH = next((p for p in possible_paths if os.path.exists(p)), None)

# KONFIGURASI TAMPILAN HALAMAN (FAVICON MENGGUNAKAN LOGO ASLI)
st.set_page_config(
    page_title="EduRetain AI - Student Retention Early Warning System",
    page_icon=LOGO_PATH if LOGO_PATH else "🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# INJEKSI CSS GLOBAL STREAMLIT (TEMA BIRU, FONT NUNITO, DAN RESPONSIVE RULES)
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

    /* 3. TOMBOL UTAMA (PRIMARY BUTTON) */
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

    /* 4. TOMBOL SEKUNDER (SECONDARY BUTTON) */
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

    /* 8. MEDIA QUERIES UNTUK TAMPILAN MOBILE & TABLET */
    @media (max-width: 768px) {
        [data-testid="column"] {
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

# PANEL SIDEBAR
with st.sidebar:
    # TAMPILAN HEADER LOGO & TEKS SEJAJAR (INLINE)
    col_logo, col_title = st.columns([1, 3.2], vertical_alignment="center")
    
    with col_logo:
        if LOGO_PATH:
            st.image(LOGO_PATH, width=100)
        else:
            st.markdown("<h2 style='margin:0;'>🎓</h2>", unsafe_allow_html=True)
            
    with col_title:
        st.markdown("""
        <div style="line-height: 1.2;">
            <div style="font-size: 1.15rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.3px;">
                EduRetain <span style="color: #60A5FA;">AI</span>
            </div>
            <div style="font-size: 0.75rem; color: #94A3B8; font-weight: 600;">
                Early Warning System
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("##### Informasi & Parameter")
    if st.button("Spesifikasi Model AI", icon=":material/memory:", use_container_width=True):
        show_model_modal()
        
    if st.button("Tentang Pengembang", icon=":material/badge:", use_container_width=True):
        show_developer_modal()
        
    st.divider()
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
        value=st.session_state.get('student_name', 'Galang Dava Ramadhan'),
        placeholder="Ketik nama mahasiswa yang akan dievaluasi...",
        help="Nama digunakan untuk personalisasi lembar rekomendasi."
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("##### <i class='fa-solid fa-wallet' style='color:#2563EB;'></i> Administrasi & Finansial", unsafe_allow_html=True)
            tuition = st.selectbox("Status Pembayaran SPP", options=[1, 0], index=0, format_func=lambda x: "Lancar / Lunas" if x == 1 else "Menunggak")
            debtor = st.selectbox("Memiliki Tunggakan Utang?", options=[1, 0], index=1, format_func=lambda x: "Ya (Ada Tunggakan)" if x == 1 else "Tidak Ada")
            scholarship = st.selectbox("Penerima Beasiswa?", options=[1, 0], index=1, format_func=lambda x: "Ya (Penerima)" if x == 1 else "Bukan Penerima")
            gender = st.selectbox("Jenis Kelamin", options=[1, 0], format_func=lambda x: "Laki-laki" if x == 1 else "Perempuan")
            age = st.number_input("Usia Saat Masuk (Tahun)", min_value=15, max_value=70, value=20)

    with col2:
        with st.container(border=True):
            st.markdown("##### <i class='fa-solid fa-book' style='color:#2563EB;'></i> Evaluasi Semester 1", unsafe_allow_html=True)
            admission_grade = st.number_input("Nilai Ujian Masuk (0 - 200)", min_value=0.0, max_value=200.0, value=125.0, step=0.5)
            sem1_enrolled = st.number_input("SKS Diambil Sem 1", min_value=1, max_value=30, value=6, key="sem1_enrolled")
            sem1_approved = st.number_input("SKS Lulus Sem 1", min_value=0, max_value=int(sem1_enrolled), value=min(5, int(sem1_enrolled)), key="sem1_approved")
            sem1_grade = st.number_input("Rata-rata Nilai Sem 1 (0 - 20)", min_value=0.0, max_value=20.0, value=13.0, step=0.1)

    with col3:
        with st.container(border=True):
            st.markdown("##### <i class='fa-solid fa-book-open' style='color:#2563EB;'></i> Evaluasi Semester 2", unsafe_allow_html=True)
            sem2_enrolled = st.number_input("SKS Diambil Sem 2", min_value=1, max_value=30, value=6, key="sem2_enrolled")
            sem2_approved = st.number_input("SKS Lulus Sem 2", min_value=0, max_value=int(sem2_enrolled), value=min(5, int(sem2_enrolled)), key="sem2_approved")
            sem2_grade = st.number_input("Rata-rata Nilai Sem 2 (0 - 20)", min_value=0.0, max_value=20.0, value=13.0, step=0.1)

    # Otomatisasi kalkulasi jumlah evaluasi
    calc_sem1_eval = int(sem1_enrolled) + (int(sem1_enrolled) - int(sem1_approved))
    calc_sem2_eval = int(sem2_enrolled) + (int(sem2_enrolled) - int(sem2_approved))

    st.write("")

    if st.button("Jalankan Analisis Risiko", type="primary", use_container_width=True):
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
        st.session_state['student_name'] = input_name
        st.session_state['has_predicted'] = True
        st.session_state['current_data'] = current_data
        st.session_state['status_result'] = status_result
        st.session_state['proba'] = proba

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
                max_enrolled = int(current_data['Curricular_units_2nd_sem_enrolled'])
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
                    value=base_grade, 
                    step=0.5
                )

            sim_sem2_eval = max_enrolled + (max_enrolled - int(sim_sem2_approved))

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

    uploaded_file = st.file_uploader("Pilih Berkas CSV", type=["csv"], help="Format berkas CSV harus memuat data angkatan mahasiswa.")

    if uploaded_file is None:
        with st.container(border=True):
            st.info("Format berkas dapat mencakup kolom identitas (`NIM`, `Nama_Mahasiswa`, `Kelas`) dan parameter akademik (`Curricular_units_...`, `Tuition_fees_up_to_date`, dll).")
    else:
        try:
            df_upload = pd.read_csv(uploaded_file)
            st.success(f"Berkas berhasil dimuat: terdeteksi **{len(df_upload)} baris data mahasiswa**.")
            
            if 'Curricular_units_1st_sem_evaluations' not in df_upload.columns and 'Curricular_units_1st_sem_enrolled' in df_upload.columns:
                df_upload['Curricular_units_1st_sem_evaluations'] = df_upload['Curricular_units_1st_sem_enrolled'] + (df_upload['Curricular_units_1st_sem_enrolled'] - df_upload.get('Curricular_units_1st_sem_approved', 0))
            if 'Curricular_units_2nd_sem_evaluations' not in df_upload.columns and 'Curricular_units_2nd_sem_enrolled' in df_upload.columns:
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

                    # KPI METRICS
                    total_mhs = len(df_upload)
                    total_dropout = (df_upload['Prediksi_Status'] == 'Dropout').sum()
                    pct_dropout = (total_dropout / total_mhs) * 100

                    st.divider()
                    k1, k2, k3 = st.columns(3)
                    k1.metric("Total Mahasiswa Dipindai", total_mhs)
                    k2.metric("Terindikasi Rawan Dropout", total_dropout)
                    k3.metric("Rasio Mahasiswa Kritis", f"{pct_dropout:.1f}%")

                    # TABEL PRIORITAS INTERVENSI
                    st.markdown("##### <i class='fa-solid fa-triangle-exclamation' style='color:#DC2626;'></i> Daftar Mahasiswa Prioritas Intervensi (Risiko > 60%)", unsafe_allow_html=True)
                    high_risk_df = df_upload[df_upload.get('Risiko_Dropout_Persen', 0) >= 60.0]
                    
                    priority_cols = [c for c in ['NIM', 'Nama_Mahasiswa', 'Kelas', 'Prediksi_Status', 'Risiko_Dropout_Persen'] if c in high_risk_df.columns]
                    other_cols = [c for c in high_risk_df.columns if c not in priority_cols]
                    ordered_display_df = high_risk_df[priority_cols + other_cols]

                    st.dataframe(ordered_display_df, use_container_width=True)

                    # EXPORT BUTTON
                    csv_export = df_upload.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Unduh Laporan Skrining (.csv)",
                        icon=":material/download:",
                        data=csv_export,
                        file_name="laporan_skrining_risiko_mahasiswa.csv",
                        mime="text/csv"
                    )

        except Exception as err:
            st.error(f"Gagal memproses berkas CSV: {err}")