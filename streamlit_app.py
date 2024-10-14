import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
from vega_datasets import data
import streamlit as st

import folium
from streamlit_folium import folium_static


df = pd.read_csv('./data/cause_of_deaths.csv', index_col=False)
country_df = pd.read_csv('https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/country_codes.csv', dtype = {'conuntry-code': str})
country_df = country_df[['Country', 'country-code']]

df.columns = df.columns.str.replace("'", "").str.replace(" ", "_")

name_mapping = {
    'Bolivia': 'Bolivia (Plurinational State of)',
    'Brunei': 'Brunei Darussalam',
    'Cape Verde': 'Cabo Verde',
    "Cote d'Ivoire": "Côte d'Ivoire",
    'Democratic Republic of Congo': 'Congo, Democratic Republic of the',
    'Iran': 'Iran (Islamic Republic of)',
    'Laos': "Lao People's Democratic Republic",
    'Micronesia': 'Micronesia (Federated States of)',
    'Moldova': 'Moldova, Republic of',
    'North Korea': "Korea (Democratic People's Republic of)",
    'Palestine': 'Palestine, State of',
    'Russia': 'Russian Federation',
    'South Korea': 'Korea, Republic of',
    'Syria': 'Syrian Arab Republic',
    'Taiwan': 'Taiwan, Province of China',
    'Tanzania': 'Tanzania, United Republic of',
    'Timor': 'Timor-Leste',
    'United Kingdom': 'United Kingdom of Great Britain and Northern Ireland',
    'United States': 'United States of America',
    'United States Virgin Islands': 'Virgin Islands (U.S.)',
    'Venezuela': 'Venezuela (Bolivarian Republic of)',
    'Vietnam': 'Viet Nam'
}

df['Country'] = df['Country'].replace(name_mapping)
merged_df = pd.merge(df, country_df, how='left', left_on='Country', right_on='Country')
# merged_df = df
source = alt.topo_feature(data.world_110m.url, 'countries')

# defining basic parameters
width = 600
height  = 300
project = 'equirectangular'


# all of this can be done made dynamic in streamlit
regions = {
    'World': {'center': [0, 0], 'scale': 100},
    'Africa': {'center': [15, 35], 'scale': 225},
    'Europe': {'center': [10, 70], 'scale': 275},
    'Asia': {'center': [100, 50], 'scale': 225},
    'North America': {'center': [-100, 40], 'scale': 300},
    'South America': {'center': [-60, -15], 'scale': 300}
}
# Select cause of death dynamically
causes = df.columns[4:]  # Cause columns start from 4th index
cause_1 = st.selectbox("Select Cause 1", causes, index=0)
cause_2 = st.selectbox("Select Cause 2", causes, index=1)
region = st.selectbox("Select Region", list(regions.keys()), index=2)
year = st.slider("Select Year", min_value=int(df['Year'].min()), max_value=int(df['Year'].max()), value=2014)
# Get the unique list of available countries from the dataset after name mapping
available_countries = df['Country'].unique().tolist()

# Define default countries with names after the name mapping
default_countries = [country for country in [
    "United States of America",  # Updated name after mapping
    "Germany"  # This country was not mapped, so it stays as is
] if country in available_countries]

# If no default countries are available in the data, fallback to the first two countries
if not default_countries:
    default_countries = available_countries[:2]  # Fallback to the first two countries

# Create the multiselect widget with the validated default values
countries = st.multiselect(
    "Select Countries for Line Plot", 
    available_countries, 
    default=default_countries
)

year_selection = alt.selection_single(
    fields=['Year'], 
    nearest=True, 
    on='click', 
    clear=False
)




# function that get projection
def get_projection(region):
    region_settings = regions.get(region, regions['World'])
    return ['mercator', region_settings['scale'], region_settings['center']]

# merged_df
merged_df[['Country', 'country-code', 'Year', cause_1, cause_2]] # mimicking what would be chosen in streamlit app
merged_df = merged_df[merged_df['Year'] == year]

# Filter data for map
# Check if the selection is empty and default to 2014 if true
selected_year = 2014  # Default year

# If the selection is not empty, get the selected year
if year_selection:
    selected_year = year_selection['Year']

# Filter the dataframe based on the selected year
filtered_df = merged_df[merged_df['Year'] == selected_year]



# defining background
background = alt.Chart(source).mark_geoshape(fill='#aaa', stroke='black').properties(
    width=width, height=height).project(type=get_projection(region)[0], scale=get_projection(region)[1], center=get_projection(region)[2])

selector = alt.selection_point(fields=['id'], on='click', clear='dblclick')


chart_base = alt.Chart(source).properties(width=width, height=height).project(
    type=get_projection(region)[0], 
    scale=get_projection(region)[1], 
    center=get_projection(region)[2]).add_selection(selector).transform_lookup(
    lookup='id',
    from_=alt.LookupData(merged_df, 'country-code', ['Country', 'Year', cause_1, cause_2]))

# first map
rate_scale_1 = alt.Scale(domain=[df[cause_1].min(), df[cause_1].max()], scheme='oranges')
rate_color_1 = alt.Color(field=cause_1, type='quantitative', scale=rate_scale_1)

chart_1 = chart_base.mark_geoshape().encode(
    color=rate_color_1,
    tooltip=[
        alt.Tooltip(f'{cause_1}:Q', title=f'{cause_1} Deaths', format=',.0f'),
        alt.Tooltip('Country:N', title='Country:')

    ]
).transform_filter(selector).properties(title=f'Number of deaths caused by {cause_1} in {year}')

# second map
rate_scale_2 = alt.Scale(domain=[df[cause_2].min(), df[cause_2].max()], scheme='blues')
rate_color_2 = alt.Color(field=cause_2, type='quantitative', scale=rate_scale_2)

chart_2 = chart_base.mark_geoshape().encode(
    color=rate_color_2,
    tooltip=[
        alt.Tooltip(f'{cause_2}:Q', title=f'{cause_2} Deaths', format=',.0f'),
        alt.Tooltip('Country:N', title='Country:')
    ]
).transform_filter(selector).properties(title=f'Number of deaths caused by {cause_2} in {year}')


# Line plot for temporal data (deaths over years for selected countries)
line_chart = alt.Chart(df[df['Country'].isin(countries)]).mark_line().encode(
    x=alt.X('Year:O', title='Year'),
    y=alt.Y(f'{cause_1}:Q', title=f'{cause_1} Deaths'),
    color='Country:N',
    tooltip=['Country:N', 'Year:O', f'{cause_1}:Q']
).add_selection(year_selection).properties(title=f'{cause_1} Deaths Over Time', width=600, height=200)

# combining charts with zoomable region settings
chart = alt.vconcat(background + chart_1, background + chart_2).resolve_scale(color='independent')

st.altair_chart(line_chart, use_container_width=True)
st.altair_chart(chart, use_container_width=True)
