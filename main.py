import requests
from bs4 import BeautifulSoup
import sqlite3
import streamlit as st
import pandas as pd
import numpy as np
from random import randint


def filter_cat_data(df,name,origin,weight_range,life_range):
    if name:
        df = df[df['name']==name]
    if origin:
        df = df[df['origin']==origin]
    df = df[df['max_weight'].between(weight_range[0],weight_range[1])]
    df = df[df['max_life_expectancy'].between(life_range[0],life_range[1])] 
    print(df['image_link'])
    st.image(df['image_link'].iat[0])
    
    return df

def filter_breeder_data(df,name,rating):
    if name:
        df = df[df['name']==name]
    df = df[df['rating'].between(rating[0],rating[1])]
    return df

conn = sqlite3.connect("Cat.sqlite")

df_CAT = pd.read_sql('SELECT * FROM CATS', conn)
df_BREEDER = pd.read_sql('SELECT * FROM BREEDERS',conn)

conn.close()

df_facts = open('CATFACTS.txt')
facts = df_facts.readlines()

st.title("This is the Cat Data and Breeder Selection APP")
cat_name = st.sidebar.text_input("Cat Breed")
origin = st.sidebar.text_input('Origin Country')
weight_range = st.sidebar.slider("Weight range", 0, 20, (0, 20))
life_range = st.sidebar.slider("Life Range", 0, 20, (0, 20))

if st.sidebar.button("Submit Cat"):
    st.write(filter_cat_data(df_CAT,cat_name,origin,weight_range,life_range))
    st.write(":red['Hey!Little Tips!']",(facts[randint(0,49)].strip()))
else:
    st.write(df_BREEDER)
    st.write(df_CAT)
    st.write(":red['Hey!Little Tips!']",(facts[randint(0,49)].strip()))



breeder_name = st.sidebar.text_input("Breeder Name")
rating = st.sidebar.slider("Rating range", 0, 5, (0, 5))

if st.sidebar.button("Submit Breeder"):
    st.write(filter_breeder_data(df_BREEDER,breeder_name,rating))
    st.write(":red['Hey!Little Tips!']",(facts[randint(0,49)].strip()))