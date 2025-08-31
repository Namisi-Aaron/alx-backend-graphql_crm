import graphene
from crm.types import ProductType, CustomerType, OrderType, CustomerInput, ProductInfo
from crm.models import Product, Customer, Order

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
