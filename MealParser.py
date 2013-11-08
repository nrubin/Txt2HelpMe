# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta
from pytz import timezone
import json

#module to contain parsing code for meal stuff

test_meals = u"""[{"dayname":"Monday","breakfast":{"Hot Cereal":[{"name":"Grits"}],"Chefs Choice":[{"name":"Fried Eggs"},{"name":"Oatmeal"},{"name":"Hard Cooked Eggs"},{"name":"Omelet Bar"},{"name":"Scrambled Eggs"}],"Entrée":[{"name":"Country Style Scrambled Eggs"},{"name":"French Fried Tater Tots"}],"Bread":[{"name":"Cobblestones with Icing (CS)"},{"name":"Apple Cinnamon Mini Scone"}],"International":[{"name":"Basmati Rice"}],"Exhibition":[{"name":"Buttermilk Whole Wheat Pancakes"},{"name":"Egg & Cheese Bagel"}],"Meat":[{"name":"Frizzled Ham"}]},"lunch":{"Soup":[{"name":"Homestyle Chicken and Rice Soup"},{"name":"Fire Roasted Corn Soup"}],"Vegetarian/Vegan":[{"name":"Spanish Style Garbanzo Beans"},{"name":"Baked Sweet Potato"}],"Pizza":[{"name":"Cheese Pizza"},{"name":"BBQ Chicken Flat Bread Pizza"},{"name":"Italian Sub Stromboli"},{"name":"Herb Seasoned Breadsticks"}],"Entrée":[{"name":"Cheese Tortellini in Marinara Sauce"},{"name":"Shrimp Etouffee"},{"name":"White Seasoned Rice"}],"Vegetable":[{"name":"Vegetarian Chili"},{"name":"Yellow Rice"},{"name":"Pot Likker Collard Greens"}],"Grill":[{"name":"Classic Cheeseburger on a Toasted Bun"},{"name":"Grilled Cheese Sandwich"},{"name":"Deli Chicken Salad on Kaiser"},{"name":"Hummus & Avocado Petite Wrap"},{"name":"French Fries"}]},"dinner":{"Vegetarian/Vegan":[{"name":"Spicy Eggplant with Garbanzo Beans"},{"name":"Basmati Rice"}],"Chefs Choice":[{"name":"Ginger Soy Vegetables"},{"name":"Asian Green Rice"},{"name":"Greek Vegetable Wrap"}],"Entrée":[{"name":"Grilled Bourbon Pork Chop"},{"name":"Roasted Sweet Potatoes"},{"name":"Whole Green Beans"}],"Deli":[{"name":"Ham & Cheese Sub"},{"name":"French Fries"}],"Dessert":[{"name":"Cheesecake Slice"},{"name":"Chocolate Chip Bread Pudding"}],"International":[{"name":"Gia Nuong"},{"name":"Vietnamese Fried Rice"},{"name":"Asian Slaw"}]}},{"dayname":"Tuesday","breakfast":{"Hot Cereal":[{"name":"Home Style Oatmeal"},{"name":"Oatmeal"}],"Chefs Choice":[{"name":"Fried Eggs"},{"name":"Scrambled Eggs"},{"name":"Omelet Bar"}],"Entrée":[{"name":"Hard Cooked Eggs"},{"name":"Leek, Spinach, and Mushroom Frittata"},{"name":"Turkey Sausage Links"},{"name":"Hash Browned Potatoes"}],"Vegetable":[{"name":"Brown Rice"}],"Grill":[{"name":"French Toast Sticks with Syrup"},{"name":"Sausage Gravy & Biscuit"}]},"lunch":{"Soup":[{"name":"Hearty Beef Vegetable Soup"},{"name":"Potato Leek Soup"}],"Vegetarian/Vegan":[{"name":"Roasted Portobello Mushrooms"},{"name":"Quinoa with Squash, Tomatoes and Basil"}],"Pizza":[{"name":"Pepperoni Pizza"},{"name":"Broccoli Cheddar Ranch Pizza"},{"name":"Eggplant Parmesan Pizzetta"},{"name":"Herb Seasoned Breadsticks"}],"Chefs Choice":[{"name":"Rigatoni with Arrabiata Sauce"},{"name":"Breaded Pork Cutlet w/Pineapple BBQ"},{"name":"Bomba di Riso (Baked Rice Torta)"}],"Entrée":[{"name":"Basmati Rice"},{"name":"Green Peas"}],"Grill":[{"name":"Classic Cheeseburger on a Toasted Bun"},{"name":"Roasted Veggie Caesar Petite Wrap"},{"name":"Sausage Sandwich w/Peppers & Onions"},{"name":"Grilled Cheese Sandwich"},{"name":"French Fries"}],"International":[{"name":"Steamed Brown Rice"}],"To Go":[{"name":"Mini Burger Sliders"}]},"dinner":{"Vegetarian/Vegan":[{"name":"Rice Noodle Salad"}],"Chefs Choice":[{"name":"Beef & Mushroom Saute w/Potatoes"},{"name":"Traditional Rotisserie Chicken"},{"name":"Eggplant Caponata Griddle Sandwich"}],"Entrée":[{"name":"Baked Potato"},{"name":"Roasted Vegetables"}],"Deli":[{"name":"Chef Salad Wrap"},{"name":"French Fries"}],"International":[{"name":"Buffalo Chicken Salad"}]}},{"dayname":"Wednesday","breakfast":{"Hot Cereal":[{"name":"Millet"},{"name":"Oatmeal"}],"Chefs Choice":[{"name":"Fried Eggs"},{"name":"Scrambled Eggs"},{"name":"Omelet Bar"}],"Entrée":[{"name":"Banana Pancakes"},{"name":"Homestyle Sausage Breakfast Bowl"}],"International":[{"name":"Brazilian Rice"}],"Meat":[{"name":"Mexican Scrambled Eggs"},{"name":"Pork Sausage Patty"},{"name":"Sliced Lyonnaise Potatoes"},{"name":"Hard Cooked Eggs"}]},"lunch":{"Soup":[{"name":"Old Fashioned Turkey Noodle Soup"},{"name":"Butternut Squash & Sweet Potato Soup"}],"Vegetarian/Vegan":[{"name":"Bandito Beans"},{"name":"Brown Rice"},{"name":"Cilantro Lime Pickled Red Onions"},{"name":"Braised Vegetables & Quinoa"}],"Pizza":[{"name":"Cheese Pizza"},{"name":"Antipasto Pizza"},{"name":"Meatball Flatbread Melt"},{"name":"Herb Seasoned Breadsticks"}],"Chefs Choice":[{"name":"Italian Sausage and Fennel Risotto"}],"Entrée":[{"name":"Hilachas"},{"name":"Aztec Corn"},{"name":"Grilled Zucchini"}],"Grill":[{"name":"Nacho Bar"},{"name":"French Fries"},{"name":"Fresh Watermelon Wedge"}],"Dessert":[{"name":"Old-Fashioned Molasses Cookies"},{"name":"Chewy Chocolate Rice Krispie Bars"},{"name":"Strawberry Jell-O Parfait"}],"International":[{"name":"Brazilian Rice"}],"To Go":[{"name":"Roasted Garlic White Flatbread Pizza"}]},"dinner":{"Soup":[{"name":"Old Fashioned Turkey Noodle Soup"},{"name":"Butternut Squash & Sweet Potato Soup"}],"Vegetarian/Vegan":[{"name":"Lentil Stew"},{"name":"Roasted Yukon Gold Potatoes"},{"name":"Broccoli Cheddar Quiche"}],"Pizza":[{"name":"Cheese Pizza"},{"name":"Meatball Flatbread Melt"},{"name":"Antipasto Pizza"},{"name":"Herb Seasoned Breadsticks"}],"Chefs Choice":[{"name":"Chicken Burrito Bowl"}],"Entrée":[{"name":"Oven Roasted Top Round Beef"},{"name":"Mashed Potatoes"},{"name":"Roasted Carrots"},{"name":"Horseradish Cream Spread"}],"Deli":[{"name":"Tuscan Turkey Biggie Sandwich"},{"name":"French Fries"}],"Dessert":[{"name":"Cupcake Bar"},{"name":"Butterscotch Vanilla Pudding Cup"}],"International":[{"name":"Blackened Chicken Breast Plate"},{"name":"Brazilian Rice"}]}},{"dayname":"Thursday","breakfast":{"Hot Cereal":[{"name":"Muesli"}],"Chefs Choice":[{"name":"Oatmeal"},{"name":"Hard Cooked Eggs"},{"name":"Fried Eggs"},{"name":"Scrambled Eggs"},{"name":"Omelet Bar"}],"Entrée":[{"name":"Cinnamon Raisin French Toast"},{"name":"Roasted Vegetable Frittata"},{"name":"Fried Egg O'Muffin"}],"Bread":[{"name":"Applesauce Coffee Cake"},{"name":"Chocolate Chunk Muffins"}],"International":[{"name":"Jasmine Steamed Rice"}],"Meat":[{"name":"Chorizo Sausage"}],"Potato":[{"name":"Hash Browned Potatoes"}]},"lunch":{"Soup":[{"name":"Grilled Chicken Tortilla Soup"},{"name":"Creamy Broccoli Cheddar Soup"}],"Vegetarian/Vegan":[{"name":"Tossed Wheat Berry & Corn Salad"},{"name":"Grilled Vegetable Wrap"},{"name":"Roasted Portobello Foccacia"}],"Pizza":[{"name":"Spinach & Ricotta Flat Bread Pizza"},{"name":"Pepperoni Pizza"},{"name":"Southwestern Vegetable Calzone"},{"name":"Herb Seasoned Breadsticks"}],"Chefs Choice":[{"name":"Bean & Cheese Chimichanga"}],"Entrée":[{"name":"Chicken Pot Pie"},{"name":"Boniato Smash"},{"name":"Steamed Cauliflower with Cheese Sauce"}],"Grill":[{"name":"Hot Dog on Bun"},{"name":"Pizza Burger"},{"name":"Cheese Quesadilla"},{"name":"BLT Panini"},{"name":"French Fries"}],"Dessert":[{"name":"Orange Sparkler Cookies"},{"name":"Oreo Cookie Blondies"},{"name":"Raspberry Jell-O Parfait"}],"International":[{"name":"Jasmine Steamed Rice"}],"To Go":[{"name":"Chef Salad Wrap"}]},"dinner":{"Soup":[{"name":"Grilled Chicken Tortilla Soup"},{"name":"Creamy Broccoli Cheddar Soup"}],"Vegetarian/Vegan":[{"name":"Grilled Vegetables"},{"name":"Chickpea Couscous Burger"},{"name":"Grilled Pita"},{"name":"Vegetarian Chili"}],"Pizza":[{"name":"Pepperoni Pizza"},{"name":"Spinach & Ricotta Flat Bread Pizza"},{"name":"Southwestern Vegetable Calzone"},{"name":"Herb Seasoned Breadsticks"}],"Chefs Choice":[{"name":"Kung Pao Beef"},{"name":"Jasmine Rice"}],"Entrée":[{"name":"Chicken Patty Cordon Bleu"},{"name":"Oven Roast Herbed Red Potatoes"},{"name":"Sliced Steamed Carrots"}],"Deli":[{"name":"Deviled Egg Salad Sandwich"},{"name":"French Fries"}],"Dessert":[{"name":"Devil's Food Cake with Mocha Icing"},{"name":"Dulce de Leche Pudding Cup"},{"name":"Raspberry Jell-O Parfait"}],"International":[{"name":"Bacon Avocado Grilled Cheese & Soup"},{"name":"Jasmine Steamed Rice"}]}},{"dayname":"Friday","breakfast":{"Hot Cereal":[{"name":"Cooked Quinoa"},{"name":"Cinnamon"}],"Chefs Choice":[{"name":"Oatmeal"},{"name":"Hard Cooked Eggs"},{"name":"Fried Eggs"},{"name":"Scrambled Eggs"},{"name":"Omelet Bar"}],"Entrée":[{"name":"Chocolate Chip Pancakes"},{"name":"Eggs Scrambled with Sausage & Peppers"},{"name":"Southwestern Breakfast Panini"}],"Bread":[{"name":"Glazed Cinnamon Roll"},{"name":"Low Fat Blueberry Muffin (2)"}],"International":[{"name":"White Seasoned Rice"}],"Meat":[{"name":"Grilled Kielbasa"}],"Potato":[{"name":"Oven Roasted Potato Wedges"}]},"lunch":{"Soup":[{"name":"New England Clam Chowder"},{"name":"Vegetarian Lentil & Spinach Soup"}],"Vegetarian/Vegan":[{"name":"Spicy Kale & Beans with Couscous"},{"name":"Hummus & Tabbouleh Wrap"}],"Pizza":[{"name":"Cheese Pizza"},{"name":"Vegetable Lovers Feast Pizza"},{"name":"Chicken, Broccoli, &Mushroom Calzone"},{"name":"Herb Seasoned Breadsticks"}],"Chefs Choice":[{"name":"Grilled Fish Taco"}],"Entrée":[{"name":"French Dip Sandwich"},{"name":"Steak Cut French Fries"},{"name":"Fresh Broccoli"}],"Grill":[{"name":"Classic Cheeseburger on a Toasted Bun"},{"name":"Grilled Cheese Sandwich"},{"name":"Chicken Bruschetta Sandwich"},{"name":"Tuna Salad Sandwich on Kaiser"},{"name":"Sweet Potato Fries"},{"name":"Carrot & Celery Sticks"}],"Dessert":[{"name":"Chocolate Chip Cookie"},{"name":"Marshmallow Rice Krispies Bars"},{"name":"Chocolate Pudding Cup"}],"International":[{"name":"White Seasoned Rice"}],"To Go":[{"name":"Lasagna Flat Bread Pizza"}]},"dinner":{"Soup":[{"name":"New England Clam Chowder"},{"name":"Vegetarian Lentil & Spinach Soup"}],"Vegetarian/Vegan":[{"name":"Ginger Tofu & Vegetable Stir Fry"},{"name":"Jasmine Rice"},{"name":"Roasted Vegetable Lasagna with Marinara"}],"Pizza":[{"name":"Cheese Pizza"},{"name":"Vegetable Lovers Feast Pizza"},{"name":"Chicken, Broccoli, &Mushroom Calzone"},{"name":"Herb Seasoned Breadsticks"}],"Chefs Choice":[{"name":"Chicken Pad Thai"}],"Entrée":[{"name":"Minnesota Fish Fingers"},{"name":"Rice Pilaf"},{"name":"Buttered Lima Beans"}],"Deli":[{"name":"French Fries"}],"Dessert":[{"name":"Homestyle Sour Cream Pound Cake"},{"name":"Chocolate Pudding Cup"},{"name":"Berry Blue Jell-O Parfait"}],"International":[{"name":"Hot Dog Bar"},{"name":"White Seasoned Rice"}]}},{"dayname":"Saturday","breakfast":{"Bread":[{"name":"Double Lemon Poppyseed Coffee Cake"},{"name":"Mini Brown Sugar Cinnamon Scone"}],"Fruit":[{"name":"Fresh Fruit Salad"}]},"lunch":{"Soup":[{"name":"Three Mushroom Barley"}],"Vegetarian/Vegan":[{"name":"Spinach Fettuccine w/Tomato Basil Sauce"}],"Chefs Choice":[{"name":"Oatmeal"},{"name":"Hard Cooked Eggs"},{"name":"Fried Eggs"},{"name":"Scrambled Eggs"},{"name":"Omelet Bar"}],"Entrée":[{"name":"Grits"},{"name":"Texas French Toast"},{"name":"Eggs Benedict with Canadian Bacon"},{"name":"Hash Browned Potatoes"},{"name":"Sausage Links"},{"name":"Honey BBQ Roast Chicken Sandwich"},{"name":"Cajun Spiced Roasted Potatoes"},{"name":"Southern Cole Slaw"}],"Dessert":[{"name":"Oatmeal Raisin Cookies"},{"name":"Chocolate Vanilla Sundae Pudding Cup"},{"name":"Lemon Jell-O Parfait"}]},"dinner":{"Soup":[{"name":"Three Mushroom Barley"}],"Vegetarian/Vegan":[{"name":"Vegan Chow Mein"}],"Pizza":[{"name":"Cheese Pizza"},{"name":"Pepperoni Pizza"},{"name":"Vegetable Lovers Calzone"},{"name":"Herb Seasoned Breadsticks"}],"Dessert":[{"name":"Blueberry Cobbler with Biscuit Topping"},{"name":"Chocolate Vanilla Sundae Pudding Cup"},{"name":"Lemon Jell-O Parfait"}],"Theme Cuisine":[{"name":"Tomato & Cucumber Salad"},{"name":"Homestyle Meatloaf"},{"name":"Macaroni & Cheese"},{"name":"Mashed Potatoes"},{"name":"Whole Green Beans"},{"name":"Broccoli, Cheese,& Rice Casserole"},{"name":"Old-Fashioned Cornbread"}]}},{"dayname":"Sunday","breakfast":{"Bread":[{"name":"Cobblestones with Icing (CS)"},{"name":"Raspberry Sour Cream Muffins"}],"Fruit":[{"name":"Fresh Fruit Salad"}]},"lunch":{"Soup":[{"name":"Cream of Broccoli Soup"}],"Vegetarian/Vegan":[{"name":"Curried Rice & Lentils"}],"Chefs Choice":[{"name":"Oatmeal"},{"name":"Hard Cooked Eggs"},{"name":"Fried Eggs"},{"name":"Scrambled Eggs"},{"name":"Omelet Bar"}],"Entrée":[{"name":"Cream of Rice Cereal"},{"name":"Waffles Diana with Blueberries"},{"name":"Croissant with Eggs & Cheese"},{"name":"Home Fried Potatoes"},{"name":"Frizzled Ham"},{"name":"Old-Fashioned Beef Stew"},{"name":"Mashed Red Potatoes"},{"name":"Spinach with Garlic & Onions"}],"Dessert":[{"name":"Sugar Cookies"},{"name":"Banana Cream Pie Pudding Cup"},{"name":"Lime Jell-O Parfait"}]},"dinner":{"Soup":[{"name":"Cream of Broccoli Soup"}],"Vegetarian/Vegan":[{"name":"Butternut Squash & Lentils"},{"name":"Hummus Cold Plate with Pita"}],"Pizza":[{"name":"Cheese Pizza"},{"name":"Pepperoni Pizza"},{"name":"Wild Mushroom & Pesto Flatbread Pizza"},{"name":"Herb Seasoned Breadstick"}],"Chefs Choice":[{"name":"Spaghetti & Meat Sauce"}],"Entrée":[{"name":"Creole Fried Chicken Breast"},{"name":"Garlic Mashed Potatoes"},{"name":"Creamed Corn"}],"Grill":[{"name":"Beef Philly-Style Cheese Steak"},{"name":"French Fries"}],"Dessert":[{"name":"Carrot Cake with Cream Cheese Frosting"},{"name":"Chocolate Cream Pie"},{"name":"Lime Jell-O Parfait"}]}}]"""
test_prompt = "what's for lunch on Wednesday"
days_to_vals = { "monday" : 0, "tuesday" : 1, "wednesday" : 2, "thursday" : 3, "friday" : 4, "saturday": 5, "sunday" : 6 }
vals_to_days = {0:"monday",1:"tuesday",2:"wednesday",3:"thursday", 4:"friday", 5:"saturday", 6:"sunday"}
meals = ["lunch", "breakfast", "dinner", "brunch"]
eastern = timezone("US/Eastern")



