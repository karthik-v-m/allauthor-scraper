
import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds_dict = json.loads(os.environ["GOOGLE_CREDS_JSON"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

sheet = client.open("AllAuthor Books").sheet1
sheet.clear()
sheet.append_row(["Book Title", "Book Link", "Author Name", "Author Link"])

url = "https://allauthor.com/books/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

rows = soup.select("tr.odd, tr.even")
print(f"🧐 Found {len(rows)} books")

if not rows:
    print("⚠️ No books found! Site might be blocking Railway or layout changed.")
    print("Page content preview:", soup.prettify()[:500])  # Debug tip


for row in rows[:5]:
    try:
        book_elem = row.select_one(".bookname a")
        author_elem = row.select_one(".book-author-name a")

        book_title = book_elem.text.strip()
        book_link = book_elem["href"]
        author_name = author_elem.text.strip()
        author_link = author_elem["href"]

        sheet.append_row([book_title, book_link, author_name, author_link])
        print(f"✅ Added: {book_title} by {author_name}")
    except Exception as e:
        print(f"⚠️ Error: {e}")
        continue

print("✅ Finished uploading 5 books to Google Sheets!")
