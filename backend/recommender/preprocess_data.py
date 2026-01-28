import pandas as pd
import numpy as np

def process_data(data: pd.DataFrame) -> pd.DataFrame:
    # Replace invalid values
    data['ProdID'] = data['ProdID'].replace(-2147483648, np.nan)
    data['ID'] = data['ID'].replace(-2147483648, np.nan)

    # Convert to numeric
    data['ID'] = pd.to_numeric(data['ID'], errors='coerce')
    data['ProdID'] = pd.to_numeric(data['ProdID'], errors='coerce')

    # Drop invalid rows
    data = data.dropna(subset=['ID', 'ProdID'])
    data = data[(data['ID'] != 0) & (data['ProdID'] != 0)]

    data['ID'] = data['ID'].astype(int)
    data['ProdID'] = data['ProdID'].astype(int)

    # Clean Rating (OPTIONAL FIX #1)
    data['Rating'] = pd.to_numeric(data['Rating'], errors='coerce').fillna(0)
    data = data[data['Rating'] > 0]

    # ReviewCount
    data['ReviewCount'] = pd.to_numeric(
        data['ReviewCount'], errors='coerce'
    ).fillna(0).astype(int)

    # Drop unwanted column
    if 'Unnamed: 0' in data.columns:
        data.drop(columns=['Unnamed: 0'], inplace=True)

    # Fill text columns
    for col in ['Category', 'Brand', 'Description', 'Tags']:
        if col in data.columns:
            data[col] = data[col].fillna('')

    # Enrich Tags (OPTIONAL FIX #2)
    data['Tags'] = (
        data['Tags'] + ' ' +
        data['Brand'] + ' ' +
        data['Category'] + ' ' +
        data['Description']
    )

    # Fix ImageURL
    if 'ImageURL' in data.columns:
        data['ImageURL'] = (
            data['ImageURL']
            .astype(str)
            .str.split('|')
            .str[0]
        )

    return data.reset_index(drop=True)