def today_is():
  	now = datetime.today().replace(tzinfo=eastern).weekday()
  	return vals_to_days[now]

def tomorrow_is():
  	now = (datetime.today().replace(tzinfo=eastern).weekday() + 1) % 7
  	return vals_to_days[now]

class Day:
	def __init__(self,name):
		name = name.lower()
		if name == "today" or name == "tonight":
			self.name = today_is()
		elif name == "tomorrow":
			self.name = tomorrow_is()
		else:
			self.name = name
		self.get_date()

	def __repr__(self):
		return "Day <%s>" % self.name

	def get_date(self):
		#what is the date today?
		#what is the day today?
		#how many days in front/behind are we?
		#add that many days to the date
		now = datetime.today().replace(tzinfo=eastern)
		today_number = now.weekday()
		name_number = days_to_vals[self.name]
		day_difference = today_number - name_number
		if day_difference == 0:
			self.date = now
		elif day_difference > 0:
			self.date = now - timedelta(days=abs(day_difference))
		else:
			self.date = now + timedelta(days=abs(day_difference))

class MealsParser():
	def __init__(self,day_requested,meal_requested):
		self.meal_json = self.get_meals_json()
		self.dishes = self.get_dishes(day_requested,meal_requested,self.meal_json)

	def get_meals_json(self):
		return json.loads(test_meals.replace(u"Entr\xe9e",u"Entree"))

	def meals_in_a_day(self,day,meals_json):
		index = days_to_vals[day.name]
		return meals_json[index]
	
	def get_specific_meal(self,meal_requested,meals_in_a_day):
		return meals_in_a_day.get(meal_requested,"meal_not_found")
	
	def meal_to_list_of_dishes(self,meal):
		meals = []
		for groups_of_dishes in meal.values():
			for dish in groups_of_dishes:
				meals.append(dish["name"])
		return sorted(meals)
	
	def get_dishes(self,day,meal_requested,meals_json):
		meals_in_day = self.meals_in_a_day(day, meals_json)
		meal = self.get_specific_meal(meal_requested, meals_in_day)
		if meal == "meal_not_found":
			return meal
		dishes = self.meal_to_list_of_dishes(meal)
		return dishes

