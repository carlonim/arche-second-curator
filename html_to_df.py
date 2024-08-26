import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

url = "https://arche.acdh.oeaw.ac.at/browser/api/getRootTable/en?_format=html"

root_table = urllib.request.urlopen(url).read()

soup = BeautifulSoup(root_table, 'html.parser')

columns = []

for cell in soup.table.contents[0].contents[0]:
    columns.append(cell.text)

lists = []

for row in soup.table.contents[1:]:
    list = []
    for cell in row.contents:
        list.append(cell.text)
    lists.append(list)

df = pd.DataFrame(lists)
df.columns = columns
df.to_pickle("root_table.pkl")