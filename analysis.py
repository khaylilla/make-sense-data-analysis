"""Analisis performa akademik siswa berdasarkan dataset Students Performance in Exams.

Program ini membaca dataset CSV, melakukan data understanding dan cleaning,
melakukan analisis sederhana, menghasilkan visualisasi, serta menyimpan
hasilnya ke folder output/.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_DIR / "output"
REQUIRED_COLUMNS = {
    "gender",
    "race/ethnicity",
    "parental level of education",
    "lunch",
    "test preparation course",
    "math score",
    "reading score",
    "writing score",
}


def find_dataset_path() -> Path:
    """Cari dataset di folder utama project atau di subfolder data/."""
    candidates = [
        PROJECT_DIR / "StudentsPerformance.csv",
        PROJECT_DIR / "data" / "StudentsPerformance.csv",
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise FileNotFoundError(
        "File dataset tidak ditemukan. Harap pastikan file StudentsPerformance.csv ada di folder utama project atau di subfolder data/."
    )


def show_basic_overview(df: pd.DataFrame) -> None:
    """Tampilkan ringkasan umum data untuk tahap data understanding."""
    print("\n===== Data Understanding =====")
    print("\n5 baris pertama dataset:")
    print(df.head().to_string(index=False))

    print(f"\nJumlah baris: {df.shape[0]}")
    print(f"Jumlah kolom: {df.shape[1]}")

    print("\nTipe data:")
    print(df.dtypes.to_string())

    print("\nStatistik deskriptif:")
    print(df.describe(include="all").to_string())


def check_missing_and_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Periksa missing values dan duplikasi tanpa mengubah dataset asli."""
    cleaned = df.copy()

    print("\n===== Data Cleaning =====")
    missing_values = cleaned.isna().sum()
    print("\nMissing values per kolom:")
    print(missing_values.to_string())

    duplicate_count = cleaned.duplicated().sum()
    print(f"\nJumlah data duplikat: {duplicate_count}")

    # Penanganan missing values: gunakan median untuk kolom numerik.
    numeric_cols = ["math score", "reading score", "writing score"]
    for col in numeric_cols:
        if cleaned[col].isna().any():
            median_value = cleaned[col].median()
            cleaned[col] = cleaned[col].fillna(median_value)
            print(f"Kolom '{col}' memiliki missing value; diisi dengan median {median_value:.2f}.")

    if duplicate_count > 0:
        print("Duplikat ditemukan; data akan dihapus pada salinan analisis, bukan dataset asli.")
        cleaned = cleaned.drop_duplicates().copy()

    return cleaned


def validate_columns(df: pd.DataFrame) -> None:
    """Pastikan kolom penting tersedia."""
    missing_columns = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing_columns:
        raise ValueError(
            "Kolom yang diperlukan tidak tersedia: " + ", ".join(missing_columns)
        )


def create_average_score(df: pd.DataFrame) -> pd.DataFrame:
    """Buat kolom average_score berdasarkan tiga skor ujian."""
    processed = df.copy()
    processed["average_score"] = processed[["math score", "reading score", "writing score"]].mean(axis=1)
    return processed


def compute_summary_tables(df: pd.DataFrame):
    """Hitung ringkasan rata-rata berdasarkan test preparation course dan parental education."""
    prep_summary = (
        df.groupby("test preparation course", as_index=False)[["math score", "reading score", "writing score", "average_score"]]
        .mean()
        .round(2)
    )

    parental_summary = (
        df.groupby("parental level of education", as_index=False)[["math score", "reading score", "writing score", "average_score"]]
        .mean()
        .sort_values("average_score", ascending=False)
        .round(2)
    )

    correlation_matrix = df[["math score", "reading score", "writing score"]].corr().round(4)
    return prep_summary, parental_summary, correlation_matrix


def save_summary_csv(prep_summary: pd.DataFrame, parental_summary: pd.DataFrame, output_dir: Path) -> pd.DataFrame:
    """Simpan tabel ringkasan ke file CSV agar mudah dibaca dan dipelajari."""
    summary_table = pd.concat(
        [
            prep_summary.assign(kategori="test preparation course"),
            parental_summary.assign(kategori="parental level of education"),
        ],
        ignore_index=True,
    )
    summary_path = output_dir / "summary.csv"
    summary_table.to_csv(summary_path, index=False)
    print(f"\nTabel ringkasan disimpan ke: {summary_path}")
    return summary_table


def plot_preparation_course(df: pd.DataFrame, output_dir: Path) -> None:
    """Buat grafik batang untuk membandingkan rata-rata skor berdasarkan test preparation course."""
    grouped = (
        df.groupby("test preparation course", as_index=False)["average_score"]
        .mean()
        .sort_values("average_score", ascending=False)
        .round(2)
    )

    plt.figure(figsize=(8, 5))
    sns.barplot(
        data=grouped,
        x="test preparation course",
        y="average_score",
        hue="test preparation course",
        palette="Set2",
        dodge=False,
        legend=False,
    )
    plt.title("Rata-rata Nilai Berdasarkan Test Preparation Course")
    plt.xlabel("Test Preparation Course")
    plt.ylabel("Rata-rata Nilai")
    plt.tight_layout()
    plt.savefig(output_dir / "preparation_course.png", dpi=300)
    plt.close()


