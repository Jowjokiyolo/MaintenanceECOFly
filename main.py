import sys
import pandas as pd
import filter_functions
import calculations
import data_structure
from base import base_days



def read_excel_to_df(excel_file_path: str, size: int=None) -> pd.DataFrame:

    return pd.read_excel(excel_file_path, nrows=size)

    

def dataframe_to_file(dataframe: pd.DataFrame, xlsx = False) -> None:
    if xlsx:
        dataframe.to_excel('data.xlsx', index=False)
    else:
        dataframe.to_csv('data.csv', index=False)



def main(argc, argv) -> None:
    if argc < 2:
        print("Please specify a file")
        return FileNotFoundError
    elif argc != 2:
        print("Unexpected Number of Arguments")
        return ValueError
    file_path = argv[1]

    try: 
        raw_df = read_excel_to_df(file_path)
    except FileNotFoundError: 
        print(f"Error: File '{file_path}' not found.")
    except Exception as e: 
        print(f"Error reading file: {e}")

    structured_df        = data_structure.structure_dataframe(raw_df)
    filtered_df          = filter_functions.filter_ac(structured_df)
    maintenance_df       = calculations.daily_tasks(filtered_df)
    full_df              = calculations.day_hours(filtered_df, maintenance_df)
    look_ahead_df        = calculations.look_ahead(full_df)
    final_base_dataframe = base_days(look_ahead_df)
    dataframe_to_file(final_base_dataframe)



if __name__ == "__main__":
    main(len(sys.argv), sys.argv)