document.getElementById('cartIcon').addEventListener('click', openSidebar);
document.getElementById('closeIcon').addEventListener('click', closeSidebar);
const buyButton = document.querySelector('.buy_button');
if (buyButton) {
    buyButton.addEventListener('click', addToCart);
}


window.onload = function() {
    var firstThumbnail = document.getElementsByClassName('clickable-thumbnail')[0];
    if (firstThumbnail) {
        changeMainImage(firstThumbnail.src, firstThumbnail);
    }
    updateCartDOM();
    updateCartVisibility();
};

function openSidebar() {
    var sidebar = document.getElementById('sidebar');
    var overlay = document.getElementById('overlay');
    document.getElementById('cartIcon').style.display = 'none';
    document.getElementById('closeIcon').style.display = 'block';
    sidebar.style.right = '0px';
}

function closeSidebar() {
    var sidebar = document.getElementById('sidebar');
    var overlay = document.getElementById('overlay');
    document.getElementById('cartIcon').style.display = 'block';
    document.getElementById('closeIcon').style.display = 'none';
    sidebar.style.right = '-580px';
}

function changeMainImage(src, element) {
    var mainImage = document.getElementById('mainImage');
    mainImage.src = src;
    var thumbnails = document.getElementsByClassName('clickable-thumbnail');
    for (var i = 0; i < thumbnails.length; i++) {
        thumbnails[i].style.border = 'none';
    }
    element.style.border = '2px solid grey';
}

function addToCart() {
    var productName = document.querySelector('.product_info > h1').textContent;
    var productPrice = document.querySelector('.product_info .price').textContent;
    var productId = document.querySelector('.product_info').dataset.productId;
    var productQuantity = parseInt(document.getElementById('quantity_input').value, 10);

    var cart = JSON.parse(localStorage.getItem('cart')) || [];
    
    // Найти продукт в корзине по ID
    var existingProduct = cart.find(product => product.id === productId);

    if(existingProduct) {
        // Увеличить количество, если продукт уже существует
        existingProduct.quantity += productQuantity;
    } else {
        // Добавить новый продукт в корзину
        cart.push({
            id: productId,
            name: productName,
            price: productPrice,
            quantity: productQuantity
        });
    }

    localStorage.setItem('cart', JSON.stringify(cart));

    updateCartDOM();
    updateCartVisibility();
    openSidebar();
}

function updateCartDOM() {
    var cart = JSON.parse(localStorage.getItem('cart')) || [];
    var cartItemsContainer = document.getElementById('cartItemsContainer');

    cartItemsContainer.innerHTML = '';

    cart.forEach(function (item, index) {
        var cartContent = document.createElement('div');
        cartContent.className = "cart-item";
        cartContent.innerHTML = `
            <h4 class="cart-item-name">${item.name}</h4>
            <div class="cart-item-quantity">
                <button class="sidebar-button" onclick="decreaseQuantity(${index})">
                    <img class="sidebar-icon" src="../static/icons/remove.svg" alt="-">
                </button>
                <p>${item.quantity}</p>
                <button class="sidebar-button" onclick="increaseQuantity(${index})">
                    <img class="sidebar-icon" src="../static/icons/add.svg" alt="plus">
                </button>
            </div>
            <p class="cart-item-price">${item.price}</p>
            <button class="sidebar-button" onclick="removeFromCart(${index})">
                <img class="sidebar-icon" src="../static/icons/cancel.svg" alt="x">
            </button>
        `;
        cartItemsContainer.appendChild(cartContent);
    });

    var total = calculateTotal();
    document.getElementById('cartTotal').innerHTML = 'Total: ' + total + ' р.';
}

function updateCartVisibility() {
    var cart = JSON.parse(localStorage.getItem('cart')) || [];
    var cartIcon = document.getElementById('cartIcon');
    var closeIcon = document.getElementById('closeIcon');

    // Устанавливаем видимость иконки корзины в зависимости от того, есть ли товары в корзине
    if (cart.length > 0) {
        cartIcon.style.display = 'block'; // Показываем иконку корзины
        closeIcon.style.display = 'none'; // Скрываем иконку закрытия
    } else {
        cartIcon.style.display = 'none';  // Скрываем иконку корзины
        closeIcon.style.display = 'none'; // Скрываем иконку закрытия, если она открыта
        closeSidebar();                   // Закрываем корзину, если она открыта
    }
}

function increaseQuantity(index) {
    var cart = JSON.parse(localStorage.getItem('cart')) || [];
    if (index >= 0 && index < cart.length) {
        cart[index].quantity += 1;  // Увеличиваем количество на 1
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartDOM(); // Обновляем DOM
    }
}

function decreaseQuantity(index) {
    var cart = JSON.parse(localStorage.getItem('cart')) || [];
    if (index >= 0 && index < cart.length && cart[index].quantity > 1) {
        cart[index].quantity -= 1;  // Уменьшаем количество на 1
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartDOM(); // Обновляем DOM
    } else if (cart[index].quantity === 1) {
        removeFromCart(index); // Если количество становится 0, удаляем элемент
    }
}

function removeFromCart(index) {
    var cart = JSON.parse(localStorage.getItem('cart')) || [];
    if (index > -1 && index < cart.length) {
        cart.splice(index, 1);
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartDOM();
        updateCartVisibility();
    }
}

function calculateTotal() {
    var cart = JSON.parse(localStorage.getItem('cart')) || [];
    var total = 0;
    cart.forEach(function(item) {
        var itemTotal = parseFloat(item.price.replace(/[^0-9.,]/g, '')) * item.quantity;
        total += itemTotal;
    });
    return total.toFixed(2); // Возвращает сумму с двумя десятичными, адаптировано под общий формат чисел.
}

function changeQuantity(change) {
    var quantity = parseInt(document.getElementById('quantity_input').value);
    quantity = isNaN(quantity) ? 0 : quantity;
    quantity += change;
    if (quantity < 1) quantity = 1;
    document.getElementById('quantity_input').value = quantity;
}