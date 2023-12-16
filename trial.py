import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configure the page
st.set_page_config(
    page_title="Sociolla Products Catalog",
    page_icon='🌟',
    layout="wide",
)

# Load data function
@st.cache
def load_data():
    # Replace 'your_kaggle_username' and 'your_kaggle_api_key' with your Kaggle credentials
    # Note: Make sure to have the Kaggle API key json file (kaggle.json) in your Streamlit app's directory
    # Download the dataset from Kaggle and use the correct path
    # Example: https://www.kaggle.com/your_kaggle_username/your-dataset
    kaggle_username = 'your_kaggle_username'
    kaggle_api_key = 'your_kaggle_api_key'
    dataset_name = 'ibrahimhafizhan/sociolla-all-brands-products-catalog'
    url = f'https://www.kaggle.com/{kaggle_username}/{dataset_name}/download'
    
    # Set up Kaggle API credentials
    st.kaggle_auth(username=kaggle_username, key=kaggle_api_key)
    
    # Download the dataset
    df = pd.read_csv(url)
    return df

# Build the UI
st.title("Sociolla Products Catalog App")
with st.spinner("Loading data..."):
    df = load_data()

st.header("Sociolla Products Catalog")
st.info("Raw data in DataFrame")
st.dataframe(df.head(), use_container_width=True)

st.success("Column information of the dataset")
cols = df.columns.tolist()
st.subheader(f'Total columns {len(cols)} ➡ {", ".join(cols)}')

# Scatter plot section
st.header("Scatter Plot")
num_cols = df.select_dtypes(include=np.number).columns.tolist()

with st.expander("Customize Scatter Plot"):
    col1 = st.selectbox("Select the first column for scatter plot", num_cols)
    col2 = st.selectbox("Select the second column for scatter plot", num_cols)
    col3 = st.selectbox("Select the third column for scatter plot", num_cols)
    scatter_fig = px.scatter(df, x=col1, y=col2, color=col3, title=f'{col1} vs {col2} by {col3}')
    st.plotly_chart(scatter_fig, use_container_width=True)


# Visualizations in tabs
t1, t2, t3, t4, t5, t6, t7, t8, t9, t10 = st.tabs([
    "Bar Plot", "Line Plot", "Pie Chart", "Histogram", 
    "Box Plot", "Violin Plot", "Scatter Matrix", 
    "Area Plot", "Pair Plot", 'About'
])

with t1:
    bar_col = st.selectbox("Select the column for bar plot", df.columns)
    bar_fig = px.bar(df, x=bar_col, title=f'Bar Plot - {bar_col}')
    st.plotly_chart(bar_fig, use_container_width=True)

with t2:
    line_col1 = st.selectbox("Select the column for line plot", df.columns)
    line_col2 = st.selectbox("Select another column for line plot", num_cols)
    line_fig = px.line(df, x=df.index, y=[line_col1, line_col2], title=f'Line Plot - {line_col1} vs {line_col2}')
    st.plotly_chart(line_fig, use_container_width=True)

with t3:
    pie_col = st.selectbox("Select the column for pie chart", df.columns)
    pie_fig = px.pie(df, names=pie_col, title=f'Pie Chart - {pie_col}')
    st.plotly_chart(pie_fig, use_container_width=True)

with t4:
    hist_col = st.selectbox("Select the column for histogram", num_cols)
    hist_fig = px.histogram(df, x=hist_col, title=f'Histogram - {hist_col}')
    st.plotly_chart(hist_fig, use_container_width=True)

with t5:
    box_col = st.selectbox("Select the column for box plot", num_cols)
    box_fig = px.box(df, x=box_col, title=f'Box Plot - {box_col}')
    st.plotly_chart(box_fig, use_container_width=True)

with t6:
    violin_col = st.selectbox("Select the column for violin plot", num_cols)
    violin_fig = px.violin(df, y=violin_col, box=True, title=f'Violin Plot - {violin_col}')
    st.plotly_chart(violin_fig, use_container_width=True)

with t7:
    scatter_matrix_fig = px.scatter_matrix(df, title='Scatter Matrix')
    st.plotly_chart(scatter_matrix_fig, use_container_width=True)

with t8:
    area_col = st.selectbox("Select the column for area plot", num_cols)
    area_fig = px.area(df, x=df.index, y=area_col, title=f'Area Plot - {area_col}')
    st.plotly_chart(area_fig, use_container_width=True)

with t9:
    pair_plot_fig = px.scatter_matrix(df, title='Pair Plot')
    st.plotly_chart(pair_plot_fig, use_container_width=True)

# About tab
with t10:
    st.markdown("This is a simple Streamlit app.")
    st.markdown("Built with love using Python and Streamlit.")

# Run the app: streamlit run your_script.py
