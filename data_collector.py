#data collection
import requests as re
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

#unstructured to structured
from bs4 import BeautifulSoup
import pandas as pd
import feature_extraction as fe

disable_warnings(InsecureRequestWarning) #disable warnings when sending requests to phishing websites

#Step1: csv to dataframe

URL_file_name = "trancolist_top-1m.csv"
data_frame = pd.read_csv(URL_file_name)

#Retrieving only "URL" and compiling to a list
URL_list = data_frame['url'].to_list()

#restrict the URL count (>65k URLs in the .csv file)
begin = 0
end = 15000
collection_list = URL_list[begin:end]

#only for legitimate websites
tag = "http://"

collection_list = [tag + url for url in collection_list]

#function to scrape the content of the URL and convert to a structured form for each URL

def create_structured_data(url_list):
    data_list = []
    for i in range(0, len(url_list)):
        try:
            response = re.get(url_list[i], verify=False, timeout=4)
            if response.status_code != 200:
                print(i, ". HTTP connection failed for the URL: ", url_list[i])
            else:
                soup = BeautifulSoup(response.content, "html.parser")
                vector = fe.create_vector(soup)
                vector.append(str(url_list[i]))
                data_list.append(vector)
        except re.exceptions.RequestException as e:
            print(i, " -->", e)
            continue
    return data_list

data = create_structured_data(collection_list)

columns = [
    'has_title',
    'has_input',
    'has_button',
    'has_image',
    'has_submit',
    'has_link',
    'has_password',
    'has_email_input',
    'has_hidden_element',
    'has_audio',
    'has_video',
    'number_of_inputs',
    'number_of_buttons',
    'number_of_images',
    'number_of_options',
    'number_of_lists',
    'number_of_TH',
    'number_of_TR',
    'number_of_href',
    'number_of_paragraph',
    'number_of_script',
    'length_of_title',
    'URL'
]


df = pd.DataFrame(data=data, columns=columns)

df.to_csv("structured_data_legitimate-1.csv", mode='a', index=False) #header should be False after the first run.