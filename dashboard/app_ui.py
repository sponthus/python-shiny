from shiny import ui
from shared import df, sorted_list, list_ages
from faicons import icon_svg

def app_ui():
	return ui.page_sidebar(
		ui.sidebar(
			ui.input_slider("time", "Time", 
				df["date_injection"].min(), 
				df["date_injection"].max(), 
				df["date_injection"].max(),
				ticks=True,
				time_format="%Y-%U"
			),
			ui.input_checkbox_group(
				"age",
				"Age",
				list_ages,
				selected=["TOUT_AGE"]
			),
			ui.input_checkbox_group(
				"city",
				"City",
				sorted_list,
				selected=["CASSIS", "PEYNIER", "SEVRES"],
			),
			title="Filtering",
		),
		ui.layout_column_wrap(
			ui.value_box(
				value=ui.output_text("show_results_full"),
				title="Number of fully vaccinated people",
				showcase=icon_svg("syringe"),
			),
			ui.value_box(
				value=ui.output_text("show_results_1_inj"),
				title="Number of people with 1 shot",
				showcase=icon_svg("heart"),
			),
			ui.value_box(
				value=ui.output_text("show_total_population"),
				title="Total population",
				showcase=icon_svg("person"),
			),
			width=1/3,
		),
		ui.tags.div(style="height: 30px;"),
		ui.layout_column_wrap(
			ui.card(
				ui.card_header("Vaccination through time"),
				ui.input_select(
						"input_scheme",
						"Select vaccination scheme",
						choices=["effectif_cumu_1_inj", "effectif_cumu_termine"],
				),
				ui.input_switch(
						"age_class",
						"Show different age classes",
						value=True
				),
				ui.output_plot("render_vaccination_time"),
				full_screen=True,
			),
			ui.card(
				ui.card_header("Vaccination data"),
				ui.output_data_frame("summary_statistics"),
				full_screen=True,
			),
		),
	)