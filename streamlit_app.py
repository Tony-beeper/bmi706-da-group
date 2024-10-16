import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
from vega_datasets import data
import streamlit as st
st.set_page_config(layout="wide")

df = pd.read_csv('./data/cause_of_deaths.csv', index_col=False)
country_df = pd.read_csv('https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/country_codes.csv', dtype = {'country-code': int})
country_df = country_df[['Country', 'country-code']]

# Mapping for countries with names abcent in the initial dataset
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

# List of all socioeconomic factors
socioeconomic_factors = [
    "Age dependency ratio (% of working-age population)", "Birth rate, crude (per 1,000 people)", 
    "Fertility rate, total (births per woman)", "Life expectancy at birth, total (years)", 
    "Mortality rate, infant (per 1,000 live births)", 
    "Number of under-five deaths",  "Population ages 0-14 (% of total population)", 
    "Population ages 65 and above, total", "Population growth (annual %)", "Population, total", 
    "Rural population (% of total population)", "Urban population (% of total population)", 
    "Urban population growth (annual %)"
]

# List of all individual and categorized causes of deaths
causes_df = pd.read_csv('./data/causes_of_death_categories.csv')
cause_categories = dict(zip(causes_df['Cause of Death'], causes_df['Category']))
causes = list(cause_categories.keys())
categories = list(set(cause_categories.values()))

# Merged dataframe
df['Country'] = df['Country'].replace(name_mapping)
merged_df = pd.merge(df, country_df, how='left', left_on='Country', right_on='Country')

# Initial map
source = alt.topo_feature(data.world_110m.url, 'countries')

# Defining basic parameters
width = 1000
height  = 500
project = 'equirectangular'

st.markdown(
    """
    <style>

            .uploadedFile {{display: none}}
            footer {{visibility: hidden;}}
            .st-emotion-cache-1y4p8pa {
                width: 100%;
                padding: 1rem 1rem 1rem;
                max-width: 1000rem;
                margin-top: 50px

            }
    </style>
    """,
    unsafe_allow_html=True
)


# Mapping regoins
regions = {
    'World': {'center': [0, 50], 'scale': 100},
    'Africa': {'center': [15, 35], 'scale': 225},
    'Europe': {'center': [10, 60], 'scale': 300},
    'Asia': {'center': [100, 50], 'scale': 225},
    'North America': {'center': [-110, 50], 'scale': 250},
    'South America': {'center': [-60, -15], 'scale': 300}
}
####################################################### Sidebar #######################################################
with st.sidebar:
    # Select region
    selected_region = 'World' # Default
    st.write('Click on region of interest')

    # Display buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('World'):
            selected_region = 'World'
        if st.button('Africa'):
            selected_region = 'Africa'
    with col2:
        if st.button('Europe'):
            selected_region = 'Europe'
        if st.button('Asia'):
            selected_region = 'Asia'
    with col3:
        if st.button('North America'):
            selected_region = 'North America'
        if st.button('South America'):
            selected_region = 'South America'

    # Show the selected region
    st.write(f'You selected: {selected_region}')

    # Select year, slider for maps
    year = st.slider('Year:', min_value=int(df['Year'].min()), max_value=int(df['Year'].max()), value=2014)

    # Select specific country, can also be done by clicking on it
    country_options = ['All Countries'] + list(df['Country'].unique())  
    selected_countries = st.multiselect('Countries for cause of death trend(line chart)', country_options, default='All Countries', max_selections=10)
    if selected_countries == ['All Countries']:
        selected_countries = list(df['Country'].unique())
    else:
        selected_countries = list(selected_countries)

    # Select specific country, can also be done by clicking on it
    selected_countries_donut = st.multiselect('Countries for cummulative cause of death(Donut chart)', country_options, default='All Countries', max_selections=10)
    if selected_countries_donut == ['All Countries']:
        selected_countries_donut = list(df['Country'].unique())
    else:
        selected_countries_donut = list(selected_countries_donut)

    # Display dropdown menus based on selection
    if 'initial_choice' not in st.session_state:
        st.session_state.initial_choice = None
    if 'reset' not in st.session_state:
        st.session_state.reset = False

    # Initial choice: Type of comparison
    initial_choice = st.sidebar.radio(
    "Choose comparison type:",
    [
        'Causes of deaths comparison', 
        'Categories of causes of deaths comparison', 
        'Cause of deaths vs socioeconomic factor comparison', 
        'Category of causes of deaths vs socioeconomic factor comparison'
    ]
    )

    # Display options based on the selected choice
    if initial_choice == 'Causes of deaths comparison':
        st.sidebar.write('Select causes of death to compare:')
        cause_1 = st.sidebar.selectbox('Select first cause', causes, index=0)
        cause_2 = st.sidebar.selectbox('Select second cause', causes, index=1)
        st.write(f'You chose to compare: {cause_1} and {cause_2}')
        title_1 = f"Number of deaths caused by {cause_1} in {year}"
        title_2 = f"Number of deaths caused by {cause_2} in {year}"
        field_1, field_2 = cause_1, cause_2

    elif initial_choice == 'Categories of causes of deaths comparison':
        st.sidebar.write('Select categories to compare:')
        category_1 = st.sidebar.selectbox('Select first category', categories, index=0)
        category_2 = st.sidebar.selectbox('Select second category', categories, index=1)
        st.write(f'You chose to compare categories: {category_1} and {category_2}')
        title_1 = f"Number of deaths in {category_1} in {year}"
        title_2 = f"Number of deaths in {category_2} in {year}"
        field_1, field_2 = category_1, category_2

    elif initial_choice == 'Cause of deaths vs socioeconomic factor comparison':
        st.sidebar.write('Select cause of death and socioeconomic factor to compare:')
        cause = st.sidebar.selectbox('Select cause of death', causes)
        socioeconomic_factor = st.sidebar.selectbox('Select socioeconomic factor', socioeconomic_factors)
        st.write(f'You chose to compare: {cause} with {socioeconomic_factor}')
        title_1 = f"{cause} Deaths vs Socioeconomic Factor in {year}"
        title_2 = f"Socioeconomic Factor in {year}"
        field_1, field_2 = cause, socioeconomic_factor

    elif initial_choice == 'Category of causes of deaths vs socioeconomic factor comparison':
        st.sidebar.write('Select category and socioeconomic factor to compare:')
        category = st.sidebar.selectbox('Select category', categories)
        socioeconomic_factor = st.sidebar.selectbox('Select socioeconomic factor', socioeconomic_factors)
        st.write(f'You chose to compare category: {category} with {socioeconomic_factor}')
        title_1 = f"{category} Deaths vs Socioeconomic Factor in {year}"
        title_2 = f"Socioeconomic Factor in {year}"
        field_1, field_2 = category, socioeconomic_factor

