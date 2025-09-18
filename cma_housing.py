import pandas as pd
import matplotlib.pyplot as plt

# read the csv file
df = pd.read_csv("chmc-cma.csv")

# get the row with total housing units
total_units = df[df["Type of unit"] == "Total units"].iloc[0]

# months of the year
months = ["Jan","Feb","Mar","Apr","May","Jun",
          "Jul","Aug","Sep","Oct","Nov","Dec"]

# function to get values for a given year
def get_values(year):
    values = []
    for m in months:
        # Remove commas and convert strings to integers
        values.append(
            int(str(total_units[f"{m}-{year}"]).replace(",", "")))
    return values

# create the dataframe with columns months and 2014 vs 2024 
table = pd.DataFrame({
    "Month": months,
    "2014": get_values("14"),
    "2024": get_values("24")
}).set_index("Month")

# print the table to show the summary statistics
print(table[["2014","2024"]].describe().round(2))

# create a bar chart
table[["2014", "2024"]].plot.bar()
plt.title("2014 vs 2024 Monthly Housing Units")
plt.xlabel("Month")
plt.ylabel("Units")
plt.legend(["2014","2024"])
plt.show()

# Get the month values across all the years
all_units = []
for column in df.columns:
    if "-" in column and column.split("-")[0] in months:
        # clean the values and add it to the list
        all_units.append(
            int(str(total_units[column]).replace(",","")))

# calculate the mean
mean_value = sum(all_units) / len(all_units)

# calculate the standard deviation
number = sum((x - mean_value) ** 2 for x in all_units)
n_minus_one = len(all_units) - 1
std_value = (number / n_minus_one) ** 0.5

# calculate the z-score for dec 2024
z_score = (table.loc["Dec", "2024"] - mean_value) / std_value

# print all calculations
print(f"Mean: {mean_value:.2f}")
print(f"Standard Deviation: {std_value:.2f}")
print(f"Z-score for December 2024: {z_score:.2f}")

# explain the result of the z-score
print("Interpretation: Dec 2024 is",
      "higher than" if z_score > 0 
      else "lower than" if z_score < 0 
      else "equal to",
      "the total average.")