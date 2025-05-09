import pandas as pd
import numpy  as np

def daily_tasks(data: pd.DataFrame, years=5):
    maintenance_df = pd.DataFrame(columns=['Day', 'Day Tasks', 'Day Men', 'Day Hours'])

    interval_groups = data.groupby('Interval')

    for day in range(1, years * 365):
        day_tasks = []
        for interval, group in interval_groups:
            if pd.notna(interval) and day % interval == 0:
                day_tasks.extend(group['Task Number'].tolist())

        if day:
            new_row = pd.DataFrame([{
            'Day': day,
            'Day Tasks': day_tasks
            }])
            maintenance_df = pd.concat([maintenance_df, new_row], ignore_index=True)

    return maintenance_df



def day_hours(mpd: pd.DataFrame, daily_df: pd.DataFrame):

    merged_df = daily_df.copy()
    
    for index, row in daily_df.iterrows():
        day_tasks = row['Day Tasks']
        if not day_tasks:
            continue

        day_task_data = mpd[mpd['Task Number'].isin(day_tasks)]

        merged_df.at[index, 'Day Men']   = day_task_data['Men'].sum() if 'Men' in day_task_data else 0
        merged_df.at[index, 'Day Hours'] = day_task_data['M/H'].sum() if 'M/H' in day_task_data else 0
        merged_df.at[index, 'Day Men']   = np.max(merged_df.loc[index, 'Day Men'])
        merged_df.at[index, 'Day Hours'] = np.round(np.sum(merged_df.loc[index, 'Day Hours']), 2)

    return merged_df