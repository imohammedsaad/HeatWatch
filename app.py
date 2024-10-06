import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from geodatasets import get_path

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv('data.csv')  # Assuming the CSV is named data.csv
    return df

# Load NYC shapefile for mapping
@st.cache_resource
def load_nyc_shapefile():
    nyc_shapefile = gpd.read_file(get_path('nybb'))
    return nyc_shapefile

# Function to create map
def create_map(df, shapefile):
    # Merge data with shapefile
    merged = shapefile.set_index('BoroCode').join(df.set_index('ZIP Code Tabulation Area (ZCTA) 2020'))  # Correct column name here
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    merged.boundary.plot(ax=ax, linewidth=1, color='black')
    merged.plot(column='Heat Vulnerability Index (HVI)', ax=ax, legend=True,
                legend_kwds={'label': "Heat Vulnerability Index (HVI)",
                             'orientation': "horizontal"},
                cmap='OrRd')
    plt.title('Heat Vulnerability Index in NYC', fontsize=16)
    plt.axis('off')  # Hide the axis
    return fig

# Load data and shapefile
df = load_data()
nyc_shapefile = load_nyc_shapefile()

# Streamlit App
st.title('NYC Heat Vulnerability Index Mapping')

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ("Map Visualization", "Story Section"))

if page == "Map Visualization":
    st.write("This map visualizes the Heat Vulnerability Index (HVI) across different ZIP Code Tabulation Areas in NYC.")
    
    # Create map
    fig = create_map(df, nyc_shapefile)
    st.pyplot(fig)

    # Insights Section
    st.subheader("Insights and Narrative")
    st.write(
        """
        The Heat Vulnerability Index (HVI) measures how susceptible different areas of NYC are to heat-related health impacts. 
        Areas with higher HVI scores indicate greater vulnerability, often correlating with socioeconomic factors and environmental conditions.
        
        By understanding the geographic distribution of heat vulnerability, policymakers can target interventions to protect at-risk communities, 
        ensuring equitable access to cooling resources during heat events.
        """
    )
elif page == "Story Section":
    # Center the image at the top of the page
    st.markdown("<h2 style='text-align: center;'>Urban Heat Island Effect</h2>", unsafe_allow_html=True)
    st.image("EPA Heat Island-illustration_v03.jpg", use_column_width='auto', width=800)  # Adjust width as needed

    # Add narrative text below the image
    st.subheader("Urban Heat Islands: A Silent Threat to Vulnerable Communities in NYC")
    st.write(
        """
        In the bustling heart of New York City, not all neighborhoods feel the heat equally. 
        As skyscrapers rise and streets pulse with life, certain areas quietly bear the brunt of increasing temperatures. 
        The combination of high Land Surface Temperatures (LST) and the Heat Vulnerability Index (HVI) tells a stark story: 
        neighborhoods with the fewest green spaces and most concrete suffer from the oppressive heat the most.
        """
    )
    st.write(
        """
        Areas in the Bronx and parts of Brooklyn, for example, show elevated LST readings, where asphalt roads and buildings 
        absorb and radiate heat. This intensifies the heat vulnerability in communities already at risk due to socioeconomic factors, 
        such as lower access to healthcare and cooling resources. The data reveals that these “urban heat islands” aren’t just uncomfortable—
        they pose real health risks to the city’s most vulnerable populations.
        """
    )
    st.write(
        """
        As NYC continues to face the impacts of climate change, the correlation between rising surface temperatures and heat vulnerability 
        underscores the urgent need for equitable climate adaptation. Green infrastructure, such as parks and tree canopies, could provide 
        a lifeline to the communities facing this invisible yet growing threat.
        """
    )

    st.markdown("---")  # Add a horizontal line for separation
