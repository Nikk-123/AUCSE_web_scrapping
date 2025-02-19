import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

URL = "https://www.aucse.in/people/student/btech/cse-batch-2022-2026"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

# Send GET request
response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Create an Excel workbook
wb = Workbook()
sheet = wb.active
sheet.title = "Scraped Data"
sheet.append(["Sl No. ", "Roll No.", "Image URL", "Name"])

# Extracting data from HTML
sections = soup.find_all("section", {"class": ["yaqOZd","cJgDec","tpmmCb"]})
for section in sections:
    paragraphs = section.find_all("p", class_="zfr3Q CDt4Ke")
    roll_number = paragraphs[0].text.strip() if len(paragraphs) > 0 else "N/A"
    name = paragraphs[1].text.strip() if len(paragraphs) > 1 else "N/A"
    image = section.find("img")["src"] if section.find("img") else "N/A"
    department = paragraphs[2].text.strip() if len(paragraphs) > 2 else "N/A"
    
    sheet.append([roll_number, name, image, department])

# Save the data to an Excel file
wb.save("college_data.xlsx")
print("Data successfully scraped and saved to college_data.xlsx")
