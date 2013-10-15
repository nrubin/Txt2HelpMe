# -*- coding: UTF-8 -*-

import json
import requests
meals = """[
  {
    "breakfast": {
      "Hot Cereal": [
        "Muesli"
      ],
      "Chefs Choice": [
        "Oatmeal",
        "Hard Cooked Eggs",
        "Fried Eggs",
        "Scrambled Eggs",
        "Omelet Bar"
      ],
      "Entrée": [
        "Buttermilk Pancakes",
        "Ham & Red Bliss Potato Frittata",
        "Sausage & Egg Breakfast Flatbread Pizza"
      ],
      "Bread": [
        "Applesauce Coffee Cake",
        "Chocolate Chip Muffin (2)"
      ],
      "International": [
        "Steamed Brown Rice"
      ],
      "Meat": [
        "Turkey Sausage Patties"
      ],
      "Potato": [
        "Home Fried Potatoes"
      ]
    },
    "lunch": {
      "Soup": [
        "Chicken Ditalini Soup",
        "Carrot and Coriander Soup"
      ],
      "Vegetarian/Vegan": [
        "Farro Salad with Garden Vegetables",
        "Tunisian Vegetable Stew",
        "Couscous (Vegetarian)"
      ],
      "Sodexo": [
        "Garlic Margarine"
      ],
      "Pizza": [
        "Flatbread Pizza Bar"
      ],
      "Chefs Choice": [
        "Vegetarian Fajitas",
        "Mexican Rice",
        "Vegetarian Refried Beans"
      ],
      "Entrée": [
        "Grilled Chicken Fajitas"
      ],
      "Grill": [
        "Classic Cheeseburger on a Toasted Bun",
        "Hot Dog on Bun",
        "Roast Vegetable & Muenster Sandwich",
        "Grilled Cheese Sandwich",
        "French Fries",
        "Fresh Watermelon Wedge"
      ],
      "Dessert": [
        "Sugar Cookies",
        "Chillin' Orange Mango Mousse",
        "Orange Jell-O Parfait"
      ],
      "International": [
        "Steamed Brown Rice"
      ],
      "To Go": [
        "Cheese Pizza"
      ]
    },
    "dinner": {
      "Soup": [
        "Chicken Ditalini Soup",
        "Carrot and Coriander Soup"
      ],
      "Vegetarian/Vegan": [
        "Fried Green Tomatoes",
        "Roasted Sweet Potatoes",
        "Cilantro Lime Pickled Red Onions",
        "Orecchiette with Broccoli and Chickpeas"
      ],
      "Sodexo": [
        "Garlic Margarine"
      ],
      "Pizza": [
        "Cheese Pizza",
        "Vegetable Lovers Feast Pizza",
        "Chicken, Broccoli, &Mushroom Calzone",
        "Herb Seasoned Breadsticks"
      ],
      "Chefs Choice": [
        "Baked Ziti",
        "Garlic Bread",
        "Whole Green Beans"
      ],
      "Entrée": [
        "Breaded Fried Pork Cutlet"
      ],
      "Deli": [
        "Panini Forno Florentino",
        "French Fries"
      ],
      "Dessert": [
        "Devil's Food Cake",
        "Chocolate Chip Bread Pudding",
        "Chillin' Orange Mango Mousse"
      ],
      "International": [
        "Ginger Sesame Salad With Chicken",
        "Steamed Brown Rice"
      ]
    }
  },
  {
    "breakfast": {
      "Hot Cereal": [
        "Maple Cinnamon Raisin Oatmeal"
      ],
      "Chefs Choice": [
        "Oatmeal",
        "Hard Cooked Eggs",
        "Fried Eggs",
        "Scrambled Eggs",
        "Omelet Bar"
      ],
      "Entrée": [
        "Whole Wheat French Toast",
        "Scrambled Eggs with Cheddar",
        "Scrambled Egg Whites on Bagel"
      ],
      "Bread": [
        "Glazed Cinnamon Roll",
        "Cranberry Orange Mini Scone"
      ],
      "International": [
        "Jasmine Steamed Rice"
      ],
      "Meat": [
        "Ham Steak"
      ],
      "Potato": [
        "Hash Browned Potatoes"
      ]
    },
    "lunch": {
      "Soup": [
        "Beef, Barley & Onion Soup",
        "Cream of Spinach Soup"
      ],
      "Vegetarian/Vegan": [
        "Roasted Eggplant",
        "Lentil Stew",
        "Corn & Poblano Cakes with Bean Salad"
      ],
      "Pizza": [
        "Tomato Bruschetta Flatbread Pizza",
        "Pepperoni Pizza",
        "Vegetable Lovers Calzone",
        "Herb Seasoned Breadsticks"
      ],
      "Chefs Choice": [
        "Macaroni & Cheese"
      ],
      "Entrée": [
        "Kansas City BBQ Pulled Pork Sandwich",
        "Southern Cole Slaw",
        "Baked Bean"
      ],
      "Grill": [
        "Egg Salad Sandwich on Multi-Grain",
        "Spinach & Jack Cheese Quesadilla",
        "Chicken Pita Sandwich",
        "Grilled Brat & Onion Sandwich",
        "French Fries"
      ],
      "Dessert": [
        "Carnival Cookies",
        "Chocolate Brownies",
        "Oreo Crumble Pudding Cup"
      ],
      "International": [
        "Jasmine Steamed Rice"
      ]
    },
    "dinner": {
      "Soup": [
        "Beef, Barley & Onion Soup",
        "Cream of Spinach Soup"
      ],
      "Vegetarian/Vegan": [
        "Ginger Tofu & Vegetable Stir Fry",
        "Jasmine Rice",
        "Mexican Vegetable Quesadilla"
      ],
      "Pizza": [
        "Pepperoni Pizza",
        "Tomato Bruschetta Flatbread Pizza",
        "Vegetable Lovers Calzone",
        "Herb Seasoned Breadsticks"
      ],
      "Chefs Choice": [
        "Fettuccine Alfredo with Broccoli"
      ],
      "Entrée": [
        "Homestyle Meatloaf",
        "Mashed Potato",
        "Fresh Broccoli"
      ],
      "Deli": [
        "Classic Italian Sub",
        "French Fries"
      ],
      "Dessert": [
        "Carrot Cake with Cream Cheese Frosting",
        "Apple Pie",
        "Cherry Jell-O Parfait"
      ],
      "International": [
        "BBQ Tilapia, Wild Rice Pilaf,Tomato",
        "Jasmine Steamed Rice"
      ]
    }
  },
  {
    "breakfast": {
      "Hot Cereal": [
        "Millet, Raw",
        "Mandarin Orange Sections",
        "Pitted Dates"
      ],
      "Chefs Choice": [
        "Oatmeal",
        "Hard Cooked Eggs",
        "Fried Eggs",
        "Scrambled Eggs",
        "Omelet Bar"
      ],
      "Entrée": [
        "Blueberry Pancakes",
        "Onion & Summer Squash Frittata",
        "Farmhouse Breakfast Bowl"
      ],
      "Bread": [
        "Blueberry Sour Cream Coffee Cake",
        "Peanut Butter Chocolate Chip Muffins"
      ],
      "International": [
        "White Seasoned Rice"
      ],
      "Meat": [
        "Turkey Bacon"
      ],
      "Potato": [
        "Sliced Lyonnaise Potatoes"
      ]
    },
    "lunch": {
      "Soup": [
        "Roast Turkey and Rice Soup",
        "Vegetarian Black Bean Soup"
      ],
      "Vegetarian/Vegan": [
        "Bandito Beans",
        "Brown Rice",
        "Cilantro Lime Pickled Red Onions",
        "Quinoa Primavera"
      ],
      "Pizza": [
        "Cheese Pizza",
        "Hot Italian Sausage Pizza",
        "Turkey, Bacon, & Swiss Stromboli",
        "Herb Seasoned Breadsticks"
      ],
      "Chefs Choice": [
        "Italian Wedge Salad",
        "Tuscan Onion Soup"
      ],
      "Entrée": [
        "Baja Beef Sandwich",
        "Lime Cilantro Rice",
        "Grilled Mexican Vegetables"
      ],
      "Grill": [
        "Fall Vegetable Wrap",
        "Classic Cheeseburger on a Toasted Bun",
        "Fish Sandwich",
        "Cheese Quesadilla",
        "French Fries",
        "Carrot & Celery Sticks"
      ],
      "Dessert": [
        "Walnut Blondies",
        "Strawberry Shortcake Pudding Cup",
        "Raspberry Jell-O Parfait"
      ],
      "International": [
        "White Seasoned Rice"
      ]
    },
    "dinner": {
      "Soup": [
        "Roast Turkey and Rice Soup",
        "Vegetarian Black Bean Soup"
      ],
      "Vegetarian/Vegan": [
        "Tuscan Chopped Salad",
        "Vegan Six Bean Soup",
        "Eggplant Parmesan Casserole"
      ],
      "Pizza": [
        "Cheese Pizza",
        "Hot Italian Sausage Pizza",
        "Turkey, Bacon, & Swiss Stromboli",
        "Herb Seasoned Breadsticks"
      ],
      "Chefs Choice": [
        "General Tso's Chicken with Jasmine Rice"
      ],
      "Entrée": [
        "Cornbread Stuffed Pork Chop",
        "Long Grain & Wild Rice",
        "Steamed Fresh Baby Carrots"
      ],
      "Deli": [
        "Turkey Reuben Melt",
        "French Fries"
      ],
      "Dessert": [
        "Homestyle Sour Cream Pound Cake",
        "Chocolate Cream Pie",
        "Raspberry Jell-O Parfait"
      ],
      "International": [
        "Queso w/ Chorizo & Tortillas Plate",
        "White Seasoned Rice"
      ]
    }
  },
  {
    "breakfast": {
      "Hot Cereal": [
        "Cooked Quinoa",
        "Cinnamon Sticks",
        "Salt"
      ],
      "Chefs Choice": [
        "Oatmeal",
        "Hard Cooked Eggs",
        "Fried Eggs",
        "Scrambled Eggs",
        "Omelet Bar"
      ],
      "Entrée": [
        "French Waffle",
        "Scrambled Eggs with Chorizo",
        "Egg & Cheese Biscuit"
      ],
      "Bread": [
        "Cobblestones   (CS)",
        "Chocolate Chunk Mini Scone"
      ],
      "International": [
        "Long Grain & Wild Rice"
      ],
      "Meat": [
        "Pork Sausage Patty"
      ],
      "Potato": [
        "Tri-Tater Patties"
      ]
    },
    "lunch": {
      "Soup": [
        "Roasted Garden Vegetable Soup",
        "Sausage Florentine Soup"
      ],
      "Vegetarian/Vegan": [
        "Penne with Fra Diavolo Sauce",
        "Tuscan White Bean Salad",
        "Curried Tofu with Jasmine Rice"
      ],
      "Pizza": [
        "Pepperoni Pizza",
        "French Bread Pizza",
        "The Classic Mini Calzone with Ham",
        "Herb Seasoned Breadsticks"
      ],
      "Chefs Choice": [
        "Roasted Vegetable Lasagna with Marinara"
      ],
      "Entrée": [
        "Baked Chicken Breast Parmesan",
        "Roasted Red Bliss Potatoes",
        "Steamed Corn"
      ],
      "Grill": [
        "Classic Cheeseburger on a Toasted Bun",
        "Veggie Monster Baguette Sandwich",
        "Turkey Sloppy Joe",
        "Grilled Cheese Sandwich",
        "French Fries"
      ],
      "Dessert": [
        "Angel Cookies",
        "Banana Cream Pie Pudding Cup",
        "Strawberry Jell-O Parfait"
      ],
      "International": [
        "Long Grain & Wild Rice"
      ]
    },
    "dinner": {
      "Soup": [
        "Roasted Garden Vegetable Soup",
        "Sausage Florentine Soup"
      ],
      "Vegetarian/Vegan": [
        "Basmati Rice with Vermicelli",
        "Grilled Pita",
        "Greek Spinach Strudel"
      ],
      "Pizza": [
        "French Bread Pizza",
        "Pepperoni Pizza",
        "The Classic Mini Calzone with Ham",
        "Herb Seasoned Breadsticks"
      ],
      "Chefs Choice": [
        "Cajun Shrimp with Rice",
        "Old-Fashioned Cornbread"
      ],
      "Entrée": [
        "Classic Roasted Turkey Breast",
        "Baked Sweet Potato",
        "Grilled Vegetables",
        "Whole Berry Cranberry Sauce"
      ],
      "Deli": [
        "Muffuletta Biggie Sandwich",
        "French Fries"
      ],
      "Dessert": [
        "Orange Angel Cupcakes",
        "Peach Crisp",
        "Banana Cream Pie Pudding Cup"
      ],
      "International": [
        "Roast Pepper & Gouda Quesadilla Plate",
        "Long Grain & Wild Rice"
      ]
    }
  },
  {
    "breakfast": {
      "Hot Cereal": [
        "Cream of Wheat (Farina)"
      ],
      "Chefs Choice": [
        "Oatmeal",
        "Hard Cooked Eggs",
        "Fried Eggs",
        "Scrambled Eggs",
        "Omelet Bar"
      ],
      "Entrée": [
        "Sourdough French Toast",
        "Mushroom, Ham & Swiss Frittata",
        "Breakfast Burrito"
      ],
      "Bread": [
        "Harvest Pumpkin Streusel Coffee Cake",
        "Low Fat Banana Muffin"
      ],
      "International": [
        "Green Rice, Arroz Verde"
      ],
      "Meat": [
        "Crisp Bacon Strip"
      ],
      "Potato": [
        "Home Fried Potatoes"
      ]
    },
    "lunch": {
      "Soup": [
        "New England Clam Chowder",
        "Three Mushroom Barley"
      ],
      "Vegetarian/Vegan": [
        "Curried Rice & Lentils",
        "Eggplant with Tomato & Onion",
        "Falafel, Tzatziki, Tahini & Pita"
      ],
      "Pizza": [
        "Pepperoni Pizza",
        "Tex Mex Pizzetta",
        "Herb Seasoned Breadsticks"
      ],
      "Chefs Choice": [
        "Fish & Chips"
      ],
      "Entrée": [
        "Spaghetti & Meatballs with Sauce",
        "Garlic Bread",
        "Leaf Spinach"
      ],
      "Grill": [
        "Classic Cheeseburger on a Toasted Bun",
        "Hot Dog on Bun",
        "Hummus, Avocado, & Roasted Veggie Wrap",
        "Chocolate Peanut Butter Banana Melt",
        "French Fries",
        "Fresh Orange Wedges"
      ],
      "Dessert": [
        "Chocolate Chip Cookies",
        "Dirt Pudding Cup",
        "Berry Blue Jell-O Parfait"
      ],
      "International": [
        "Green Rice, Arroz Verde"
      ],
      "To Go": [
        "Cheese Pizza",
        "Cheese Pizza"
      ]
    },
    "dinner": {
      "Soup": [
        "New England Clam Chowder",
        "Three Mushroom Barley"
      ],
      "Vegetarian/Vegan": [
        "Hummus & Tabbouleh Wrap",
        "Polenta alla Funghi"
      ],
      "Pizza": [
        "Cheese Pizza",
        "Pepperoni Pizza",
        "Tex Mex Pizzetta",
        "Herb Seasoned Breadsticks"
      ],
      "Chefs Choice": [
        "Linguine with Light Clam Sauce"
      ],
      "Entrée": [
        "Southern Fried Chicken",
        "Country Mashed Potatoes",
        "Sliced Steamed Carrots"
      ],
      "Deli": [
        "Fresh Orange Wedges"
      ],
      "Dessert": [
        "Pineapple Upside Down Cake",
        "Dirt Pudding Cup",
        "Berry Blue Jell-O Parfait"
      ],
      "International": [
        "Awesome French Fry Bar",
        "Green Rice, Arroz Verde"
      ]
    }
  },
  {
    "breakfast": {
      "Bread": [
        "Glazed Cinnamon Roll",
        "Raspberry White Chocolate Mini Scone"
      ],
      "Fruit": [
        "Fresh Fruit Salad"
      ]
    },
    "lunch": {
      "Soup": [
        "American Bounty Vegetable Soup"
      ],
      "Vegetarian/Vegan": [
        "Black-Eyed Pea & Rice Cake"
      ],
      "Chefs Choice": [
        "Oatmeal",
        "Hard Cooked Eggs",
        "Fried Eggs",
        "Scrambled Eggs",
        "Omelet Bar"
      ],
      "Entrée": [
        "Cheese Grits",
        "Buttermilk Pancakes",
        "Eggs Benedict with Canadian Bacon",
        "Hash Browned Potatoes",
        "Sausage Links",
        "Turkey London Broil",
        "Mashed Sweet Potatoes",
        "Fresh Broccoli"
      ],
      "Dessert": [
        "Oatmeal Raisin Cookies",
        "Seven Layer Bars",
        "Vanilla Pudding Cup"
      ]
    },
    "dinner": {
      "Soup": [
        "American Bounty Vegetable Soup"
      ],
      "Vegetarian/Vegan": [
        "Curried Rice Noodles"
      ],
      "Pizza": [
        "Cheese Pizza",
        "Pepperoni Pizza",
        "Creamy Seafood Fusilli Casserette",
        "Herb Seasoned Breadsticks"
      ],
      "Dessert": [
        "Coconut Cream Pie",
        "Vanilla Pudding Cup",
        "Lemon Jell-O Parfait"
      ],
      "Theme Cuisine": [
        "Asian Vegetable Salad",
        "Teriyaki Chicken",
        "Szechuan Beef and Noodles Stir Fry",
        "Korean Stir-Fried Vegetables with Tofu",
        "Vegetarian Fried Rice",
        "Crisp Gingered Chinese Cabbage"
      ]
    }
  },
  {
    "breakfast": {
      "Bread": [
        "Low Fat Banana Muffin",
        "Peach Sour Cream Coffee Cake"
      ],
      "Fruit": [
        "Fresh Fruit Salad"
      ]
    },
    "lunch": {
      "Soup": [
        "Roasted Tomato Tortilla Soup"
      ],
      "Vegetarian/Vegan": [
        "Tofu Fried Rice"
      ],
      "Chefs Choice": [
        "Oatmeal",
        "Hard Cooked Eggs",
        "Fried Eggs",
        "Scrambled Eggs",
        "Omelet Bar"
      ],
      "Entrée": [
        "Cream of Rice Cereal",
        "Peanut Butter & Jelly French Toast",
        "Croissant with Eggs & Cheese",
        "Home Fried Potatoes",
        "Corned Beef Hash",
        "Baked Potato",
        "Whole Green Beans"
      ],
      "Dessert": [
        "Sugar Cookies",
        "Cream Cheese Swirl Brownies",
        "Lime Jell-O Parfait"
      ]
    },
    "dinner": {
      "Soup": [
        "Roasted Tomato Tortilla Soup"
      ],
      "Vegetarian/Vegan": [
        "White Bean Chili with Wheat Berries",
        "Grilled Pita",
        "General Tso's Tofu"
      ],
      "Pizza": [
        "Cheese Pizza",
        "Pepperoni Pizza",
        "Penne with Italian Sausage",
        "Herb Seasoned Breadsticks"
      ],
      "Chefs Choice": [
        "Grilled Chicken Fajitas"
      ],
      "Entrée": [
        "Baked Breaded Cod",
        "Lemon Rice",
        "Spinach with Garlic & Onions"
      ],
      "Grill": [
        "Mozzarella and Tomato Biggie",
        "French Fries"
      ],
      "Dessert": [
        "Devil's Food Cake",
        "Cherry Cobbler",
        "Lime Jell-O Parfait"
      ]
    }
  }
]"""

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


if __name__ == '__main__':
	print humanize_food_list(parse_meal_request("what is for brunch on sunday"))