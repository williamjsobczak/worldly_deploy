import dash
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np

import plotly.graph_objs as go

from dash import html, dcc
from dash import dash_table
from components.navbar import navbar
from components.footer import footer

import components.dropdown as dropdown
import ids
import functions
import data

# BLANK GLOBE MAP
blank_data = pd.DataFrame(columns=["lat", "lon"])

# Create a blank scatter geo plot
blank_globe_fig = px.scatter_geo(blank_data, lat="lat", lon="lon")

# COMPLEX QUERIES
query_string_complex_globe_1 = 'WITH countries_contributing_to_75_percent_of_global_CO2_emissions AS ( SELECT year, code, entity, CO2_emissions_metric_tons     FROM     (     SELECT cf1.year, entity, code, CO2_emissions_metric_tons,  SUM(CO2_emissions_metric_tons) over(PARTITION BY year ORDER BY CO2_emissions_metric_tons DESC) running_sum     FROM CarbonFootprint cf1     WHERE entity != \'World\'     ORDER BY CO2_emissions_metric_tons DESC     ) cf1 WHERE running_sum < (SELECT CO2_emissions_metric_tons*0.9 FROM CarbonFootprint WHERE entity = \'World\' AND year = cf1.year) )  SELECT year, code, entity country, (Electricity_from_coal_in_TWh + Electricity_fom_gas_in_TWh + Electricity_from_nuclear_in_TWh + Electricity_from_hydro_in_TWh + Electricity_from_solar_in_TWh + Electricity_from_oil_in_TWh + Electricity_from_wind_in_TWh) total_electricity_production_in_TWh, CO2_emissions_metric_tons,     Case         WHEN Electricity_from_coal_in_TWh > Electricity_fom_gas_in_TWh AND Electricity_from_coal_in_TWh > Electricity_from_nuclear_in_TWh AND Electricity_from_coal_in_TWh > Electricity_from_hydro_in_TWh AND Electricity_from_coal_in_TWh > Electricity_from_solar_in_TWh AND Electricity_from_coal_in_TWh > Electricity_from_oil_in_TWh AND Electricity_from_coal_in_TWh > Electricity_from_wind_in_TWh THEN \'Coal\'         WHEN Electricity_fom_gas_in_TWh > Electricity_from_coal_in_TWh AND Electricity_fom_gas_in_TWh > Electricity_from_nuclear_in_TWh AND Electricity_fom_gas_in_TWh > Electricity_from_hydro_in_TWh AND Electricity_fom_gas_in_TWh > Electricity_from_solar_in_TWh AND Electricity_fom_gas_in_TWh > Electricity_from_oil_in_TWh AND Electricity_fom_gas_in_TWh > Electricity_from_wind_in_TWh THEN \'Gas\'         WHEN Electricity_from_nuclear_in_TWh > Electricity_fom_gas_in_TWh AND Electricity_from_nuclear_in_TWh > Electricity_from_coal_in_TWh AND Electricity_from_nuclear_in_TWh > Electricity_from_hydro_in_TWh AND Electricity_from_nuclear_in_TWh > Electricity_from_solar_in_TWh AND Electricity_from_nuclear_in_TWh > Electricity_from_oil_in_TWh AND Electricity_from_nuclear_in_TWh > Electricity_from_wind_in_TWh THEN \'Nuclear\'         WHEN Electricity_from_hydro_in_TWh > Electricity_fom_gas_in_TWh AND Electricity_from_hydro_in_TWh > Electricity_from_nuclear_in_TWh AND Electricity_from_hydro_in_TWh > Electricity_from_coal_in_TWh AND Electricity_from_hydro_in_TWh > Electricity_from_solar_in_TWh AND Electricity_from_hydro_in_TWh > Electricity_from_oil_in_TWh AND Electricity_from_hydro_in_TWh > Electricity_from_wind_in_TWh THEN \'Hydroelectric\'         WHEN Electricity_from_solar_in_TWh > Electricity_fom_gas_in_TWh AND Electricity_from_solar_in_TWh > Electricity_from_nuclear_in_TWh AND Electricity_from_solar_in_TWh > Electricity_from_hydro_in_TWh AND Electricity_from_solar_in_TWh > Electricity_from_coal_in_TWh AND Electricity_from_solar_in_TWh > Electricity_from_oil_in_TWh AND Electricity_from_solar_in_TWh > Electricity_from_wind_in_TWh THEN \'Solar\'         WHEN Electricity_from_oil_in_TWh > Electricity_fom_gas_in_TWh AND Electricity_from_oil_in_TWh > Electricity_from_nuclear_in_TWh AND Electricity_from_oil_in_TWh > Electricity_from_hydro_in_TWh AND Electricity_from_oil_in_TWh > Electricity_from_solar_in_TWh AND Electricity_from_oil_in_TWh > Electricity_from_coal_in_TWh AND Electricity_from_oil_in_TWh > Electricity_from_wind_in_TWh THEN \'Oil\'         WHEN Electricity_from_wind_in_TWh > Electricity_fom_gas_in_TWh AND Electricity_from_wind_in_TWh > Electricity_from_nuclear_in_TWh AND Electricity_from_wind_in_TWh > Electricity_from_hydro_in_TWh AND Electricity_from_wind_in_TWh > Electricity_from_solar_in_TWh AND Electricity_from_wind_in_TWh > Electricity_from_oil_in_TWh AND Electricity_from_wind_in_TWh > Electricity_from_coal_in_TWh THEN \'Wind\'         END AS primary_electricity_source FROM (     SELECT e.year, c.CO2_emissions_metric_tons, c.code, c.entity, Electricity_from_coal_in_TWh, Electricity_fom_gas_in_TWh, Electricity_from_nuclear_in_TWh, Electricity_from_hydro_in_TWh, Electricity_from_solar_in_TWh, Electricity_from_oil_in_TWh, Electricity_from_wind_in_TWh, Electricity_from_bioenergy_in_TWh, Other_renewables_excluding_bioenergy_in_TWh     FROM countries_contributing_to_75_percent_of_global_CO2_emissions c, ElectricityProductionBySource e     WHERE e.code = c.code AND e.year = c.year ) ORDER BY year'
query_string_complex_globe_2 = 'SELECT l.code, l.entity, l.year, life_expectancy_at_birth, life_expectancy_percentile, public_health_expenditure_percentage_of_gdp-avg_public_health_expenditure_percentage_of_gdp difference_in_public_health_expenditure_percentage_of_gdp_to_years_average FROM (     SELECT *     FROM     (     SELECT code, year, entity, life_expectancy_at_birth,  ROUND(PERCENT_RANK() OVER(PARTITION BY YEAR ORDER BY life_expectancy_at_birth),2) life_expectancy_percentile     FROM LifeExpectancy     ORDER BY year     )     WHERE life_expectancy_percentile > 0.9 ) l LEFT OUTER JOIN (SELECT code,year, public_health_expenditure_percentage_of_gdp, AVG(public_health_expenditure_percentage_of_gdp) OVER(PARTITION BY YEAR ORDER BY public_health_expenditure_percentage_of_gdp) avg_public_health_expenditure_percentage_of_gdp FROM PublicHealthGovExpenditureShareGDP) h ON (l.code = h.code AND l.year = h.year)   '
query_string_complex_globe_3 = 'SELECT RealGdpPerCapita.code, RealGdpPerCapita.entity, RealGdpPerCapita.year, GDP_per_capita, GDP_per_capita_percent_growth, Energy_consumption_per_capita_in_kwh - avg_Energy_consumption_per_capita_in_kwh difference_in_per_capita_energy_use_in_kwh_compared_to_the_yearly_average FROM (     SELECT RealGdpPerCapita.code, RealGdpPerCapita.entity, RealGdpPerCapita.year, GDP_per_capita, GDP_per_capita_percent_growth, max_real_gdp_per_capita_per_continent_and_year     FROM     (         SELECT RealGdpPerCapita.code, RealGdpPerCapita.entity, RealGdpPerCapita.year, GDP_per_capita, MAX(GDP_per_capita) OVER(PARTITION BY continent, RealGdpPerCapita.year) max_real_gdp_per_capita_per_continent_and_year         FROM RealGdpPerCapita, Continents         WHERE RealGdpPerCapita.code = Continents.code     ) RealGdpPerCapita     LEFT OUTER JOIN GdpPerCapitaGrowth ON (GdpPerCapitaGrowth.code = RealGdpPerCapita.code AND GdpPerCapitaGrowth.year = RealGdpPerCapita.year)     WHERE GDP_per_capita = max_real_gdp_per_capita_per_continent_and_year ) RealGDPPerCapita LEFT OUTER JOIN  ( SELECT EnergyPerPerson.code, EnergyPerPerson.year, Energy_consumption_per_capita_in_kwh, AVG(Energy_consumption_per_capita_in_kwh) OVER(PARTITION BY EnergyPerPerson.YEAR, continent) avg_Energy_consumption_per_capita_in_kwh  FROM EnergyPerPerson JOIN Continents ON (Continents.code = EnergyPerPerson.code) ) EnergyPerPerson  ON RealGDPPerCapita.code = EnergyPerPerson.code AND RealGDPPerCapita.year = EnergyPerPerson.year ORDER BY YEAR'
query_string_complex_globe_4 = 'SELECT GNI.entity, GNI.code, GNI.year, (GNI_index_contribution + life_expectancy_index_contribution + primary_education_index_contribution + secondary_education_index_contribution + tertiary_education_index_contribution) HDI_index FROM     (     SELECT entity, code, year, (gross_national_income_per_capita/max_GNI_per_capita)/3 GNI_index_contribution     FROM         (         SELECT entity, code, year, gross_national_income_per_capita, MAX(gross_national_income_per_capita) OVER(PARTITION BY YEAR) max_GNI_per_capita         FROM GrossNationalIncomePerCapita         )     ) GNI,               (        SELECT entity, code, year, (life_expectancy_at_birth/max_life_expectancy)/3 life_expectancy_index_contribution     FROM         (         SELECT entity, code, year, life_expectancy_at_birth, MAX(life_expectancy_at_birth) OVER(PARTITION BY YEAR) max_life_expectancy         FROM LifeExpectancy         )              ) LifeExpectancy,                  (             SELECT entity, code, year, (primary_education_gross_enrollment_percent/max_primary_education_gross_enrollment_percent)/9 primary_education_index_contribution     FROM         (         SELECT entity, code, year, primary_education_gross_enrollment_percent, MAX(primary_education_gross_enrollment_percent) OVER(PARTITION BY YEAR) max_primary_education_gross_enrollment_percent         FROM GrossEnrollmentRatioInPrimaryEducation         )     ) primary,                  (         SELECT entity, code, year, (secondary_education_gross_enrollment_percent/max_secondary_education_gross_enrollment_percent)/9 secondary_education_index_contribution     FROM         (         SELECT entity, code, year, secondary_education_gross_enrollment_percent, MAX(secondary_education_gross_enrollment_percent) OVER(PARTITION BY YEAR) max_secondary_education_gross_enrollment_percent         FROM GrossEnrollmentRatioInSecondaryEducation         )     ) secondary,              (     SELECT entity, code, year, (percentage_with_tertiary_education/max_percentage_with_tertiary_education)/9 tertiary_education_index_contribution     FROM         (         SELECT entity, code, year, percentage_with_tertiary_education, MAX(percentage_with_tertiary_education) OVER(PARTITION BY YEAR) max_percentage_with_tertiary_education         FROM ShareOfThePopulationWithCompletedTertiaryEducation         )     ) tertiary WHERE GNI.code = LifeExpectancy.code AND GNI.year = LifeExpectancy.year AND GNI.code = primary.code AND GNI.year = primary.year AND GNI.code = secondary.code AND GNI.year = secondary.year AND GNI.code = tertiary.code AND GNI.year = tertiary.year ORDER BY year, hdi_index'
query_string_complex_globe_5 = ' WITH Energy AS (     SELECT entity, code, year, energy_consumption_per_capita_in_kwh - avg_energy_consumption_per_capita_in_kwh difference_in_energy_consumption_per_capita_in_kwh     FROM     (     SELECT Continents.entity, Continents.code, EnergyPerPerson.year, energy_consumption_per_capita_in_kwh, AVG(energy_consumption_per_capita_in_kwh) OVER(PARTITION BY EnergyPerPerson.year, continents.continent) avg_energy_consumption_per_capita_in_kwh     FROM EnergyPerPerson, Continents     WHERE EnergyPerPerson.code = Continents.code     ) ),  Forest AS (     SELECT entity, code, year, Forest_area_square_km - avg_Forest_area_square_km difference_in_forest_area_square_km     FROM     (     SELECT Continents.entity, Continents.code, ForestArea.year, Forest_area_square_km, AVG(Forest_area_square_km) OVER(PARTITION BY ForestArea.year, continents.continent) avg_Forest_area_square_km     FROM ForestArea, Continents     WHERE ForestArea.code = Continents.code     ) ),  Deforestation AS (     SELECT entity, code, year, Deforestation_square_km - avg_Deforestation_square_km difference_in_deforestation_square_km     FROM     (     SELECT Continents.entity, Continents.code, AnnualDeforestation.year, Deforestation_square_km, AVG(Deforestation_square_km) OVER(PARTITION BY AnnualDeforestation.year, continents.continent) avg_Deforestation_square_km     FROM AnnualDeforestation, Continents     WHERE AnnualDeforestation.code = Continents.code     ) ),  Obesity AS (     SELECT entity, code, year, Percent_of_adults_overweight - avg_Percent_of_adults_overweight difference_in_percent_of_adults_overweight     FROM     (     SELECT Continents.entity, Continents.code, ShareOfAdultsWhoAreOverweight.year, Percent_of_adults_overweight, AVG(Percent_of_adults_overweight) OVER(PARTITION BY ShareOfAdultsWhoAreOverweight.year, continents.continent) avg_Percent_of_adults_overweight     FROM ShareOfAdultsWhoAreOverweight, Continents     WHERE ShareOfAdultsWhoAreOverweight.code = Continents.code     ) ),  CO2 AS (     SELECT entity, code, year, CO2_emissions_metric_tons - avg_CO2_emissions_metric_tons difference_in_CO2_emissions_metric_tons     FROM     (     SELECT Continents.entity, Continents.code, CarbonFootprint.year, CO2_emissions_metric_tons, AVG(CO2_emissions_metric_tons) OVER(PARTITION BY CarbonFootprint.year, continents.continent) avg_CO2_emissions_metric_tons     FROM CarbonFootprint, Continents     WHERE CarbonFootprint.code = Continents.code     ) ),  Literacy AS (     SELECT entity, code, year, literacy_rate - avg_literacy_rate difference_in_avg_literacy_rate     FROM     (     SELECT Continents.entity, Continents.code, CrossCountryLiteracyRates.year, literacy_rate, AVG(literacy_rate) OVER(PARTITION BY CrossCountryLiteracyRates.year, continents.continent) avg_literacy_rate     FROM CrossCountryLiteracyRates, Continents     WHERE CrossCountryLiteracyRates.code = Continents.code     ) )   SELECT TotalPopulationSize.entity, TotalPopulationSize.code, LandArea.year, land_area_in_square_km/total_population_size population_density, difference_in_energy_consumption_per_capita_in_kwh, difference_in_forest_area_square_km, difference_in_deforestation_square_km, difference_in_percent_of_adults_overweight, difference_in_CO2_emissions_metric_tons, difference_in_avg_literacy_rate FROM LandArea JOIN TotalPopulationSize ON (LandArea.code = TotalPopulationSize.code AND LandArea.year = TotalPopulationSize.year) LEFT OUTER JOIN Energy ON (LandArea.year = Energy.year AND LandArea.code = Energy.code) LEFT OUTER JOIN Forest ON (LandArea.year = Forest.year AND LandArea.code = Forest.code) LEFT OUTER JOIN Deforestation ON (LandArea.year = Deforestation.year AND LandArea.code = Deforestation.code) LEFT OUTER JOIN Obesity ON (LandArea.year = Obesity.year AND LandArea.code = Obesity.code) LEFT OUTER JOIN CO2 ON (LandArea.year = CO2.year AND LandArea.code = CO2.code) LEFT OUTER JOIN Literacy ON (LandArea.year = Literacy.year AND LandArea.code = Literacy.code ) WHERE land_area_in_square_km/total_population_size < 5 '

