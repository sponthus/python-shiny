import seaborn as sns
from faicons import icon_svg

# Import data from shared.py
from shared import app_dir, df

from shiny import reactive
from shiny.express import input, render, ui

import pandas as pd

ui.page_opts(title="Vaccination dashboard", fillable=True)

df = pd.read_csv("donnees-de-vaccination-par-commune.csv", sep=";")

df["year"] = df["semaine_injection"].str.extract("^(\d{4})").astype(int)
df["week"] = df["semaine_injection"].str.extract("-(\d{2})").astype(int)
df["date_injection"] = pd.to_datetime(df["semaine_injection"] + "-1", format="%G-%V-%u")

list_cities = df["libelle_commune"].unique().tolist()
cleaned_list = [city for city in list_cities if pd.notna(city)]
list_cities = sorted(cleaned_list)

list_ages = ["TOUT_AGE", "00-19", "20-39", "40-54", "55-64", "65-74", "75 et +"]

# TODO = Apply data treatment in other file to complete missing values

@reactive.Effect
def age_filter():
    selected = input.age()

    if "TOUT_AGE" in selected and len(selected) > 1:
        selected = [a for a in selected if a != "TOUT_AGE"]
        ui.update_selectize("age", selected=selected)
        ui.notification_show("Invalid selection : \"TOUT_AGE\" cannot be combined with another age group")

with ui.sidebar(title="Filtering"):
    ui.input_slider("time", "Time", df["date_injection"].min(), df["date_injection"].max(), df["date_injection"].median())
    
    ui.input_checkbox_group(
        "age",
        "Age",
        list_ages,
        selected=["TOUT_AGE"]
    )

# TODO = Better system ? Too many choices ...
    ui.input_checkbox_group(
        "city",
        "City",
        list_cities,
        selected=["CASSIS", "PEYNIER", "SEVRES"],
    )


with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("syringe")):
        "Number of fully vaccinated people"

        @render.text
        def count_full():
            if "TOUT_AGE" in input.age():
                return filtered_df().groupby("libelle_commune")["effectif_cumu_termine"].max().sum()
            else:
                return filtered_df().groupby("libelle_commune", "classe_age")["effectif_cumu_termine"].max().sum()

    with ui.value_box(showcase=icon_svg("heart")):
        "Number of people with 1 shot"

        def count_partial():
            if "TOUT_AGE" in input.age():
                return filtered_df().groupby("libelle_commune")["effectif_cumu_1_inj"].max().sum()
            else:
                return filtered_df().groupby("libelle_commune", "classe_age")["effectif_cumu_1_inj"].max().sum()

        def count_rate():
            if "TOUT_AGE" in input.age():
                return filtered_df().groupby("libelle_commune")["taux_cumu_1_inj"].max().sum()
            else:
                return filtered_df().groupby("libelle_commune", "classe_age")["taux_cumu_1_inj"].max().sum()
        
        # TODO = Figure out how to show 2 data in 1 block
        @render.text
        def show_results():
            partial = count_partial()
            rate = count_rate()

            return "{patial}\n{rate:.1f}\% of population"
        

    with ui.value_box(showcase=icon_svg("percent")):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"


with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Bill length and depth")

# TODO = Render a plot through time and age classes

        # @render.plot
        # def length_depth():
        #     return sns.scatterplot(
        #         data=filtered_df(),
        #         x="bill_length_mm",
        #         y="bill_depth_mm",
        #         hue="species",
        #     )

    with ui.card(full_screen=True):
        ui.card_header("Vaccination data")

        @render.data_frame
        def summary_statistics():
            cols = [
                "semaine_injection",
                "commune_residence",
                "libelle_commune",
                "libelle_classe_age",
                "effectif_cumu_1_inj",
                "effectif_cumu_termine",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


ui.include_css(app_dir / "styles.css")

# TODO = Chose other columns to display ?
@reactive.calc
def filtered_df():
    filt_df = df[df["libelle_commune"].isin(input.city())]
    filt_df = filt_df.loc[filt_df["classe_age"].isin(input.age())]
    filt_df = filt_df.loc[filt_df["date_injection"] < input.time()]
    return filt_df
