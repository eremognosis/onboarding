import pandas as pd


PATH = "./csvs"

df0 = pd.read_csv(f"{PATH}/Resume.csv")
df1 = pd.read_csv(f"{PATH}/job_title_des.csv")
df2 = pd.read_excel(f"{PATH}/")