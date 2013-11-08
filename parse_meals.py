# -*- coding: UTF-8 -*-

import json
import requests

def to_food_list(food):
  items = []
  for meal_type_list in food.values():
    for meal_dict in meal_type_list:
      items.append(meal_dict["name"])
  return items

def parse_meal_request(text):
  day_requested = "monday"
  meal_requested = "lunch"
  weekdays = ["monday", "tuesday" , "wednesday" , "thursday", "friday"]
  meals = ["breakfast","lunch","dinner","brunch"]
  indices = { "monday" : 0, "tuesday" : 1, "wednesday" : 2, "thursday" : 3, "friday" : 4, "saturday": 5, "sunday" : 6 }
  weekday = False

  lower_text = text.lower()
  text = lower_text
  r = requests.get("http://olinapps-dining.herokuapp.com/api")  
  raw_text = r.text
  # raw_text.replace(u"Entrée",u"Entree")
  raw_text.replace(u"Entr\xe9e",u"Entree")
  meal_data = json.loads(raw_text)

  #is it a weekday? -> what day -> what meal?
  #is it the weekend? -> which day? -> brunch or dinner?
  for day in weekdays:
    if day in text:
      weekday = True
      day_requested = day
  if not weekday:
    if "saturday" in text:
      day_requested = "saturday"
    else:
      day_requested = "sunday"
    if "dinner" in text:
      meal_requested = "dinner"
    else:
      meal_requested = "brunch"
  else:
    for meal in meals:
      if meal in text:
        meal_requested = meal
  food = meal_data[indices[day_requested]]
  if meal_requested == "brunch":
    if weekday:
      return "there is no brunch on weekdays!"
    brunch = to_food_list(food["breakfast"])
    brunch.extend(to_food_list(food["lunch"]))
    return brunch
  else:
    return to_food_list(food[meal_requested])

def humanize_food_list(food_list):
  food_list = map(lambda x: str(x),food_list)
  humanized = ", ".join(food_list)
  return humanized

def today_is():
  from pytz import timezone
  import datetime
  days = {0:"Monday",1:"Tuesday",2:"Wednesday",3:"Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"}
  eastern = timezone("US/Eastern")
  now = datetime.datetime.today().replace(tzinfo=eastern).weekday()
  return days[now]

if __name__ == '__main__':
	print today_is()