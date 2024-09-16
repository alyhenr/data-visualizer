import base64
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

class DataModel:
    def __init__(self, file_path):
        """
        Initialize the DataModel object by reading a .txt file
        and parsing the first row as labels and the rest as data.
        """
        self.file_path = file_path
        self.data = self.read_file()
        self.labels = self.data.columns if self.data is not None else []

    def read_file(self):
        """
        Reads the .txt file and loads it into a pandas DataFrame.
        Assumes the first row contains the labels.
        """
        try:
            # Assume the first row has labels
            data = pd.read_csv(self.file_path, delimiter='\t', header=0)  # Tab-separated or change delimiter
            return data
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

    def show_summary(self):
        """
        Display a basic summary of the data (e.g., first few rows, description, etc.).
        """
        if self.data is not None:
            print("Labels:", self.labels)
            print(self.data.head())  # First few rows
            print(self.data.describe())  # Summary statistics
        else:
            print("No data to display.")

    def plot_column(self, column_name, plot_type='line'):
        """
        Plots data from a specific column.
        """
        if self.data is not None and column_name in self.data.columns:
            fig = Figure()
            buf = BytesIO()
            print("Creating plotting...")
            # plt.figure(figsize=(10, 6))
             # Check if the column is numeric
            if pd.api.types.is_numeric_dtype(self.data[column_name]):
                # Generate the appropriate plot for numeric columns
                if plot_type == 'line':
                    self.data[column_name].plot(kind='line')
                elif plot_type == 'hist':
                    self.data[column_name].plot(kind='hist', bins=10)
                else:
                    print("Unsupported plot type for numeric data.")
                    return None
            else:
                # For non-numeric data, we can only plot a bar chart of value counts
                if plot_type == 'bar':
                    self.data[column_name].value_counts().plot(kind='bar')
                else:
                    print("Only bar plots are supported for non-numeric data.")
                    return None
            plt.title(f'{plot_type.capitalize()} Plot for {column_name}')
            plt.xlabel(column_name)
            plt.ylabel('Values')
            fig.savefig(buf, format="png")
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            plt.show()
            data = None
            return data
        else:
            print(f"Column '{column_name}' not found in data.")

    def get_column_data(self, column_name):
        """
        Returns the data for a specific column (label).
        """
        if self.data is not None and column_name in self.data.columns:
            return self.data[column_name]
        else:
            print(f"Column '{column_name}' not found.")
            return None
