import pandas as pd
import glob
import os

# Create output folder if it doesn't exist
os.makedirs("output", exist_ok=True)

# Read all CSV files from data folder
files = glob.glob("data/*.csv")

# Combine all CSV files into one dataframe
df_list = [pd.read_csv(file) for file in files]
df = pd.concat(df_list, ignore_index=True)

# Keep only Pink Morsel products
df = df[df["product"].str.lower() == "pink morsel"]

# Clean price column by removing $ sign
df["price"] = (
    df["price"]
    .replace("[$,]", "", regex=True)
    .astype(float)
)

# Create sales column
df["sales"] = df["quantity"] * df["price"]

# Keep only required columns
output_df = df[["sales", "date", "region"]]

# Save final output CSV
output_df.to_csv("output/formatted_output.csv", index=False)

print("Data processing completed successfully.")