from bs4 import BeautifulSoup
import requests
from codecs import open
from re import sub
import pandas as pd
import pandas.io.sql as psql

# cell indices of the following attributes
NAME = 1
ROLE = 2
TEAM = 3
KILLS = 4
DEATHS = 5
ULTS = 6
FK = 7
FD = 8
RES = 9
PTS = 10
PTS10 = 11


def clean(text):
    # remove all HTML code and surrounding whitespace to get the clean attribute
    try:
        return re.sub('<.*?>', '', text).strip()
    except:
        return text.strip()

class Player:
    def __init__(self, info):
        self.info = info
        self.name = clean(self.info[NAME].text)
        self.role = clean(self.info[ROLE].text)
        self.team = clean(self.info[TEAM].text)
        self.kills = clean(self.info[KILLS].text)
        self.deaths = clean(self.info[DEATHS].text)
        self.ults = clean(self.info[ULTS].text)
        self.fk = clean(self.info[FK].text)
        self.fd = clean(self.info[FD].text)
        self.res = clean(self.info[RES].text)
        self.pts = clean(self.info[PTS].text)
        self.pts10 = clean(self.info[PTS10].text)

        self.attrs = []
        self.attrs.append(self.name)
        self.attrs.append(self.role)
        self.attrs.append(self.team)
        self.attrs.append(self.kills)
        self.attrs.append(self.deaths)
        self.attrs.append(self.ults)
        self.attrs.append(self.fk)
        self.attrs.append(self.fd)
        self.attrs.append(self.res)
        self.attrs.append(self.pts)
        self.attrs.append(self.pts10)


# this function takes a URL and makes a dataframe out of it
def create_week_dataframe(url):
    content = requests.get(url).content
    # page = open(url, 'r', 'utf-8')
    soup = BeautifulSoup(content, 'html.parser')

    # get the table headers
    table_header = soup.find_all('th')
    columns = ['Week']
    for cell in table_header[1:]:  # skip 0 because that just has the player picture
        columns.append(clean(cell.text))

    # loop through the rows within the table for each player
    table = soup.find('tbody')
    player_table = table.find_all('tr')
    players = []
    for row in player_table[0:]:  # skip first row because there is no data there
        person = row.find_all('td')
        players.append(Player(person))

    week_num = url.split('week=')[1]

    # add the data into the dataframe table
    df = pd.DataFrame(columns=columns)
    for player in players:
        df = df.append(pd.DataFrame(columns=columns, data=[[week_num] + player.attrs]))

    df = df.set_index('Player')

    return df


OWL_URL_BASE = "https://www.winstonslab.com/fantasy/result.php?cID=22&league=2171&week="
weekly_data = []
for i in range(0, 20):
    weekly_data.append(create_week_dataframe(OWL_URL_BASE + str(i + 1)))

i = 0
for week in weekly_data:
    i += 1
    week[week.columns[3:]] = week[week.columns[3:]].apply(pd.to_numeric)
    week['Week'] = week['Week'].apply(pd.to_numeric)
    week.to_csv('Week' + str(i) + '.csv')
    week.to_sql('Week' + str(i))
