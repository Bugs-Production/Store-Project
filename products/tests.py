from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse

from .models import Product, ProductCategory


# Create your tests here.
# class IndexViewsTestCase(TestCase):
#     def test_view(self):
#         path = reverse('home')
#         response = self.client.get(path)
#
#         self.assertEquals(response.status_code, HTTPStatus.OK)
#         self.assertTemplateUsed(response, 'products/index.html')


class ProductViewsTestCase(TestCase):
    fixtures = ['categories.json', 'products.json']

    def setUp(self):
        self.products = Product.objects.all()

    def test_list_products(self):
        path = reverse('products')
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEquals(list(response.context_data['object_list']), list(self.products[:3]))

    def test_list_category(self):
        category = ProductCategory.objects.first()
        path = reverse('filter', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEquals(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=category.id))
        )

    def _common_tests(self, response):
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/products.html')
