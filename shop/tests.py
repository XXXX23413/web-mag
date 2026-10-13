from django.test import TestCase
from django.urls import reverse
from .models import Category,Brand,Product


class Catalog(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name = 'Смартфоны',
            slug = 'smartfony',
            is_active = True
        )
        self.brand = Brand.objects.create(
            name = 'Apple',
            slug = 'apple',
            is_active = True
        )
        self.product = Product.objects.create(
            category= self.category,
            brand = self.brand,
            name = 'IPHONE 15',
            slug = 'iphone-15',
            price = 99999.00,
            is_active=True
        )
    def test_catalog_page_open(self):
        response = self.client.get(reverse('shop:catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'shop/catalog.html')
        self.assertIn(self.product,response.context['products'])
        self.assertContains(response,'IPHONE 15')
    def test_catalog_filter_by_category(self):
        other_category = Category.objects.create(
            name = 'Наушники',
            slug = 'naushniki',
            is_active =True
        )
        other_product = Product.objects.create(
            category= other_category,
            name ='Sony WH-1000XM5',
            slug = 'sony-wh-1000xm5',
            price = 29999.00,
            is_active =True
        )        
        response = self.client.get(
            reverse('shop:catalog'),
            {'category':'smartfony'}
        )
        self.assertEqual(response.status_code,200)
        self.assertIn(self.product,response.context['products'])
        self.assertNotIn(other_product,response.context['products'])