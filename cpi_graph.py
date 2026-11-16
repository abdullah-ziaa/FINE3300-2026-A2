# Import necessary libraries
import matplotlib.pyplot as plt
from cpi_calc import cpi_calc

# Open the CSV file and create a CPI_Calculator object to load the data
calc = cpi_calc("STATIC_INFLATIONCALC.csv")
df = calc.data

# Create a line plot of the CPI data over time
fig, ax = plt.subplots(figsize=(12, 6))

# Set the title, labels, and grid for the plot, and set the x-axis limits to the first and last dates in the dataset
ax.set_title("Canada Consumer Price Index (CPI), 1914-2026", fontsize=16)
ax.set_xlabel("Year", fontsize=14)
ax.set_ylabel("CPI, 2002=100", fontsize=14)
ax.grid()
x_min = df["date"].iloc[0]
y_min = df["date"].iloc[-1]
ax.set_xlim(x_min, y_min)

# Plot the CPI data as a blue line and add a red dashed line at the base year (2002) for reference
cpi_line = ax.plot(df["date"], df["CPI"], label="CPI", color="blue", linewidth=2)
line_base = ax.plot([df["date"].iloc[0], df["date"].iloc[-1]], [100, 100], color="red", linestyle="--", label="Base Year")

