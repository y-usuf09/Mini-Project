import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Configure the page
st.set_page_config(
    page_title="Video Game Sales and Ratings Analysis",
    page_icon='🎮',
    layout="wide",
)

#1. Load the data
@st.cache_data
def load_data():
    url = 'data/Video_Games.csv'
    df = pd.read_csv(url)
    return df

# Build the UI
st.title("🌟 Game Changers: Unveiling the Secrets Behind Video Game Triumphs and Ratings Triumphs 🚀")
st.header("Level Up Your Insights: A Deep Dive into Video Game Sales Strategies and Ratings Success 🎮💡")

with st.spinner("Loading data..."):
    df = load_data()

# Handle missing values
df.dropna(inplace=True)  # Drop rows with any missing values.

# Remove specific columns
columns_to_remove = [""]

# Check if the columns exist in the DataFrame before removing
columns_exist = all(column in df.columns for column in columns_to_remove)

if columns_exist:
    # Remove the specified columns
    df.drop(columns=columns_to_remove, inplace=True)
else:
    st.error("One or more columns do not exist in the DataFrame.")

# Display the dataset
st.dataframe(df, use_container_width=True)

st.success("Column information of the dataset")
cols = df.columns.tolist()
st.subheader(f'Total columns {len(cols)} ➡ {", ".join(cols)}')

# Additional Plots
st.header("Additional Visualizations")

# Select box for the type of graph
selected_graph = st.selectbox("Select the type of graph", ['Bar', 'Pie', 'Histogram', 'Box', 'Violin',
                                                        'Scatter', 'Area', 'Pair',
                                                        'Funnel', 'Treemap','Line','Sunburst','Choropleth'])

# Dynamically generate select box for column based on the selected graph type
selected_column = None

if selected_graph in ['Bar', 'Pie', 'Histogram', 'Box', 'Violin', 'Area', 'Funnel']:
    selected_column = st.selectbox(f"Select the column for {selected_graph} plot", df.columns)

elif selected_graph in ['Scatter', 'Bubble', 'Pair']:
    selected_column = st.selectbox(f"Select the column for {selected_graph} plot (x-axis)", df.columns)

elif selected_graph == 'Bubble':
    selected_column_size = st.selectbox("Select the column for bubble size", df.columns)

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
    selected_columns_treemap = st.multiselect("Select columns for treemap", df.columns)
    if selected_columns_treemap:  
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
    selected_column_size = st.selectbox("Select the column for Pair plot size", df.columns)
    pair_fig = px.scatter_matrix(df, dimensions=[selected_column, selected_column_size], title=f'Pair Plot - {selected_column} vs {selected_column_size}')
    st.plotly_chart(pair_fig, use_container_width=True)

elif selected_graph == 'Funnel':
    funnel_fig = px.funnel(df, x=selected_column, title=f'Funnel Plot - {selected_column}')
    st.plotly_chart(funnel_fig, use_container_width=True)

elif selected_graph == 'Line':
    selected_column_x_line = st.selectbox("Select the column for X-axis", df.columns)
    line_fig = px.line(df, x=df[selected_column_x_line], y=selected_column, title=f'Line Plot - {selected_column_x_line} vs {selected_column}')
    st.plotly_chart(line_fig, use_container_width=True)

elif selected_graph == 'Sunburst':
    selected_columns_sunburst = st.multiselect("Select columns for Sunburst plot", df.columns)
    if selected_columns_sunburst:
        sunburst_fig = px.sunburst(df, path=selected_columns_sunburst, title="Sunburst Plot")
        st.plotly_chart(sunburst_fig, use_container_width=True)

elif selected_graph == 'Choropleth':
    st.header("Choropleth Map Settings")
    
    # Select column for locations (countries or regions)
    selected_column_locations = st.selectbox("Select the column for locations", df.columns)
    
    # Select the column for color intensity on the map
    selected_column_color = st.selectbox("Select the column for color intensity", df.columns)
    
    # Additional settings (optional)
    title_text = st.text_input("Enter the title for the Choropleth Map", f'Choropleth Map - {selected_column_color}')
    projection_type = st.selectbox("Select the map projection type", ["equirectangular", "mercator", "orthographic", "natural earth", "kavrayskiy7"])
    
    choropleth_fig = px.choropleth(df, 
                                    locations=df[selected_column_locations], 
                                    locationmode='country names', 
                                    color=df[selected_column_color], 
                                    title=title_text,
                                    projection=projection_type)
    
    st.plotly_chart(choropleth_fig, use_container_width=True)


