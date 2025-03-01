import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st


# Configurations
st.set_page_config(
    page_title="Automotive Market Analytics",
    layout="wide",  # Use wide layout
    initial_sidebar_state="expanded",  # Expand sidebar by default
)



# Load data frames with error handling
try:
    brand_share = pd.read_csv("data/brand_share.csv")
    old = pd.read_csv("data/old.csv")
    new = pd.read_csv("data/New Feb 2025 Prices.csv")
except FileNotFoundError as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Group old data
old_grouped = old[["Brand", "Model", "City", "Color"]].value_counts().reset_index().sort_values(["Brand", "Model", "City", "Color"])

# Define a professional color palette
professional_colors = color_list = [
    "#202A44",  # Blue
    "#1B365D",  # Blue
    "#7089AC",  # Blue
    "#CED9E5",  # Blue
    "#53565A",  # Grey
    "#888B8D",  # Grey
    "#A7A8A9",  # Grey
    "#C8C9C7",  # Grey
    "#E1DFDD",  # Grey
    "#000000",  # Black
    "#141414",  # Black
    "#FFFFFF",  # White
    "#A85F02",  # Orange
    "#BF834B",  # Orange
    "#D9B48B",  # Orange
    "#F0DFC6",  # Orange
    "#622128",  # Red
    "#9E2A2B",  # Red
    "#DDA69D",  # Red
    "#F0DDD7",  # Red
    "#22372B",  # Green
    "#476D3B",  # Green
    "#A3B2A4",  # Green
    "#E0E7D9",  # Green
]

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Market Overview", "Segment Analysis", "Price Analysis"])

# Page 1: Market Overview
if page == "Market Overview":
    st.title("Automotive Market Overview")
    st.caption("""
        The dataset provides a comprehensive overview of vehicle sales across various segments, brands, models, and years (2021–2025).\n
        It includes detailed information on hatchbacks, sedans, SUVs, luxury cars, and MPVs, with sales volumes (Vol) for each model.\n
        Key highlights include the dominance of certain models like the Suzuki Spresso, Hyundai Tucson, and Toyota Corolla, as well as the growing presence of 
        electric vehicles (EVs) and luxury SUVs. The data reflects trends in consumer preferences,\n
        with increasing interest in compact SUVs, EVs, and premium vehicles over the years.
    """)

    # Bar chart for brand market share over the years
    if not brand_share.empty:
        with st.container():
            st.subheader("Brand Market Share Over The Years")
            brand_share_bar_chart = px.bar(
                brand_share,
                x="Brand",
                y="Vol",
                text_auto=True,
                title="Brand Market Share Over The Years",
                color="Brand",
                animation_frame="Year",
                color_discrete_sequence=professional_colors,
            ).update_xaxes(categoryorder="total descending")

            st.markdown(f"Over {brand_share["Brand"].nunique()} Brands from the data set in the Traffic report and the data from 2021 to 2025")

            st.plotly_chart(brand_share_bar_chart, use_container_width=True)

            
    else:
        st.warning("No data available for brand market share.")

    # Year selection for icicle chart
    st.subheader("Passenger Car Distribution by Year")
    year_selection = st.selectbox("Select the desired year", brand_share["Year"].unique())

    # Filter data for the selected year
    mask = brand_share["Year"] == year_selection
    if not brand_share[mask].empty:
        brand_share_icicle_chart = px.icicle(
            brand_share[mask],
            path=[px.Constant("all"), "Segment", 'Brand', 'Model'],
            values='Vol',
            color_discrete_sequence=professional_colors,
            title=f"Passenger Car Distribution for the Selected Year {year_selection}"
        ).update_traces(root_color="lightgrey")
        st.plotly_chart(brand_share_icicle_chart, use_container_width=True)
    else:
        st.warning(f"No data available for the selected year: {year_selection}")

