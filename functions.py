import numpy as np
import pandas as pd


def import_and_clean(file):
    """
    Function performs the data loading, cleaning, and preprocessing for the datasets

    Input is the csv file after downloading from specified site

    Returns:
    A cleaned dataframe, but may contain null values

    The following function:
        Read the csv file and skips the first two rows
        Makes the first row the column headers and then drops index 2, which contained the header names in a row
        Strip the empty space at the end of the column names using rstrip
        Strip the emissions data where there are commas in the numbers
        Drop all rows where every column is null and drop all unnecessary columns not needed for analysis
        Create a dictionary of the US states and their abbreviations
        Add a new column where the abbreviated state names are mapped to the full state name
        Drop the other districts/places that are not direct US states
        Convert columns to either floats or strings
        Capitalize the first letter of each word in the specified columns
    """
    data = pd.read_csv(file) # import the csv file 
    data = data.iloc[2:] # skip the first two rows
    data.columns = data.iloc[0]  # make the first row the column headers
    data = data.drop(2) # drop index 2 (it is now the column headers)
    data.columns = data.columns.str.rstrip() # strip the empty space at the end of each column name
    # strip the commas from the values in the column
    data['CO2 emissions (non-biogenic)'] = data['CO2 emissions (non-biogenic)'].str.replace(',', '', regex=True)
    # drop unnecessary columns for analysis
    data = data.drop(['Facility Id', 'FRS Id', 'Methane (CH4) emissions', 'Nitrous Oxide (N2O) emissions', 'HFC emissions', 'PFC emissions',
                      'SF6 emissions', 'NF3 emissions', 'Other Fully Fluorinated GHG emissions', 'HFE emissions',
                      'Very Short-lived Compounds emissions', 'Stationary Combustion', 'Electricity Generation', 'Adipic Acid Production',
                      'Aluminum Production', 'Ammonia Manufacturing', 'Cement Production', 'Electronics Manufacture', 'Ferroalloy Production',
                      'Fluorinated GHG Production', 'Glass Production', 'HCFC–22 Production from HFC–23 Destruction', 'Hydrogen Production',
                      'Iron and Steel Production', 'Lead Production', 'Lime Production', 'Magnesium Production', 'Miscellaneous Use of Carbonates',
                      'Nitric Acid Production', 'Petroleum and Natural Gas Systems – Offshore Production', 'Petroleum and Natural Gas Systems – Processing',
                      'Petroleum and Natural Gas Systems – Transmission/Compression', 'Petroleum and Natural Gas Systems – Underground Storage',
                      'Petroleum and Natural Gas Systems – LNG Storage', 'Petroleum and Natural Gas Systems – LNG Import/Export', 'Petrochemical Production',
                      'Petroleum Refining', 'Phosphoric Acid Production', 'Pulp and Paper Manufacturing', 'Silicon Carbide Production', 'Soda Ash Manufacturing',
                      'Titanium Dioxide Production', 'Underground Coal Mines', 'Zinc Production', 'Municipal Landfills', 'Industrial Wastewater Treatment',
                      'Manufacture of Electric Transmission and Distribution Equipment', 'Industrial Waste Landfills',
                      'Is some CO2 collected on-site and used to manufacture other products and therefore not emitted from the affected manufacturing process unit(s)? (as reported under Subpart G or S)',
                      'Is some CO2 reported as emissions from the affected manufacturing process unit(s) under Subpart AA, G or P collected and transferred off-site or injected (as reported under Subpart PP)?',
                      'Does the facility employ continuous emissions monitoring?'], axis=1)
    data = data.drop(data.index[data.isna().all(axis=1)]) # drop all rows where every column contains null values
    # create a dictionary of us states and their abbreviations
    us_states = {
        "AL": "Alabama",  "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
        "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
        "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
        "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
        "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
        "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire",
        "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina",
        "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
        "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee",
        "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington",
        "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming", "DC": "District of Columbia"
    }
    data['State Name'] = data['State'].map(us_states) # add a new column with state names
    data.insert(3, 'State Name', data.pop('State Name')) # move it to column 3
    # drop Guam, Puerto Rico, U.S. Virgin Islands, and District of Columbia as they are not direct U.S. states
    data = data[~data['State'].isin(['GU', 'PR', 'VI', 'DC'])]
    # define columns to convert
    columns_to_convert = ['Facility Name', 'City', 'State', 'State Name', 'Address', 'County', 'Industry Type (subparts)', 'Industry Type (sectors)', 'Primary NAICS Code']
    convert_to_floats = ['Latitude', 'Longitude', 'CO2 emissions (non-biogenic)']
    convert_to_integers = ['Zip Code']
    # convert columns to respective type
    data[columns_to_convert] = data[columns_to_convert].astype(str)
    data[convert_to_floats] = data[convert_to_floats].astype(float)
    data[convert_to_integers] = data[convert_to_integers].astype(int)
    # capitalize first letter of each word in the following string columns
    columns_to_capitalize = ['Facility Name', 'City', 'Address', 'County']
    for column in columns_to_capitalize:
        data[column] = data[column].str.title()
    return data


