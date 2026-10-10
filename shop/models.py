from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100,verbose_name="Название")
    slug = models.SlugField(unique=True,verbose_name="URL-слаг")
    description = models.TextField(blank=True,verbose_name="Описание")
    is_active=models.BooleanField(default=True,verbose_name="Активна")
    created_at=models.DateTimeField(auto_now_add=True,verbose_name="Дата создания")
    
    def __str__(self):
     return self.name

    class Meta:
     verbose_name="Категория"
     verbose_name_plural="Категории"

class Brand(models.Model):
   name=models.CharField(max_length=100,verbose_name="Название")
   slug = models.SlugField(unique=True,verbose_name="URL-слаг")
   is_active = models.BooleanField(default=True,verbose_name="Активен")

   def __str__(self):
      return self.name

   class Meta:
      verbose_name = "Бренд"
      verbose_name_plural = "Бренды"


class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products',verbose_name="Категория")
    brand = models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True,blank=True,related_name='products',verbose_name="Бренд")
    name=models.CharField(max_length=200,verbose_name="Название")
    slug=models.SlugField(unique=True,verbose_name="URL-слаг")
    short_description = models.CharField(max_length=255,blank=True,verbose_name="Краткое описание")
    description=models.TextField(blank=True,verbose_name="Описание")
    price=models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Цена")
    old_price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True,verbose_name="Старая цена")
    stock_quantity = models.PositiveIntegerField(default=0,verbose_name="Количество на складе")
    image=models.ImageField(upload_to='products/',blank=True,null=True,verbose_name="Изображение")
    is_active = models.BooleanField(default=True,verbose_name="Активен")
    created_at=models.DateTimeField(auto_now_add=True,verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="Дата обновления")
    
    def __str__(self):
       return self.name

    class Meta:
       verbose_name="Товар"
       verbose_name_plural = "Товары"

class ProductSpecification(models.Model):
   product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='specifiсation',verbose_name="Товар")
   name=models.CharField(max_length=100,verbose_name="Характеристика")
   value = models.CharField(max_length=255,verbose_name="Значение")

   def __str__(self):
      return f"{self.product.name} - {self.name}"

   class Meta:
      verbose_name = "Характеристика товара"
      verbose_name_plural = "Характеристики товаров"

class Cart(models.Model):
   user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='carts',verbose_name="Пользователь")
   created_at = models.DateTimeField(auto_now_add=True,verbose_name="Дата создания")
   updated_at=models.DateTimeField(auto_now=True,verbose_name="Дата обновления")

   def __str__(self):
      return f"Корзина {self.user}"

   class Meta:
      verbose_name="Корзина"
      verbose_name_plural ="Корзины"

class CartItem(models.Model):
   cart= models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='items',verbose_name="Корзина")
   product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="Товар")
   quantity = models.PositiveIntegerField(default=1,verbose_name="Количество")

   def __str__(self):
      return f"{self.product.name} x {self.quantity}"

   class Meta:
      verbose_name = "Товар в корзине"
      verbose_name_plural = "Товары в корзине"

class Order(models.Model):
    STATUS_CHOICES = [
       ('new','Новый'),
       ('processing','В обработке'),
       ('shipped','Отправлен'),
       ('completed','Выполнен'),
       ('cancelled','Отменен'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='orders',verbose_name='Пользователь')
    number = models.CharField(max_length=20,unique=True,verbose_name="Номер заказа")
    delivery_address=models.TextField(verbose_name="Адрес доставки")
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='new', verbose_name="Статус")
    payment_status = models.CharField(max_length=20,default='Не оплачен',verbose_name="Статус оплаты")
    total_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0,verbose_name="Итоговая сумма")
    customer_name=models.CharField(max_length=100,verbose_name="Имя покупателя")
    phone=models.CharField(max_length=20,verbose_name="Телефон")
    email=models.EmailField(verbose_name="Email")
    city = models.CharField(max_length=100,blank=True,verbose_name="Город")
    address = models.TextField(verbose_name="Адрес доставки")
    payment_method = models.CharField(max_length=100,blank=True,verbose_name="Способ оплаты")
    comment=models.TextField(blank=True,verbose_name="Комментарий")
    created_at=models.DateTimeField(auto_now_add=True,verbose_name="Дата заказа")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="Дата обновления")
    
    def __str__ (self):
     return f"Заказ {self.number}-{self.customer_name}"

    class Meta:
     verbose_name ="Заказ"
     verbose_name_plural ="Заказы"

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items',verbose_name="Заказ")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="Товар")
    product_name = models.CharField(max_length=200,verbose_name="Название товара")
    quantity=models.PositiveIntegerField(default=1,verbose_name="Количество")
    price=models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Цена на момент заказа")
    total_price =models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Сумма по позиции")
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity} "

    class Meta:
     verbose_name="Товар в заказе"
     verbose_name_plural="Товары в заказе"

class Review (models.Model):
   user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='reviews',verbose_name="Пользователь")
   product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews',verbose_name="Товар")
   rating = models.PositiveSmallIntegerField(default=5,verbose_name="Оценка")
   text=models.TextField(verbose_name="Текст отзыва")
   is_published=models.BooleanField(default=False,verbose_name="Опубликован")
   created_at = models.DateTimeField(auto_now_add=True,verbose_name="Дата создания")

   def __str__(self):
      return f"Отзыв на {self.product.name}"    

   class Meta:
      verbose_name = "Отзыв"
      verbose_name_plural = "Отзывы"