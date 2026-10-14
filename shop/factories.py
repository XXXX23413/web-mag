import factory
from .models import Category,Brand,Product


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f'Категория{n}')
    slug = factory.Sequence(lambda n: f'category-{n}')
    is_active = True


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Sequence(lambda n: f'Бренд {n}')
    slug = factory.Sequence(lambda n: f'brand-{n}')
    is_active = True


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Product

    category = factory.SubFactory(CategoryFactory)
    brand = factory.SubFactory(BrandFactory)
    name = factory.Sequence(lambda n: f'Товар {n}')
    slug = factory.Sequence(lambda n: f'product-{n}')
    short_description = 'Тестовое описание'
    price = 1000.00
    stock_quantity =10 
    is_active = True                    