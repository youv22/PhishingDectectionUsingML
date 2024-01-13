import requests as re
from bs4 import BeautifulSoup
import os

URL = "https://www.kb.parallels.com"
response = re.get(URL)

print("response --> ", response, "\ntype --> ", type(response))

print("text --> ", response.text, "\ncontent -->", response.content, "\nstatus_code ", response.status_code)

if response.status_code != 200:
    print("HTTP connection failed! Try again.")
else:
    print("HTTP connection successful!")

soup = BeautifulSoup(response.content, "html.parser")

print("title with tags -->", soup.title, "\ntitle without tags --> ", soup.title.text)

for link in soup.find_all("link"):
    print(link.get("href"))

print(soup.get_text())

#1 create a folder to save HTML files
folder = "mini_dataset"

if not os.path.exists(folder):
    os.mkdir(folder)

#2 Define a function that scrapes and returns it
def scrape_content(URL):
    response = re.get(URL)
    if response.status_code == 200:
        print("HTTP connections is successful for the URL: ", URL)
        return response
    else:
        print("HTTP connections is NOT successful for the URL: ", URL)
        return None

#3 Define a function to save an HTML file of the scraped webpage in a directory/folder
path = os.getcwd() + "/" + folder

def save_html(to_where, text, name):
    file_name = name + ".html"
    with open(os.path.join(to_where, file_name), "w", encoding="utf-8") as f:
        f.write(text)

test_text = response.text
save_html(path, test_text, "example")



#4 Define a URL list variable

URL_list = [
    "https://www.utm.ac.mu",
    "https://www.facebook.com",
    "https://www.linkedin.com",
    "https://www.defimedia.info",
    "https://www.weshare.mu",
    "https://www.instagram.com",
    "https://www.netflix.com",
    "https://www.yahoo.com",
    "https://www.ebay.com",
    "https://www.github.com",
    "https://www.python.org"
]


#5 Define a function which takes the URL list and runs Step 2, 3 for each URL

def create_mini_dataset(to_where, URL_list):
    for i in range(0, len(URL_list)):
        content = scrape_content(URL_list[i])
        if content is not None:
            save_html(to_where, content.text, str(i))
        else:
            pass
    print("Mini dataset is created!")

create_mini_dataset(path, URL_list)

#6 Check 11 different files have been generated

