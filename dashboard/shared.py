from pathlib import Path
import datetime
import pandas as pd

app_dir = Path(__file__).parent
# df = pd.read_csv(app_dir / "donnees-de-vaccination-par-commune.csv", sep=";") # Final mode
df = pd.read_csv(app_dir / "modified-data.csv", sep=",") # Dev mode

# print(df.head())

# Tests to handle side bar : transform str date to date format
# df["year"] = df["semaine_injection"].str.extract("^(\d{4})").astype(int)
# df["week"] = df["semaine_injection"].str.extract("-(\d{2})").astype(int)
# df["date_injection"] = df.apply(
#     lambda row: datetime.date.fromisocalendar(row["year"], row["week"], 1), axis=1
# )

list_ages = ["TOUT_AGE", "00-19", "20-39", "40-54", "55-64", "65-74", "75 et +"]

df["date_injection"] = pd.to_datetime(df["semaine_injection"] + "-1", format="%G-%V-%u")

min_date = df["date_injection"].min()
max_date = df["date_injection"].max()

# # print(df[["semaine_injection", "date_injection"]].head())

# #Tests to sort list of cities
list_cities = df["libelle_commune"].unique().tolist()

cleaned_list = [city for city in list_cities if pd.notna(city)]
sorted_list = sorted(cleaned_list)

# print(list_cities)

# Cleaning data : deduce missing data

# Drop lines without any data
df = df.dropna(subset=['taux_1_inj', 'taux_termine',\
     'taux_cumu_1_inj', 'taux_cumu_termine', \
        'effectif_cumu_1_inj', 'effectif_cumu_termine', \
            'effectif_termine', 'effectif_1_inj'], how='all')

# For incomplete data = deduce what we easily can
def complete_data(df):
    for i, row  in df.iterrows():
        population = row.get("population_carto")
        taux_1_inj = row.get("taux_1_inj")
        taux_termine = row.get("taux_termine")
        effectif_1_inj = row.get("effectif_1_inj")
        effectif_termine = row.get("effectif_termine")
        taux_cumu_termine = row.get("taux_cumu_termine")
        taux_cumu_1_inj = row.get("taux_cumu_1_inj")
        effectif_cumu_1_inj = row.get("effectif_cumu_1_inj")
        effectif_cumu_termine = row.get("effectif_cumu_termine")

        if (pd.isna(taux_1_inj) and not pd.isna(effectif_1_inj)):
            taux_1_inj = effectif_1_inj / population
        elif (pd.isna(effectif_1_inj) and not pd.isna(taux_1_inj)):
            effectif_1_inj = population * taux_1_inj
        
        if (pd.isna(taux_termine) and not pd.isna(effectif_termine)):
            taux_termine = effectif_termine / population
        elif (pd.isna(effectif_termine) and not pd.isna(taux_termine)):
            effectif_termine = population * taux_termine
        
        if (pd.isna(taux_cumu_termine) and not pd.isna(effectif_cumu_termine)):
            taux_cumu_termine = effectif_cumu_termine / population
        elif (pd.isna(effectif_cumu_termine) and not pd.isna(taux_cumu_termine)):
            effectif_cumu_termine = taux_cumu_termine * population
        
        if (pd.isna(taux_cumu_1_inj) and not pd.isna(effectif_cumu_1_inj)):
            taux_cumu_1_inj = effectif_cumu_1_inj / population
        elif (pd.isna(effectif_cumu_1_inj) and not pd.isna(taux_cumu_1_inj)):
            effectif_cumu_1_inj = taux_cumu_1_inj * population

        df.at[i, "taux_1_inj"] = taux_1_inj
        df.at[i, "effectif_1_inj"] = effectif_1_inj
        df.at[i, "taux_termine"] = taux_termine
        df.at[i, "effectif_termine"] = effectif_termine
        df.at[i, "taux_cumu_termine"] = taux_cumu_termine
        df.at[i, "effectif_cumu_termine"] = effectif_cumu_termine
        df.at[i, "taux_cumu_1_inj"] = taux_cumu_1_inj
        df.at[i, "effectif_cumu_1_inj"] = effectif_cumu_1_inj

# complete_data(df)
# df.to_csv("modified-data.csv", index=False)