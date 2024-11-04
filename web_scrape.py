import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

class Event:
  def __init__(self, name, date, event_link, fights):
    self.name = name
    self.date = date
    self.event_link = event_link
    self.fights = fights


class Fight:
  def __init__(self, method, winner, weightclass, fight_link, both_stats):
    self.method = method
    self.winner = winner
    self.weightclass = weightclass
    self.fight_link = fight_link
    self.fighter1_stats = both_stats[0]
    self.fighter2_stats = both_stats[1]


class Fighter_Stats:
  def __init__(self, name, link, score, kd, siglanded, sigattempt, totallanded, totalattempt, tdlanded, tdattempt, subatt, rev, ctrl, headlanded, headattempt, bodylanded, bodyattempt, leglanded, legattempt, distancelanded, distanceattempt, clinchlanded, clinchattempt, groundlanded, groundattempt):
    self.name = name
    self.link = link
    self.score = score
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


def get_events(saved_filename):

  file_frame = pd.read_csv(saved_filename)
  names_list = file_frame['name'].tolist()

  r = requests.get('http://ufcstats.com/statistics/events/completed?page=all')
  raw = BeautifulSoup(r.content, 'html.parser')
  raw = raw.find_all(class_= "b-statistics__table-content")
  
  upcoming_link = raw[0].find('a', class_='b-link b-link_style_white')['href']
  upcoming_name = raw[0].find('a', class_='b-link b-link_style_white').get_text(strip=True)
  upcoming_date = datetime.strptime(raw[0].find('span', class_='b-statistics__date').get_text(strip=True), "%B %d, %Y")
  upcoming_event = Event(upcoming_name, upcoming_date, upcoming_link, [])
  
  events = []
  unification_date = datetime(2002, 2, 1)
  for i in range(1, len(raw)):
    name = raw[i].find('a', class_='b-link b-link_style_black').get_text(strip=True)
    date = datetime.strptime(raw[i].find('span', class_='b-statistics__date').get_text(strip=True), "%B %d, %Y")
    event_link = raw[i].find('a', class_='b-link b-link_style_black')['href']

    if (date < unification_date):
      print("Unification Date Reached - Stopping")
      break

    if name not in names_list:
      events.append(Event(name, date, event_link, get_fights(event_link)))
      print("Found New Event:", name)
    else:
      print("Already Have", name)
      
  events.reverse()
  return upcoming_event, events


def get_fights(event_link):
  r = requests.get(event_link)
  raw = BeautifulSoup(r.content, 'html.parser')
  raw = raw.find_all(class_ = "b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click")

  fights_list = []
  for i in range(len(raw)):
    result = raw[i].find(class_="b-fight-details__table-col b-fight-details__table-col_style_align-top").find(class_="b-flag__text").get_text(strip=True)
    if (result == "win"):
      method = raw[i].find_all(class_="b-fight-details__table-col l-page_align_left")[2].find(class_="b-fight-details__table-text").get_text(strip=True)
      winner = raw[i].find(class_="b-fight-details__table-col l-page_align_left").find_all(class_="b-link b-link_style_black")[0].get_text(strip=True)
    else:
      method = "N/A"
      winner = "N/A"
    
    weightclass = raw[i].find_all(class_="b-fight-details__table-col l-page_align_left")[1].find(class_="b-fight-details__table-text").get_text(strip=True)
    fight_link = raw[i]['data-link']

    was_dec = "DEC" in method
    both_stats = get_stats(fight_link, was_dec)
    if (was_dec):
      lower_score = min(both_stats[0].score, both_stats[1].score)
      higher_score = max(both_stats[0].score, both_stats[1].score)
      if(winner == both_stats[0].name):
        both_stats[0].score = higher_score
        both_stats[1].score = lower_score
      else:
        both_stats[1].score = higher_score
        both_stats[0].score = lower_score

    fights_list.append(Fight(method, winner, weightclass, fight_link, both_stats))
  fights_list.reverse()
  return fights_list


def get_stats(fight_link, was_dec):
  r = requests.get(fight_link)
  raw = BeautifulSoup(r.content, 'html.parser')
  
  f1_score = 0
  f2_score = 0
  if was_dec:
    f1_score += int(raw.find_all(class_="b-fight-details__text")[1].find_all(class_="b-fight-details__text-item")[0].get_text(strip=True)[-8:-6])
    f1_score += int(raw.find_all(class_="b-fight-details__text")[1].find_all(class_="b-fight-details__text-item")[1].get_text(strip=True)[-8:-6])
    f1_score += int(raw.find_all(class_="b-fight-details__text")[1].find_all(class_="b-fight-details__text-item")[2].get_text(strip=True)[-8:-6])
    f2_score += int(raw.find_all(class_="b-fight-details__text")[1].find_all(class_="b-fight-details__text-item")[0].get_text(strip=True)[-3:-1])
    f2_score += int(raw.find_all(class_="b-fight-details__text")[1].find_all(class_="b-fight-details__text-item")[1].get_text(strip=True)[-3:-1])
    f2_score += int(raw.find_all(class_="b-fight-details__text")[1].find_all(class_="b-fight-details__text-item")[2].get_text(strip=True)[-3:-1])
  
  raw = raw.find_all(class_ = "b-fight-details__table-body")
  first_table = raw[0].find_all(class_ = "b-fight-details__table-text")
  second_table = raw[2].find_all(class_ = "b-fight-details__table-text")
  
  f1_name = first_table[0].get_text(strip=True)
  f2_name = first_table[1].get_text(strip=True)

  f1_link = first_table[0].find(class_="b-link b-link_style_black")['href']
  f2_link = first_table[1].find(class_="b-link b-link_style_black")['href']

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

  f1 = Fighter_Stats(f1_name, f1_link, f1_score, f1_kd, f1_siglanded, f1_sigattempt, f1_totallanded, f1_totalattempt, f1_tdlanded, f1_tdattempt, f1_subatt, f1_rev, f1_ctrl, f1_headlanded, f1_headattempt, f1_bodylanded, f1_bodyattempt, f1_leglanded, f1_legattempt, f1_distancelanded, f1_distanceattempt, f1_clinchlanded, f1_clinchattempt, f1_groundlanded, f1_groundattempt)
  f2 = Fighter_Stats(f2_name, f2_link, f2_score, f2_kd, f2_siglanded, f2_sigattempt, f2_totallanded, f2_totalattempt, f2_tdlanded, f2_tdattempt, f2_subatt, f2_rev, f2_ctrl, f2_headlanded, f2_headattempt, f2_bodylanded, f2_bodyattempt, f2_leglanded, f2_legattempt, f2_distancelanded, f2_distanceattempt, f2_clinchlanded, f2_clinchattempt, f2_groundlanded, f2_groundattempt)
  return [f1, f2]


def get_percentage(landed, attempted):
  if(attempted):
    return landed/attempted
  else:
    return 0