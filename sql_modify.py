import re
import os

# File paths (Modify these)
sql_file = "Batch_2022-26.sql"   # Change to your actual .sql file
photo_folder = "renamed_images"  # Change to your actual folder containing photos
output_sql_file = "Batch_2022-26_updated1.sql"  # Output file with photo column

# Read SQL file
with open(sql_file, "r", encoding="utf-8") as f:
    sql_data = f.read()

# Extract student_id values using regex (Pattern: 'AU/2022/0007520')
student_ids = re.findall(r"'(AU/\d{4}/\d{7})'", sql_data)

# Get list of available photo filenames (without .jpg extension)
photo_names = {f.split(".")[0] for f in os.listdir(photo_folder) if f.endswith(".jpg")}

# Function to format student_id -> AU20220007520
def format_student_id(student_id):
    return student_id.replace("/", "")

# Dictionary to store student_id -> photo mapping
photo_mapping = {}

# Count match and non-match
match_count = 0
no_match_count = 0

# Generate the mapping
for student_id in student_ids:
    formatted_id = format_student_id(student_id)
    photo_file = formatted_id + ".jpg"

    if formatted_id in photo_names:
        photo_mapping[student_id] = photo_file
        print(f"{student_id} - {photo_file} - match")
        match_count += 1
    else:
        photo_mapping[student_id] = "NULL"  # No photo found
        print(f"{student_id} - NO match")
        no_match_count += 1

# Modify SQL file: Add a 'photo' column and insert photo filenames
sql_modified = sql_data

# Add the 'photo' column if not present
if "photo" not in sql_modified:
    sql_modified = re.sub(r"(\(.*?student_id.*?)(\))", r"\1, photo TEXT\2", sql_modified, flags=re.DOTALL)

# Update 'INSERT' statements to include photo filenames
def replace_insert_statements(match):
    values = match.group(1)
    student_id_match = re.search(r"'(AU/\d{4}/\d{7})'", values)

    if student_id_match:
        student_id = student_id_match.group(1)
        photo_value = f"'{photo_mapping.get(student_id, 'NULL')}'"
        return f"({values}, {photo_value})"

    return match.group(0)

sql_modified = re.sub(r"\(([^)]+)\)", replace_insert_statements, sql_modified)

# Save the modified SQL file
with open(output_sql_file, "w", encoding="utf-8") as f:
    f.write(sql_modified)

# Display summary
print("\nSummary:")
print(f"Total Matches: {match_count}")
print(f"Total Non-Matches: {no_match_count}")
print(f"Updated SQL file saved as: {output_sql_file}")
