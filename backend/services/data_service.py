# backend/services/data_service.py
import pandas as pd
import os
import uuid
from config import Config
from utils.preprocessing import load_dataset

def save_uploaded_file(file):
    """
    Simpan file yang diupload, return filepath
    """
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
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