############################# Some Supporting functions for plots #####################################

# Choosing color schema
color_schemes = ['oranges', 'blues', 'greens', 'reds', 'purples', 'viridis', 'plasma', 'inferno']

# Defining filtered data
if selected_countries == 'All Countries':
    merged_df_selected = merged_df[merged_df['Year'] == year][['Country', 'Year', 'country-code', field_1, field_2]]
else:
    merged_df_selected = merged_df[(merged_df['Year'] == year) & (merged_df['Country'].isin(selected_countries))][['Country', 'Year', 'country-code', field_1, field_2]]

def clean_column_name(name):
    return name.replace("'", "").replace(" ", "_")  # Remove apostrophes and replace spaces with underscores

# Cleaning field_1 and field_2
field_1 = clean_column_name(field_1)
field_2 = clean_column_name(field_2)

# Renaming columns in the merged df
merged_df_selected = merged_df_selected.rename(columns=lambda x: clean_column_name(x))

# st.write("Filtered Table based on selections:")
# st.write(merged_df_selected)

# Function for projection creation
def get_projection(region):
    region_settings = regions.get(region, regions['World'])
    return ['mercator', region_settings['scale'], region_settings['center']]

# Defining background
background = alt.Chart(source).mark_geoshape(fill='#aaa', stroke='black').properties(
    width=width, height=height).project(type=get_projection(selected_region)[0], 
    scale=get_projection(selected_region)[1], center=get_projection(selected_region)[2])

selector = alt.selection_point(fields=['id'], on='click', clear='dblclick')

chart_base = alt.Chart(source).properties(width=width, height=height).project(
    type=get_projection(selected_region)[0], 
    scale=get_projection(selected_region)[1], 
    center=get_projection(selected_region)[2]).add_selection(selector).transform_lookup(
    lookup='id',
    from_=alt.LookupData(merged_df_selected, 'country-code', ['Country', 'Year', field_1, field_2]))

############################# Actual Maps and Chart functions ######################################
# First map
rate_scale_1 = alt.Scale(domain=[merged_df_selected[field_1].min(), merged_df_selected[field_1].max()], scheme='oranges')
rate_color_1 = alt.Color(field=field_1, type='quantitative', scale=rate_scale_1)

chart_1 = chart_base.mark_geoshape().encode(
    color=rate_color_1,
    tooltip=[
        alt.Tooltip(f'{field_1}:Q', title=f'{field_1} Deaths'),
        alt.Tooltip('Country:N', title='Country:')

    ]
).transform_filter(selector).properties(title=title_1)

