# plotting_utils.py

import matplotlib.pyplot as plt
import seaborn as sns

class Plotter:
    def __init__(self, data):
        self.data = data

    def plot_temporal_analysis(self, columns, analysis_level="Entire Fleet"):
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if analysis_level == "Entire Fleet":
                ax.plot(
                    self.data['sample_dt'],
                    self.data[columns],
                    label=columns,
                    marker='o',
                    linestyle='-'
                )
        else:
            unique_equip_numbers = self.data["equip_number"].unique()
            for equip_number in unique_equip_numbers:
                subset_data = self.data[self.data["equip_number"] == equip_number].sort_values(by='sample_dt')

                ax.plot(
                    subset_data['sample_dt'],
                    subset_data[columns],
                    label=f'{columns} - equip_number: {equip_number}',
                    marker='o',
                    linestyle='-'
                )
        # Adjust x-axis properties
        ax.set_xlim(min(self.data['sample_dt']), max(self.data['sample_dt']))
        ax.set_xticks(range(0, len(self.data['sample_dt']), 10))  # Adjust the step as needed
        
        
        plt.title(f'Temporal Analysis of {columns.capitalize()} Across All Equipment')
        plt.xlabel('Sample Date')
        plt.ylabel('Values')
        plt.legend()
        return fig

    def plot_histogram(self, column, analysis_level="Entire Fleet"):
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if analysis_level == "Entire Fleet":
            self.data[column].hist(bins=20, alpha=0.5, label='Entire Fleet', ax=ax)
        else:
            for equip_number, group in self.data.groupby('equip_number'):
                group[column].hist(bins=20, alpha=0.5, label=f'equip_number: {equip_number}', ax=ax)
        plt.title(f'Histogram of {column.capitalize()} Across All Equipment')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.legend()
        return fig

    def plot_boxplot(self, column, analysis_level="Entire Fleet"):
        fig, ax = plt.subplots(figsize=(10, 6))

        if analysis_level == "Entire Fleet":
            sns.boxplot(y=column, data=self.data, ax=ax)

            # Calculate Q3 and Q1
            q1 = self.data[column].quantile(0.25)
            q3 = self.data[column].quantile(0.75)
            iqr = q3 - q1

            # Find outliers
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            # Annotate Q3-Q1 and outliers
            ax.text(0.95, 0.95, f'IQR: {iqr:.2f}', transform=ax.transAxes, ha='right', va='top')
            ax.text(0.95, 0.90, f'Lower Bound: {lower_bound:.2f}', transform=ax.transAxes, ha='right', va='top')
            ax.text(0.95, 0.85, f'Upper Bound: {upper_bound:.2f}', transform=ax.transAxes, ha='right', va='top')

        else:
            sns.boxplot(x='equip_number', y=column, data=self.data, ax=ax)

        plt.title(f'Boxplot of {column.capitalize()} Across All Equipment')
        plt.xlabel('Equip Number')
        plt.ylabel(column.capitalize())
        return fig

