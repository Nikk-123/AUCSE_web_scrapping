import pandas as pd

# Configuration
input_file = "final_updated_file.xlsx"  # Replace with your actual Excel file
output_sql_file = "output22-26.sql"
table_name = "cse_22_26"  # Define table name as a variable

# Define expected schema (without primary key)
schema = [
    ("name", "varchar(255)", "NO", "NULL"),
    ("student_id", "varchar(100)", "NO", "NULL"),
    ("roll_no", "varchar(100)", "NO", "NULL"),
    ("sec", "varchar(10)", "NO", "NULL"),
    ("aoi", "varchar(255)", "NO", "'N/A'"),
    ("email", "varchar(250)", "NO", "NULL"),
    ("phone", "bigint", "NO", "NULL"),
    ("course", "varchar(250)", "NO", "NULL"),
    ("year", "int", "NO", "NULL"),
    ("photo", "varchar(100)", "NO", "NULL"),
    ("status", "int", "NO", "NULL"),
    ("upload_date_time", "varchar(20)", "NO", "'2025-02-12 09:13 AM'"),  # Default value added
    ("twelfth_percentage", "float", "NO", "NULL"),
    ("twelfth_school", "varchar(255)", "NO", "NULL"),
]

# Read Excel file
df = pd.read_excel(input_file)

# Check for missing columns
missing_columns = [col[0] for col in schema if col[0] not in df.columns]

if missing_columns:
    print(f"Missing columns in Excel: {', '.join(missing_columns)}")
else:
    print("All required columns are present.")

# Open SQL file for writing
with open(output_sql_file, "w", encoding="utf-8") as sql_file:
    # Write CREATE TABLE statement
    sql_file.write(f"CREATE TABLE {table_name} (\n")
    column_definitions = []
    for col_name, col_type, is_nullable, col_default in schema:
        default_clause = f" DEFAULT {col_default}" if col_default != "NULL" else ""
        column_definitions.append(f"  {col_name} {col_type} {'NOT NULL' if is_nullable == 'NO' else ''}{default_clause}")
    sql_file.write(",\n".join(column_definitions))  # ✅ No extra comma at the end
    sql_file.write("\n);\n\n")  # ✅ Correctly closes the statement

    # Write INSERT statements
    for _, row in df.iterrows():
        values = []
        for col_name, col_type, _, col_default in schema:
            value = row[col_name] if col_name in df.columns else col_default

            # Handle NULL values
            if pd.isna(value) or value == "NULL":
                if col_name == "upload_date_time":
                    value = "'2025-02-12 09:13 AM'"  # Assign dummy value
                elif col_default != "NULL":
                    value = col_default
                else:
                    value = "NULL"
            else:
                if "varchar" in col_type or col_type == "date":
                    value = f"'{str(value).replace('\'', '\'\'')}'"
                elif col_type in ["bigint", "int", "float"]:
                    value = str(value)

            values.append(value)

        sql_file.write(f"INSERT INTO {table_name} ({', '.join([col[0] for col in schema])}) VALUES ({', '.join(values)});\n")

print(f"SQL file generated: {output_sql_file}")
