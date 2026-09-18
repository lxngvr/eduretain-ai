import numpy as np
import pandas as pd

def generate_cohort(
    n_students=120,
    scenario="kritis",
    year=2024,
    prodi_code="IF",
    class_prefix="IF"
):
    """
    Menghasilkan data angkatan sintetis dengan format yang kompatibel dengan EduRetain AI.
    Pilihan skenario: 'kritis', 'waspada', 'stabil'.
    """
    # Seed berbeda per skenario agar data bervariasi namun konsisten
    seeds = {"kritis": 42, "waspada": 100, "stabil": 200}
    np.random.seed(seeds.get(scenario, 42))

    # Generator Nama Mahasiswa Indonesia yang realistis
    first_names = [
        "Aditya", "Bagas", "Citra", "Dian", "Eko", "Fajar", "Gita", "Hadi",
        "Indah", "Joko", "Kartika", "Lestari", "Muhammad", "Nadia", "Oki",
        "Putri", "Rian", "Siti", "Taufik", "Wahyu", "Ilham", "Dinda", "Rafi",
        "Annisa", "Budi", "Aulia", "Dimas", "Dewi", "Reza", "Farhan"
    ]
    last_names = [
        "Pratama", "Saputra", "Wijaya", "Kusuma", "Utami", "Santoso", "Hidayat",
        "Ramadhan", "Nugroho", "Wulandari", "Setiawan", "Permana", "Anggraini",
        "Firmansyah", "Puspa", "Mahendra", "Siregar", "Nasution"
    ]

    names = [f"{np.random.choice(first_names)} {np.random.choice(last_names)}" for _ in range(n_students)]
    
    # Pembagian kelas (misal: IF-A, IF-B, IF-C per 40 mahasiswa)
    classes = [f"{class_prefix}-{chr(65 + i // 40)}" for i in range(n_students)]
    nims = [f"{year}{prodi_code}{classes[i][-1]}{(i % 40) + 1:03d}" for i in range(n_students)]
    gender = np.random.choice([0, 1], size=n_students, p=[0.45, 0.55])

    # Skenario 1: Kritis (Mayoritas Rawan Dropout / > 50%)
    if scenario == "kritis":
        tuition = np.random.choice([1, 0], size=n_students, p=[0.40, 0.60])   # 60% menunggak SPP
        debtor = np.random.choice([0, 1], size=n_students, p=[0.60, 0.40])    # 40% punya utang
        scholarship = np.random.choice([0, 1], size=n_students, p=[0.90, 0.10])
        age = np.random.randint(18, 26, size=n_students)
        adm_grade = np.round(np.random.normal(118, 10, size=n_students), 1)

        sem1_enrolled = np.full(n_students, 6)
        sem1_approved = np.random.choice([0, 1, 2, 3, 4, 5, 6], size=n_students, p=[0.10, 0.20, 0.25, 0.20, 0.15, 0.08, 0.02])
        sem1_eval = sem1_enrolled + (sem1_enrolled - sem1_approved)
        sem1_grade = np.where(sem1_approved == 0, 0.0, np.round(np.random.normal(9.8, 2.2, size=n_students), 1))

        sem2_enrolled = np.full(n_students, 6)
        sem2_approved = np.random.choice([0, 1, 2, 3, 4, 5, 6], size=n_students, p=[0.15, 0.25, 0.25, 0.18, 0.10, 0.05, 0.02])
        sem2_eval = sem2_enrolled + (sem2_enrolled - sem2_approved)
        sem2_grade = np.where(sem2_approved == 0, 0.0, np.round(np.random.normal(9.2, 2.4, size=n_students), 1))

    # Skenario 2: Waspada (Tingkat Risiko Menengah / 25% - 50%)
    elif scenario == "waspada":
        tuition = np.random.choice([1, 0], size=n_students, p=[0.75, 0.25])   # 25% menunggak SPP
        debtor = np.random.choice([0, 1], size=n_students, p=[0.82, 0.18])
        scholarship = np.random.choice([0, 1], size=n_students, p=[0.80, 0.20])
        age = np.random.randint(18, 24, size=n_students)
        adm_grade = np.round(np.random.normal(128, 8, size=n_students), 1)

        sem1_enrolled = np.full(n_students, 6)
        sem1_approved = np.random.choice([2, 3, 4, 5, 6], size=n_students, p=[0.05, 0.15, 0.35, 0.30, 0.15])
        sem1_eval = sem1_enrolled + (sem1_enrolled - sem1_approved)
        sem1_grade = np.round(np.random.normal(12.5, 1.6, size=n_students), 1)

        sem2_enrolled = np.full(n_students, 6)
        sem2_approved = np.random.choice([1, 2, 3, 4, 5, 6], size=n_students, p=[0.05, 0.15, 0.25, 0.30, 0.15, 0.10])
        sem2_eval = sem2_enrolled + (sem2_enrolled - sem2_approved)
        sem2_grade = np.round(np.random.normal(12.0, 1.8, size=n_students), 1)

    # Skenario 3: Stabil (Mayoritas Aman / < 25%)
    else:
        tuition = np.random.choice([1, 0], size=n_students, p=[0.92, 0.08])   # 92% lunas
        debtor = np.random.choice([0, 1], size=n_students, p=[0.92, 0.08])
        scholarship = np.random.choice([0, 1], size=n_students, p=[0.75, 0.25])
        age = np.random.randint(18, 22, size=n_students)
        adm_grade = np.round(np.random.normal(138, 10, size=n_students), 1)

        sem1_enrolled = np.full(n_students, 6)
        sem1_approved = np.random.choice([3, 4, 5, 6], size=n_students, p=[0.05, 0.15, 0.45, 0.35])
        sem1_eval = sem1_enrolled + (sem1_enrolled - sem1_approved)
        sem1_grade = np.round(np.random.normal(14.2, 1.5, size=n_students), 1)

        sem2_enrolled = np.full(n_students, 6)
        sem2_approved = np.random.choice([2, 3, 4, 5, 6], size=n_students, p=[0.03, 0.07, 0.25, 0.40, 0.25])
        sem2_eval = sem2_enrolled + (sem2_enrolled - sem2_approved)
        sem2_grade = np.round(np.random.normal(13.9, 1.6, size=n_students), 1)

    # Batasi agar nilai tetap berada pada skala valid (0-200 dan 0-20)
    adm_grade = np.clip(adm_grade, 95.0, 190.0)
    sem1_grade = np.clip(sem1_grade, 0.0, 20.0)
    sem2_grade = np.clip(sem2_grade, 0.0, 20.0)

    # Susun kolom identik dengan berkas acuan
    df_cohort = pd.DataFrame({
        'NIM': nims,
        'Nama_Mahasiswa': names,
        'Kelas': classes,
        'Age_at_enrollment': age,
        'Gender': gender,
        'Admission_grade': adm_grade,
        'Curricular_units_1st_sem_enrolled': sem1_enrolled,
        'Curricular_units_1st_sem_evaluations': sem1_eval,
        'Curricular_units_1st_sem_approved': sem1_approved,
        'Curricular_units_1st_sem_grade': sem1_grade,
        'Curricular_units_2nd_sem_enrolled': sem2_enrolled,
        'Curricular_units_2nd_sem_evaluations': sem2_eval,
        'Curricular_units_2nd_sem_approved': sem2_approved,
        'Curricular_units_2nd_sem_grade': sem2_grade,
        'Tuition_fees_up_to_date': tuition,
        'Debtor': debtor,
        'Scholarship_holder': scholarship
    })

    return df_cohort

if __name__ == "__main__":
    scenarios = [
        ("kritis", "data_angkatan_2024_kritis.csv"),
        ("waspada", "data_angkatan_2024_waspada.csv"),
        ("stabil", "data_angkatan_2024_stabil.csv")
    ]

    print("Membuat data angkatan sintetis...")
    for sc, filename in scenarios:
        df = generate_cohort(n_students=120, scenario=sc)
        df.to_csv(filename, index=False)
        print(f"-> Berkas '{filename}' berhasil dibuat ({len(df)} baris data - skenario {sc.upper()}).")
    
    print("\nSelesai! Berkas siap diunggah pada tab 'Pemindaian Angkatan (Batch Screening)'.")