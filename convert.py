import pandas as pd

# Load Excel file
file_path = "college_data_updated.xlsx"  # Change this to your file path
table_name = "your_table"      # Change this to your desired table name

df = pd.read_excel(file_path)

# Generate SQL statements
sql_statements = []
sql_statements.append(f"CREATE TABLE IF NOT EXISTS `{table_name}` (\n    id INT AUTO_INCREMENT PRIMARY KEY,")  # Add columns dynamically

for col in df.columns:
    sql_statements.append(f"    `{col}` TEXT,")

sql_statements[-1] = sql_statements[-1][:-1]  # Remove last comma
sql_statements.append(");\n")

# Insert data into the table
for _, row in df.iterrows():
    values = "', '".join(str(x).replace("'", "''") for x in row)
    sql_statements.append(f"INSERT INTO `{table_name}` ({', '.join(df.columns)}) VALUES ('{values}');")

# Save SQL file
with open("output.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(sql_statements))

print("SQL file created successfully!")

