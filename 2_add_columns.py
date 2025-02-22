import pandas as pd
import os

# Load existing Excel file
input_file = "college_data_updated.xlsx"  # Replace with your actual file
output_file = "updated_file.xlsx"  # Output file
photo_folder = "renamed_images"  # Replace with your actual photo folder path

# Read the Excel file
df = pd.read_excel(input_file)

# Ensure required columns exist
df["photo"] = ""
df["upload_date_time"] = ""
df["twelfth_percentage"] = 0
df["twelfth_school"] = "na"

# Get list of photo filenames from the folder
photo_files = {f for f in os.listdir(photo_folder) if f.endswith(".jpg")}

# Function to convert student ID to filename format
def format_student_id(student_id):
    return student_id.replace("/", "").strip() + ".jpg"

# Update 'photo' column based on matching filenames
for index, row in df.iterrows():
    student_id = str(row["student_id"])  # Assuming column name is 'student_id'
    photo_filename = format_student_id(student_id)
    
    if photo_filename in photo_files:
        df.at[index, "photo"] = photo_filename

# Save to a new file
df.to_excel(output_file, index=False)

print(f"Updated file saved as: {output_file}")
