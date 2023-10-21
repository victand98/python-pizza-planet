from ..controllers import OrderController
from ..repositories.managers import BeverageManager, IngredientManager, OrderManager, SizeManager
from faker import Faker
import time

fake = Faker()

NUMBER_OF_ORDERS = 100
NUMBER_OF_CLIENTS = 30
PRICE_RANGES = {
    "beverage": (0.25, 10),
    "ingredient": (0.25, 5),
    "size": (5, 40)
}

ingredient_names = [
    "Pepperoni",
    "Mushrooms",
    "Onions",
    "Sausage",
    "Bacon",
    "Extra cheese",
    "Black olives",
    "Green peppers",
    "Pineapple",
    "Spinach"
]

beverage_names = [
    "Coke",
    "Sprite",
    "Fanta",
    "Lemonade",
    "Iced Tea",
    "Root Beer",
    "Dr. Pepper",
    "Mountain Dew",
    "Pepsi",
    "Ginger Ale"
]

size_names = [
    "Small",
    "Medium",
    "Large",
    "Extra Large",
    "Party Size"
]


def generate_random_price(object_type):
    min_value, max_value = PRICE_RANGES[object_type]
    return fake.pyfloat(left_digits=None, right_digits=2, positive=True, min_value=min_value, max_value=max_value)


def populate_fake_ingredients():
    for i in range(len(ingredient_names)):
        IngredientManager.create({
            "name": ingredient_names[i],
            "price": generate_random_price('ingredient'),
        })


def populate_fake_sizes():
    for i in range(len(size_names)):
        SizeManager.create({
            "name": size_names[i],
            "price": generate_random_price('size'),
        })


def populate_fake_beverages():
    for i in range(len(beverage_names)):
        BeverageManager.create({
            "name": beverage_names[i],
            "price": generate_random_price('beverage'),
        })


def get_random_order_size():
    sizes = SizeManager.get_all()
    return sizes[fake.random_int(min=0, max=len(sizes) - 1)]["_id"]


def get_random_ingredients(max_ingredients: int):
    ingredients = IngredientManager.get_all()
    num_ingredients = fake.random_int(min=1, max=max_ingredients)
    selected_ingredients = []
    while len(selected_ingredients) < num_ingredients:
        ingredient = ingredients[fake.random_int(
            min=0, max=len(ingredients) - 1)]['_id']
        if ingredient not in selected_ingredients:
            selected_ingredients.append(ingredient)
    return selected_ingredients


def get_random_beverages(max_beverages: int):
    beverages = BeverageManager.get_all()
    num_beverages = fake.random_int(min=1, max=max_beverages)
    selected_beverages = []
    while len(selected_beverages) < num_beverages:
        beverage = beverages[fake.random_int(
            min=0, max=len(beverages) - 1)]['_id']
        if beverage not in selected_beverages:
            selected_beverages.append(beverage)
    return selected_beverages


def generate_client():
    return {
        "client_name": fake.name(),
        "client_address": fake.address(),
        "client_phone": fake.phone_number(),
        "client_dni": fake.random_int(min=1000000000, max=9999999999)
    }


def populate_fake_orders():
    order_controller = OrderController()

    clients = []
    for _ in range(NUMBER_OF_CLIENTS):
        clients.append(generate_client())

    for _ in range(NUMBER_OF_ORDERS):
        size_id = get_random_order_size()
        ingredients_ids = get_random_ingredients(5)
        beverages_ids = get_random_beverages(5)
        size_price = SizeManager.get_by_id(size_id).get('price')
        ingredients = IngredientManager.get_by_id_list(ingredients_ids)
        beverages = BeverageManager.get_by_id_list(beverages_ids)
        total_price = order_controller.order_creator.calculate_order_price(
            size_price, ingredients, beverages)
        client = clients[fake.random_int(min=0, max=len(clients) - 1)]
        OrderManager.create({
            "date": fake.date_time_between(start_date="-1y", end_date="now", tzinfo=None),
            "size_id": size_id,
            "total_price": total_price,
            "client_name": client["client_name"],
            "client_dni": client["client_dni"],
            "client_address": client["client_address"],
            "client_phone": client["client_phone"],
        }, ingredients, beverages)


def populate_database():
    try:
        populate_fake_sizes()
        populate_fake_beverages()
        populate_fake_ingredients()
        time.sleep(2)
        populate_fake_orders()
        print('The database was populated successfully')
    except:
        print('An error occurred while populating the database')
