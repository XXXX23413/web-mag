from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=100,verbose_name="Название")
    slug = models.SlugField(unique=True,verbose_name="URL-слаг")

    def __str__(self):
     return self.name

    class Meta:
     verbose_name="Категория"
     verbose_name_plural="Категория"

class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products',verbose_name="Категория")
    name=models.CharField(max_length=200,verbose_name="Название")
    slug=models.SlugField(unique=True,verbose_name="URL-слаг")
    description=models.TextField(blank=True,verbose_name="Описание")
    price=models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Цена")
    is_available=models.BooleanField(default=True,verbose_name="Доступен")
    created_at=models.DateTimeField(auto_now_add=True,verbose_name="Дата создания")

    def __str__(self):
       return self.name
class Order(models.Model):
    customer_name=models.CharField(max_length=100,verbose_name="Имя покупателя")
    phone=models.CharField(max_length=20,verbose_name="Телефон")
    email=models.EmailField(verbose_name="Email")
    delivery_address=models.TextField(verbose_name="Адрес доставки")
    comment=models.TextField(blank=True,verbose_name="Комментарий")
    created_at=models.DateTimeField(auto_now_add=True,verbose_name="Дата заказа")
    status=models.CharField(max_length=20,default='Новый',verbose_name="Статус")

    def __str__ (self):
     return f"Заказ {self.id}-{self.customer_name}"

class Meta:
    verbose_name ="Заказ"
    verbose_name_plural ="Заказы"
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items',verbose_name="Заказ")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="Товар")
    quantity=models.PositiveIntegerField(default=1,verbose_name="Количество")
    price=models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Цена на момент заказа")

    def __str__(self):
        return f"{self.product.name} x {self.quantity} "

class Meta:
    verbose_name="Товар в заказе"
    verbose_name_plural="Товары в заказе"