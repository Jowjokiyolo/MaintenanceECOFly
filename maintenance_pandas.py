import pandas as pd
import numpy as np

def read_excel_to_df(filepath: str, size: int=None):          # Function to read a .xlsx file and transform it into a pandas DataFrame object.
    
    data = pd.read_excel(filepath, nrows=size)          # Pandas function to read file from an excel file.

    return data

SCHED = read_excel_to_df(r".Files/MPD.xlsx")

def structure_dataframe(data):
    return "under construction"