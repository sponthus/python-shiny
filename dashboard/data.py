import datetime
import pandas as pd
from pathlib import Path

app_dir = Path(__file__).parent
df = pd.read_csv(app_dir / "donnees-de-vaccination-par-commune.csv", sep=";")

print(df.head())

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

complete_data(df)
df.to_csv("modified-data.csv", index=False)