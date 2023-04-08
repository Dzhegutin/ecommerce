var updateBtns = document.getElementsByClassName('update-cart')  /* использует метод "getElementsByClassName" для поиска
 на странице всех элементов с классом "update-cart" и сохранения их в переменной*/


for (var i = 0; i < updateBtns.length; i++){               /*цикл перебирает все найденные элементы и добавляет обработчик событий "click"
 к каждому элементу. Когда пользователь кликает на элементе, выполняется функция, которая была передана обработчику событий.*/
    updateBtns[i].addEventListener('click', function(){
     /*  две строки сохраняют значения атрибутов
    "data-product" и "data-action" текущего элемента, на котором пользователь кликнул, в соответствующие переменные.*/
    var productId = this.dataset.product
    var action = this.dataset.action
    console.log('productId:', productId,'action:', action)

    console.log('USER', user)
    if(user==='AnonmousUser'){
    console.log('Not logged in')}else{updateUserOrder(productId, action)} /*если пользователь авторизован,
     вызывается функция "updateUserOrder" с передачей идентификатора продукта и действия.  функция "updateUserOrder"
      обновляет информацию о продукте на сервере и перезагружает текущую страницу, чтобы отобразить изменения в интерфейсе. */
    })
}
/* а если вкратце, то эта функция есть счетчик товара, привязанная к бд */

function updateUserOrder(productId, action) {   /*принимает два аргумента: productId и action, которые представляют
 идентификатор продукта и действие */
    console.log('User is logged in, sending data..');

    var url = '/update_item/'; /*определяет URL-адрес, на который будут отправлены данные с помощью метода fetch().*/

    fetch(url, {              /*отправляет запрос на сервер с помощью метода fetch()
    Заголовки headers содержат Content-Type, который сообщает серверу, что данные,
     в формате JSON, и X-CSRFToken, который содержит токен защиты от подделки межсайтовых запросов */
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action}) /*Тело запроса содержит данные, которые мы отправляем на сервер, в формате JSON.*/
    })
    .then(response => {   /* при получении ответа от сервера мы будем преобразовывать его в формат JSON */
        return response.json()
    })
    .then(data => {                         /* определяет действия, которые нужно выполнить после получения ответа от сервера.
    мы выводим данные, которые мы получили в ответ, в консоль с помощью console.log(),
      и перезагружаем страницу с помощью location.reload(). после обновления страницы, мы увидим изменения,
      которые были внесены в заказ пользователя.*/
        console.log('data', data)
        location.reload()
    })

}


