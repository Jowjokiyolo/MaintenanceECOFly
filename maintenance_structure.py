import pandas as pd
import numpy as np
from filter_functions import filter_interval_notes

def read_excel_to_df(excel_file_path: str, size: int=None) -> pd.DataFrame:        # Function to read a .xlsx file and transform it into a pandas DataFrame object.
    
    raw_dataframe = pd.read_excel(excel_file_path, nrows=size)                                # Pandas function to read file from an excel file.

    return raw_dataframe



def structure_dataframe(data: pd.DataFrame, hours: int=13.5) -> pd.DataFrame:

    # Access all rows of DataFrame Object
    for index, row in data.iterrows():

    # Convert interval variables into interval days    
        structured_interval = str(data.loc[index, 'Interval']).split() # Specific for 'Interval'
        
        # Check if Interval variable is DAILY/WEEKLY or any other literal string.
        if len(structured_interval) == 1:
            if    structured_interval[0].upper() == "DAILY":  structured_interval = 1

            elif  structured_interval[0].upper() == "WEEKLY": structured_interval = 7

            elif  structured_interval[0].upper() == "NOTE":   structured_interval = filter_interval_notes(row, index)

            else: structured_interval = None

            data.at[index,'Interval'] = structured_interval



        # Check if Interval variable is numerical
        elif len(structured_interval) > 1:
            match structured_interval[1].upper():
                # Convert from Flight Hours (FH)
                case "FH":
                    structured_interval = int(np.floor(int(structured_interval[0]) / hours))

                # Convert from APU Hours (AH)
                case "AH":
                    structured_interval = int(structured_interval[0]) * 2

                # Convert from Flight Cycles (FC)
                case "FC":
                    structured_interval = int(structured_interval[0])

                # Convert from Months (MO)
                case "MO":
                    structured_interval = int(np.floor(int(structured_interval[0]) * 365 / 12))

                # Convert from Years (YR)
                case "YR":
                    structured_interval = int(structured_interval[0]) * 365

                case _:
                    structured_interval = None

            # Append to DataFrame
            data.at[index, 'Interval'] = structured_interval



        # Change Manhour string into an array
        manhour = str(data.loc[index, 'M/H']).split()
        structured_manhour = []
        for manhour_value in manhour:

            # Structure the Manhour array
            value = float(manhour_value.replace('<','').replace(',',''))
            structured_manhour.append(value)
            data.at[index, 'M/H'] = structured_manhour



        # Change Men string into an array
        men = str(data.loc[index, 'Men']).split()
        structured_men = []
        for men_value in men:
            # Skip invalid or missing values
            if men_value.lower() == 'nan':
                continue

            # Structure no. Men array
            value = int(men_value.replace(',', ''))
            structured_men.append(value)
        data.at[index, 'Men'] = structured_men



        # Change Effectivity string into an array
        effectivity = str(data.loc[index, 'Effectivity']).split(',')
        structured_effectivity = []
        for effectivity_value in effectivity:

            # Structure for the Effectivity array
            structured_effectivity.append(effectivity_value)
            data.at[index,'Effectivity'] = structured_effectivity



    return data[['Task Number','Interval','Effectivity', 'Men', 'M/H']]
