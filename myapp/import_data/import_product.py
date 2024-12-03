from django.db import transaction
from django_q.tasks import async_task
from myapp.models import Product

def import_products(data):
    with transaction.atomic():
        for product_data in data:
            Product.objects.create(
                name=product_data['name'],
                price=product_data['price'],
                in_stock=product_data['in_stock']
            )