import numpy as np
import pandas as pd

from functions import import_and_clean, fill_na_values, power_plants_data, top_5_states, state_facility_data, power_plant_emissions_per_state_year

# define the states in this analysis
states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California",
        "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
        "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
        "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
        "Massachusetts", "Michigan", "Minnesota", "Mississippi",
        "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
        "New Jersey", "New Mexico", "New York", "North Carolina",
        "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
        "Rhode Island", "South Carolina", "South Dakota", "Tennessee",
        "Texas", "Utah", "Vermont", "Virginia", "Washington",
        "West Virginia", "Wisconsin", "Wyoming"]

# import 2011 data
data_2011 = import_and_clean('datasets\direct_emitters2011.csv')
data_2011 = fill_na_values(data_2011)

# import 2012 data
data_2012 = import_and_clean('datasets\direct_emitters2012.csv')
data_2012 = fill_na_values(data_2012)

# Import 2013 data
data_2013 = import_and_clean('datasets\direct_emitters2013.csv')
data_2013 = fill_na_values(data_2013)

# Import 2014 data
data_2014 = import_and_clean('datasets\direct_emitters2014.csv')
data_2014 = fill_na_values(data_2014)

# Import 2015 data
data_2015 = import_and_clean('datasets\direct_emitters2015.csv')
data_2015 = fill_na_values(data_2015)

# Import 2016 data
data_2016 = import_and_clean('datasets\direct_emitters2016.csv')
data_2016 = fill_na_values(data_2016)

# Import 2017 Data
data_2017 = import_and_clean('datasets\direct_emitters2017.csv')
data_2017 = fill_na_values(data_2017)

# Import 2018 data
data_2018 = import_and_clean('datasets\direct_emitters2018.csv')
data_2018 = fill_na_values(data_2018)

# Import 2019 data
data_2019 = import_and_clean('datasets\direct_emitters2019.csv')
data_2019 = fill_na_values(data_2019)

# Import 2020 CO2 emissions data
data_2020 = import_and_clean('datasets\direct_emitters2020.csv')
data_2020 = fill_na_values(data_2020)


# create dataframe of all data
# all_data = pd.concat([data_2020,
#                       data_2019,
#                       data_2018,
#                       data_2017,
#                       data_2016,
#                       data_2015,
#                       data_2014,
#                       data_2013,
#                       data_2012,
#                       data_2011], axis=0)


# find all power plant data per year
power_plants_2011 = power_plants_data(data_2011, 2011)
power_plants_2012 = power_plants_data(data_2012, 2012)
power_plants_2013 = power_plants_data(data_2013, 2013)
power_plants_2014 = power_plants_data(data_2014, 2014)
power_plants_2015 = power_plants_data(data_2015, 2015)
power_plants_2016 = power_plants_data(data_2016, 2016)
power_plants_2017 = power_plants_data(data_2017, 2017)
power_plants_2018 = power_plants_data(data_2018, 2018)
power_plants_2019 = power_plants_data(data_2019, 2019)
power_plants_2020 = power_plants_data(data_2020, 2020)
power_plant_state_year = pd.concat([power_plants_2011,
                                 power_plants_2012,
                                 power_plants_2013,
                                 power_plants_2014,
                                 power_plants_2015,
                                 power_plants_2016,
                                 power_plants_2017,
                                 power_plants_2018,
                                 power_plants_2019,
                                 power_plants_2020], axis=0)

# find the total power plant co2 emissions emitted across the U.S. in 2020
total2020_power_plant_emissions = power_plants_2020['CO2 emissions (non-biogenic)'].sum()
data_2020_power_plants_total = pd.DataFrame({'Total Power Plant Emissions': [total2020_power_plant_emissions]}) # create dataframe
data_2020_power_plants_total['Total Power Plant Emissions'] = data_2020_power_plants_total['Total Power Plant Emissions'].round(2) # round to two decimal places

# find top 5 emitting states across all years
top_emitting_states = top_5_states(power_plant_state_year)

# find total emissions for each year across the united states
total_emissions_per_year = power_plant_state_year.groupby('Year').sum('CO2 emissions (non-biogenic)').reset_index()
# find total facilities for each year across the united states
total_facilities_per_year = power_plant_state_year.groupby('Year').sum('Facility Count').reset_index()

# find the change in emissions from 2011 to 2020
initial_emissions = total_emissions_per_year.loc[total_emissions_per_year['Year'] == 2011, 'CO2 emissions (non-biogenic)'].values[0]
end_emissions = total_emissions_per_year.loc[total_emissions_per_year['Year'] == 2020, 'CO2 emissions (non-biogenic)'].values[0]
emissions_change_calculation = end_emissions - initial_emissions
emissions_change = abs(emissions_change_calculation.round(2)) # round to 2 decimals

# find all state facility data per year
state_facilities2011 = state_facility_data(data_2011, 2011)
state_facilities2012 = state_facility_data(data_2012, 2012)
state_facilities2013 = state_facility_data(data_2013, 2013)
state_facilities2014 = state_facility_data(data_2014, 2014)
state_facilities2015 = state_facility_data(data_2015, 2015)
state_facilities2016 = state_facility_data(data_2016, 2016)
state_facilities2017 = state_facility_data(data_2017, 2017)
state_facilities2018 = state_facility_data(data_2018, 2018)
state_facilities2019 = state_facility_data(data_2019, 2019)
state_facilities2020 = state_facility_data(data_2020, 2020)
top_state_facilities_per_year = pd.concat([state_facilities2011,
                     state_facilities2012,
                     state_facilities2013,
                     state_facilities2014,
                     state_facilities2015,
                     state_facilities2016,
                     state_facilities2017,
                     state_facilities2018,
                     state_facilities2019,
                     state_facilities2020], axis=0)

# count how many power plant facilities across the U.S. in 2020
total_state_facilities_2020 = state_facilities2020['Facility Name'].count()

# find change in facilities from 2011 to 2020
initial_facilities = total_emissions_per_year.loc[total_emissions_per_year['Year'] == 2011, 'Facility Count'].values[0]
end_facilities = total_emissions_per_year.loc[total_emissions_per_year['Year'] == 2020, 'Facility Count'].values[0]
facilities_change_calculation = end_facilities - initial_facilities
facilities_change = abs(facilities_change_calculation.round(2)) # round to 2 decimals

# find the power plant emissions totals per year
emission_sums2011 = power_plant_emissions_per_state_year(data_2011, 2011)
emission_sums2012 = power_plant_emissions_per_state_year(data_2012, 2012)
emission_sums2013 = power_plant_emissions_per_state_year(data_2013, 2013)
emission_sums2014 = power_plant_emissions_per_state_year(data_2014, 2014)
emission_sums2015 = power_plant_emissions_per_state_year(data_2015, 2015)
emission_sums2016 = power_plant_emissions_per_state_year(data_2016, 2016)
emission_sums2017 = power_plant_emissions_per_state_year(data_2017, 2017)
emission_sums2018 = power_plant_emissions_per_state_year(data_2018, 2018)
emission_sums2019 = power_plant_emissions_per_state_year(data_2019, 2019)
emission_sums2020 = power_plant_emissions_per_state_year(data_2020, 2020)
emission_sums_by_state = pd.concat([emission_sums2011,
                                  emission_sums2012,
                                  emission_sums2013,
                                  emission_sums2014,
                                  emission_sums2015,
                                  emission_sums2016,
                                  emission_sums2017,
                                  emission_sums2018,
                                  emission_sums2019,
                                  emission_sums2020], axis=0)


