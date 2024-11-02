import requests
from datetime import datetime
from bs4 import BeautifulSoup

class Event:
  def __init__(self, name, date, event_link, fights):
    self.name = name
    self.date = date
    self.event_link = event_link
    self.fights = fights


class Fight:
  def __init__(self, result, fighter1, fighter1_link, fighter2, fighter2_link, weightclass, method, fight_link, both_stats):
    self.result = result
    self.fighter1 = fighter1
    self.fighter1_link = fighter1_link
    self.fighter1_stats = both_stats[0]
    self.fighter2 = fighter2
    self.fighter2_link = fighter2_link
    self.fighter2_stats = both_stats[1]
    self.weightclass = weightclass
    self.method = method
    self.fight_link = fight_link


class Fighter_Stats:
  def __init__(self, kd, siglanded, sigattempt, totallanded, totalattempt, tdlanded, tdattempt, subatt, rev, ctrl, headlanded, headattempt, bodylanded, bodyattempt, leglanded, legattempt, distancelanded, distanceattempt, clinchlanded, clinchattempt, groundlanded, groundattempt):
    self.kd = kd
    self.siglanded = siglanded
    self.sigattempt = sigattempt
    self.sigpercent = get_percentage(siglanded, sigattempt)
    self.totallanded = totallanded
    self.totalattempt = totalattempt
    self.totalpercent = get_percentage(totallanded, totalattempt)
    self.tdlanded = tdlanded
    self.tdattempt = tdattempt
    self.tdpercent = get_percentage(tdlanded, tdattempt)
    self.subatt = subatt
    self.rev = rev
    self.ctrl = ctrl
    self.headlanded = headlanded
    self.headattempt = headattempt
    self.headpercent = get_percentage(headlanded,headattempt)
    self.bodylanded = bodylanded
    self.bodyattempt = bodyattempt
    self.bodypercent = get_percentage(bodylanded,bodyattempt)
    self.leglanded = leglanded
    self.legattempt = legattempt
    self.legpercent = get_percentage(leglanded,legattempt)
    self.distancelanded = distancelanded
    self.distanceattempt = distanceattempt
    self.distancepercent = get_percentage(distancelanded,distanceattempt)
    self.clinchlanded = clinchlanded
    self.clinchattempt = clinchattempt
    self.clinchpercent = get_percentage(clinchlanded,clinchattempt)
    self.groundlanded = groundlanded
    self.groundattempt = groundattempt
    self.groundpercent = get_percentage(groundlanded,groundattempt)


def populate_events():
  r = requests.get('http://ufcstats.com/statistics/events/completed?page=all')
  raw = BeautifulSoup(r.content, 'html.parser')
  raw = raw.find_all(class_= "b-statistics__table-content")
  
  upcoming_link = raw[0].find('a', class_='b-link b-link_style_white')['href']
  upcoming_name = raw[0].find('a', class_='b-link b-link_style_white').get_text(strip=True)
  upcoming_date = datetime.strptime(raw[0].find('span', class_='b-statistics__date').get_text(strip=True), "%B %d, %Y")
  upcoming_event = Event(upcoming_name, upcoming_date, upcoming_link, [])
  
  events_list = []
  unification_date = datetime(2000, 11, 1)
  for i in range(1, len(raw)):
    name = raw[i].find('a', class_='b-link b-link_style_black').get_text(strip=True)
    date = datetime.strptime(raw[i].find('span', class_='b-statistics__date').get_text(strip=True), "%B %d, %Y")
    event_link = raw[i].find('a', class_='b-link b-link_style_black')['href']
    if (date < unification_date):
      print("Unification Date Reached - Stopping")
      break
    events_list.append(Event(name, date, event_link, get_fights(event_link)))
    print(i, name, date.strftime("%d %b %Y"))
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
    fights_list.append(Fight(result, fighter1, fighter1_link, fighter2, fighter2_link, weightclass, method, fight_link, get_stats(fight_link)))
  fights_list.reverse()
  return fights_list


