# backend/utils/preprocessing.py
import pandas as pd

def load_dataset(filepath):
    """
    Load dataset dari file Excel (ambil sheet pertama)
    """
    df = pd.read_excel(filepath, sheet_name=0)
    return df

def prepare_skills(df):
    """
    Mengubah kolom skill_diekstrak menjadi list of tokens
    """
    skills_list = df['skill_diekstrak'].fillna('').apply(
        lambda x: [skill.strip().lower() for skill in str(x).split(',')] if x else []
    )
    return skills_list

def get_skill_string_corpus(df):
    """
    Mengubah list skills menjadi string untuk TF-IDF
    """
    skills_list = prepare_skills(df)
    text_corpus = [' '.join(skills) for skills in skills_list]
    return text_corpus