import pandas as pd
import matplotlib.pyplot as plt

# STEP 1 _________________________________________________________________
# read the csv file
df = pd.read_csv("chmc-cma.csv")

# get the row with total housing units
total_units = df[df["Type of unit"] == "Total units"].iloc[0]

# months of the year
months = ["Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"]

# STEP 2 _________________________________________________________________
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

# STEP 3 _________________________________________________________________
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
print("Interpretation: Dec 2024 is", "higher than" 
    if z_score > 0 
    else "lower than" 
    if z_score < 0 
    else "equal to", "the total average.")

# STEP 4 _________________________________________________________________
# change two digit year to full year
def parse_year(two_digit_year):
    record_year = int(two_digit_year)
    if record_year >= 90:
        return 1900 + record_year
    else:
        return 2000 + record_year

# store all year, month, and units
monthly_records = []
for column_name in df.columns:
    if "-" in column_name and column_name.split("-")[0] in months:
        selected_month, selected_year = column_name.split("-")
        full_year = parse_year(selected_year)
        month_index = months.index(selected_month) + 1
        units = int(str(total_units[column_name]).replace(",", ""))
        monthly_records.append((full_year, month_index, units))

# check if the year and month are within range
def within_range(record_year, record_month, start_year, 
                start_month, end_year, end_month):
    if record_year > start_year:
        start = True
    elif record_year == start_year and record_month >= start_month:
        start = True
    else:
        start = False
    if record_year < end_year:
        end = True
    elif record_year == end_year and record_month <= end_month:
        end = True
    else:
        end = False
    return start and end

# data for both harper and trudeau
harper = []
for (record_year, record_month, record_units) in monthly_records:
    if within_range(record_year, record_month, 2006, 2, 2015, 10):
        harper.append(record_units)

trudeau = []
for (record_year, record_month, record_units) in monthly_records:
    if within_range(record_year, record_month, 2015, 11, 9999, 12):
        trudeau.append(record_units)

# cutoff units
unit_cutoff = 10000

# probability for both harper and trudeau
harper_success = sum(1 for record_units in harper if record_units > unit_cutoff)
harper_probability = harper_success / len(harper)

trudeau_success = sum(1 for record_units in trudeau if record_units > unit_cutoff)
trudeau_probability = trudeau_success / len(trudeau)

# print the probabilities for both harper and trudeau
print(f"Harper (more than 10,000 units): {harper_probability:.2f} "
    f"({harper_success} out of {len(harper)} months)")

print(f"Trudeau (more than 10,000 units): {trudeau_probability:.2f} "
    f"({trudeau_success} out of {len(trudeau)} months)")

# compare the results
if harper_probability > trudeau_probability:
    print("Compare: Harper has a higher probability than Trudeau")
elif trudeau_probability > harper_probability:
    print("Compare: Trudeau has a higher probability than Harper")
else:
    print("Compare: Both have the same probability")