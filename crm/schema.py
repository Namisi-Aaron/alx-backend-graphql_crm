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

class ProductInfo(graphene.ObjectType):
    name = graphene.String()
    stock = graphene.Int()

class UpdateLowStockProducts(graphene.Mutation):
    success = graphene.Boolean()
    products = graphene.List(ProductInfo)

    class Arguments:
        pass

    def mutate(root, info):

            try:
                restocked_products = []
                low_stock_products = Product.objects.filter(stock__lt=10)

                if low_stock_products.exists():
                    for product in low_stock_products:
                        product.stock += 10
                        product.save()
                        restocked_products.append(
                            ProductInfo(name=product.name, stock=product.stock)
                        )

                    return UpdateLowStockProducts(success=True, products=restocked_products)
                
                else:
                    return UpdateLowStockProducts(success=False, products=[])

            except Exception as e:
                print(f"Error: {e}")
                return UpdateLowStockProducts(success=False, products=[])

class Query(graphene.ObjectType):
    hello = graphene.String()
    all_products = graphene.List(ProductType)
    all_customers = graphene.List(CustomerType)
    all_orders = graphene.List(OrderType)

    def resolve_hello(root, info):
        return "Hello, Graphql!"

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
    update_low_stock_products = UpdateLowStockProducts.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
