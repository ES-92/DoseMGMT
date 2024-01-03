import streamlit as st
import pandas as pd
import plot_creation
import statistical_analysis

# Set page configuration
st.set_page_config(
    page_title="Complex CT Analysis",
    page_icon=":bar_chart:",
    layout="wide"
)

# Encoding dropdown list
encoding_options = ["ANSI", "UTF-8", "UTF-16", "UTF-32", "latin-1", "ASCII"]
encoding = st.selectbox("Select the encoding of the CSV file:", encoding_options)

# Empty dataframe
df = pd.DataFrame()

# File uploader
uploaded_file = st.file_uploader("Select a CSV file", type="csv")

# Plots configuration
plots_config = {
    "First Plot": {'x': 'Datum', 'y': 'CTDI_vol', 'plot_type': 0},
    "Second Plot": {'x': 'Geschlecht', 'y': 'CTDI_vol', 'plot_type': 2},
    # Weitere Plots hinzufügen
}

# Create button to add a plot
if st.sidebar.button('Add Plot'):
    plot_name = st.sidebar.text_input('Enter plot name:')
    plots_config[plot_name] = {'x': 'Datum', 'y': 'CTDI_vol', 'plot_type': 0}

# Create button to remove a plot
if st.sidebar.button('Remove Plot'):
    plot_name = st.sidebar.selectbox('Select plot to remove', list(plots_config.keys()))
    del plots_config[plot_name]

# If a file is uploaded, read the CSV and display it as a dataframe
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding=encoding, sep=",")
    df['Datum'] = pd.to_datetime(df['Datum'], errors='coerce') # Convert date to datetime

    # Sidebar
    st.sidebar.title("Filter Settings")

    # Gender Selection
    st.sidebar.subheader("Gender Filter")
    filter_gender = st.sidebar.multiselect("Select Gender:", df["Geschlecht"].unique(), df["Geschlecht"].unique())

    # Institute Selection
    st.sidebar.subheader("Institute Filter")
    filter_institute = st.sidebar.multiselect("Select Institute:", df["Institut"].unique(), df["Institut"].unique())

    # Apply filters
    df = df[df["Geschlecht"].isin(filter_gender)]
    df = df[df["Institut"].isin(filter_institute)]

    # Create plots
    for plot_name, config in plots_config.items():
        plot_creation.create_plot(df, plots_config)

    # Separator
    st.sidebar.markdown("---")

    # Descriptive Statistics
    statistical_analysis.descriptive_statistics(df)

    # Missing Values
    statistical_analysis.missing_values_analysis(df)

    # Uncomment below lines for additional analyses
    # statistical_analysis.outlier_analysis(df)
    # statistical_analysis.distribution_analysis(df)
    # statistical_analysis.time_series_analysis(df)
    # statistical_analysis.t_test_analysis(df)
    # statistical_analysis.anova_analysis(df)
