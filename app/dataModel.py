import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import io
import base64

class DataModel:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.read_file()
        self.labels = self.data.columns if self.data is not None else []

    def read_file(self):
        try:
            # Read the file with tab delimiter and infer header row
            data = pd.read_csv(self.file_path, delimiter='\t', header=0)
            return data
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

    def plot_column(self, column_name, plot_type='line'):
        """
        Plots data from a specific column and returns the plot as a base64-encoded image.
        """
        if self.data is not None and column_name in self.data.columns:
            plt.figure(figsize=(10, 6))

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

            # Set plot title and labels
            plt.title(f'{plot_type.capitalize()} Plot for {column_name}')
            plt.xlabel(column_name)
            plt.ylabel('Values')

            # Save the plot to a BytesIO object instead of a file
            img = io.BytesIO()
            plt.savefig(img, format='png')
            plt.close()  # Close the plot to avoid display in GUI

            # Encode the image to base64 to send as a string
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode('utf-8')
            img.close()

            return plot_url
        else:
            print(f"Column '{column_name}' not found in data.")
            return None


    def get_column_data(self, column_name):
        """
        Returns the data for a specific column (label).
        """
        if self.data is not None and column_name in self.data.columns:
            return self.data[column_name]
        else:
            print(f"Column '{column_name}' not found.")
            return None
