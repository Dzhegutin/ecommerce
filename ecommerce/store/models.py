from django.db import models
from django.contrib.auth.models import User #импорт стандарт модели пользователя
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True,on_delete=models.CASCADE) # создает связь между двумя моделями таким образом,
    # что каждый экземпляр одной модели может быть связан только с одним экземпляром другой модели и наоборот
    # null указывает, что поле может быть не заполнено
    # blank=True: указывает, что поле не является обязательным для заполнения при создании экземпляра модели
    # on_delete=models.CASCADE: указывает, что при удалении связанного объекта
    # (в данном случае, экземпляра модели User) должны быть удалены и все связанные с ним экземпляры модели Customer
    name = models.CharField(max_length=200, null=True) # используется для хранения текстовых данных ограниченной длины, необходимо
    # указать максимальную длину поля, с помощью параметра max_length
    email =models.CharField(max_length=200)
    def __str__(self): # возвращает имя клиента (self.name) в виде строки, что позволит отображать объекты этой модели в более читаемом виде
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField() # используется для хранения числовых данных, которые могут иметь дробную часть
    digital = models.BooleanField(default=False, null=True, blank=True) #используется для хранения булевых данных, где
    #default - значение по умолчанию для поля, null - если установлено значение True, то поле будет разрешать значение NULL в базе данных.
    #blank - если установлено значение True, то поле может быть пустым.
    image = models.ImageField(null=True, blank=True) #используется для хранения изображений.
    # null - если установлено значение True, то поле будет разрешать значение NULL в базе данных.
     #blank - если установлено значение True, то поле может быть пустым.

    def __str__(self):
        return self.name

    @property #позволяет использовать функцию как свойство
    def imageURL(self): #функция для обр изобр. чтобы не было ошибкок на сайте, если картинки нет
        try:
            url = self.image.url
        except:
              url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete= models.SET_NULL, null=True, blank=True) #ForeignKey используется для создания связи
    # многие-к-одному (многие заказы могут принадлежать одному покупателю)
    #on_delete=models.SET_NULL означает, что если объект покупателя был удален, то значение этого поля будет заменено на NULL.
    date_ordered = models.DateTimeField(auto_now_add=True) #поле, которое хранит дату и время создания заказа.
    # Параметр auto_now_add=True означает, что это поле будет автоматически заполнено текущей датой и временем при создании заказа.
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    @property
    def get_cart_total(self):     #вычисляет общую стоимость всех товаров, которые находятся в корзине заказа.
        orderitems = self.orderitem_set.all() # получает все элементы заказа (OrderItem) по связи orderitem_set
        # аналогично вот этому запросу OrderItem.objects.filter(order_id=self.id)
        total = sum([item.get_total for item in orderitems]) #get_total - метод модели OrderItem, который вычисляет стоимость товаров для заказа
        return total
    @property
    def get_cart_items(self): #вычисляет общее количество товаров в корзине данного заказа.
        orderitems = self.orderitem_set.all() #получает все элементы заказ
        total = sum([item.quantity for item in orderitems]) #вычисляет их общее количество, используя атрибут quantity каждого элемента.
        return total

    def __str__(self):
        return str(self.pk)

    @property
    def shipping(self): #проверяет, нужна ли доставка для данного заказа
        shipping = False #по умолч не нужна
        orderitems = self.orderitem_set.all() #получ все заказы
        for i in orderitems: #пробегается по ним
            if i.product.digital == False: #если один из них не цифровой - доставка нужна
                shipping = True
        return shipping

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0,null=True, blank=True) #поле, которое представляет целочисленное значение.
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

