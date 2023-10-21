from .order import OrderController

order_controller = OrderController()


class ReportController():

    def get_orders_data(self):
        orders = order_controller.get_all()
        client_names = [order['client_name'] for order in orders[0]]
        order_sizes = [order['size']['name'] for order in orders[0]]
        order_dates_and_prices = [
            {'date': order['date'], 'price': order['total_price']} for order in orders[0]]
        order_ingredients = []
        order_beverages = []

        for order in orders[0]:
            orders_detail = order['detail']
            detail_len = len(orders_detail)
            for i in range(detail_len):
                if orders_detail[i]['ingredient']:
                    order_ingredients.extend(
                        [orders_detail[i]['ingredient']['name']])
                if orders_detail[i]['beverage']:
                    order_beverages.extend(
                        [orders_detail[i]['beverage']['name']])

        return {'clients': client_names,
                'sizes': order_sizes,
                'dates_and_prices': order_dates_and_prices,
                'ingredients': order_ingredients,
                'beverages': order_beverages
                }

    def get_the_most_requested_ingredient(self):
        orders_data = self.get_orders_data()
        ingredients = orders_data['ingredients']
        return max(set(ingredients), key=ingredients.count)

    def get_month_with_more_revenue(self):
        orders_data = self.get_orders_data()
        dates_and_prices = orders_data['dates_and_prices']
        months_revenue = {}
        for date_price in dates_and_prices:
            month = date_price['date'].split('-')[1]
            if month not in months_revenue:
                months_revenue[month] = 0
            months_revenue[month] += date_price['price']
        return max(months_revenue, key=months_revenue.get)

    def get_top_customers(self, top: int):
        orders_data = self.get_orders_data()
        clients = orders_data['clients']
        top_clients = sorted(
            set(clients), key=clients.count, reverse=True)[:top]
        return top_clients

    def generate_report(self):
        return {
            'the_most_requested_ingredient': self.get_the_most_requested_ingredient(),
            'month_with_more_revenue': self.get_month_with_more_revenue(),
            'top_customers': self.get_top_customers(3)
        }
