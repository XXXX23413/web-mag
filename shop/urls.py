from django.urls import path
from. import views

app_name ='shop'
urlpatterns = [
    path('catalog/',views.catalog,name='catalog'),
    path('product/<slug:slug>/', views.product_detail,name='product_detail'),
]