# Page 2: Segment Analysis
elif page == "Segment Analysis":
    st.title("Segment Analysis")
    st.markdown("Analyze the performance of brands and models within specific segments.")

    # Segment selection
    segment_selection = st.selectbox("Select the required segment", brand_share["Segment"].unique())

    # Filter data based on selected segment
    mask = brand_share["Segment"] == segment_selection
    brand_share_masked = brand_share[mask]

    if not brand_share_masked.empty:
        # Bar chart for brand analysis in the selected segment
        with st.container():
            st.subheader(f"Brand Analysis for {segment_selection}")
            segment_brand_bar_chart = px.bar(
                brand_share_masked,
                x="Brand",
                hover_name="Brand",
                y="Vol",
                text_auto=True,
                title=f"Brand Analysis for {segment_selection}",
                animation_frame="Year",
                color_discrete_sequence=professional_colors,
            ).update_xaxes(categoryorder="total descending")
            st.plotly_chart(segment_brand_bar_chart, use_container_width=True)

        # Bar chart for model analysis in the selected segment
        with st.container():
            st.subheader(f"Model Analysis for {segment_selection}")
            segment_model_bar_chart = px.bar(
                brand_share_masked,
                x="Model",
                hover_name="Brand",
                y="Vol",
                text_auto=True,
                title=f"Model Analysis for {segment_selection}",
                color="Brand",
                animation_frame="Year",
                color_discrete_sequence=professional_colors,
            ).update_xaxes(categoryorder="total descending")
            st.plotly_chart(segment_model_bar_chart, use_container_width=True)

        # Additional Summary Statistics
        with st.expander("View Summary Statistics"):
            st.dataframe(brand_share_masked)
    else:
        st.warning(f"No data available for the selected segment: {segment_selection}")

# Page 3: Price Analysis
elif page == "Price Analysis":
    st.title("Price Analysis")
    st.markdown("Analyze the price and mileage distribution of used and new cars.")

    # Brand selection
    st.header("Used Car Prices", divider=True)
    filtered_brand = st.selectbox("Select the required brand", old["Brand"].unique())

    # Filter data based on selected brand
    filtered_data = old[old["Brand"] == filtered_brand]

    if not filtered_data.empty:
        # Scatter plot for price and mileage distribution
        with st.container():
            st.subheader(f"Mileage and Price Distribution for {filtered_brand}")
            price_scatter = px.scatter(
                filtered_data,
                x="Price",
                y="Milage",  
                hover_name="Model",
                animation_frame="Year",
                marginal_y="rug",
                text="Model",
                color="Model",
                title=f"Mileage and Price Distribution for {filtered_brand}",
                color_discrete_sequence=professional_colors,
            )
            price_scatter.update_layout(
                xaxis=dict(range=[filtered_data["Price"].min(), filtered_data["Price"].max()]),
                yaxis=dict(range=[filtered_data["Milage"].min(), filtered_data["Milage"].max()])
            )
            st.plotly_chart(price_scatter, use_container_width=True)

        # Car density across cities and models
        with st.container():
            st.subheader(f"Car Density for {filtered_brand} Across Cities and Models")
            mask = (old_grouped["Brand"] == filtered_brand)
            if not old_grouped[mask].empty:
                City_car_dist = px.scatter(
                    old_grouped[mask],
                    x="City",
                    y="Model",
                    size="count",
                    color="Model",
                    title=f"Car Density for {filtered_brand} Across Cities and Models",
                    color_discrete_sequence=professional_colors,
                ).update_xaxes(categoryorder="total descending")
                st.plotly_chart(City_car_dist, use_container_width=True)
            else:
                st.warning(f"No data available for the selected brand: {filtered_brand}")
    else:
        st.warning(f"No data available for the selected brand: {filtered_brand}")

    # New car prices
    st.header("New Car Prices", divider=True)
    if not new.empty:
        new_filtered = new[new["Brand"] == filtered_brand]
        if not new_filtered.empty:
            st.dataframe(new_filtered)
        else:
            st.warning(f"No new car data available for the selected brand: {filtered_brand}")
    else:
        st.warning("No new car data available.")
    
