from pathlib import Path
import pandas as pd

app_dir = Path(__file__).parent
df = pd.read_csv(app_dir / "modified-data.csv", sep=",")

# Tests to handle side bar : transform str date to date format
# df["year"] = df["semaine_injection"].str.extract("^(\d{4})").astype(int)
# df["week"] = df["semaine_injection"].str.extract("-(\d{2})").astype(int)
# df["date_injection"] = df.apply(
#     lambda row: datetime.date.fromisocalendar(row["year"], row["week"], 1), axis=1
# )

list_ages = ["TOUT_AGE", "00-19", "20-39", "40-54", "55-64", "65-74", "75 et +"]

# Simpler way of transforming to a date
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