# Query the database and store the results in a dataframe
df_complex_1 = functions.query_db(query_string_complex_globe_1)
df_complex_2 = functions.query_db(query_string_complex_globe_2)
df_complex_3 = functions.query_db(query_string_complex_globe_3)
df_complex_4 = functions.query_db(query_string_complex_globe_4)
df_complex_5 = functions.query_db(query_string_complex_globe_5)


# ---------------------------------------------------------------------------------------------- FIX FIRST GLOBE ----------------------------------------------------------------------------------------------
unique_country_code_combos_1 = df_complex_1.groupby(['COUNTRY', 'CODE']).size().reset_index().drop(0, axis=1)
unique_country_code_combos_1.drop_duplicates()

# Append the new rows to the dataframe in a loop to fill in the missing years in complex_4
for index, row in unique_country_code_combos_1.iterrows():
    country = row['COUNTRY']
    code = row['CODE']
    new_row = {'YEAR': 1985, 'CODE': code, 'COUNTRY': country, 'TOTAL_ELECTRICITY_PRODUCTION_IN_TWH' : 0, 'CO2_EMISSIONS_METRIC_TONS': 0, 'PRIMARY_ELECTRICITY_SOURCE': 0}
    df_complex_1 = df_complex_1._append(new_row, ignore_index=True)
    # df_complex_1.fillna(0, inplace=True)

