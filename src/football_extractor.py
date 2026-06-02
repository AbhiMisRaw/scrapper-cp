import httpx
from bs4 import BeautifulSoup as bs

URL = "https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals"

def print_table(file):
    table = soup.find(
        "table",
        class_="sortable plainrowheaders wikitable"
    )
    headers = [
        th.get_text(strip=True)
        for th in table.find("tr").find_all("th")
    ]
    print("Data :")
    headers = headers[0:4]
    rows = []

    for tr in table.find_all("tr")[1:]:  # skip header row
        cells = tr.find_all(["th", "td"])
        row = [cell.get_text(" ", strip=True) for cell in cells]

        # Since we require only year, Winner Country, Score and Runner-up
        rows.append(row[0:4])

    rows = rows[0:10]
    
    print(f"Length of rows", len(rows))
    payload = {
        "values": [
            headers,
            *rows
        ]
    }
    return payload


print("Sending")
# url_link = httpx.get(URL)

html_content = open("./footbal_result.html", "r")

soup = bs(html_content, "html.parser")
print(f"File : {soup}")
payload = print_table(soup)


