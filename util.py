import pandas as pd
import streamlit as st
from plotting_utils import Plotter
from scipy.stats import mannwhitneyu

def handle_tab(file: pd.DataFrame, file_basename, col_target, analysis_type, analysis_level, component, threshold=None):
    for column in col_target:
        file = clean_data(file=file, file_basename=file_basename, component=component, column=column, threshold_limit=threshold)
        plotter = Plotter(file)
        if analysis_type == "Line Chart":
            fig = plotter.plotly_line_chart(column, analysis_level=analysis_level)
            st.plotly_chart(fig)
        elif analysis_type == "Histogram":
            fig = plotter.plotly_histogram(column, analysis_level=analysis_level)
            st.plotly_chart(fig)
        elif analysis_type == "Boxplot":
            fig = plotter.plotly_boxplot(column, analysis_level=analysis_level)
            st.plotly_chart(fig)

def handle_comparison(file: pd.DataFrame, col_target, analysis_type, component, threshold=None):
    for column in col_target:
        file = clean_data(file=file, file_basename=None, component=component, column=column, threshold_limit=threshold)
        calculate_mann_whitney_u_test(df=file, column=column)
        calculate_z_test(df=file, column=column)
        plotter = Plotter(file)
        if analysis_type == "Line Chart":
            fig = plotter.plotly_compare_line_chart(column)
            st.plotly_chart(fig)
            pass
        elif analysis_type == "Histogram":
            fig = plotter.plotly_compare_histogram(column)
            st.plotly_chart(fig)
            pass
        elif analysis_type == "Boxplot":
            fig = plotter.plotly_compare_boxplot(column)
            st.plotly_chart(fig)
            pass

def clean_data(file: pd.DataFrame, file_basename, component, column, threshold_limit):
    st.subheader(f'{column.capitalize()}')

    threshold_value = file[column].quantile(threshold_limit)
    _file = file[file[column] <= threshold_value]
    st.write(f'For {component.capitalize()} in {file_basename}, originally had {len(file)} samples.')
    st.write(f'Following the threshold limit of {threshold_limit} for "{column.capitalize()}" column, we have removed {len(file) - len(_file)} samples.')
    _file_stats = _file[column].describe()
    st.dataframe(_file_stats)
    return _file

def calculate_mann_whitney_u_test(df, column):
    #TODO: Unmock this
    data1 = df[df['fleet'] == '785C'][column]
    data2 = df[df['fleet'] == '793F'][column]
    stat, p = mannwhitneyu(data1, data2, alternative='two-sided')
    
    st.subheader(f'{column.capitalize()} - Mann-Whitney U Test Results')
    st.write(f'Statistic: {stat}, p-value: {p}')
    
    if p < 0.05:
        st.write("There are significant differences between the two groups.")
    else:
        st.write("There is no significant difference between the two groups.")

def calculate_z_test(df, column):
    #TODO: Unmock this
    data1 = df[df['fleet'] == '785C'][column]
    data2 = df[df['fleet'] == '793F'][column]
    
    mean1 = data1.mean()
    mean2 = data2.mean()
    std1 = data1.std()
    std2 = data2.std()
    n1 = len(data1)
    n2 = len(data2)
    
    z_score = (mean1 - mean2) / ((std1**2/n1 + std2**2/n2)**0.5)
    
    st.subheader(f'{column.capitalize()} - Z-Test Results')
    st.write(f'Z-Score: {z_score}')
    
    critical_value = 1.96  # For a two-tailed test with alpha=0.05
    if abs(z_score) > critical_value:
        st.write("There are significant differences between the two groups.")
    else:
        st.write("There is no significant difference between the two groups.")
