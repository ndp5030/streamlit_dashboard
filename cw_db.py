# Imports
import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import json
from geopy.geocoders import Nominatim

# Functions 
if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def set_clicked():
    st.session_state.clicked = True
def unclick():
    st.session_state.clicked = False

@st.cache_data
def load_data(path: str):
    data = pd.read_csv(path)
    return data

def get_geolocation(city, state):
    geolocator = Nominatim(user_agent="my_geocoder")

    location = geolocator.geocode(f"{city}, {state}")

    if location:
        return location.latitude, location.longitude
    else:
        return None


# Main app
st.set_page_config(page_title='Citrus Wave Analytics', layout = 'wide')
st.markdown("<h1 style='color: #000066;'> Citrus Wave Metrics </h1>", unsafe_allow_html=True)
metric = st.selectbox('Metric', ['Sales', 'Profit'], on_change=unclick)
analytics_selection = st.button("Submit", on_click=set_clicked)

if st.session_state.clicked:
    df = load_data('C:\\Users\\Nicholas\\Desktop\\Projects\\Current Job Ledger - Job Costs.csv')
    # Add year, month, change date to timestamp
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year.astype('int')
    df['Month'] = df['Date'].dt.month
    df['Month_name'] = df['Date'].dt.month_name()
    month_names = ["January", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    # Drop down df preview
    with st.expander("Data Preview"):
            st.dataframe(df,
                         column_config={
                             "Year": st.column_config.NumberColumn(format="%d")
                         })

    # Page 1: Sales
    # Row 1 : Pie - Total Sales, Bar - Sales by Month
    # Row 2 : Line - Sales by group over month,  Map - Heatmap of sale dist
    if metric == 'Sales':
        st.markdown(f"<h1 style= 'color: #000066;', align = 'center'>2024 Total Sales: {df['Sold For '].sum()} </h1>", unsafe_allow_html=True)
        top_left, top_middle, top_right = st.columns([2,2,3])
        with top_left:
            #Pie chart
            new_fig_data = df.groupby('What')['Sold For '].sum()
            # st.markdown(f"<h4 style= 'color: #000066;'>Sales by Category </h4>", unsafe_allow_html=True)
            fig = px.pie(values=new_fig_data, names = new_fig_data.keys(), title= 'Most of our sales were in...')
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig)

        with top_middle:
            #Bar chart by month
            figure = px.bar(df.groupby('Month')['Sold For '].sum(),title='Over the year, our sale amounts per month were...', y=df.groupby('Month')['Sold For '].sum().values, x=month_names, labels = {'y': '', 'x': ''})
            st.plotly_chart(figure)

        with top_right:
            # Histogram
            hist_fig = px.histogram(df, x = 'Sold For ', nbins = 20, title='The distribution of sales we made by amount were...', color = 'What')
            st.plotly_chart(hist_fig)

        bottom_left, bottom_right = st.columns([3,5])
        with bottom_left:
            # Heat map - work locations
            city_cnts = df['City'].value_counts().reset_index()
            city_cnts.columns = ['City', 'Count']

            # # Section to dynamically generate geo_coords
            # geo_coord_lat = {}
            # geo_coord_long = {}

            # for c in city_cnts['City']:
            #     latitude, longitude = get_geolocation(c, "FL")

            #     geo_coord_lat[c] = latitude
            #     geo_coord_long[c] = longitude


            geo_coord_lat = {
                            'Clearwater': 27.9658533,
                            'Tampa': 27.950575,
                            'St. Petersburg': 27.773056,
                            'St. Cloud': 28.2489016,
                            'Orlando': 28.5383355,
                            'Sarasota': 27.3364347,
                            'Largo': 27.909466499999997,
                            'Bradenton': 27.4989278,
                            'Dade City': 28.36290546861878,
                            'Inverness': 28.832995383120863,
                            'Port Charlotte': 26.999752387446023,
                            'Punta Gorda': 26.923972623612105,
                            'St. Cloud': 28.242860059550935,
                            'Seminole': 27.858380773419405,
                            'Spring Hill': 28.512460928051087,
                            'Temple Terrace': 28.046580081522222,
                            'Belleair': 27.936010365867467,
                            'Tierra Verde': 27.690472546403942,
                            'Lutz': 28.167168736643028,
                            'Parrish': 27.588561415716306,
                            'Longwood': 28.703671179162104,
                            'Wesley Chapel': 28.215749493603344,
                            'Gulfport': 27.758730941991107,
                        }
            
            geo_coord_long = {
                            'Clearwater': -82.8001026,
                            'Tampa': -82.4571776,
                            'St. Petersburg': -82.64,
                            'St. Cloud': -81.2811801,
                            'Orlando': -81.3792365,
                            'Sarasota': -82.5306527,
                            'Largo': -82.7873244,
                            'Bradenton': -82.5748194,
                            'Dade City': -82.19546463847938,
                            'Inverness': -82.35410336205621,
                            'Port Charlotte': -82.12839724370488,
                            'Punta Gorda': -82.05602764974323,
                            'St. Cloud': -81.28339495294536,
                            'Seminole': -82.79401818398074,
                            'Spring Hill': -82.49427150248721,
                            'Temple Terrace': -82.38583055271141,
                            'Belleair': -82.80520562244472,
                            'Tierra Verde': -82.72414537190643,
                            'Lutz': -82.44091662443638,
                            'Parrish': -82.42148335207604,
                            'Longwood': -81.3472070378461,
                            'Wesley Chapel': -82.29102602104317,
                            'Gulfport': -82.71623997863435
                        }
            
            city_cnts['Lat'] = city_cnts['City'].map(geo_coord_lat)
            city_cnts['Long'] = city_cnts['City'].map(geo_coord_long)
            city_cnts_fig = px.scatter_geo(city_cnts,
                     lat='Lat',
                     lon='Long',
                     size='Count',
                     hover_name='City',
                     title='The majority of our work was in the following areas...')
            # city_cnts_fig.update_geos(fitbounds = 'locations')
            # city_cnts_fig.update_geos(scope='usa')
            city_cnts_fig.update_layout(
            geo=dict(
                scope='usa',
                center=dict(lat=27, lon=-80),
                projection_scale=4,  
                showland=True,
                landcolor='rgb(243, 243, 243)'
            )
        )
            st.plotly_chart(city_cnts_fig)

        with bottom_right:
            # Line chart 
            line_data = df.groupby(['Month', 'What'])['Sold For '].sum().unstack(fill_value=0)
            line_chart = px.line(line_data, title = 'Sales over the year by sector...')
            st.plotly_chart(line_chart)


    # Page 2: Profit
    # Row 1 : Pie - Total Profit, Bar - Profit by Month
    # Row 2 : Line - Profit pct by Sector, Bar - Profit by Sector
    if metric == 'Profit':
        st.markdown(f"<h1 style= 'color: #000066;', align = 'center'>Total Profit: {df['Profit/Loss'].sum()} </h4>", unsafe_allow_html=True)
        top_left, top_middle, top_right = st.columns([2,2,3])
        with top_left:
            #Pie chart
            new_fig_data = df.groupby('What')['Profit/Loss'].sum()
            fig = px.pie(values=new_fig_data, names = new_fig_data.keys(), title= 'Most of our profits were in...')
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig)

        with top_middle:
            #Bar chart by month
            figure = px.bar(df.groupby('Month')['Profit/Loss'].sum(),title="Beginning of the year was slow, but it's picking up", y=df.groupby('Month')['Profit/Loss'].sum().values, x=month_names, labels = {'y': '', 'x': ''})
            st.plotly_chart(figure)

        with top_right:
            # Histogram
            hist_fig = px.histogram(df, x = 'Profit/Loss', nbins = 8, title='The distribution of profit we made by amount were...', color = 'What')
            st.plotly_chart(hist_fig)
        
        bottom_left, bottom_right = st.columns([3,5])
        with bottom_left:
            # Bar chart profit margin
            bar_avg = df.groupby('What')[['Profit/Loss', 'Sold For ']].sum()
            bar_avg['Profit_Margin'] = bar_avg['Profit/Loss'] / bar_avg['Sold For '] * 100
            bar_fig = px.bar(bar_avg, x=bar_avg.index, y='Profit_Margin', title = 'The total profit margin percentage across all jobs was...')
            bar_fig.update_layout(xaxis={'categoryorder': 'total descending'})
            st.plotly_chart(bar_fig)
        with bottom_right:
            # Line chart
            line_data = df.groupby(['Month', 'What'])['Profit/Loss'].sum().unstack(fill_value=0)
            line_chart = px.line(line_data, title = 'Profit over the year by sector...')
            st.plotly_chart(line_chart)
