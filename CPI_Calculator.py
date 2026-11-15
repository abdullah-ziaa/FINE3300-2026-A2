# Import necessary libraries
import datetime as dt
import numpy as np
import pandas as pd

# Define the CPI_Calculator class that will load CPI data and answers
class CPI_Calculator:
    def __init__(self, filename):
        # Load the CPI data from a CSV file (in our case, skip the first 8 rows since data starts from row 9)
        self.data = pd.read_csv(filename, skiprows=8)

        # Rename the columns to "date" and "CPI" for easier access
        self.data.columns = ["date", "CPI"]

        # Convert the "date" column to datetime format for easier manipulation and analysis
        self.data["date"] = pd.to_datetime(self.data["date"], format="%Y-%m-%d")]

        # Reset the index of the DataFrame to ensure it starts from 0 and is sequential
        self.data = self.data.reset_index(drop=True)