def fill_na_values(data):
    """
    Fill in the null values in the non-biogenic CO2 emissions column using the grouped mean
    The grouped mean is found by grouping by state and industry type (sectors)

    Function takes a cleaned dataframe (after running import_and_clean function)
    Function drops any null values that cannot be filled with the grouped mean

    Returns:
    A dataframe with all non-biogenic CO2 emissions filled in with the mean value of the group in which it belongs
    """
    grouped_data = data.groupby(['State', 'Industry Type (sectors)'])['CO2 emissions (non-biogenic)'].transform('mean')
    data['CO2 emissions (non-biogenic)'].fillna(grouped_data, inplace=True)
    data = data.dropna(subset=['CO2 emissions (non-biogenic)'])
    return data


def power_plants_data(data, year):
    """
    Find the power plant emissions per year by state

    Function takes a dataframe
        Counts up how many facilities per state
        Sum up the emissions
        Merge the facilities counts and emissions sums on state
        Add a new column year which represents the year that the emissions represent

    Returns:
    A dataframe that contains the power plant facility counts and emissions for each state and years

    Note:
    The primary NAICS code for power plants includes 22111. The following number 1-8 determines the type of power plant
    https://www.naics.com/naics-code-description/?code=22111#:~:text=22111%20%2D%20Electric%20Power%20Generation&text=This%20industry%20comprises%20establishments%20primarily,solar%20power%2C%20into%20electrical%20energy.
    """
    # return all columns that are within this code. Case=False means it is not case-sensitive
    power_plant_data = data[data['Primary NAICS Code'].str.contains('22111', case=False)]
    # count how many facilities per state
    power_plant_facilities = power_plant_data['State Name'].value_counts().reset_index(name='Count')
    power_plant_facilities = power_plant_facilities.rename(columns={'index': 'State'}) # rename columns
    # sum up emissions
    power_plant_emissions = power_plant_data.groupby('State Name')['CO2 emissions (non-biogenic)'].sum().reset_index()
    power_plant_emissions = power_plant_emissions.rename(columns={'State Name': 'State'}) # rename columns
    # merge the data
    power_plants = pd.merge(power_plant_facilities, power_plant_emissions, on='State')
    power_plants = power_plants.rename(columns={'Count': 'Facility Count'}) # rename columns
    power_plants['Year'] = year # add the year in which this data represents
    return power_plants

def top_5_states(states_data):
    """
    Find the top 5 states per year based on emissions
    
    Input is a dataframe
    
    Returns a dataframe with top 5 emitting states grouped by year
    """
    top_5 = states_data.groupby('Year').apply(lambda x:x.nlargest(5, 'CO2 emissions (non-biogenic)'))
    # Count how many times each state occurs and create a dataframe
    top_states_counts = top_5['State'].value_counts().reset_index()
    top_states_counts.columns = ['State', 'count']
    # Sort the dataframe by the count of occurrences in descending order
    top_states_counts = top_states_counts.sort_values(by='count', ascending=False)
    # Get the top 5 emitting states
    top_states_df = top_states_counts.head(5)
    # Convert the top 5 states to a comma-separated string
    top_states_df = ', '.join(top_states_df['State'].tolist())
    return top_states_df

def state_facility_data(data, year):
    """
    Find state power plant facilities data
    Using the NAICS code to specify power plants

    Function iterates through the list of states using state name
    Using nlargest to find the top 30 largest power plant facilities per state
    Add a new column, assigning the year in which the data represents
    Concatenate all data into one dataframe vertically (stacking on top)

    Returns:
    A dataframe with the 30 largest power plant facilities per state amd year
    """
    all_states_data = []
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
        "West Virginia", "Wisconsin", "Wyoming"
    ]
    for state in states:
        state_data = data[data['State Name'] == state].copy()
        # find power plant facilities in the corresponding state
        state_power_plant_facilities = state_data[state_data['Primary NAICS Code'].str.contains('22111', case=False)]
        # find the top 30 facilities
        state_top_facilities = state_power_plant_facilities.nlargest(30, 'CO2 emissions (non-biogenic)')
        state_top_facilities['Year'] = year # specify the year
        state_top_facilities.reset_index(drop=True, inplace=True)
        all_states_data.append(state_top_facilities)
    # add all states data together
    state_top_facilities = pd.concat(all_states_data, axis=0)
    return state_top_facilities


def power_plant_emissions_per_state_year(data, year):
    """
    Find all the power plant emissions for each state and year

    Function uses the primary NAICS code for power plants
    Groups the emissions by State and sums up the non-biogeic CO2 emissions
    Assign the year in which the data represents

    Returns:
    A dataframe with the total power plant CO2 emissions by state and year
    """
    # retrieve all power plant data
    power_plants_data = data[data['Primary NAICS Code'].str.contains('22111', case=False)]
    # group by state and sum emissions
    state_emission_sums = power_plants_data.groupby('State')['CO2 emissions (non-biogenic)'].sum().reset_index()
    state_emission_sums['Year'] = year # assigns the year
    return state_emission_sums