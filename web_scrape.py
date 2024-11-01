import requests
from bs4 import BeautifulSoup

class Event:
  def __init__(self, name, date, event_link, fights):
    self.name = name
    self.date = date
    self.event_link = event_link
    self.fights = fights


class Fight:
  def __init__(self, result, fighter1, fighter1_link, fighter2, fighter2_link, weightclass, method, fight_link):
    self.result = result
    self.fighter1 = fighter1
    self.fighter1_link = fighter1_link
    self.fighter2 = fighter2
    self.fighter2_link = fighter2_link
    self.weightclass = weightclass
    self.method = method
    self.fight_link = fight_link
    self.rounds = []


class Round:
  def __init__(self):
    pass


def populate_events():
  r = requests.get('http://ufcstats.com/statistics/events/completed?page=all')
  raw = BeautifulSoup(r.content, 'html.parser')
  raw = raw.find_all(class_= "b-statistics__table-content")
  
  upcoming_link = raw[0].find('a', class_='b-link b-link_style_white')['href']
  upcoming_name = raw[0].find('a', class_='b-link b-link_style_white').get_text(strip=True)
  upcoming_date = raw[0].find('span', class_='b-statistics__date').get_text(strip=True)
  upcoming_event = Event(upcoming_name, upcoming_date, upcoming_link, [])
  
  events_list = []
  for i in range(1, len(raw)):
    name = raw[i].find('a', class_='b-link b-link_style_black').get_text(strip=True)
    date = raw[i].find('span', class_='b-statistics__date').get_text(strip=True)
    event_link = raw[i].find('a', class_='b-link b-link_style_black')['href']
    events_list.append(Event(name, date, event_link, get_fights(event_link)))
    print(i, name)
  events_list.reverse()
  return upcoming_event, events_list


def get_fights(event_link):
  r = requests.get(event_link)
  raw = BeautifulSoup(r.content, 'html.parser')
  raw = raw.find_all(class_ = "b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click")

  fights_list = []
  for i in range(len(raw)):
    result = raw[i].find(class_="b-fight-details__table-col b-fight-details__table-col_style_align-top").find(class_="b-flag__text").get_text(strip=True)
    fighters_info = raw[i].find(class_="b-fight-details__table-col l-page_align_left").find_all(class_="b-link b-link_style_black")
    fighter1 = fighters_info[0].get_text(strip=True)
    fighter1_link = fighters_info[0]['href']
    fighter2 = fighters_info[1].get_text(strip=True)
    fighter2_link = fighters_info[1]['href']
    weightclass = raw[i].find_all(class_="b-fight-details__table-col l-page_align_left")[1].find(class_="b-fight-details__table-text").get_text(strip=True)
    method = raw[i].find_all(class_="b-fight-details__table-col l-page_align_left")[2].find(class_="b-fight-details__table-text").get_text(strip=True)
    fight_link = raw[i]['data-link']
    fights_list.append(Fight(result, fighter1, fighter1_link, fighter2, fighter2_link, weightclass, method, fight_link))
  fights_list.reverse()
  return fights_list