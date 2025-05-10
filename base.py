import pandas as pd
import numpy as np

# Function to insert row in the dataframe
def insert_row(row_number, df, row_value):
	df1 = df[0:row_number]

	df2 = df[row_number:]

	df1.loc[row_number]=row_value

	df_result = pd.concat([df1, df2])

	df_result.index = [*range(df_result.shape[0])]

	return df_result



def base_days(data: pd.DataFrame, men=6, job_hours=8):

    base_df = data.copy()

    for index, row in data.iterrows():
        day_hours    = row['Day Hours']
        day_men      = 0

        if row['Base']:
            row_value     = row
            days_required = int(np.ceil(day_hours/men/job_hours))
            for _ in range(days_required):
                base_df = insert_row(index, base_df, row_value)
            index += days_required

        else:
            day_men = int(np.ceil(day_hours / 3))
            base_df.at[index, 'Day Men'] = day_men


    return base_df
