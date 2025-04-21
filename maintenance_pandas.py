import pandas as pd

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
        interval = str(df.loc[index, 'Interval']).split() # Specific for 'Interval'
        
        # Check if Interval variable is DAILY/WEEKLY or any other literal string.
        if len(interval) == 1:
            if interval[0].upper() == "DAILY": interval = 1

            elif interval[0].upper() == "WEEKLY": interval = 7

            else: interval = None

            df.at[index,'Interval'] = interval


        elif len(interval) > 1:
            match interval[1].upper():
                # Convert from Flight Hours (FH)
                case "FH":
                    interval = round(int(interval[0]) / hours)

                # Convert from APU Hours (AH)
                case "AH":
                    interval = int(interval[0]) * 2

                # Convert from Flight Cycles (FC)
                case "FC":
                    interval = int(interval[0])

                # Convert from Months (MO)
                case "MO":
                    interval = round(int(interval[0]) * 365 / 12)

                # Convert from Years (YR)
                case "YR":
                    interval = int(interval[0]) * 365

            # Append to DataFrame
            df.at[index, 'Interval'] = interval


    print(df['Interval'])
        

structure_dataframe(SCHEDULE)