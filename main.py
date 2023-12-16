import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

#0. configure the page
st.set_page_config(
    page_title="Product Details",
    page_icon='🧥',
    layout="wide",
    )

#1. Load the data
@st.cache_data()
def load_data():
    url = 'data/products_all_brands.csv'
    df = pd.read_csv(url, index_col=['product_id'])
    return df