# ---------------------------------------------------------------------------------------------- FIX FIRST GLOBE ----------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------- FIX SECOND GLOBE ----------------------------------------------------------------------------------------------

# Get unique country code combinations from complex 2 dataframe
unique_country_code_combos_2 = df_complex_2.groupby(['ENTITY', 'CODE']).size().reset_index().drop(0, axis=1)
unique_country_code_combos_2.drop_duplicates()
# print(unique_country_code_combos_2.head(30))

# Append the new rows to the dataframe in a loop to fill in the missing years in complex_2
for index, row in unique_country_code_combos_2.iterrows():
    entity = row['ENTITY']
    code = row['CODE']
    new_row = {'YEAR': 1753, 'CODE': code, 'ENTITY': entity, 'LIFE_EXPECTANCY_AT_BIRTH': None, 'LIFE_EXPECTANCY_PERCENTILE': None, 'DIFFERENCE_IN_PUBLIC_HEALTH_EXPENDITURE_PERCENTAGE_OF_GDP_TO_YEARS_AVERAGE': None}
    df_complex_2 = df_complex_2._append(new_row, ignore_index=True)

# Fill all the NaN values with 0
df_complex_2.fillna(0, inplace=True)
# df_complex_2 = df_complex_2.sort_values(by='YEAR')
# print(df_complex_2.head(50))

