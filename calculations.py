import pandas as pd
import numpy  as np


def daily_tasks(data: pd.DataFrame, years=5):
    maintenance_df = pd.DataFrame(columns=['Day', 'Day Tasks', 'Day Men', 'Day Hours', 'Base'])

    interval_groups = data.groupby('Interval')

    for day in range(1, years * 365):
        day_tasks = []
        base = False
        for interval, group in interval_groups:
            if pd.notna(interval) and day % interval == 0:
                day_tasks.extend(group['Task Number'].tolist())
                if interval >= 365: base = True

        if day:
            new_row = pd.DataFrame([{
            'Day': day,
            'Day Tasks': day_tasks,
            'Base': base
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
        merged_df.at[index, 'Day Hours'] = np.sum(merged_df.loc[index, 'Day Hours'])

    return merged_df



def look_ahead(data: pd.DataFrame):

    smart_df = data.copy()
    max_index = len(data) - 1
    processed_indices = set()  # Keep track of days we've already processed

    for index, row in data.iterrows():
        # Skip if this day has already been processed
        if index in processed_indices:
            continue

        if data.loc[index, 'Base']:
            # This is the first day of base maintenance we've found
            consolidated_tasks = []
            consolidated_men = []
            consolidated_hours = []
            indices_to_process = []

            # Look ahead 365 days for other base maintenance
            for days_ahead in range(365):
                check_index = index + days_ahead
                if check_index > max_index:
                    break

                if data.loc[check_index, 'Base']:
                    # Add this day's maintenance to our consolidated lists
                    consolidated_tasks.append(data.loc[check_index, 'Day Tasks'])
                    consolidated_men.append(data.loc[check_index, 'Day Men'])
                    consolidated_hours.append(data.loc[check_index, 'Day Hours'])
                    indices_to_process.append(check_index)
                    processed_indices.add(check_index)

            # Add all consolidated maintenance to the first day
            smart_df.at[index, 'Day Tasks'] = consolidated_tasks
            smart_df.at[index, 'Day Men'] = np.max(consolidated_men) if consolidated_men else 0
            smart_df.at[index, 'Day Hours'] = np.sum(consolidated_hours) if consolidated_hours else 0

            # Clear maintenance from other days that were consolidated
            for clear_index in indices_to_process[1:]:  # Skip first index (that's our target day)
                smart_df.at[clear_index, 'Day Tasks'] = []
                smart_df.at[clear_index, 'Day Men'] = 0
                smart_df.at[clear_index, 'Day Hours'] = 0
                smart_df.at[clear_index, 'Base'] = False  # Set Base flag to False

    return smart_df