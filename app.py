#importing the required libraries
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# set browser tab title
st.set_page_config(page_title="Insight View", page_icon="🔍")

# title and sidebar
st.title("📊 Insight View")
st.subheader("Interactive Data Analysis using Streamlit")

# upload file
file = st.file_uploader("Upload a CSV file", type=["csv"])
if file is not None:
    # read the csv file
    df = pd.read_csv(file)

    # display the preview of the dataframe
    if st.checkbox("Show DataFrame Preview"):
        with st.expander("Head"):
            st.write(df.head())
        with st.expander("Tail"):
            st.write(df.tail())

    # display datatype of each column
    if st.checkbox("Show DataFrame Data Types"):
        st.text("Data Types of each column")
        st.write(df.dtypes)
        st.write(f"**Shape -** Number of Rows: {df.shape[0]} and Columns: {df.shape[1]}")

    # check the null values in the dataframe
    if st.checkbox("Check for Null Values"):
        is_null = df.isnull().values.any()
        if is_null == True:
            st.warning("Null Values Found")
            viz = st.radio("Do you want to visualize null values?", ("No", "Yes"))
            if viz == "Yes":
                fig, ax = plt.subplots()
                sns.heatmap(df.isnull(), ax=ax, cbar=False, cmap='viridis')
                st.pyplot(fig)
            else:
                pass
        else:
            st.success("No Null Values Found")

    # check for duplicate values in the dataframe
    if st.checkbox("Check for Duplicate Values"):
        is_duplicate = df.duplicated().any()
        if is_duplicate == True:
            st.warning("Duplicate Values Found")
            dup = st.radio("Do you want to remove the duplicate values?", ("No", "Yes"))
            if dup == "Yes":
                df = df.drop_duplicates()
                st.success("Duplicate Values Removed")
                st.write(df)
            else:
                pass
        else:
            st.text("No Duplicate Values Found")

    # display the summary of the dataframe
    if st.checkbox("Show DataFrame Summary"):
        st.text("Summary of the DataFrame")
        if st.checkbox("Show all columns"):
            st.write(df.describe(include='all'))
        else:
            st.write(df.describe())

    # Interactive Visualizations
    if st.checkbox("Show Visualizations"):
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if numeric_cols:
            st.subheader("Histogram")
            col_to_plot = st.selectbox("Select column for histogram", numeric_cols)
            bins = st.slider("Number of bins", 5, 50, 10)
            fig, ax = plt.subplots()
            sns.histplot(df[col_to_plot], bins=bins, kde=True, ax=ax)
            st.pyplot(fig)

            st.subheader("Scatter Plot")
            x_axis = st.selectbox("X-axis", numeric_cols, index=0)
            y_axis = st.selectbox("Y-axis", numeric_cols, index=1)
            fig, ax = plt.subplots()
            sns.scatterplot(data=df, x=x_axis, y=y_axis, ax=ax)
            st.pyplot(fig)

            st.subheader("Correlation Heatmap")
            corr = df[numeric_cols].corr()
            fig, ax = plt.subplots(figsize=(8,6))
            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)
        else:
            st.info("No numeric columns available for visualization")