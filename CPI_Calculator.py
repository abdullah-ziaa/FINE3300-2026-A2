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
        self.data["date"] = pd.to_datetime(self.data["date"], format="%Y-%m-%d")

        # Create a lookup dictionary for CPI values based on year and month
        cpi_lookup = {}
        for i in range(len(self.data)):
            d = self.data["date"].iloc[i]
            key = (d.year, d.month)
            if key not in cpi_lookup:
                cpi_lookup[key] = self.data["CPI"].iloc[i]

        # Create a list of annual changes in CPI for each year and Loop over the data rows and compare CPI values to the same month in the previous year to calculate the annual percent change
        annual_change = []
        for i in range(len(self.data)):
            d = self.data["date"].iloc[i]
            prev = cpi_lookup.get((d.year - 1, d.month))
            if prev is None:
                annual_change.append(np.nan)
            else:
                annual_change.append((self.data["CPI"].iloc[i] - prev) / prev * 100)
        self.data["Annual Percent Change"] = annual_change

        # Set first and last dates for validation purposes
        self.first_date = self.data["date"].iloc[0]
        self.last_date = self.data["date"].iloc[-1]

    def get_cpi(self, year, month):
        target_date = pd.Timestamp(year, month, 1)

        return self.data[self.data["date"] == target_date]["CPI"].iloc[0]


