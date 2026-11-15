import datetime as dt
import numpy as np
import pandas as pd

class CPI_Calculator:
    def __init__(self, filename):
        self.data = pd.read_csv(filename, skiprows=8)

        self.data.columns = ["date", "CPI"]

        self.data["date"] = pd.to_datetime(self.data["date"], format="%Y-%m-%d")

        self.data = self.data.reset_index(drop=True)