# ---------------------------------------------------------------------------------------------- FIX SECOND GLOBE ----------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------- FIX THIRD GLOBE ----------------------------------------------------------------------------------------------

unique_country_code_combos_3 = df_complex_3.groupby(['ENTITY', 'CODE']).size().reset_index().drop(0, axis=1)
unique_country_code_combos_3.drop_duplicates()

# Append the new rows to the dataframe in a loop to fill in the missing years in complex_3
for index, row in unique_country_code_combos_3.iterrows():
    entity = row['ENTITY']
    code = row['CODE']
    new_row = {'YEAR': 1950, 'CODE': code, 'ENTITY': entity, 'GDP_PER_CAPITA': 0, 'GDP_PER_CAPITA_PERCENT_GROWTH': 0, 'DIFFERENCE_IN_PER_CAPITA_ENERGY_USE_IN_KWH_COMPARED_TO_THE_YEARLY_AVERAGE': 0}
    df_complex_3 = df_complex_3._append(new_row, ignore_index=True)
    # df_complex_3.fillna(0, inplace=True)
# ---------------------------------------------------------------------------------------------- FIX THIRD GLOBE ----------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------- FIX FOURTH GLOBE ----------------------------------------------------------------------------------------------

unique_country_code_combos_4 = df_complex_4.groupby(['ENTITY', 'CODE']).size().reset_index().drop(0, axis=1)
unique_country_code_combos_4.drop_duplicates()

