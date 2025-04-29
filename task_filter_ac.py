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