# 3D Visualizations
st.header("3D Visualizations")
selected_3d_graph = st.selectbox("Select the type of 3D graph", ['3D Scatter Plot', '3D Line Plot',
                                                                '3D Scatter Matrix', '3D Bubble Plot',
                                                                '3D Mesh Plot'])


if selected_3d_graph == '3D Scatter Plot':
    col1 = st.selectbox("Select the column for X-axis", [None] + df.columns.tolist())
    col2 = st.selectbox("Select the column for Y-axis", [None] + df.columns.tolist())
    col3 = st.selectbox("Select the column for Z-axis", [None] + df.columns.tolist())
    fig_3d_scatter = px.scatter_3d(df, x=col1, y=col2, z=col3, title=f'3D Scatter Plot - {col1} vs {col2} vs {col3}')
    st.plotly_chart(fig_3d_scatter, use_container_width=True,height=800)

elif selected_3d_graph == '3D Line Plot':
    col1 = st.selectbox("Select the column for X-axis", [None] + df.columns.tolist())
    col2 = st.selectbox("Select the column for Y-axis", [None] + df.columns.tolist())
    col3 = st.selectbox("Select the column for Z-axis", [None] + df.columns.tolist())
    fig_3d_line = px.line_3d(df, x=col1, y=col2, z=col3, title=f'3D Line Plot - {col1} vs {col2} vs {col3}')
    st.plotly_chart(fig_3d_line, use_container_width=True,height=800)

elif selected_3d_graph == '3D Scatter Matrix':
    dimensions = st.multiselect("Select the columns for Scatter Matrix", df.columns.tolist())
    fig_3d_scatter_matrix = px.scatter_matrix(df, dimensions=dimensions, title='3D Scatter Matrix')
    st.plotly_chart(fig_3d_scatter_matrix, use_container_width=True,height=800)

elif selected_3d_graph == '3D Bubble Plot':
    col1 = st.selectbox("Select the column for X-axis", [None] + df.columns.tolist())
    col2 = st.selectbox("Select the column for Y-axis", [None] + df.columns.tolist())
    col3 = st.selectbox("Select the column for Z-axis", [None] + df.columns.tolist())
    fig_3d_bubble = px.scatter_3d(df, x=col1, y=col2, z=col3, title=f'3D Bubble Plot - {col1} vs {col2} vs {col3}')
    st.plotly_chart(fig_3d_bubble, use_container_width=True,height=800)


elif selected_3d_graph == '3D Mesh Plot':
    col1 = st.selectbox("Select the column for X-axis", [None] + df.columns.tolist())
    col2 = st.selectbox("Select the column for Y-axis", [None] + df.columns.tolist())
    col3 = st.selectbox("Select the column for Z-axis", [None] + df.columns.tolist())
    fig_3d_mesh = px.scatter_3d(df, x=col1, y=col2, z=col3, color=col3, title=f'3D Mesh Plot - {col1} vs {col2} vs {col3}')
    st.plotly_chart(fig_3d_mesh, use_container_width=True,height=800)


st.header("About")
st.markdown(
    """
    **🌟 Video Game Sales and Ratings Explorer 🎮**

    Welcome to the Video Game Sales and Ratings Explorer, where we unlock the secrets behind gaming triumphs! This app is your passport to a deep dive into the fascinating world of video game sales strategies and ratings success.

    **Key Features:**
    - Explore and visualize the extensive dataset of video game sales and ratings.
    - Select from a variety of interactive plots to uncover insights and patterns.
    - Immerse yourself in 3D visualizations for a unique perspective on gaming data.

    Ready to level up your understanding of video game dynamics? Dive into the data, explore the plots,
    and unveil the stories behind the success of your favorite games!

    *Built with Streamlit, Pandas, Plotly, Seaborn, and Matplotlib.*

    *Created By: Yusuf Tajwar*
    """
)



# how to run the app 
# open terminal and run: 
# streamlit run main.py  