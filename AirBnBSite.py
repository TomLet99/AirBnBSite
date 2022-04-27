"""
CREATED BY: Thomas Letourneau

Description: This code creates an interactive web page where the user can manipulate the data shown in the map through widgets.
This is an updated and altered version of my CS299 Final


To run, use the the following command in the terminal: streamlit run AirBnBSite
"""



import matplotlib.pyplot as plt
import csv
import streamlit as st
import pydeck as pdk
import pandas as pd
import mapbox as mb
import numpy as np
import statistics

DATA_FILE = 'listings.csv'
MAPKEY = "" #insert Google maps API key here

#filters the dataframe and returns a dict of the values between prices x and y, of room_type: 'size' and in the neighborhoods array
def filterList(doc, x, y, size, neighbourhoods):
    filteredResults = dict(name=[], price=[], neighbourhood=[],
                             room_type=[], latitude=[],
                             longitude=[], minimum_nights=[])

    for index, row in doc.iterrows():
        if x < int(row['price']) < y and row['neighbourhood'] in neighbourhoods and row['room_type'] == size:
            for i in row.keys():
                if i in filteredResults.keys():
                    filteredResults[i].append(row[i])

    return filteredResults


#Creates a map of all listings. The map is Centered on Boston and provides a Tooltip for each listing
def listingMap(listings):

    view_state = pdk.ViewState(
        latitude=42.3601,
        longitude=-71.0589,
        zoom=12,
        pitch=0)

    layer1 = pdk.Layer('ScatterplotLayer',
                      data=listings,
                      get_position='[longitude, latitude]',
                      get_radius=20,
                      get_color=[200,20,0],
                      pickable=True)

    tool_tip = tool_tip = {"html": "Listing Name:<br/> <b>{name}</b> ",
            "style": { "backgroundColor": "red",
                        "color": "white"}
          }

    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        #mapbox_key=MAPKEY,
        layers=[layer1],
        tooltip=tool_tip
    )

    st.pydeck_chart(map)


def main():
    #open the csv file as a dictionary

    doc = pd.read_csv(DATA_FILE)

    st.title(f'{"Thomas Letourneau: AirBnB Listings Map"}')

    x = st.sidebar.slider('Minimum Price', 100.0, 1500.0)
    y = st.sidebar.slider('Maximum Price', 100.0, 1500.0, value=1500.0)

    sizes = ['Entire home/apt', 'Private room', 'Hotel room', 'Shared room']
    size = st.sidebar.radio("Select a size: ", sizes)

    neighborhoodList = list(doc['neighbourhood'].unique())
    neighbourhoods = st.sidebar.multiselect('What neighbourhoods would you like to stay in?', neighborhoodList, default=neighborhoodList)

    filteredResults = filterList(doc, x, y, size, neighbourhoods)

    #if the filtered list is empty, inform user, else show map and datafram
    if len(filteredResults['name']) == 0:
        st.text("There are no results with the following specifications. \n" 
                "Please enter your specifications in the sidebar.")
    else:
        st.text(f"All Listings between ${x} and ${y} \nwith Room Type: '{size}' \nin the following neighborhoods:")
        st.dataframe(neighbourhoods)
        listingMap(pd.DataFrame(filteredResults))
        st.dataframe(filteredResults)


main()
