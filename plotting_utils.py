# plotting_utils.py

import matplotlib.pyplot as plt
import plotly.express as px


class Plotter:
    def __init__(self, data):
        self.data = data

    def plotly_line_chart(self, column: str, analysis_level="Entire Fleet"):
        if analysis_level == "Entire Fleet":
            fig = px.line(
                data_frame=self.data,
                x='sample_dt',
                y=column,
                labels={'x': 'Sample Date', 'y': column.capitalize()},
                title=f'Time Series Analysis of {column.capitalize()} Over Time'
            )
        else:
            fig = px.line(
                data_frame=self.data,
                x='sample_dt',
                y=column,
                color='equip_number',
                labels={'x': 'Sample Date', 'y': column.capitalize()},
                title=f'Time Series Analysis of {column.capitalize()} Over Time'
            )
            
        
        return fig

    def plotly_histogram(self, column: str, analysis_level="Entire Fleet"):
        if analysis_level == "Entire Fleet":
            fig = px.histogram(
                data_frame=self.data, 
                x=column, 
                nbins=30,
                title=f'Histogram of {column.capitalize()} Across All Equipment',
            )
        else:
            fig = px.histogram(
                data_frame=self.data, 
                x=column, 
                nbins=30,
                color='equip_number',
                title=f'Histogram of {column.capitalize()} Across All Equipment',
            )
        return fig

    def plotly_boxplot(self, column: str, analysis_level="Entire Fleet"):
        if analysis_level == "Entire Fleet":
            fig = px.box(
                data_frame=self.data, 
                y=column, 
                orientation='v',
                title=f'Boxplot of {column.capitalize()} Across All Equipment',
            )
        else:
            fig = px.box(
                data_frame=self.data,
                y=column, 
                x='equip_number', 
                orientation='v',
                color='equip_number',
                title=f'Boxplot of {column.capitalize()} Across All Equipment',
            )        
        return fig

    def plotly_compare_line_chart(self, column: str):
        fig = px.line(
            data_frame=self.data,
            x='sample_dt',
            y=column,
            color='fleet',
            labels={'x': 'Sample Date', 'y': column.capitalize()},
            title=f'Time Series Analysis of {column.capitalize()} Over Time'
        )
        return fig
    
    def plotly_compare_histogram(self, column: str):
        fig = px.histogram(
            data_frame=self.data, 
            x=column, 
            nbins=30,
            color='fleet',
            title=f'Histogram of {column.capitalize()} Across All Equipment',
        )
        return fig
    
    def plotly_compare_boxplot(self, column: str):
        fig = px.box(
            data_frame=self.data,
            y=column,
            x='fleet',  
            orientation='v',
            color='fleet',
            title=f'Boxplot of {column.capitalize()} Across All Equipment',
        )        
        return fig