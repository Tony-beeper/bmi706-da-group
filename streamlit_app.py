import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
from vega_datasets import data
import streamlit as st
st.set_page_config(layout="wide")
with open( "./style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

merged_df = pd.read_csv('./data/final_data.csv', index_col=False)
merged_df = merged_df.round(3)
categories = ['External_Causes', 'Infectious_Diseases',
       'Maternal_and_Neonatal_Health', 'Non_Communicable_Diseases',
       'Nutritional_and_Metabolic_Disorders', 'Substance_Use_Disorders',
       'Violence_and_Conflict']
socioeconomic_factors = ['Age_dependency_ratio', 'Annual_Population_growth',
       'Annual_Urban_population_growth', 'Crude_Birth_rate', 'Fertility_rate',
       'Infant_Mortality_rate', 'Life_expectancy_at_birth',
       'Number_of_under_five_deaths', 'Percentage_of_Rural_population',
       'Percentage_of_Urban_population', 'Population_ages_0_14',
       'Population_ages_65_and_above', 'Total_Population']
causes = ['Meningitis', 'Alzheimers_Disease_and_Other_Dementias',
       'Parkinsons_Disease', 'Nutritional_Deficiencies', 'Malaria', 'Drowning',
       'Interpersonal_Violence', 'Maternal_Disorders', 'HIV_AIDS',
       'Drug_Use_Disorders', 'Tuberculosis', 'Cardiovascular_Diseases',
       'Lower_Respiratory_Infections', 'Neonatal_Disorders',
       'Alcohol_Use_Disorders', 'Self_harm', 'Exposure_to_Forces_of_Nature',
       'Diarrheal_Diseases', 'Environmental_Heat_and_Cold_Exposure',
       'Neoplasms', 'Conflict_and_Terrorism', 'Diabetes_Mellitus',
       'Chronic_Kidney_Disease', 'Poisonings', 'Protein_Energy_Malnutrition',
       'Road_Injuries', 'Chronic_Respiratory_Diseases',
       'Cirrhosis_and_Other_Chronic_Liver_Diseases', 'Digestive_Diseases',
       'Fire_Heat_and_Hot_Substances', 'Acute_Hepatitis']
continent_mapping = {'Albania': 'Europe','Andorra': 'Europe','Austria': 'Europe','Belarus': 'Europe','Belgium': 'Europe','Bosnia and Herzegovina': 'Europe',
 'Bulgaria': 'Europe','Croatia': 'Europe','Cyprus': 'Europe','Czechia': 'Europe','Denmark': 'Europe','Estonia': 'Europe','Finland': 'Europe',
 'France': 'Europe','Germany': 'Europe','Greece': 'Europe','Hungary': 'Europe','Iceland': 'Europe','Ireland': 'Europe','Italy': 'Europe','Latvia': 'Europe',
 'Lithuania': 'Europe', 'Luxembourg': 'Europe','Malta': 'Europe','Moldova, Republic of': 'Europe','Monaco': 'Europe','Montenegro': 'Europe','Netherlands': 'Europe',
 'North Macedonia': 'Europe','Norway': 'Europe','Poland': 'Europe','Portugal': 'Europe','Romania': 'Europe','San Marino': 'Europe','Serbia': 'Europe',
 'Slovakia': 'Europe','Slovenia': 'Europe','Spain': 'Europe','Sweden': 'Europe','Switzerland': 'Europe','Ukraine': 'Europe','United Kingdom of Great Britain and Northern Ireland': 'Europe',
 'Afghanistan': 'Asia','Armenia': 'Asia','Azerbaijan': 'Asia','Bahrain': 'Asia','Bangladesh': 'Asia','Bhutan': 'Asia','Brunei Darussalam': 'Asia','Cambodia': 'Asia',
 'China': 'Asia','Georgia': 'Asia','India': 'Asia','Indonesia': 'Asia','Iran (Islamic Republic of)': 'Asia','Iraq': 'Asia','Israel': 'Asia','Japan': 'Asia',
 'Jordan': 'Asia','Kazakhstan': 'Asia','Kuwait': 'Asia','Kyrgyzstan': 'Asia',"Lao People's Democratic Republic": 'Asia','Lebanon': 'Asia','Malaysia': 'Asia',
 'Maldives': 'Asia','Mongolia': 'Asia','Myanmar': 'Asia','Nepal': 'Asia','Oman': 'Asia','Pakistan': 'Asia','Philippines': 'Asia','Qatar': 'Asia','Saudi Arabia': 'Asia','Singapore': 'Asia',
 'Sri Lanka': 'Asia','Syrian Arab Republic': 'Asia','Tajikistan': 'Asia','Thailand': 'Asia','Timor-Leste': 'Asia','Turkey': 'Asia','Turkmenistan': 'Asia','United Arab Emirates': 'Asia',
 'Uzbekistan': 'Asia','Viet Nam': 'Asia','Yemen': 'Asia','Algeria': 'Africa','Angola': 'Africa','Benin': 'Africa','Botswana': 'Africa','Burkina Faso': 'Africa','Burundi': 'Africa',
 'Cabo Verde': 'Africa','Cameroon': 'Africa','Central African Republic': 'Africa','Chad': 'Africa','Comoros': 'Africa','Congo': 'Africa','Congo, Democratic Republic of the': 'Africa',
 "Côte d'Ivoire": 'Africa','Djibouti': 'Africa','Egypt': 'Africa','Equatorial Guinea': 'Africa','Eritrea': 'Africa','Eswatini': 'Africa','Ethiopia': 'Africa','Gabon': 'Africa','Gambia': 'Africa',
 'Ghana': 'Africa','Guinea': 'Africa','Guinea-Bissau': 'Africa','Kenya': 'Africa','Lesotho': 'Africa','Liberia': 'Africa','Libya': 'Africa','Madagascar': 'Africa','Malawi': 'Africa',
 'Mali': 'Africa','Mauritania': 'Africa','Mauritius': 'Africa','Morocco': 'Africa','Mozambique': 'Africa','Namibia': 'Africa','Niger': 'Africa','Nigeria': 'Africa','Rwanda': 'Africa',
 'Sao Tome and Principe': 'Africa','Senegal': 'Africa','Seychelles': 'Africa','Sierra Leone': 'Africa','Somalia': 'Africa','South Africa': 'Africa','South Sudan': 'Africa','Sudan': 'Africa',
 'Tanzania, United Republic of': 'Africa','Togo': 'Africa','Tunisia': 'Africa','Uganda': 'Africa', 'Zambia': 'Africa','Zimbabwe': 'Africa', 'Antigua and Barbuda': 'North America',
 'Bahamas': 'North America','Barbados': 'North America','Belize': 'North America','Bermuda': 'North America','Canada': 'North America', 'Costa Rica': 'North America',
 'Cuba': 'North America','Dominica': 'North America','Dominican Republic': 'North America','El Salvador': 'North America','Grenada': 'North America','Guatemala': 'North America',
 'Haiti': 'North America','Honduras': 'North America','Jamaica': 'North America','Mexico': 'North America','Nicaragua': 'North America','Panama': 'North America','Puerto Rico': 'North America',
 'Saint Kitts and Nevis': 'North America','Saint Lucia': 'North America','Saint Vincent and the Grenadines': 'North America', 'Trinidad and Tobago': 'North America',
 'United States of America': 'North America', 'Virgin Islands (U.S.)': 'North America','Argentina': 'South America','Bolivia (Plurinational State of)': 'South America','Brazil': 'South America',
 'Chile': 'South America','Colombia': 'South America','Ecuador': 'South America','Guyana': 'South America','Paraguay': 'South America','Peru': 'South America','Suriname': 'South America','Uruguay': 'South America',
 'Venezuela': 'South America','Australia': 'Australia','Fiji': 'Australia','Kiribati': 'Australia','Marshall Islands': 'Australia','Micronesia (Federated States of)': 'Australia','Nauru': 'Australia',
 'New Zealand': 'Australia','Palau': 'Australia','Papua New Guinea': 'Australia','Samoa': 'Australia','Solomon Islands': 'Australia','Tonga': 'Australia','Tuvalu': 'Australia','Vanuatu': 'Australia'}

# Initial map
source = alt.topo_feature(data.world_110m.url, 'countries')

# Defining basic parameters
width = 1000
height  = 500
project = 'equirectangular'

# Mapping regoins
regions = {
    'World': {'center': [0, -30], 'scale': 90},
    'Africa': {'center': [15, -5], 'scale': 300},
    'Europe': {'center': [10, 51], 'scale': 450},
    'Asia': {'center': [100, 40], 'scale': 260},
    'North America': {'center': [-110, 50], 'scale': 250},
    'South America': {'center': [-60, -30], 'scale': 300},
    'Australia': {'center': [140, -40], 'scale': 450}
}
####################################################### Sidebar and Widgets #######################################################

# Select year, slider for maps
year = st.slider('Year:', min_value=int(merged_df['year'].min()), max_value=int(merged_df['year'].max()), value=2014)

with st.sidebar:
    # Select region
    selected_region = 'World' # Default
    st.write('Click on region of interest')
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('World'):
            selected_region = 'World'
        if st.button('Africa'):
            selected_region = 'Africa'
        if st.button('Australia'):
            selected_region = 'Australia'   
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
    st.write(f'You selected: {selected_region}')

    # Select country
    country_options = ['All Countries'] + list(merged_df['Country Name'].unique())  
    selected_countries = st.multiselect('Countries for cause of death trend(line chart)', country_options, default='All Countries', max_selections=10)
    if selected_countries == ['All Countries']:
        selected_countries = list(merged_df['Country Name'].unique())
    else:
        selected_countries = list(selected_countries)

    # Select color schema
    color_schemes = ['viridis', 'plasma', 'inferno', 'oranges', 'blues', 'greens', 'reds', 'purples']

    # Select options for the first map
    st.sidebar.write('Map 1 selection:')
    map1_selection = st.sidebar.selectbox('Select cause of death or category for Map 1', categories + causes, index=0)
    st.write(f'You chose to compare for Map 1: {map1_selection}')
    color_scheme_1 = st.selectbox('Color Scheme for Map 1', color_schemes, index=0)

    # Select options for the second map
    st.sidebar.write('Map 2 selection:')
    second_map_radio = st.sidebar.radio('Choose what to compare for Map 2:', ['Individual cause of death or category', 'Socioeconomic factor'])
    map2_selection = 'Drowning'   
    if second_map_radio == 'Individual cause of death or category':
        cat_and_causes = categories + causes
        map2_selection = st.sidebar.selectbox('Select cause of death or category for Map 2', [item for item in cat_and_causes if item != map1_selection], index=0)
    else:
        map2_selection = st.sidebar.selectbox('Select socioeconomic factor for Map 2', socioeconomic_factors)
    color_scheme_2 = st.selectbox('Color Scheme for Map 2', color_schemes, index=1)

    field_1, field_2 = map1_selection, map2_selection

############################# Some Supporting functions for plots #####################################

# Defining filtered data
if selected_countries == list(merged_df['Country Name'].unique()):
    merged_df_selected = merged_df[merged_df['year'] == year][['Country Name', 'year', 'Country Code', field_1, field_2]]
else:
    merged_df_selected = merged_df[(merged_df['year'] == year) & (merged_df['Country Name'].isin(selected_countries))][['Country Name', 'year', 'Country Code', field_1, field_2]]

# Function for projection creation
def get_projection(region):
    region_settings = regions.get(region, regions['World'])
    return ['equirectangular', region_settings['scale'], region_settings['center']]

# Defining background
background = alt.Chart(source).mark_geoshape(fill='#aaa', stroke='black').properties(
    width=width, height=height).project(type=get_projection(selected_region)[0], 
    scale=get_projection(selected_region)[1], center=get_projection(selected_region)[2])

chart_base = alt.Chart(source).properties(width=width, height=height).project(
    type=get_projection(selected_region)[0], 
    scale=get_projection(selected_region)[1], 
    center=get_projection(selected_region)[2]).transform_lookup(
    lookup='id',
    from_=alt.LookupData(merged_df_selected, 'Country Code', ['Country Name', 'year', field_1, field_2]))

######################################################## Maps ###############################################################
title_1 = f"Number of deaths caused by {map1_selection} in {year}"
if second_map_radio == 'Individual cause of death or category':
    title_2 = f"Number of deaths caused by {map2_selection} in {year}"
    tooltip_title = f"{map2_selection} Deaths per 100,000"
else:
    title_2 = f"Socioeconomic Factor: {map2_selection} in {year}"
    tooltip_title = f"{map2_selection}"

# First map
rate_scale_1 = alt.Scale(domain=[merged_df_selected[field_1].min(), merged_df_selected[field_1].max()], scheme=color_schemes[0])
rate_color_1 = alt.Color(field=field_1, type='quantitative', scale=rate_scale_1)

chart_1 = chart_base.mark_geoshape().encode(
    color=rate_color_1,
    tooltip=[
        alt.Tooltip(f'{field_1}:Q', title=f'{field_1} Deaths per 100,000'),
        alt.Tooltip('Country Name:N', title='Country')

    ]
).properties(title={'text': title_1})

# Second map
rate_scale_2 = alt.Scale(domain=[merged_df_selected[field_2].min(), merged_df_selected[field_2].max()], scheme=color_schemes[1])
rate_color_2 = alt.Color(field=field_2, type='quantitative', scale=rate_scale_2)

chart_2 = chart_base.mark_geoshape().encode(
    color=rate_color_2,
    tooltip=[
        alt.Tooltip(f'{field_2}:Q', title=tooltip_title),
        alt.Tooltip('Country Name:N', title='Country')
    ]
).properties(title={'text': title_2})

cola, colb = st.columns(2)

with cola:
    col1, spacer1, col2 = st.columns([24, 0.1, 1])
    with col2:
        # Update color scheme
        rate_scale_1 = alt.Scale(domain=[merged_df[field_1].min(), merged_df[field_1].max()], scheme=color_scheme_1)
        rate_color_1 = alt.Color(field=field_1, type='quantitative', scale=rate_scale_1, legend=alt.Legend(title="Rate",titleFontSize=10,         # Smaller title font
            labelFontSize=8,          # Smaller label font
            gradientLength=150,       # Shorter gradient bar
            gradientThickness=8,      # Thinner gradient bar
            orient='right' ))
        # Redraw first map with the selected color scheme
        chart_1 = chart_base.mark_geoshape().encode(
            color=rate_color_1,
            tooltip=[
                alt.Tooltip(f'{field_1}:Q', title=f'{field_1} Deaths per 100,000'),
                alt.Tooltip('Country Name:N', title='Country')
            ]
        ).properties( title=alt.TitleParams(
        text=title_1,
        fontSize=19,
        font='Montserrat',  # Optionally set a custom font
        anchor='start',  # Align title to the left
    ),)
    with col1:
        st.altair_chart(background + chart_1, use_container_width=True)

with colb:
    col3, spacer2, col4 = st.columns([24, 0.5, 1])
    with col4:
        # Update color scheme
        rate_scale_2 = alt.Scale(domain=[merged_df[field_2].min(), merged_df[field_2].max()], scheme=color_scheme_2)
        rate_color_2 = alt.Color(field=field_2, type='quantitative', scale=rate_scale_2, legend=alt.Legend(title="Rate",titleFontSize=10,         # Smaller title font
            labelFontSize=8,          # Smaller label font
            gradientLength=150,       # Shorter gradient bar
            gradientThickness=8,      # Thinner gradient bar
            orient='right' ))
        # Redraw second map with the selected color scheme
        chart_2 = chart_base.mark_geoshape().encode(
            color=rate_color_2,
            tooltip=[
                alt.Tooltip(f'{field_2}:Q', title=tooltip_title),
                alt.Tooltip('Country Name:N', title='Country')
            ]
        ).properties(
            title=alt.TitleParams(
                text=title_2,   # Set the title text here
                fontSize=19,    # Adjust the font size
                font='Montserrat',  # Optionally set a custom font
                anchor='start',  # Control the alignment ('start', 'middle', 'end')
                # color='black'    # Set the color of the title (optional)
            )
        )

    with col3:
        st.altair_chart(background + chart_2, use_container_width=True)

############################# Line Chart & Donut Chart ##################################################
colc, cold = st.columns([20, 10])

if selected_countries == list(merged_df['Country Name'].unique()):
    merged_df_selected = merged_df[['Country Name', 'year', 'Country Code', 'Total_Population', field_1, field_2]]
    merged_df_selected['Continent'] = merged_df_selected['Country Name'].map(continent_mapping)
    for field in [field_1,field_2]:
        merged_df_selected[field] = merged_df_selected[field]*merged_df_selected['Total_Population']/100000
    summed_df = merged_df_selected.groupby(by = ['Continent', 'year']).sum().reset_index()
    for field in [field_1,field_2]:
        summed_df[field] = 100000*summed_df[field]/summed_df['Total_Population']
    merged_df_selected = summed_df
    merged_df_selected['Country Name'] = merged_df_selected['Continent']
else:
    merged_df_selected = merged_df[merged_df['Country Name'].isin(selected_countries)][['Country Name', 'year', 'Country Code', field_1, field_2]]

# Sample data and data type assignment (Current Data or Prediction)
merged_df_selected['data_type'] = merged_df_selected['year'].apply(lambda x: 'Current Data' if x <= 2019 else 'Prediction')

# Base chart for common encoding
base = alt.Chart(merged_df_selected).encode(
    x=alt.X('year:O', title='Year'),
    y=alt.Y(f'{field_1}:Q', title=f'{field_1} Deaths'),
    color='Country Name:N',
    tooltip=['Country Name:N', 'year:O', f'{field_1}:Q']
)

# Solid line for current data
current_data = base.transform_filter(alt.datum.data_type == 'Current Data').mark_line(strokeDash=[0])

# Dashed line for prediction data
prediction_data = base.transform_filter(alt.datum.data_type == 'Prediction').mark_line(strokeDash=[5, 5])

# Combine both layers
line_chart = alt.layer(current_data, prediction_data).properties(
    title=alt.TitleParams(
        text=f'{field_1} Deaths per 100,000 Over Time',
        fontSize=19,  # Set the desired font size here
        font='Montserrat',  # Optionally, set the font family if needed
        anchor='start'  # You can control the alignment of the title
    ),
    width=500,
    height=300
)


# Creating the legend for line styles (Current Data and Prediction)
legend_data = pd.DataFrame({
    'label': ['', ''],
    'Representation': ['Collected data','Model Prediction'],
    'y': [1, 2]  # Dummy y-values for positioning
})

legend_chart = alt.Chart(legend_data).mark_line().encode(
    y=alt.Y('y:O', axis=None),  # Hides the axis
    x=alt.value(0),  # Position the legend lines horizontally
    strokeDash='Representation:N',
    color=alt.value('red'),
    size=alt.value(2)
).properties(
    width=20,
    height=50
).encode(
    alt.Tooltip('label:N')
)

# Combine line_chart and legend
final_chart = alt.hconcat(legend_chart,line_chart)

# Display the final chart
with colc:
    st.altair_chart(final_chart, use_container_width=True)

# Donut Chart
# Filter data for the selected countries
country_data = merged_df[merged_df['Country Name'].isin(selected_countries)]
country_data = country_data.loc[country_data[country_data['year']==year].index, :]
for category in categories:
    country_data[category] = country_data[category]*country_data['Total_Population']/100000
# Select only numeric columns for death causes
numeric_data = country_data.sum()
numeric_data = numeric_data[categories]*100000/numeric_data['Total_Population']

# Get the top 5 causes of death (sum the numeric columns across the selected countries and sort)
top_causes = numeric_data.sort_values(ascending=False).head(7).reset_index()
top_causes.columns = ['Cause', 'Deaths']


# Create the donut chart
donut_chart = alt.Chart(top_causes).mark_arc(innerRadius=50, outerRadius=110).encode(
    theta=alt.Theta(field='Deaths', type='quantitative'),
    color=alt.Color(field='Cause', type='nominal', title='Category'),
    tooltip=[alt.Tooltip('Cause:N', title='Category'), alt.Tooltip('Deaths:Q', title='Deaths per 100,000')]
).properties(
    title={
        'text': [
            f'Category-wise distribution of deaths per 100,000',
            f'for selected countries in {year}'

        ],
        'fontSize': 19,  # Set the title font size to 19
        'font': 'Montserrat',  # Set the custom font to Montserrat
        'anchor': 'start'      # Align the title to the left
    }

    # title=alt.TitleParams(
    #     text=f'Category-wise distribution of deaths per 100,000 for selected countries in {year}',  # Setting the title text
    #     fontSize=19,
    #     font='Montserrat',  # Optionally set a custom font
    #     anchor='start',  # Align title to the left
    # )
)



with cold:
    # # Display the title separately
    # # Add the div with a specific ID to apply custom styles
    # st.markdown(f"""
    #     <div id='custom-title'>
    #         <p style='font-size:19px; margin-top: 0px;'>Category-wise distribution of deaths per 100,000 for selected countries in {year}</p>
    #     </div>
    #     """, unsafe_allow_html=True)

    # # Apply custom CSS specifically for the custom-title
    # st.markdown(
    #     """
    #     <style>
    #     #custom-title p {
    #         font-size: 19px !important; 
    #         margin-top: 0px !important; 
    #     }
    #     </style>
    #     """, 
    #     unsafe_allow_html=True
    # )
        
    # # Add some empty space between the title and the chart
    # st.write("")  # Add as many st.write("") as needed for spacing
    # st.write("")  # Add as many st.write("") as needed for spacing
    # st.write("")  # Add as many st.write("") as needed for spacing
    # Display the chart below the title
    st.altair_chart(donut_chart, use_container_width=True)