# Append the new rows to the dataframe in a loop to fill in the missing years in complex_4
for index, row in unique_country_code_combos_4.iterrows():
    entity = row['ENTITY']
    code = row['CODE']
    new_row = {'YEAR': 1990, 'CODE': code, 'ENTITY': entity, 'HDI_INDEX' : 0}
    df_complex_4 = df_complex_4._append(new_row, ignore_index=True)
    # df_complex_4.fillna(0, inplace=True)

# ---------------------------------------------------------------------------------------------- FIX FOURTH GLOBE ----------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------- FIX FIFTH GLOBE ----------------------------------------------------------------------------------------------

unique_country_code_combos_5 = df_complex_5.groupby(['ENTITY', 'CODE']).size().reset_index().drop(0, axis=1)
unique_country_code_combos_5.drop_duplicates()

# Append the new rows to the dataframe in a loop to fill in the missing years in complex_4
for index, row in unique_country_code_combos_5.iterrows():
    entity = row['ENTITY']
    code = row['CODE']
    new_row = {'YEAR': 1961, 'CODE': code, 'ENTITY': entity, 'POPULATION_DENSITY': 0, 'DIFFERENCE_IN_ENERGY_CONSUMPTION_PER_CAPITA_IN_KWH': 0, 'DIFFERENCE_IN_FOREST_AREA_SQUARE_KM': 0, 'DIFFERENCE_IN_DEFORESTATION_SQUARE_KM': 0, 'DIFFERENCE_IN_PERCENT_OF_ADULTS_OVERWEIGHT' : 0, 'DIFFERENCE_IN_CO2_EMISSIONS_METRIC_TONS' : 0, 'DIFFERENCE_IN_AVG_LITERACY_RATE' : 0}
    df_complex_5 = df_complex_5._append(new_row, ignore_index=True)
    # df_complex_5.fillna(0, inplace=True)

