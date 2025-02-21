import os
import shutil
import pandas as pd

# Define paths
image_folder = r"C:\Users\chaya\Desktop\AUCSE\AUCSE_web_scrapping\images"
excel_file = r"C:\Users\chaya\Desktop\AUCSE\AUCSE_web_scrapping\college_data_updated.xlsx"
renamed_folder = os.path.join(image_folder, "renamed_images")  # Folder for renamed images

# Create the renamed_images folder if it doesn't exist
os.makedirs(renamed_folder, exist_ok=True)

# Load Excel file
df = pd.read_excel(excel_file)

# Ensure column names match your Excel sheet
roll_no_column = "roll_no"
student_id_column = "student_id"

# Function to convert roll number format to image name
def convert_roll_no(roll_no):
    return roll_no.replace("/", "") + ".jpg"

# Initialize counters
found_count = 0
not_found_count = 0
renamed_count = 0

# Print header
print("Student ID - Roll No - Image Name - Status")

# Iterate through DataFrame rows to ensure correct mapping
for _, row in df.iterrows():
    student_id = row[student_id_column]  # Get student ID
    roll_no = row[roll_no_column]  # Get roll number
    image_name = convert_roll_no(roll_no)  # Convert roll number to image format
    new_image_name = student_id.replace("/", "") + ".jpg"  # Format new filename (AU20220006955.jpg)

    # Check if the image exists in the folder
    old_image_path = os.path.join(image_folder, image_name)
    new_image_path = os.path.join(renamed_folder, new_image_name)

    if os.path.exists(old_image_path):
        status = "found"
        found_count += 1

        # Copy and rename the image to the new folder
        shutil.copy(old_image_path, new_image_path)
        renamed_count += 1
        status += " - renamed"
    else:
        status = "not found"
        not_found_count += 1

    # Print the result
    print(f"{student_id} - {roll_no} - {image_name} - {status}")

# Print summary
print("\nSummary:")
print(f"Total Found: {found_count}")
print(f"Total Renamed: {renamed_count}")
print(f"Total Not Found: {not_found_count}")
