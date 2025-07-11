import pandas as pd
import os

def save_to_excel(data, filename=None):
    """
    data: list of dicts
    filename: путь к файлу Excel (по умолчанию data/collected_data.xlsx)
    """
    if filename is None:
        filename = os.path.join("data", "collected_data.xlsx")
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    return filename
