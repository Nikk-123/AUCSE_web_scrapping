import re
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from collections import defaultdict
import os

def extract_student_data(file_path):
    student_data = defaultdict(set)  # Dictionary to store {student_id: {roll_no1, roll_no2}}
    original_lines = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            original_lines.append(line)
            match = re.search(r"INSERT INTO .*? \((.*?)\) VALUES \((.*?)\);", line, re.IGNORECASE)
            if match:
                columns = [col.strip().strip("`") for col in match.group(1).split(",")]
                values = [val.strip().strip("'") for val in match.group(2).split(",")]

                if "student_id" in columns and "roll_no" in columns:
                    student_id_index = columns.index("student_id")
                    roll_no_index = columns.index("roll_no")

                    student_id = values[student_id_index]
                    roll_no = values[roll_no_index]

                    student_data[student_id].add(roll_no)

    return student_data, original_lines

def find_duplicates(student_data):
    duplicates = {}
    for sid, roll_nos in student_data.items():
        if len(roll_nos) > 1:
            roll_nos = list(roll_nos)
            
            # Separate roll numbers based on pattern
            btcse_pattern = re.compile(r"UG/02/BTCSE/2022/\d{3}")
            roll_no_1 = next((rn for rn in roll_nos if btcse_pattern.match(rn)), "N/A")
            roll_no_2 = next((rn for rn in roll_nos if rn != roll_no_1), "N/A")

            duplicates[sid] = (roll_no_1, roll_no_2)

    return duplicates

def open_file():
    global file_path, original_lines
    file_path = filedialog.askopenfilename(filetypes=[("SQL Files", "*.sql")])
    if file_path:
        student_data, original_lines = extract_student_data(file_path)
        global duplicates
        duplicates = find_duplicates(student_data)
        display_duplicates(duplicates)

def display_duplicates(duplicates):
    for row in tree.get_children():
        tree.delete(row)

    if duplicates:
        for student_id, (roll_no_1, roll_no_2) in duplicates.items():
            tree.insert("", "end", values=(student_id, roll_no_1, roll_no_2))
    else:
        messagebox.showinfo("Result", "No duplicate student IDs found with different roll numbers.")

def delete_entries(by_roll_no):
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Warning", "No entries selected!")
        return

    for item in selected_items:
        values = tree.item(item, "values")
        student_id = values[0]

        if by_roll_no == 1:
            duplicates[student_id] = ("N/A", duplicates[student_id][1])
        elif by_roll_no == 2:
            duplicates[student_id] = (duplicates[student_id][0], "N/A")

        if duplicates[student_id] == ("N/A", "N/A"):
            del duplicates[student_id]

        tree.delete(item)

def save_cleaned_sql():
    if not file_path:
        messagebox.showerror("Error", "No SQL file selected!")
        return

    # Generate new file name
    dir_name, original_filename = os.path.split(file_path)
    new_filename = os.path.join(dir_name, f"new_{original_filename}")

    # Create cleaned SQL content
    cleaned_sql = []
    for line in original_lines:
        match = re.search(r"INSERT INTO .*? \((.*?)\) VALUES \((.*?)\);", line, re.IGNORECASE)
        if match:
            columns = [col.strip().strip("`") for col in match.group(1).split(",")]
            values = [val.strip().strip("'") for val in match.group(2).split(",")]

            if "student_id" in columns and "roll_no" in columns:
                student_id_index = columns.index("student_id")
                roll_no_index = columns.index("roll_no")

                student_id = values[student_id_index]
                roll_no = values[roll_no_index]

                if student_id in duplicates:
                    roll_no_1, roll_no_2 = duplicates[student_id]
                    if roll_no != roll_no_1 and roll_no != roll_no_2:
                        continue  # Skip the duplicate entry

        cleaned_sql.append(line)  # Keep original structure

    # Save new SQL file
    with open(new_filename, "w", encoding="utf-8") as file:
        file.writelines(cleaned_sql)

    messagebox.showinfo("Success", f"Cleaned SQL file saved as:\n{new_filename}")

# GUI setup
root = tk.Tk()
root.title("SQL Duplicate Finder")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

button = tk.Button(frame, text="Open SQL File", command=open_file)
button.pack(pady=5)

columns = ("Student ID", "Roll No 1", "Roll No 2")
tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=250)

tree.pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

delete_roll1_btn = tk.Button(btn_frame, text="Delete Entries with Roll No 1", command=lambda: delete_entries(1))
delete_roll1_btn.pack(side="left", padx=5)

delete_roll2_btn = tk.Button(btn_frame, text="Delete Entries with Roll No 2", command=lambda: delete_entries(2))
delete_roll2_btn.pack(side="left", padx=5)

save_sql_btn = tk.Button(btn_frame, text="Save Cleaned SQL File", command=save_cleaned_sql)
save_sql_btn.pack(side="left", padx=5)

root.mainloop()
