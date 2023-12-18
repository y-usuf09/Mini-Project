import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


# Configure the page
st.set_page_config(
    page_title="Sociolla Products Catalog",
    page_icon='🧿',
    layout="wide",
)

#1. Load the data
@st.cache_data
def load_data():
    url = 'data/products_all_brands.csv'
    df = pd.read_csv(url)
    return df

# Build the UI
st.title("Sociolla Products Catalog")
st.header("Products Catalog Dataset")
with st.spinner("Loading data..."):
    df = load_data()

# Remove specific columns
columns_to_remove = ["url", "price_by_combinations", "active_date", "rating_types_str", "average_rating_by_types"]

# Check if the columns exist in the DataFrame before removing
columns_exist = all(column in df.columns for column in columns_to_remove)

if columns_exist:
    # Remove the specified columns
    df.drop(columns=columns_to_remove, inplace=True)
else:
    st.error("One or more columns do not exist in the DataFrame.")

# Display the updated DataFrame
st.dataframe(df, use_container_width=True)

st.success("Column information of the dataset")
cols = df.columns.tolist()
st.subheader(f'Total columns {len(cols)} ➡ {", ".join(cols)}')

# Additional Plots
st.header("Additional Visualizations")

# Select box for the type of graph
selected_graph = st.selectbox("Select the type of graph", ['Bar', 'Pie', 'Histogram', 'Box', 'Violin',
                                                        'Scatter', 'Area', 'Pair', 'Bubble',
                                                        'Heatmap', 'Funnel', 'Treemap',
                                                        '3D Scatter Plot', '3D Line Plot', '3D Surface Plot'])

# Dynamically generate select box for column based on the selected graph type
selected_column = None

if selected_graph in ['Bar', 'Pie', 'Histogram', 'Box', 'Violin', 'Area', 'Funnel']:
    selected_column = st.selectbox(f"Select the column for {selected_graph} plot", df.columns)

elif selected_graph in ['Scatter', 'Bubble', 'Pair']:
    selected_column = st.selectbox(f"Select the column for {selected_graph} plot (x-axis)", df.columns)

elif selected_graph == 'Bubble':
    selected_column_size = st.selectbox("Select the column for bubble size", df.columns)

elif selected_graph == 'Heatmap':
    selected_columns_heatmap = st.multiselect("Select columns for heatmap", df.columns)

elif selected_graph == 'Treemap':
    # Assuming you want to choose a numerical column for treemap
    selected_columns_treemap = st.multiselect("Select columns for treemap", df.select_dtypes(include=np.number).columns.tolist())

# Plot based on the selected graph and column
if selected_graph == 'Bar':
    bar_fig = px.bar(df, x=selected_column, title=f'Bar Plot - {selected_column}')
    st.plotly_chart(bar_fig, use_container_width=True)

elif selected_graph == 'Pie':
    pie_fig = px.pie(df, names=selected_column, title=f'Pie Chart - {selected_column}')
    st.plotly_chart(pie_fig, use_container_width=True)

elif selected_graph == 'Histogram':
    hist_fig = px.histogram(df, x=selected_column, title=f'Histogram - {selected_column}')
    st.plotly_chart(hist_fig, use_container_width=True)

elif selected_graph == 'Treemap':
    treemap_fig = px.treemap(df, path=selected_columns_treemap, title="Treemap")
    st.plotly_chart(treemap_fig, use_container_width=True)

# 3D Plots
st.header("3D Visualizations")
selected_3d_graph = st.selectbox("Select the type of 3D graph", ['3D Scatter Plot', '3D Line Plot', '3D Surface Plot'])

if selected_3d_graph == '3D Scatter Plot':
    col1 = st.selectbox("Select the column for X-axis", df.columns)
    col2 = st.selectbox("Select the column for Y-axis", df.columns)
    col3 = st.selectbox("Select the column for Z-axis", df.columns)
    fig_3d_scatter = px.scatter_3d(df, x=col1, y=col2, z=col3, title=f'3D Scatter Plot - {col1} vs {col2} vs {col3}')
    st.plotly_chart(fig_3d_scatter, use_container_width=True)

elif selected_3d_graph == '3D Line Plot':
    col1 = st.selectbox("Select the column for X-axis", df.columns)
    col2 = st.selectbox("Select the column for Y-axis", df.columns)
    col3 = st.selectbox("Select the column for Z-axis", df.columns)
    fig_3d_line = px.line_3d(df, x=col1, y=col2, z=col3, title=f'3D Line Plot - {col1} vs {col2} vs {col3}')
    st.plotly_chart(fig_3d_line, use_container_width=True)

elif selected_3d_graph == '3D Surface Plot':
    col1 = st.selectbox("Select the column for X-axis", df.columns)
    col2 = st.selectbox("Select the column for Y-axis", df.columns)
    col3 = st.selectbox("Select the column for Z-axis", df.columns)
    fig_3d_surface = px.surface(df, x=col1, y=col2, z=col3, title=f'3D Surface Plot - {col1} vs {col2} vs {col3}')
    st.plotly_chart(fig_3d_surface, use_container_width=True)

# About section
st.header("About")
st.markdown(
    """
    **Sociolla Products Catalog App**

    Explore and visualize the Sociolla Products Catalog with interactive plots.
    Select different types of plots and customize them based on your preferences.
    Use the 3D visualizations to gain insights from three-dimensional perspectives.

    *Built with Streamlit, Pandas, Plotly, Seaborn, and Matplotlib.*

    *Created By: Yusuf Tajwar*
    """
)







# how to run the app 
# open terminal and run: 
# streamlit run main.py 
