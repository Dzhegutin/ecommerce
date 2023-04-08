from django.shortcuts import render #нужен для обработки возврата функции
from django.http import JsonResponse #для возврата данных в формате json
from .models import * #импортируем модели
import json #модуль для работы с json файлами

import datetime #модуль для работы с датой и временем

def store(request): #создание представления для store.html
    if request.user.is_authenticated: #если пользователь аудентифицирован
        customer = request.user.customer #Получаем объект Customer, связанный с аутентифицированным пользователем в запросе ИНАЧЕ ГОВОРЯ ИМЯ ЗАРЕГИСТР ПОЛЬЗОВОВАТЕЛЯ
        order, created = Order.objects.get_or_create(customer=customer, complete=False)  #создаем номер заказа
        cartItems = order.get_cart_items #отображает количество товаров в корзине, используя метод модели order get_cart_items
    else:

        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False} #если пользователь не зареган, то все по нулям
        cartItems = order['get_cart_items'] #берется из словаря прошлой строки, где это значение равно 0
    products = Product.objects.all() #импортируется для отображения всех продуктов нашего магазина на главной странице. в store.html перебирается с помощью шаблонизатора
    context = {'products': products, 'cartItems': cartItems} #формируем словарь того что нужно передать
    return render(request, 'store/store.html', context) #показываем что возвращаем в ответ на request запрос



def cart(request): #создание представления для cart.html
    if request.user.is_authenticated: #если пользователь аудентифицирован
        customer = request.user.customer #Получаем объект Customer, связанный с аутентифицированным пользователем в запросе ИНАЧЕ ГОВОРЯ ИМЯ ЗАРЕГИСТР ПОЛЬЗОВОВАТЕЛЯ
        order, created = Order.objects.get_or_create(customer=customer, complete=False) #создаем номер заказа
        items = order.orderitem_set.all() #отвечает за отображние товаров-продуктов добавленных в cart.html. перебираются с помощью шаблонизатора в html
        cartItems = order.get_cart_items #отображает количество товаров в корзине, используя метод модели order get_cart_items
    else:
        items = [] #если ниче не купили то товары не от отображаются
        order = {'get_cart_total':0, 'get_cart_items': 0, 'shipping': False}  #если пользователь не зареган, то все по нулям
        cartItems = order['get_cart_items'] #берется из словаря прошлой строки, где это значение равно 0

    context = {'items': items, 'order': order,'cartItems': cartItems} #формируем словарь того что нужно передать
    return render(request, 'store/cart.html', context) #показываем что возвращаем в ответ на request запрос


def checkout(request):
    if request.user.is_authenticated:  #если пользователь аудентифицирован
        customer = request.user.customer  #Получаем объект Customer, связанный с аутентифицированным пользователем в запросе ИНАЧЕ ГОВОРЯ ИМЯ ЗАРЕГИСТР ПОЛЬЗОВОВАТЕЛЯ
        order, created = Order.objects.get_or_create(customer=customer, complete=False)  #создаем номер заказа
        items = order.orderitem_set.all()  #отвечает за отображние товаров-продуктов добавленных в checkout.html. перебираются с помощью шаблонизатора в html
        cartItems = order.get_cart_items  #отображает количество товаров в корзине, используя метод модели order get_cart_items
    else:
        items = [] #если ниче не купили то товары не от отображаются
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False} #если пользователь не зареган, то все по нулям
        cartItems = order['get_cart_items']  #берется из словаря прошлой строки, где это значение равно 0

    context = {'items': items, 'order': order, 'cartItems': cartItems}   #формируем словарь того что нужно передать
    return render(request, 'store/checkout.html', context) #показываем что возвращаем в ответ на request запрос



def updateItem(request):
    data = json.loads(request.body) #прогружаем из запроса на сервер в формате json тело в виде словаря из 2 ключей, называем его data

    productId = data['productId'] #извлекаем из словаря номер продукта
    action = data['action'] #извлекаем из словаря действия(add или remove)

    customer = request.user.customer  #Получаем объект Customer, связанный с аутентифицированным пользователем в запросе ИНАЧЕ ГОВОРЯ ИМЯ ЗАРЕГИСТР ПОЛЬЗОВОВАТЕЛЯ
    product = Product.objects.get(id=productId) #достаем все товары
    order, created = Order.objects.get_or_create(customer=customer, complete=False)  #Получаем объект заказа Order, связанный с текущим пользователем, либо создаем новый, если его еще нет. created - булевый флаг, указывающий был ли создан новый заказ.

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product) #Получаем или создаем объект OrderItem для текущего заказа order и продукта product. created - булевый флаг, указывающий был ли создан новый OrderItem.


    if  action == 'add':
        orderItem.quantity = (orderItem.quantity + 1) #Увеличиваем количество orderItem на 1, если action == 'add', либо уменьшаем на 1, если action == 'remove'.
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save() #Сохраняем изменения в объекте orderItem.

    if orderItem.quantity <= 0: #Если количество orderItem меньше или равно 0, удаляем его.
        orderItem.delete()

    return JsonResponse('Item was added', safe=False) #Возвращаем JSON ответ, сообщающий, что элемент был добавлен





def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()   # Генерируем уникальный ID транзакции на основе текущего времени
    data = json.loads(request.body)     # Разбираем тело запроса как данные JSON(форму)


    if request.user.is_authenticated:   #если пользователь аудентифицирован
        customer = request.user.customer  # ... получаем объект заказчика на основе текущего пользователя
        order, created = Order.objects.get_or_create(customer=customer, complete=False)  # Получаем или создаем объект заказа для данного заказчика
        total = float(data['form']['total'])  # Получаем общую стоимость товаров в корзине из данных формы, обращаясь ко вложенному словарю

        order.transaction_id = transaction_id    # Связываем транзакционный ID с заказом


        if total == order.get_cart_total:  # Если общая стоимость товаров в корзине совпадает с фактической стоимостью, которую мы высчитали
            order.complete = True # ... отмечаем заказ как завершенный

        order.save()   # Сохраняем изменения в заказе

        if order.shipping == True:  # Если в заказе указан адрес доставки(может быть не указан, тк есть электронные товары)...
            ShippingAddress.objects.create(   # то создаем объект адреса доставки для данного заказчика и заказа на основе data, полученного из json
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print('User is not logged in..')
    return JsonResponse('Payment complete!', safe=False)  # Возвращаем JSON-ответ с сообщением о завершении оплаты