# SORT FIFTH DF
df_complex_5 = df_complex_5.sort_values(by='YEAR')
# ---------------------------------------------------------------------------------------------- FIX FIFTH GLOBE ----------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------- FIRST GLOBE ----------------------------------------------------------------------------------------------

world_map_for_complex_1 = px.scatter_geo(df_complex_1, locations = 'CODE',
                    animation_frame='YEAR',
                    animation_group='COUNTRY',
                    color='COUNTRY',
                    hover_name='COUNTRY',
                    size='CO2_EMISSIONS_METRIC_TONS',
                    projection='orthographic',
                    hover_data={'COUNTRY': True, 'TOTAL_ELECTRICITY_PRODUCTION_IN_TWH': True, 'CO2_EMISSIONS_METRIC_TONS': True, 'CODE': False, 'PRIMARY_ELECTRICITY_SOURCE': True})
world_map_for_complex_1.update_layout(width=1250, height=800)

complex_1_map_section = html.Div(children=[
        html.H1("Countries Constituting the Majority of Global Greenhouse Gas Emissions along with their Total Electricity Generation Quantity (TWh) and Primary Source"),
        dcc.Graph(id='data-visualization', figure=world_map_for_complex_1),
        html.Br(),
        html.P(r"The map displays the countries which in combination constitute 90% of the world's Carbon Dioxide emissions in a particular year (i.e., the largest carbon polluters). Additionally, for each of those countries, the total CO2 emission for the particular is are displayed in metric tons, as is the total electricity production (of the country) in TWh and the primary source of electricity.")
], className="centered")

