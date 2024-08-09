import os
import pandas as pd

state = ["California","Texas","Florida","New York"]
population = ["123","234","345636","23525"]

dict_state = {"state":state,"population":population}

df_state=pd.DataFrame.from_dict(dict_state)
print(df_state)

# df_state.to_csv('states.csv',index=False)
