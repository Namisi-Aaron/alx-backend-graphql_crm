import graphene
from graphene_django import DjangoObjectType
from crm.models import Product, Customer, Order

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("name", "price", "stock")

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ("name", "email", "phone")

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ("id", "customer_id", "product_ids", "order_date")

class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String(required=False)

class ProductInfo(graphene.ObjectType):
    name = graphene.String()
    stock = graphene.Int()
