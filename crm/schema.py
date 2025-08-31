import graphene
from graphene_django import DjangoObjectType

from .models import Product, Customer, Order

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

class ProductMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        stock = graphene.Int(required=True)

    product = graphene.Field(ProductType)

    def mutate(root, info, name, price, stock):
        product = Product(name=name, price=price, stock=stock)
        product.save()
        return ProductMutation(product=product)

class CustomerMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=True)

    customer = graphene.Field(CustomerType)

    def mutate(root, info, name, email, phone):
        customer = Customer(name=name, email=email, phone=phone)
        customer.save()
        return CustomerMutation(customer=customer)

class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String(required=False)

class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        customers = graphene.List(CustomerInput, required=True)

    success = graphene.Boolean()
    customers = graphene.List(CustomerType)

    def mutate(root, info, customers):
        created_customers = []
        for customer_data in customers:
            customer = Customer(**customer_data)
            customer.save()
            created_customers.append(customer)
        return BulkCreateCustomers(success=True, customers=created_customers)

class OrderMutation(graphene.Mutation):
    class Arguments:
        customer_id = graphene.Int(required=True)
        product_ids = graphene.List(graphene.Int, required=True)

    order = graphene.Field(OrderType)

    def mutate(root, info, customer_id, product_ids):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            raise Exception("Customer not found")
        
        order = Order(customer_id=customer)
        order.save()

        product_ids = Product.objects.filter(id__in=product_ids)
        order.product_ids.set(product_ids)
        return OrderMutation(order=order)

class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)
    all_customers = graphene.List(CustomerType)
    all_orders = graphene.List(OrderType)

    def resolve_all_products(root, info):
        return Product.objects.all()

    def resolve_all_customers(root, info):
        return Customer.objects.all()

    def resolve_all_orders(root, info):
        return Order.objects.all()

class Mutation(graphene.ObjectType):
    create_product = ProductMutation.Field()
    create_customer = CustomerMutation.Field()
    create_order = OrderMutation.Field()
    bulk_create_customers = BulkCreateCustomers.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
