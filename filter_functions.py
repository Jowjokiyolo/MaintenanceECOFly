import pandas as pd
import re

# FUNCTION THAT FILTERS AWAY ANY TASKS THAT ARENT FOR THE FOKKER-MK0100
def filter_ac(data: pd.DataFrame):

    ret = pd.DataFrame(columns=data.columns)

    for index, row in data.iterrows():
        for i in data.loc[index,'Effectivity']:
            if re.search(r"ALL|\b(MK 0100)\b",str(i)):
                ret = pd.concat([ret, pd.DataFrame([row])], ignore_index=True)
                break

    return ret



def filter_interval_notes(data: pd.DataFrame, index):

    pattern = r"\b(\d{1,3}(?:\.\d{3})*)\s*(FH|YR|MO|FC|AH)\b"
    intervals = re.findall(pattern, data['Description'])

    if not intervals:
        return None

    def calculate_days(value, unit):
        value = float(value.replace('.', ''))  # Handle numbers with thousands separators

        if unit == "FH":
            return int(value / 13.5)           # Assuming 13.5 flight hours per day
        elif unit == "YR":
            return int(value * 365)
        elif unit == "MO":
            return int(value * 365 / 12)
        elif unit == "FC":
            return int(value)                  # Assuming 1 flight cycle equals 1 day
        elif unit == "AH":
            return int(value * 2)              # Assuming 2 APU hours per day

    returnable = None
    if len(intervals) == 1:
        for value, unit in intervals:
            returnable = calculate_days(value, unit)
    elif len(intervals) == 2:
        value1, unit1 = intervals[0]
        value2, unit2 = intervals[1]

        days1 = calculate_days(value1, unit1)
        days2 = calculate_days(value2, unit2)

        returnable = min(days1, days2)

    return returnable