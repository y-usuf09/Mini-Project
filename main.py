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
                                                        'Heatmap', 'Funnel', 'Treemap'])

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
    if 'selected_columns_treemap' in locals():  
        treemap_fig = px.treemap(df, path=selected_columns_treemap, title="Treemap")
        st.plotly_chart(treemap_fig, use_container_width=True)

elif selected_graph == 'Box':
    box_fig = px.box(df, x=selected_column, title=f'Box Plot - {selected_column}')
    st.plotly_chart(box_fig, use_container_width=True)

elif selected_graph == 'Violin':
    violin_fig = px.violin(df, y=selected_column, title=f'Violin Plot - {selected_column}')
    st.plotly_chart(violin_fig, use_container_width=True)

elif selected_graph == 'Scatter':
    selected_column_y = st.selectbox("Select the column for Scatter plot (y-axis)", df.columns)
    scatter_fig = px.scatter(df, x=selected_column, y=selected_column_y, title=f'Scatter Plot - {selected_column} vs {selected_column_y}')
    st.plotly_chart(scatter_fig, use_container_width=True)

elif selected_graph == 'Area':
    area_fig = px.area(df, x=selected_column, title=f'Area Plot - {selected_column}')
    st.plotly_chart(area_fig, use_container_width=True)

elif selected_graph == 'Pair':
    pair_fig = px.scatter_matrix(df, dimensions=[selected_column, selected_column_size], title=f'Pair Plot - {selected_column} vs {selected_column_size}')
    st.plotly_chart(pair_fig, use_container_width=True)

elif selected_graph == 'Bubble':
    bubble_fig = px.scatter(df, x=selected_column, y=selected_column_size, size=selected_column_size, title=f'Bubble Plot - {selected_column} vs {selected_column_size}')
    st.plotly_chart(bubble_fig, use_container_width=True)

elif selected_graph == 'Heatmap':
    heatmap_fig = px.imshow(df[selected_columns_heatmap].corr(), title='Heatmap - Correlation Matrix')
    st.plotly_chart(heatmap_fig, use_container_width=True)

elif selected_graph == 'Funnel':
    funnel_fig = px.funnel(df, x=selected_column, title=f'Funnel Plot - {selected_column}')
    st.plotly_chart(funnel_fig, use_container_width=True)


# 3D Visualizations
st.header("3D Visualizations")
selected_3d_graph = st.selectbox("Select the type of 3D graph", ['3D Scatter Plot', '3D Line Plot', '3D Surface Plot',
                                                                '3D Bar Plot', '3D Scatter Matrix', '3D Bubble Plot',
                                                                '3D Cone Plot', '3D Mesh Plot', '3D Scatter Polar Plot'])

if selected_3d_graph == '3D Scatter Plot':
    col1 = st.selectbox("Select the column for X-axis", [None] + df.columns.tolist())
    col2 = st.selectbox("Select the column for Y-axis", [None] + df.columns.tolist())
    col3 = st.selectbox("Select the column for Z-axis", [None] + df.columns.tolist())
    fig_3d_scatter = px.scatter_3d(df, x=col1, y=col2, z=col3, title=f'3D Scatter Plot - {col1} vs {col2} vs {col3}')
    st.plotly_chart(fig_3d_scatter, use_container_width=True)

elif selected_3d_graph == '3D Line Plot':
    col1 = st.selectbox("Select the column for X-axis", [None] + df.columns.tolist())
    col2 = st.selectbox("Select the column for Y-axis", [None] + df.columns.tolist())
    col3 = st.selectbox("Select the column for Z-axis", [None] + df.columns.tolist())
    fig_3d_line = px.line_3d(df, x=col1, y=col2, z=col3, title=f'3D Line Plot - {col1} vs {col2} vs {col3}')
    st.plotly_chart(fig_3d_line, use_container_width=True)

elif selected_3d_graph == '3D Surface Plot':
    col1 = st.selectbox("Select the column for X-axis", [None] + df.columns.tolist())
    col2 = st.selectbox("Select the column for Y-axis", [None] + df.columns.tolist())
    col3 = st.selectbox("Select the column for Z-axis", [None] + df.columns.tolist())
    fig_3d_surface = px.surface_3d(df, x=col1, y=col2, z=col3, title=f'3D Surface Plot - {col1} vs {col2} vs {col3}')
    st.plotly_chart(fig_3d_surface, use_container_width=True)

elif selected_3d_graph == '3D Bar Plot':
    col1 = st.selectbox("Select the column for X-axis", [None] + df.columns.tolist())
    col2 = st.selectbox("Select the column for Y-axis", [None] + df.columns.tolist())
    col3 = st.selectbox("Select the column for Z-axis", [None] + df.columns.tolist())
    fig_3d_bar = px.bar_3d(df, x=col1, y=col2, z=col3, title=f'3D Bar Plot - {col1} vs {col2} vs {col3}')
    st.plotly_chart(fig_3d_bar, use_container_width=True)

elif selected_3d_graph == '3D Scatter Matrix':
    dimensions = st.multiselect("Select the columns for Scatter Matrix", df.columns.tolist())
    fig_3d_scatter_matrix = px.scatter_matrix(df, dimensions=dimensions, title='3D Scatter Matrix')
    st.plotly_chart(fig_3d_scatter_matrix, use_container_width=True)

elif selected_3d_graph == '3D Bubble Plot':
    col1 = st.selectbox("Select the column for X-axis", [None] + df.columns.tolist())
    col2 = st.selectbox("Select the column for Y-axis", [None] + df.columns.tolist())
    col3 = st.selectbox("Select the column for Z-axis", [None] + df.columns.tolist())
    fig_3d_bubble = px.scatter_3d(df, x=col1, y=col2, z=col3, title=f'3D Bubble Plot - {col1} vs {col2} vs {col3}')
    st.plotly_chart(fig_3d_bubble, use_container_width=True)

elif selected_3d_graph == '3D Cone Plot':
    col1 = st.selectbox("Select the column for X-axis", [None] + df.columns.tolist())
    col2 = st.selectbox("Select the column for Y-axis", [None] + df.columns.tolist())
    col3 = st.selectbox("Select the column for Z-axis", [None] + df.columns.tolist())
    fig_3d_cone = px.cone(df, x=col1, y=col2, z=col3, title=f'3D Cone Plot - {col1} vs {col2} vs {col3}')
    st.plotly_chart(fig_3d_cone, use_container_width=True)

elif selected_3d_graph == '3D Mesh Plot':
    col1 = st.selectbox("Select the column for X-axis", [None] + df.columns.tolist())
    col2 = st.selectbox("Select the column for Y-axis", [None] + df.columns.tolist())
    col3 = st.selectbox("Select the column for Z-axis", [None] + df.columns.tolist())
    fig_3d_mesh = px.scatter_3d(df, x=col1, y=col2, z=col3, color=col3, title=f'3D Mesh Plot - {col1} vs {col2} vs {col3}')
    st.plotly_chart(fig_3d_mesh, use_container_width=True)

elif selected_3d_graph == '3D Scatter Polar Plot':
    col1 = st.selectbox("Select the column for Theta-axis", [None] + df.columns.tolist())
    col2 = st.selectbox("Select the column for Phi-axis", [None] + df.columns.tolist())
    col3 = st.selectbox("Select the column for R-axis", [None] + df.columns.tolist())
    fig_3d_polar = px.scatter_3d_polar(df, theta=col1, phi=col2, r=col3, title=f'3D Scatter Polar Plot - {col1} vs {col2} vs {col3}')
    st.plotly_chart(fig_3d_polar, use_container_width=True)


# About Section
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