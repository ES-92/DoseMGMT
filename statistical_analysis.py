import streamlit as st
from scipy.stats import zscore, ttest_ind
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf

def descriptive_statistics(df):
    st.write("### Descriptive Statistics")
    st.write(df.describe())

def missing_values_analysis(df):
    st.write("### Missing Values Analysis")
    st.write(df.isnull().sum())

def outlier_analysis(df):
    z_scores = zscore(df['CTDI_vol'])
    outliers = df[(z_scores > 2) | (z_scores < -2)]
    st.write("### Outlier Analysis")
    st.write(outliers)

def distribution_analysis(df):
    st.write("### Distribution Analysis")
    sns.histplot(df['CTDI_vol'])
    sns.kdeplot(df['CTDI_vol'])
    st.pyplot()

def time_series_analysis(df):
    if 'Datum' in df.columns:
        st.write("### Time Series Analysis")
        df['CTDI_vol'] = df['CTDI_vol'].interpolate()
        decomposition = seasonal_decompose(df['CTDI_vol'], model='additive', period=1)

        st.write("Trend:")
        st.line_chart(decomposition.trend)

        plot_acf(df['CTDI_vol'])
        st.pyplot()

def t_test_analysis(df):
    if 'Geschlecht' in df.columns:
        st.write("### T-Test Analysis")
        group1 = df[df['Geschlecht'] == 'M']['CTDI_vol']
        group2 = df[df['Geschlecht'] == 'F']['CTDI_vol']
        t_stat, p_val = ttest_ind(group1, group2)
        st.write(f"T-Statistic: {t_stat}, P-Value: {p_val}")

def anova_analysis(df):
    if 'Institut' in df.columns:
        st.write("### ANOVA Analysis")
        anova_res = stats.f_oneway(df['CTDI_vol'][df['Institut'] == 'Inst1'],
                                   df['CTDI_vol'][df['Institut'] == 'Inst2'],
                                   df['CTDI_vol'][df['Institut'] == 'Inst3'])
        st.write(f"F-Statistic: {anova_res.statistic}, P-Value: {anova_res.pvalue}")