def get_stats(fight_link):
  r = requests.get(fight_link)
  raw = BeautifulSoup(r.content, 'html.parser')
  raw = raw.find_all(class_ = "b-fight-details__table-body")
  
  first_table = raw[0].find_all(class_ = "b-fight-details__table-text")
  second_table = raw[2].find_all(class_ = "b-fight-details__table-text")
  
  f1_kd = int(first_table[2].get_text(strip=True))
  f2_kd = int(first_table[3].get_text(strip=True))

  f1_siglanded = int(first_table[4].get_text(strip=True).split(" ")[0])
  f2_siglanded = int(first_table[5].get_text(strip=True).split(" ")[0])

  f1_sigattempt = int(first_table[4].get_text(strip=True).split(" ")[2])
  f2_sigattempt = int(first_table[5].get_text(strip=True).split(" ")[2])

  f1_totallanded = int(first_table[8].get_text(strip=True).split(" ")[0])
  f2_totallanded = int(first_table[9].get_text(strip=True).split(" ")[0])

  f1_totalattempt = int(first_table[8].get_text(strip=True).split(" ")[2])
  f2_totalattempt = int(first_table[9].get_text(strip=True).split(" ")[2])

  f1_tdlanded = int(first_table[10].get_text(strip=True).split(" ")[0])
  f2_tdlanded = int(first_table[11].get_text(strip=True).split(" ")[0])

  f1_tdattempt = int(first_table[10].get_text(strip=True).split(" ")[2])
  f2_tdattempt = int(first_table[11].get_text(strip=True).split(" ")[2])

  f1_subatt = int(first_table[14].get_text(strip=True))
  f2_subatt = int(first_table[15].get_text(strip=True))

  f1_rev = int(first_table[16].get_text(strip=True))
  f2_rev = int(first_table[17].get_text(strip=True))

  f1_ctrl = 60*int(first_table[18].get_text(strip=True).split(":")[0])+int(first_table[18].get_text(strip=True).split(":")[1])
  f2_ctrl = 60*int(first_table[19].get_text(strip=True).split(":")[0])+int(first_table[19].get_text(strip=True).split(":")[1])

  f1_headlanded = int(second_table[6].get_text(strip=True).split(" ")[0])
  f2_headlanded = int(second_table[7].get_text(strip=True).split(" ")[0])

  f1_headattempt = int(second_table[6].get_text(strip=True).split(" ")[2])
  f2_headattempt = int(second_table[7].get_text(strip=True).split(" ")[2])

  f1_bodylanded = int(second_table[8].get_text(strip=True).split(" ")[0])
  f2_bodylanded = int(second_table[9].get_text(strip=True).split(" ")[0])

  f1_bodyattempt = int(second_table[8].get_text(strip=True).split(" ")[2])
  f2_bodyattempt = int(second_table[9].get_text(strip=True).split(" ")[2])

  f1_leglanded = int(second_table[10].get_text(strip=True).split(" ")[0])
  f2_leglanded = int(second_table[11].get_text(strip=True).split(" ")[0])

  f1_legattempt = int(second_table[10].get_text(strip=True).split(" ")[2])
  f2_legattempt = int(second_table[11].get_text(strip=True).split(" ")[2])

  f1_distancelanded = int(second_table[12].get_text(strip=True).split(" ")[0])
  f2_distancelanded = int(second_table[13].get_text(strip=True).split(" ")[0])

  f1_distanceattempt = int(second_table[12].get_text(strip=True).split(" ")[2])
  f2_distanceattempt = int(second_table[13].get_text(strip=True).split(" ")[2])

  f1_clinchlanded = int(second_table[14].get_text(strip=True).split(" ")[0])
  f2_clinchlanded = int(second_table[15].get_text(strip=True).split(" ")[0])

  f1_clinchattempt = int(second_table[14].get_text(strip=True).split(" ")[2])
  f2_clinchattempt = int(second_table[15].get_text(strip=True).split(" ")[2])

  f1_groundlanded = int(second_table[16].get_text(strip=True).split(" ")[0])
  f2_groundlanded = int(second_table[17].get_text(strip=True).split(" ")[0])

  f1_groundattempt = int(second_table[16].get_text(strip=True).split(" ")[2])
  f2_groundattempt = int(second_table[17].get_text(strip=True).split(" ")[2])

  f1 = Fighter_Stats(f1_kd, f1_siglanded, f1_sigattempt, f1_totallanded, f1_totalattempt, f1_tdlanded, f1_tdattempt, f1_subatt, f1_rev, f1_ctrl, f1_headlanded, f1_headattempt, f1_bodylanded, f1_bodyattempt, f1_leglanded, f1_legattempt, f1_distancelanded, f1_distanceattempt, f1_clinchlanded, f1_clinchattempt, f1_groundlanded, f1_groundattempt)
  f2 = Fighter_Stats(f2_kd, f2_siglanded, f2_sigattempt, f2_totallanded, f2_totalattempt, f2_tdlanded, f2_tdattempt, f2_subatt, f2_rev, f2_ctrl, f2_headlanded, f2_headattempt, f2_bodylanded, f2_bodyattempt, f2_leglanded, f2_legattempt, f2_distancelanded, f2_distanceattempt, f2_clinchlanded, f2_clinchattempt, f2_groundlanded, f2_groundattempt)
  return [f1, f2]


def get_percentage(landed, attempted):
  if(attempted):
    return landed/attempted
  else:
    return 0