import factory
from .models import Category,Brand,Product
from faker import Faker

fake = Faker('ru_RU')

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.LazyFunction(lambda: fake.word().capitalize())
    slug = factory.LazyFunction(lambda: fake.slug())
    is_active = True

class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.LazyFunction(lambda: fake.company())
    slug = factory.LazyFunction(lambda: fake.slug())
    is_active=True

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Product

    category = factory.SubFactory(CategoryFactory)
    brand = factory.SubFactory(BrandFactory)
    name = factory.LazyFunction(lambda:fake.word().capitalize()) 
    slug = factory.LazyFunction(lambda:fake.slug())
    short_description = 'Тестовое описание'
    price = 1000.00
    stock_quantity = 10
    is_active =True                   