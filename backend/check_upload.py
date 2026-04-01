# backend/check_upload.py
import pandas as pd
import os

# Ganti dengan path file yang diupload (lihat dari log terminal)
filepath = r'C:\SKRIPSI\app\backend\uploads\e917a2826b10455ea25733e74e41d13d_dataset.xlsx'

print("="*50)
print("CHECKING UPLOADED FILE")
print("="*50)
print(f"File: {filepath}")
print(f"Exists: {os.path.exists(filepath)}")

try:
    # Coba baca file
    df = pd.read_excel(filepath, sheet_name=0)
    print(f"\nShape: {df.shape}")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nFirst 3 rows:")
    print(df.head(3))
    
    # Cek kolom yang diperlukan
    required = ['judul', 'skill_diekstrak', 'platform']
    missing = [col for col in required if col not in df.columns]
    if missing:
        print(f"\n❌ MISSING COLUMNS: {missing}")
    else:
        print("\n✅ All required columns found!")
        
        # Cek sample skills
        print(f"\nSample skills from first row:")
        print(df['skill_diekstrak'].iloc[0][:200])
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")