# Second map
rate_scale_2 = alt.Scale(domain=[merged_df_selected[field_2].min(), merged_df_selected[field_2].max()], scheme='blues')
rate_color_2 = alt.Color(field=field_2, type='quantitative', scale=rate_scale_2)

chart_2 = chart_base.mark_geoshape().encode(
    color=rate_color_2,
    tooltip=[
        alt.Tooltip(f'{field_2}:Q', title=f'{field_2} Deaths'),
        alt.Tooltip('Country:N', title='Country:')
    ]
).transform_filter(selector).properties(title=title_2)

cola, colb = st.columns(2)

with cola:
    col1, spacer1, col2 = st.columns([20, 0.1, 5])
    with col2:
        color_scheme_1 = st.selectbox("Color Scheme for Map 1", color_schemes, index=0)
        # Update color scheme
        rate_scale_1 = alt.Scale(domain=[df[field_1].min(), df[field_1].max()], scheme=color_scheme_1)
        rate_color_1 = alt.Color(field=field_1, type='quantitative', scale=rate_scale_1, legend=alt.Legend(title="Deaths"))
        # Redraw first map with the selected color scheme
        chart_1 = chart_base.mark_geoshape().encode(
        color=rate_color_1,
        tooltip=[
            alt.Tooltip(f'{field_1}:Q', title=f'{field_1} Deaths'),
            alt.Tooltip('Country:N', title='Country:')
        ]
        ).transform_filter(selector).properties(title=f'Number of deaths caused by {field_1} in {year}')
    with col1:
        st.altair_chart(background + chart_1, use_container_width=True)

with colb:

    col3, spacer2, col4 = st.columns([20, 0.5, 5])

    with col4:
        color_scheme_2 = st.selectbox("Color Scheme for Map 2", color_schemes, index=1)
        # Update color scheme
        rate_scale_2 = alt.Scale(domain=[merged_df_selected[field_2].min(), merged_df_selected[field_2].max()], scheme=color_scheme_2)
        rate_color_2 = alt.Color(field=field_2, type='quantitative', scale=rate_scale_2, legend=alt.Legend(title="Deaths"))
        # Redraw second map with the selected color scheme
        chart_2 = chart_base.mark_geoshape().encode(
        color=rate_color_2,
        tooltip=[
            alt.Tooltip(f'{field_2}:Q', title=f'{field_2} Deaths'),
            alt.Tooltip('Country:N', title='Country:')
        ]
        ).transform_filter(selector).properties(title=f'Number of deaths caused by {field_2} in {year}')


    with col3:
        st.altair_chart(background + chart_2, use_container_width=True)



############################# Line Chart & Donut Chart ##################################################
colc, cold = st.columns(2)

merged_df = merged_df.rename(columns=lambda x: clean_column_name(x))

if selected_countries == 'All Countries':
    merged_df_selected = merged_df[['Country', 'Year', 'country-code', field_1, field_2]]
else:
    merged_df_selected = merged_df[merged_df['Country'].isin(selected_countries)][['Country', 'Year', 'country-code', field_1, field_2]]

# Line plot for temporal data (deaths over years for selected countries)
line_chart = alt.Chart(merged_df_selected).mark_line().encode(
    x=alt.X('Year:O', title='Year'),
    y=alt.Y(f'{field_1}:Q', title=f'{field_1} Deaths'),
    color='Country:N',
    tooltip=['Country:N', 'Year:O', f'{field_1}:Q']
).properties(title=f'{field_1} Deaths Over Time', width=600, height=500)



with colc:
    st.altair_chart(line_chart, use_container_width=True)

# Donut Chart
# Filter data for the selected countries
country_data = df[df['Country'].isin(selected_countries_donut)]

# Select only numeric columns for death causes
numeric_data = country_data.select_dtypes(include='number')

# Get the top 5 causes of death (sum the numeric columns across the selected countries and sort)
top_causes = numeric_data.sum().sort_values(ascending=False).head(5).reset_index()
top_causes.columns = ['Cause', 'Deaths']

# Create the donut chart
donut_chart = alt.Chart(top_causes).mark_arc(innerRadius=50, outerRadius=100).encode(
    theta=alt.Theta(field='Deaths', type='quantitative'),
    color=alt.Color(field='Cause', type='nominal'),
    tooltip=['Cause:N', 'Deaths:Q']
).properties(title=f'Top accumulated causes of deaths in your selected countries')

with cold:
    # Display the chart
    st.altair_chart(donut_chart, use_container_width=True)