# ---------------------------------------------------------------------------------------------- FIRST GLOBE ----------------------------------------------------------------------------------------------




# ---------------------------------------------------------------------------------------------- SECOND GLOBE ----------------------------------------------------------------------------------------------

world_map_for_complex_2 = px.scatter_geo(df_complex_2, locations = 'CODE',
                    animation_frame='YEAR',
                    animation_group='ENTITY',
                    color='ENTITY',
                    hover_name='ENTITY',
                    size='LIFE_EXPECTANCY_AT_BIRTH',
                    projection='orthographic',
                    hover_data={'ENTITY': True, 'LIFE_EXPECTANCY_AT_BIRTH': True, 'LIFE_EXPECTANCY_PERCENTILE': True, 'CODE': False, 'DIFFERENCE_IN_PUBLIC_HEALTH_EXPENDITURE_PERCENTAGE_OF_GDP_TO_YEARS_AVERAGE': True})
world_map_for_complex_2.update_layout(width=1250, height=800)


complex_2_map_section = html.Div(children=[
        html.H1("Countries in the 90+ percentile for life expectancy for each year, along with the difference in their public health expenditure compared to the year's average"),
        dcc.Graph(id='data-visualization', figure=world_map_for_complex_2),
        html.Br(),
        html.P(r"The map displays countries in the 90+ percentile for life expectancy for each year, along with the difference in their public health expenditure compared to the year's average (as percent of GDP).")
], className="centered")

# ---------------------------------------------------------------------------------------------- SECOND GLOBE ----------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------- THIRD GLOBE ----------------------------------------------------------------------------------------------
world_map_for_complex_3 = px.scatter_geo(df_complex_3, locations = 'CODE',
                    animation_frame='YEAR',
                    animation_group='ENTITY',
                    color='ENTITY',
                    hover_name='ENTITY',
                    size='GDP_PER_CAPITA',
                    projection='orthographic',
                    hover_data={'ENTITY': True, 'GDP_PER_CAPITA': True, 'GDP_PER_CAPITA_PERCENT_GROWTH': True, 'CODE': False, 'DIFFERENCE_IN_PER_CAPITA_ENERGY_USE_IN_KWH_COMPARED_TO_THE_YEARLY_AVERAGE': True})
world_map_for_complex_3.update_layout(width=1250, height=800)


complex_3_map_section = html.Div(children=[
        html.H1("Country with Highest GDP Per Capita for each Continent along with Corresponding Percent Growth and Difference in Per Capita Energy Use Compared to the Continent's Average"),
        dcc.Graph(id='data-visualization', figure=world_map_for_complex_3),
        html.Br(),
        html.P(r"The map displays the country in each continent that has the highest real GDP per capita, along with the corresponding value (in 2016 USD) and the difference between its per capita energy use (in TWh) and that of the average of the year within the respective continent.")
], className="centered")
# ---------------------------------------------------------------------------------------------- THIRD GLOBE ----------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------- FOURTH GLOBE ----------------------------------------------------------------------------------------------

world_map_for_complex_4 = px.scatter_geo(df_complex_4, locations = 'CODE',
                    animation_frame='YEAR',
                    animation_group='ENTITY',
                    color='ENTITY',
                    hover_name='ENTITY',
                    size='HDI_INDEX',
                    projection='orthographic',
                    hover_data={'ENTITY': True, 'HDI_INDEX': True, 'CODE': False})
world_map_for_complex_4.update_layout(width=1250, height=800)



