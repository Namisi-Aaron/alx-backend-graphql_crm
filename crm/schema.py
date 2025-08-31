import graphene
from django.db.models import Sum

from crm.types import (
    ProductType, CustomerType,
    OrderType
)
from crm.models import Product, Customer, Order
from crm.mutations import (
    ProductMutation,
    CustomerMutation,
    OrderMutation,
    BulkCreateCustomers,
    UpdateLowStockProducts
)

class Query(graphene.ObjectType):
    hello = graphene.String()
    all_products = graphene.List(ProductType)
    all_customers = graphene.List(CustomerType)
    all_orders = graphene.List(OrderType)

    total_customers = graphene.Int()
    total_orders = graphene.Int()
    total_revenue = graphene.Float()

    def resolve_hello(root, info):
        return "Hello, Graphql!"

    def resolve_all_products(root, info):
        return Product.objects.all()

    def resolve_all_customers(root, info):
        return Customer.objects.all()

    def resolve_all_orders(root, info):
        return Order.objects.all()
    
    def resolve_total_customers(root, info):
        return Customer.objects.count()

    def resolve_total_orders(root, info):
        return Order.objects.count()

    def resolve_total_revenue(root, info):
        orders = Order.objects.all()
        return sum(
            p.price for order in orders for p in order.product_ids.all()
        )

class Mutation(graphene.ObjectType):
    create_product = ProductMutation.Field()
    create_customer = CustomerMutation.Field()
    create_order = OrderMutation.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    update_low_stock_products = UpdateLowStockProducts.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
