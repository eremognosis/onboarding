import pandas as pd
import numpy as np
import re, os
PATH = "./Data/csvs"
CLEANPATH = "./cleaneddata"

os.makedirs(CLEANPATH, exist_ok=True)

####### dta loaded

df0 = pd.read_csv(f"{PATH}/Resume.csv")
df1 = pd.read_csv(f"{PATH}/job_title_des.csv")
df2 = pd.read_excel(f"{PATH}/Knowledge.xlsx")
df3 = pd.read_excel(f"{PATH}/Skills.xlsx")
df4 = pd.read_excel(f"{PATH}/tskills.xlsx")

##############
### doitn the dold pnes

df0.drop(columns='Resume_html', inplace=True)

#############

def getoverview(df:pd.DataFrame):
    # df.
    print("-"*30)
    print("Basic dhape")
    print("-*30")
    r,c = df.shape
    print(f"Rows:    {r:,}")
    print(f"Columns: {c:,}")
    print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"Duplicates: {df.duplicated().sum()} rows")
    
    print("-"*30)
    print("Col Integrity")  
    
    integrity = pd.DataFrame({
        'Dtype': df.dtypes,
        'Nulls': df.isnull().sum(),
        'Null %': (df.isnull().sum() / r * 100).round(2),
        'Unique': df.nunique(),
        'Entropy (Uniqueness %)': (df.nunique() / r * 100).round(2)
    })
    print(integrity)
    
    print("CATEGORICAL ANALYSIS")
    print("-" * 30)
    cat_df = df.select_dtypes(include=['object', 'category', 'bool']) #### meow
    if not cat_df.empty:
        for col in cat_df.columns:
            top_val = cat_df[col].mode().iloc[0] if not cat_df[col].mode().empty else "N/A"
            freq = cat_df[col].value_counts().iloc[0] if len(cat_df[col].value_counts()) > 0 else 0
            print(f"{col}: {df[col].nunique()} uniques | Mode: {top_val} ({freq} hits)")
    else:
        print("No categorical columns detected.")
    
    
    print(" 1 RANDOM smple")
    print(df.sample(n=1))
    
# 
# 
# 
# getoverview(df3)


# print(f"OVERVIEWS")
# getoverview(df0)
# getoverview(df1)
# getoverview(df2)
# getoverview(df3)
# getoverview(df4)
### we doibnt nee dit to be printed every tuesadya



#######

def clean(text:str) ->str:
    if not isinstance(text, str): return ""
    
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+',' ', text)
    perks = [r"Benefits:.*", r"Job Type:.*", r"Schedule:.*", r"Salary:.*"]
    for p in perks:
        text = re.sub(p, '', text, flags=re.IGNORECASE | re.DOTALL)
    return text.strip()


df0 = df0.drop_duplicates(subset=['Resume_str']).dropna(subset=['Resume_str'])
df0['Resume_str'] = df0['Resume_str'].apply(clean)

df1 = df1.drop(columns=['Unnamed: 0'], errors='ignore')
df1 = df1.drop_duplicates(subset=['Job Description']).dropna(subset=['Job Description'])
df1['Job Description'] = df1['Job Description'].apply(clean)



def refine(df:pd.DataFrame)->pd.DataFrame:
    df = df[df['Scale ID'] == 'IM'].copy()
    if 'Not Relevant' in df.columns:
        df = df[df['Not Relevant'] != 'Y']
    nec = ['O*NET-SOC Code', 'Title', 'Element Name', 'Data Value']
    return df[nec].sort_values(by=['O*NET-SOC Code','Data Value'])

df2c = refine(df2)
df3c = refine(df3)

df4c = df4[['O*NET-SOC Code', 'Title', 'Example', 'Hot Technology', 'In Demand']].copy()
df4c['Example'] = df4c['Example'].str.strip()

print(f"OVERVIEWS  after clenaing")
getoverview(df0)
getoverview(df1)
getoverview(df2)
getoverview(df3)
getoverview(df4)

df0.to_csv(f"{CLEANPATH}/resume.csv")
df1.to_csv(f"{CLEANPATH}/jobdesc.csv")
df2c.to_csv(f"{CLEANPATH}/knowledge.csv")
df3c.to_csv(f"{CLEANPATH}/skills.csv")
df4c.to_csv(f"{CLEANPATH}/techskills.csv")