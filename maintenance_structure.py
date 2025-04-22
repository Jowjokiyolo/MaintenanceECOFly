import pandas as pd
import numpy as np

def read_excel_to_df(filepath: str, size: int=None):        # Function to read a .xlsx file and transform it into a pandas DataFrame object.
    
    df = pd.read_excel(filepath, nrows=size)                # Pandas function to read file from an excel file.

    return df

SCHEDULE = read_excel_to_df(r".Files/MPD.xlsx", 10)

def structure_dataframe(data, hours: int=13.5):

    # Make argument 'data' a DataFrame Object
    df = pd.DataFrame(data)

    # Access all rows of DataFrame Object
    for index, row in df.iterrows():

    # Convert interval variables into interval days    
        structured_interval = str(df.loc[index, 'Interval']).split() # Specific for 'Interval'
        
        # Check if Interval variable is DAILY/WEEKLY or any other literal string.
        if len(structured_interval) == 1:
            if    structured_interval[0].upper() == "DAILY":  structured_interval = 1

            elif  structured_interval[0].upper() == "WEEKLY": structured_interval = 7

            else: structured_interval = None

            df.at[index,'Interval'] = structured_interval


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

            # Append to DataFrame
            df.at[index, 'Interval'] = structured_interval



        # Change Manhour string into an array
        manhour = str(df.loc[index, 'M/H']).split()
        structured_manhour = []
        for manhour_value in manhour:

            # Structure the Manhour array
            value = float(manhour_value.replace('<','').replace(',',''))
            structured_manhour.append(value)
            df.at[index, 'M/H'] = structured_manhour



        # Change Men string into an array
        men = str(df.loc[index, 'Men']).split()
        structured_men = []
        for men_value in men:

            # Structure no. Men array
            value = int(men_value.replace(',',''))
            structured_men.append(value)
            df.at[index, 'Men'] = structured_men



        # Change Effectivity string into an array
        effectivity = str(df.loc[index, 'Effectivity']).split()
        structured_effectivity = []
        for effectivity_value in effectivity:

            # Structure for the Effectivity array
            value = effectivity_value.replace(',','')
            structured_effectivity.append(value)
            df.at[index,'Effectivity'] = structured_effectivity



    return df
        
structure_dataframe(SCHEDULE)