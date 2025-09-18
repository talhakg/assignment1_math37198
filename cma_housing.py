import pandas as pd
import matplotlib.pyplot as plt

# read the csv file
df = pd.read_csv("chmc-cma.csv")

# get the row with total housing units
total_units = df[df["Type of unit"] == "Total units"].iloc[0]

# months of the year
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# function to get values for a given year
def get_values(year):
    values = []
    for m in months:
        # clean formatting by removing commas and convert strings to integers
        values.append(int(str(total_units[f"{m}-{year}"]).replace(",", "")))
    return values

# create the dataframe with columns months and 2014 vs 2024 
table = pd.DataFrame({
    "Month": months,
    "2014": get_values("14"),
    "2024": get_values("24")
}).set_index("Month")

# print the table to show the summary statistics
print(table[["2014","2024"]].describe())

# create a bar chart
table[["2014", "2024"]].plot.bar()
plt.title("2014 vs 2024 Monthly Housing Units")
plt.xlabel("Month")
plt.ylabel("Units")
plt.legend(["2014","2024"])
plt.show()