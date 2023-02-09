import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

html_file = open("02092023-01.html")

index = html_file.read()

soup = BeautifulSoup(index, 'html.parser')
table = soup.find_all("table")

#table = table.get_text().split("\n\n")

print(table)

text = soup.get_text().splitlines()
for section in text:
    if "BUILD" in section:
        print(section)


# git add .
# git commit -m "commit here"
# git push -u origin master