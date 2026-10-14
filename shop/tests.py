from django.test import TestCase
from django.urls import reverse
from .factories import CategoryFactory,BrandFactory,ProductFactory


class CatalogTest(TestCase):
   
    def test_catalog_page_open(self):
        product = ProductFactory(name = 'IPHONE 15')
        response = self.client.get(reverse('shop:catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'shop/catalog.html')
        self.assertIn(product,response.context['products'])
        self.assertContains(response,'IPHONE 15')
        
    def test_catalog_filter_by_category(self):
        smartphones = CategoryFactory(name = 'Смартфоны',slug='smartfony')
        headphones = CategoryFactory(name = 'Наушники',slug='naushniki')

        iphone = ProductFactory(name='IPHONE',category=smartphones)
        sony = ProductFactory(name ='Sony',category = headphones)

        
        response = self.client.get(
            reverse('shop:catalog'),
            {'category':'smartfony'}
        )
        self.assertEqual(response.status_code,200)
        self.assertIn(iphone,response.context['products'])
        self.assertNotIn(sony,response.context['products'])

    def test_catalog_filter_by_brand(self):

        apple =BrandFactory(name = 'Apple',slug = 'apple')
        samsung =BrandFactory(name = 'Samsung',slug = 'samsung') 

        iphone =ProductFactory(name = 'Iphone',brand = apple)
        galaxy =ProductFactory(name = 'Galaxy',brand = samsung)

        response = self.client.get(
            reverse('shop:catalog'),
            {'brand':'apple'}
        )

        self.assertEqual(response.status_code,200)
        self.assertIn(iphone,response.context['products'])
        self.assertNotIn(galaxy,response.context['products'])
