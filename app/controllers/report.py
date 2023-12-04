from .order import OrderController


class ReportController:
    @staticmethod
    def get_orders_data():
        orders, _ = OrderController.get_all()
        client_names = [order["client_name"] for order in orders]
        order_dates_and_prices = [
            {"date": order["date"], "price": order["total_price"]} for order in orders
        ]
        order_ingredients = []
        order_beverages = []

        for order in orders:
            order_detail = order["detail"]
            for detail in order_detail:
                element_type = detail["element"]["element_type"]
                element_name = detail["element"]["name"]
                if element_type == "ingredient":
                    order_ingredients.append(element_name)
                elif element_type == "beverage":
                    order_beverages.append(element_name)

        return {
            "clients": client_names,
            "dates_and_prices": order_dates_and_prices,
            "ingredients": order_ingredients,
            "beverages": order_beverages,
        }

    @staticmethod
    def get_the_most_requested_ingredient(orders_data: dict):
        ingredients = orders_data["ingredients"]
        return max(set(ingredients), key=ingredients.count)

    @staticmethod
    def get_the_most_requested_beverage(orders_data: dict):
        beverages = orders_data["beverages"]
        return max(set(beverages), key=beverages.count)

    @staticmethod
    def get_month_with_more_revenue(orders_data: dict):
        dates_and_prices = orders_data["dates_and_prices"]
        months_revenue = {}
        for date_price in dates_and_prices:
            month = date_price["date"].split("-")[1]
            if month not in months_revenue:
                months_revenue[month] = 0
            months_revenue[month] += date_price["price"]
        return max(months_revenue, key=months_revenue.get)

    @staticmethod
    def get_top_customers(orders_data: dict, top: int):
        clients = orders_data["clients"]
        top_clients = sorted(set(clients), key=clients.count, reverse=True)[:top]
        return top_clients

    @classmethod
    def generate_report(cls):
        orders_data = cls.get_orders_data()
        return {
            "the_most_requested_ingredient": cls.get_the_most_requested_ingredient(
                orders_data
            ),
            "the_most_requested_beverage": cls.get_the_most_requested_beverage(
                orders_data
            ),
            "month_with_more_revenue": cls.get_month_with_more_revenue(orders_data),
            "top_customers": cls.get_top_customers(orders_data, 3),
        }