def plot_parental_education(df: pd.DataFrame, output_dir: Path) -> None:
    """Buat grafik batang untuk membandingkan rata-rata skor berdasarkan pendidikan orang tua."""
    grouped = (
        df.groupby("parental level of education", as_index=False)["average_score"]
        .mean()
        .sort_values("average_score", ascending=False)
        .round(2)
    )

    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=grouped,
        x="average_score",
        y="parental level of education",
        hue="parental level of education",
        palette="Blues_d",
        dodge=False,
        legend=False,
    )
    plt.title("Rata-rata Nilai Berdasarkan Pendidikan Orang Tua")
    plt.xlabel("Rata-rata Nilai")
    plt.ylabel("Pendidikan Orang Tua")
    plt.tight_layout()
    plt.savefig(output_dir / "parental_education.png", dpi=300)
    plt.close()


def plot_correlation(df: pd.DataFrame, output_dir: Path) -> None:
    """Buat heatmap korelasi antarnilai matematis, membaca, dan menulis."""
    corr = df[["math score", "reading score", "writing score"]].corr()

    plt.figure(figsize=(7, 5))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Korelasi Antarnilai")
    plt.tight_layout()
    plt.savefig(output_dir / "score_correlation.png", dpi=300)
    plt.close()


def write_insight(prep_summary: pd.DataFrame, parental_summary: pd.DataFrame, corr_matrix: pd.DataFrame, output_dir: Path) -> str:
    """Buat insight dari hasil analisis yang benar-benar dihasilkan program."""
    prep_by_group = prep_summary.set_index("test preparation course")
    parent_by_group = parental_summary.set_index("parental level of education")

    prep_completed = float(prep_by_group.loc["completed", "average_score"])
    prep_none = float(prep_by_group.loc["none", "average_score"])

    highest_parent = parent_by_group.iloc[0]
    lowest_parent = parent_by_group.iloc[-1]

    corr_flat = corr_matrix.where(~pd.DataFrame(np.eye(len(corr_matrix), dtype=bool), index=corr_matrix.index, columns=corr_matrix.columns)).stack()
    corr_flat = corr_flat[corr_flat.index.map(lambda x: x[0] != x[1])]
    strongest_pair = corr_flat.abs().idxmax()
    strongest_corr = float(corr_matrix.loc[strongest_pair[0], strongest_pair[1]])

    insight = (
        "Insight Analisis Performa Akademik Siswa\n"
        "====================================\n"
        f"1. Rata-rata nilai gabungan (average_score) pada kelompok dengan test preparation course 'completed' adalah {prep_completed:.2f}, "
        f"sedangkan kelompok 'none' adalah {prep_none:.2f}.\n"
        f"2. Rata-rata nilai gabungan tertinggi berdasarkan pendidikan orang tua terjadi pada '{highest_parent.name}' yaitu {highest_parent['average_score']:.2f}. "
        f"Rata-rata terendah terjadi pada '{lowest_parent.name}' yaitu {lowest_parent['average_score']:.2f}.\n"
        f"3. Korelasi paling kuat di antara skor matematika, membaca, dan menulis adalah antara '{strongest_pair[0]}' dan '{strongest_pair[1]}' dengan nilai {strongest_corr:.2f}.\n\n"
        "Catatan: hasil ini menunjukkan pola asosiasi dalam data, bukan bukti sebab-akibat. Perbedaan rata-rata dan korelasi perlu diinterpretasikan "
        "secara hati-hati dan tetap didukung konteks data serta analisis lanjutan jika diperlukan."
    )

    output_path = output_dir / "insight.txt"
    with output_path.open("w", encoding="utf-8") as file:
        file.write(insight)

    print(f"\nInsight disimpan ke: {output_path}")
    return insight


def main() -> None:
    """Fungsi utama program."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    try:
        dataset_path = find_dataset_path()
    except FileNotFoundError as exc:
        print(exc)
        sys.exit(1)

    print(f"Dataset ditemukan di: {dataset_path}")

    try:
        df = pd.read_csv(dataset_path)
        validate_columns(df)
        show_basic_overview(df)
        cleaned_df = check_missing_and_duplicates(df)
        processed_df = create_average_score(cleaned_df)

        print("\n===== Data Processing =====")
        print(processed_df[["math score", "reading score", "writing score", "average_score"]].head().to_string(index=False))

        prep_summary, parental_summary, corr_matrix = compute_summary_tables(processed_df)
        print("\nRingkasan rata-rata berdasarkan test preparation course:")
        print(prep_summary.to_string(index=False))

        print("\nRingkasan rata-rata berdasarkan parental level of education:")
        print(parental_summary.to_string(index=False))

        print("\nMatriks korelasi antar nilai:")
        print(corr_matrix.to_string())

        plot_preparation_course(processed_df, OUTPUT_DIR)
        plot_parental_education(processed_df, OUTPUT_DIR)
        plot_correlation(processed_df, OUTPUT_DIR)

        save_summary_csv(prep_summary, parental_summary, OUTPUT_DIR)
        write_insight(prep_summary, parental_summary, corr_matrix, OUTPUT_DIR)

        print("\nSemua file grafik dan ringkasan berhasil dibuat dalam folder output/.")

    except ValueError as exc:
        print(f"\nError validasi data: {exc}")
        sys.exit(1)
    except Exception as exc:  # pragma: no cover - penanganan error umum
        print(f"\nTerjadi kesalahan: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
