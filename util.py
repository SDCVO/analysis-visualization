import pandas as pd
import streamlit as st

from plotting_utils import Plotter



def handle_tab(file: pd.DataFrame, col_target, analysis_type, analysis_level, component):    
    plotter = Plotter(file)
    for column in col_target:
        st.subheader(f"{analysis_type} of {column.capitalize()} Across All Equipment for {component.capitalize()}")
        if analysis_type == "Line Chart":
            fig = plotter.plot_temporal_analysis(columns=column, analysis_level=analysis_level)
            st.pyplot(fig)
        elif analysis_type == "Histogram":
            fig = plotter.plot_histogram(column, analysis_level)
            st.pyplot(fig)
        elif analysis_type == "Boxplot":
            fig = plotter.plot_boxplot(column, analysis_level)
            st.pyplot(fig)