complex_4_map_section = html.Div(children=[
        html.H1("Human Development Index (HDI)"),
        dcc.Graph(id='data-visualization', figure=world_map_for_complex_4),
        html.Br(),
        html.P(r"Human Development Index (HDI) is a metric developed and employed by the World Health Organization (WHO) designed to summarize composite indicators for the developmental status of humans, most often applied to countries. It is a function of life expectancy at birth, mean number of years in schooling, and Gross Nataional Income (GNI) per capita. The worldy team has created a pseudo-HDI based on life expectancy at birth, GNI per capita, and percent of the population with primary, secondary, and tertiary educations. Each component is weighted equally, and the education subset is also weighted equally between the three education levels. The index generated is therefore a composite measure in the form of a decimal between 0 and 1, with indices near the lower bound denoting a low composite developmental score and indices near the upper bound denoting a high composite developmental score. Note that the scale is relative and is capped at the maximum real-world values for the given year.")
], className="centered")

# ---------------------------------------------------------------------------------------------- FOURTH GLOBE ----------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------- FIFTH GLOBE ----------------------------------------------------------------------------------------------

world_map_for_complex_5 = px.scatter_geo(df_complex_5, locations = 'CODE',
                    animation_frame='YEAR',
                    animation_group='ENTITY',
                    color='ENTITY',
                    hover_name='ENTITY',
                    size='POPULATION_DENSITY',
                    projection='orthographic',
                    hover_data={'ENTITY': True, 'POPULATION_DENSITY': True, 'CODE': False, 'DIFFERENCE_IN_ENERGY_CONSUMPTION_PER_CAPITA_IN_KWH': True, 'DIFFERENCE_IN_FOREST_AREA_SQUARE_KM': True, 'DIFFERENCE_IN_DEFORESTATION_SQUARE_KM': True, 'DIFFERENCE_IN_PERCENT_OF_ADULTS_OVERWEIGHT': True, 'DIFFERENCE_IN_CO2_EMISSIONS_METRIC_TONS': True, 'DIFFERENCE_IN_AVG_LITERACY_RATE': True})
world_map_for_complex_5.update_layout(width=1250, height=800)



complex_5_map_section = html.Div(children=[
                                    html.H1("Population Density Dependency of Associated Metrics"),
                                    dcc.Graph(id='data-visualization', figure=world_map_for_complex_5),
                                    html.Br(),
                                    html.P(r"The map displays countries and their respective population densities, as well as the following related parameters in terms of their deviation from the average on the given year, relative to all other countries on the continent: energy consumption per capita in kwh, forest area in km, deforestation in square km, percent of adults who are overweight, CO2 emissions in metric tons, and average literacy rate.")
                                ], className="centered")

# ---------------------------------------------------------------------------------------------- FIFTH GLOBE ----------------------------------------------------------------------------------------------


# MAIN COMPLEX QUERY SECTION
complex_query_section = dbc.Container(
    [
    # Add dropdown and buttons here
        dbc.Row(
            dbc.Col(
                [
                html.H1('Visualize Complex Queries with an Interactive Globe'),
                html.Br(),
                html.Br(),
                html.Br(),
                html.H4('Use the dropdown to select complex insights into our demographic data.'),
                dcc.Dropdown(
                    id=ids.COMPLEX_QUERY_DROPDOWN,
                    options=[{'label': i, 'value': i} for i in data.complex_queries],
                    value=None,
                    multi=False,
                    className = 'dropdown-style',
                ),
                ],
                style={'margin-top': '50px', 'margin-bottom': '50px'},
                className='centered'
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            children=[
                                dcc.Graph(
                                    id=ids.COMPLEX_QUERY_WORLD_MAP,
                                    figure=blank_globe_fig,
                                ),
                            ],
                            id=ids.COMPLEX_QUERY_CONTAINER,
                        )
                    ]
                )
            ]
        ),
    ],
    # className = 'scatter-plot-container'
)

# RENDER FUNCTIONS

def render():
    return complex_query_section

def render_world_map_1():
    return complex_1_map_section

def render_world_map_2():
    return complex_2_map_section

def render_world_map_3():
    return complex_3_map_section

def render_world_map_4():
    return complex_4_map_section

def render_world_map_5():
    return complex_5_map_section