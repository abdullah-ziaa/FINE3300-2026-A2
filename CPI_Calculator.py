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
            loc = self.data["date"].iloc[i]
            entry = (loc.year, loc.month)
            if entry not in cpi_lookup:
                cpi_lookup[entry] = self.data["CPI"].iloc[i]

        # Create a list of annual changes in CPI for each year and Loop over the data rows and compare CPI values to the same month in the previous year to calculate the annual percent change
        annual_change = []
        for i in range(len(self.data)):
            loc = self.data["date"].iloc[i]
            prev = cpi_lookup.get((loc.year - 1, loc.month))
            if prev is None:
                annual_change.append(np.nan)
            else:
                annual_change.append((self.data["CPI"].iloc[i] - prev) / prev * 100)
        self.data["Annual Percent Change"] = annual_change

        # Store the first and last dates in the dataset for reference and validation
        self.first_date = self.data["date"].iloc[0]
        self.last_date = self.data["date"].iloc[-1]

    # Calculate the CPI for a given year and month by looking it up in the data
    def get_cpi(self, year, month):
        target_date = pd.Timestamp(year, month, 1)

        return self.data[self.data["date"] == target_date]["CPI"].iloc[0]

    # Validate the input date to ensure it is in the correct format and within the range of available data
    def date_validation(self, text):
        while True:
            # Convert the input string to a datetime object and check if it is within the range of available data
            date_str = input(text)
            # Use a try-except block to handle invalid date formats and out-of-range dates
            try:
                date = dt.datetime.strptime(date_str, "%Y-%m")
                if self.first_date <= date <= self.last_date:
                    return (date.year, date.month)
                else:
                    print(f"Date must be between {self.first_date.strftime('%Y-%m')} and {self.last_date.strftime('%Y-%m')}. Please try again.")
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM format.")

    # Calculate the new amount and percent change based on the CPI values for two given dates
    def get_apc(self, amount, date1, date2):
        # Get the CPI values for the two dates using the get_cpi method
        cpi1 = self.get_cpi(date1[0], date1[1])
        cpi2 = self.get_cpi(date2[0], date2[1])

        # Calculate the ratio of the two CPI values and use it to calculate the new amount and percent change
        ratio = cpi2 / cpi1
        new_amount = amount * ratio
        percent_change = (ratio - 1) * 100

        # Calculate the number of months and years between the two dates
        months = (date2[0] - date1[0]) * 12 + (date2[1] - date1[1])
        years = months / 12

        # Calculate the annualized rate of change using the formula for compound annual growth rate (CAGR)
        if years == 0:
            annual_rate = 0.0
        else: 
            annual_rate = (ratio ** (1 / years) - 1) * 100

        return {
            "CPI1": cpi1,
            "CPI2": cpi2,
            "New Amount": new_amount,
            "Percent Change": percent_change,
            "Years": years,
            "Annual Rate": annual_rate
        }

    def run(self):
        # Prompt the user for amount value and validate the input to ensure it is a non-negative number
        while True:
            try:
                amount = float(input("Enter the amount: "))
                if amount < 0:
                    print("Amount must be a non-negative number. Please try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        # Prompt the user for two dates and validate the input to ensure they are in the correct format and within the range of available data
        date1 = self.date_validation("Enter the first date (YYYY-MM): ")
        date2 = self.date_validation("Enter the second date (YYYY-MM): ")

        # Convert the input strings to tuples of integers representing year and month
        date1 = (int(date1[0]), int(date1[1]))
        date2 = (int(date2[0]), int(date2[1]))

        # Call the get_apc method to calculate the new amount and percent change
        result = self.get_apc(amount, date1, date2)

        # Print the results in a formatted manner
        print(f"\nPercent Change: {result['Percent Change']:.2f}%")
        print(f"Years between dates: {result['Years']:.2f}")
        print(f"Annual Rate of Change: {result['Annual Rate']:.2f}%")
        print(f"CPI on {date1[0]}-{date1[1]:02d}: {result['CPI1']:.2f}")
        print(f"CPI on {date2[0]}-{date2[1]:02d}: {result['CPI2']:.2f}")
        print(f"New Amount: {result['New Amount']:.2f}")

if __name__ == "__main__":
    calculator = CPI_Calculator("STATIC_INFLATIONCALC.csv")
    calculator.run()