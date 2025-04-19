import pandas as pd

def load_excel(filepath: str):
    data = pd.read_excel(filepath)

    headers = ['Task Number', 'Interval (Days)']
    task_data = data[headers]
    return task_data

SCHED = load_excel(r"sorted_maintenance_tasks.xlsx")
print(SCHED)