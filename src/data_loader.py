import pandas as pd

def load_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path, sep=';')
    return df

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    
    data['parent_edu'] = (data['Medu'] + data['Fedu']) / 2.0
    
    data['parent_edu_group'] = pd.cut(
        data['parent_edu'],
        bins=[-0.1, 1.5, 2.5, 4.1],
        labels=['Low', 'Normal', 'High']
    )
    
    data['total_alc'] = data['Dalc'] + data['Walc']
    
    data['passed'] = data['G3'].apply(lambda x: 1 if x >= 10 else 0)
    
    return data