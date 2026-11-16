# Import necessary libraries
import matplotlib.pyplot as plt
import cpi_calc

# Create an instance of the CPI_Calculator class and load the CPI data from the CSV file
calc = cpi_calc.CPI_Calculator("STATIC_INFLATIONCALC.csv")
df = calc.data

# Create a plot of the CPI data and the annual percent change in CPI using Matplotlib
fig, ax = plt.subplots(figsize=(12, 6))

# Plot the CPI data and the annual percent change in CPI on the same graph with dual y-axes
ax.set_title("Canada Consumer Price Index (CPI), 1914-2026", fontsize=16)
ax.set_xlabel("Year")
ax.set_ylabel("CPI, 2002=100")
ax.grid()

# Plot the CPI data and the base year line (2002=100) on the left y-axis
cpi_line = ax.plot(df["date"], df["CPI"], color="C0")
line_base = ax.plot([df["date"].iloc[0], df["date"].iloc[-1]], [100, 100], color="k", linestyle=":")

# Create a secondary y-axis for the annual percent change in CPI and plot it on the right y-axis
ax2 = ax.inset_axes([0, 0, 1, 1])
ax2.patch.set_alpha(0.0)
line_pct = ax2.plot(df["date"], df["Annual Percent Change"], color="C3", linewidth=0.8, alpha=0.6)


ax2.set_xticks([])
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")
ax2.set_ylabel("Annual Percent Change in CPI")

# Add a legend to the graph to identify the different lines and their corresponding data
ax.legend([cpi_line[0], line_base[0], line_pct[0]], ["CPI (left)", "Base Year (2002)", "Annual Percent Change (right)"], loc="upper center")

# Adjust the layout of the graph to ensure that all elements are properly displayed and save the graph as a PNG file with a resolution of 150 dpi. Finally, display the graph using plt.show().
fig.tight_layout()
fig.savefig("cpi_graph.png", dpi=150)
plt.show()
