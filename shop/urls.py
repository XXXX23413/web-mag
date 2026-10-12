from django.urls import path
from. import views

app_name ='shop'
urlpatterns = [
    path('catalog/',views.catalog,name='catalog')
]