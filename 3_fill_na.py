import pandas as pd

# Load the existing Excel file
input_file = "updated_file.xlsx"  # Replace with your actual file
output_file = "final_updated_file.xlsx"  # Output file

# Read the Excel file
df = pd.read_excel(input_file)

# Fill all blank values with 'na' except for 'upload_date_time'
df = df.fillna("na")  # Fill all NaN values with 'na'
df["upload_date_time"] = ""  # Keep 'upload_date_time' blank

# Save to a new file
df.to_excel(output_file, index=False)

print(f"Final updated file saved as: {output_file}")
