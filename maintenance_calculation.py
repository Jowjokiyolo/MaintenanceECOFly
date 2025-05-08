import pandas as pd

def daily_tasks(data: pd.DataFrame, years=5):
    maintenance_df = pd.DataFrame(columns=['Day', 'Day Tasks', 'Day Men', 'Day Hours'])

    # Precompute intervals and group tasks by interval
    interval_groups = data.groupby('Interval')

    for day in range(1, years * 365 + 1):
        day_tasks = []
        for interval, group in interval_groups:
            if pd.notna(interval) and day % interval == 0:
                day_tasks.extend(group['Task Number'].tolist())


    return maintenance_df
