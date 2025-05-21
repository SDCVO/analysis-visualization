import pandas as pd
import streamlit as st
from plotting_utils import Plotter

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