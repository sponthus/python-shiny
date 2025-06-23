from shiny import reactive, render, ui
import seaborn as sb
import matplotlib.pyplot as plt
from shared import df
# from ridgeplot import ridgeplot

def app_server(input, output, session):

	@reactive.calc
	def filtered_df():
		filt_df = df[df["libelle_commune"].isin(input.city())]
		filt_df = filt_df.loc[filt_df["classe_age"].isin(input.age())]
		filt_df = filt_df.loc[filt_df["date_injection"] < input.time()]
		return filt_df

	# Results for complete vaccination box
	@render.text
	def show_results_full():
		def count_full():
			if "TOUT_AGE" in input.age():
				return filtered_df().groupby("libelle_commune")["effectif_cumu_termine"].max().sum()
			else:
				return filtered_df().groupby(["libelle_commune", "classe_age"])["effectif_cumu_termine"].max().sum()
		
		if "TOUT_AGE" in input.age():
			pop = filtered_df().groupby("libelle_commune")["population_carto"].max().sum()
		else:
			pop = filtered_df().groupby(["libelle_commune", "classe_age"])["population_carto"].max().sum()
		
		partial = count_full()
		if (pop == 0):
			rate = 0
		else:
			rate = (partial / pop) * 100
		return f"{partial} ({rate:.1f}%)"

	# Results for 1 injection box
	@render.text
	def show_results_1_inj():
		def count_partial():
			if "TOUT_AGE" in input.age():
				return filtered_df().groupby("libelle_commune")["effectif_cumu_1_inj"].max().sum()
			else:
				return filtered_df().groupby(["libelle_commune", "classe_age"])["effectif_cumu_1_inj"].max().sum()

		if "TOUT_AGE" in input.age():
			pop = filtered_df().groupby("libelle_commune")["population_carto"].max().sum()
		else:
			pop =filtered_df().groupby(["libelle_commune", "classe_age"])["population_carto"].max().sum()
		
		partial = count_partial()
		if (pop == 0):
			rate = 0
		else:
			rate = (partial / pop) * 100
		return f"{partial} ({rate:.1f}%)"

	@render.text
	def show_total_population():
		if "TOUT_AGE" in input.age():
			count = filtered_df().groupby("libelle_commune")["population_carto"].max().sum()
		else:
			count =filtered_df().groupby(["libelle_commune", "classe_age"])["population_carto"].max().sum()
		return f"{count} people selected"

	@render.text
	def bill_depth():
		return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

	@reactive.Effect
	def age_filter():
		selected = input.age()
		if "TOUT_AGE" in selected and len(selected) > 1:
			selected = [a for a in selected if a != "TOUT_AGE"]
			ui.update_selectize("age", selected=selected)
			ui.notification_show('Invalid selection: "TOUT_AGE" cannot be combined with another age group')

	#Visualize raw data
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

	# Dynamic plot
	@render.plot
	def render_vaccination_time():
		df = filtered_df()
		scheme = input.input_scheme() #Choice
		show_by_age = input.age_class() #switch

		if show_by_age:
			# Group by date and age class
			df_grouped = (
				df.groupby(["date_injection", "classe_age"], as_index=False)[scheme]
				.sum()
				.sort_values("date_injection")
			)
		else:
			# Group by date only
			df_grouped = (
				df.groupby("date_injection", as_index=False)[scheme]
				.sum()
				.sort_values("date_injection")
			)

		plt.figure(figsize=(10, 5))
		if show_by_age:
			sb.lineplot(data=df_grouped, x="date_injection", y=scheme, hue="classe_age")
		else:
			sb.lineplot(data=df_grouped, x="date_injection", y=scheme)

		plt.xlabel("Date")
		plt.ylabel("Number of people")
		plt.xticks(rotation=45)