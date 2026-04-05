# backend/services/data_service.py
import pandas as pd
import os
from config import Config
import uuid

def load_dataset(filepath):
    ext = os.path.splitext(filepath)[1].lower()

    if ext == '.csv':
        df = pd.read_csv(filepath)
    elif ext in ['.xls', '.xlsx']:
        df = pd.read_excel(filepath)
    else:
        raise ValueError("Format file tidak didukung")

    # Normalisasi nama kolom
    df.columns = df.columns.str.strip().str.lower()

    # Validasi kolom wajib
    required_cols = ['judul', 'skill_diekstrak', 'platform']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Kolom '{col}' tidak ditemukan di dataset")

    return df


def save_uploaded_file(file):
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)

    # Biar nama file unik (penting!)
    filename = f"{uuid.uuid4()}_{file.filename}"
    filepath = os.path.join(upload_folder, filename)

    file.save(filepath)
    return filepath


def get_dataframe(file=None):
    """
    Dapatkan dataframe dari file upload atau dataset default
    """
    if file and file.filename:
        filepath = save_uploaded_file(file)
        df = load_dataset(filepath)
        return df, filepath
    else:
        df = load_dataset(Config.DEFAULT_DATASET)
        return df, Config.DEFAULT_DATASET