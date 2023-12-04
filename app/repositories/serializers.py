from app.plugins import ma

from .models import Beverage, Element, Ingredient, Order, OrderDetail, Size


class ElementSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Element
        load_instance = True
        fields = ("_id", "name", "price", "element_type")


class BeverageSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Beverage
        load_instance = True
        fields = ("_id", "name", "price")


class IngredientSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ingredient
        load_instance = True
        fields = ("_id", "name", "price")


class SizeSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Size
        load_instance = True
        fields = ("_id", "name", "price")


class OrderDetailSerializer(ma.SQLAlchemyAutoSchema):
    element = ma.Nested(ElementSerializer)

    class Meta:
        model = OrderDetail
        load_instance = True
        fields = ("element_price", "element")


class OrderSerializer(ma.SQLAlchemyAutoSchema):
    size = ma.Nested(SizeSerializer)
    detail = ma.Nested(OrderDetailSerializer, many=True)

    class Meta:
        model = Order
        load_instance = True
        fields = (
            "_id",
            "client_name",
            "client_dni",
            "client_address",
            "client_phone",
            "date",
            "total_price",
            "size",
            "detail",
        )
