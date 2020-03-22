import requests
from bs4 import BeautifulSoup

page = requests.get('https://ncov2019.live/data')
soup = BeautifulSoup(page.text, 'html.parser')
ORDER_DATA = []

class collected_data:
    def __init__(self,data):
        # print (data)
        self.name = data[0]
        self.confirmed = data[1]
        self.confirmed_changes_today = data[3]
        self.deceased = data[4]
        self.deceased_changes_today = data[5]
        self.recovered = data[7]
        self.serious = data[8]

def find_in_data(place):
    for x in ORDER_DATA:
        if x.name == place:
            return (x)
    return (None)


places_list = soup.find("tbody")
place_data = places_list.find_all("tr")
for places in place_data:
    allStats = places.find_all("td")
    order_data = []
    for data in allStats:
        order_data.append(data.get_text().replace("  ","").replace("\n",""))
    ORDER_DATA.append(collected_data(order_data))
    print (find_in_data("France"))


 