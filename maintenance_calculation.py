import pandas as pd
from maintenance_structure import read_excel_to_df, structure_dataframe
from filter_functions import filter_ac

def daily_tasks(data: pd.DataFrame, years=5):
    maintenance_df = pd.DataFrame(columns=['Day', 'Day Tasks', 'Day Men', 'Day Hours'])

    # Precompute intervals and group tasks by interval
    interval_groups = data.groupby('Interval')

    for day in range(1, years * 365 + 1):
        day_tasks = []
        for interval, group in interval_groups:
            if pd.notna(interval) and day % interval == 0:
                day_tasks.extend(group['Task Number'].tolist())

        if day_tasks:
            maintenance_df = pd.concat(
                [maintenance_df, pd.DataFrame({'Day': [day], 'Day Tasks': [day_tasks]})],
                ignore_index=True
            )
    maintenance_df.to_csv(r"goon.csv")
    return maintenance_df

GOON = read_excel_to_df(r".Files/MPD.xlsx")
STRUC = structure_dataframe(GOON)
FILTER = filter_ac(STRUC)
CUNNY = daily_tasks(FILTER)
print(CUNNY)