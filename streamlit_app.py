import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
from vega_datasets import data
import streamlit as st

df = pd.read_csv('./data/cause_of_deaths.csv', index_col=False)
country_df = pd.read_csv('https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/country_codes.csv', dtype = {'conuntry-code': str})
country_df = country_df[['Country', 'country-code']]

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
cause_1 = 'Meningitis'
cause_2 = 'Nutritional Deficiencies'
year = 2014
region = 'Asia'

# function that get projection
def get_projection(region):
    region_settings = regions.get(region, regions['World'])
    return ['mercator', region_settings['scale'], region_settings['center']]

# merged_df
merged_df[['Country', 'country-code', 'Year', cause_1, cause_2]] # mimicking what would be chosen in streamlit app
merged_df = merged_df[merged_df['Year'] == year]


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
        alt.Tooltip(f'{cause_1}:Q', title='Deaths:'),
        alt.Tooltip('Country:N', title='Country:')
    ]
).transform_filter(selector).properties(title=f'Number of deaths caused by {cause_1} in {year}')

# second map
rate_scale_2 = alt.Scale(domain=[df[cause_2].min(), df[cause_2].max()], scheme='blues')
rate_color_2 = alt.Color(field=cause_2, type='quantitative', scale=rate_scale_2)

chart_2 = chart_base.mark_geoshape().encode(
    color=rate_color_2,
    tooltip=[
        alt.Tooltip(f'{cause_2}:Q', title='Deaths:'),
        alt.Tooltip('Country:N', title='Country:')
    ]
).transform_filter(selector).properties(title=f'Number of deaths caused by {cause_2} in {year}')

# combining charts with zoomable region settings
chart = alt.vconcat(background + chart_1, background + chart_2).resolve_scale(color='independent')

st.altair_chart(chart, use_container_width=True)