class MessageParser():
	def __init__(self,msg):
		msg = msg.lower()
		self.msg = msg
		self.meal = self.get_meal(msg)
		self.day = self.get_day(msg)

	def get_meal(self,msg):
		breakfast = False
		if "breakfast" in msg:
			breakfast = True
		if "lunch" in msg:
			if breakfast:
				return "brunch"
			return "lunch"
		if breakfast:
			return "breakfast"
		if "brunch" in msg:
			return "brunch"
		if "dinner" in msg:
			return "dinner"
	
	def get_day(self,msg):
		if msg.lower() != msg:
			raise ValueError, "Message must be in lower case"
		day = Day("today") #default in case a day is not included
		options = [Day("monday"), Day("tuesday") , Day("wednesday"), Day("thursday"), Day("friday"), Day("saturday"), Day("sunday"), Day("today"), Day("tomorrow"), Day("tonight") ]
		for option in options:
			if option.name in msg:
				day = option
		return day

class MessageResponseBuilder():
	def __init__(self,msg):
		msgP = MessageParser(msg)
		m = MealsParser(msgP.day,msgP.meal)
		dishes = m.dishes
		if dishes == "meal_not_found":
			self.response = "Do you want breakfast, lunch, dinner, or brunch? Also, I can't detect typos. Try again!"
			return None
		date = msgP.day.date
		preamble = "Food for %s on %s, %s/%s: " % (msgP.meal,msgP.day.name,date.month,date.day)
		self.response = preamble + "; ".join(dishes)

if __name__ == '__main__':
	a = Day("friday")
	a.get_date()
	print a.name
	print a.date
	msg = "what's for dinner on Tuesday"
	# msgP = MessageParser(msg)
	# print msgP.day
	# print msgP.meal
	# m = MealsParser(msgP.day,msgP.meal)
	# print m.dishes
	mrb = MessageResponseBuilder(msg)
	print mrb.response

	# print meals_in_a_day(a)
