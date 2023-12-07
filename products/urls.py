from django.urls import path

from .views import ProductsListView, basket_add, basket_remove, index

urlpatterns = [
    path('', index, name='home'),
    path('products/', ProductsListView.as_view(), name='products'),
    path('products/<int:category_id>/', ProductsListView.as_view(), name='filter'),
    path('page/<int:page>/', ProductsListView.as_view(), name='pagination'),
    path('products/add/<int:product_id>/', basket_add, name='basket_add'),
    path('products/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]
