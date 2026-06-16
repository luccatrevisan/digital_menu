const URL = "http://127.0.0.1:8000/api/orders"
const STORAGE_KEY = "chewie_cart";

let cart = JSON.parse(
    localStorage.getItem(STORAGE_KEY)
) || [];

function saveCart(){
    localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify(cart)
    );
}

function addToCart(id, name, price){
    const existingItem = cart.find(item => item.id === id);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id,
            name,
            price,
            quantity: 1
        });
    }
    
    saveCart()
    updateCart();
    showFeedback(id);
}

function removeFromCart(id){
    cart = cart.filter(item => item.id !== id);

    saveCart()
    updateCart();
}

function changeQuantity(id, newQuantity){
    const item = cart.find(item => item.id === id);
    
    if (!item) {
        return;
    }

    if (newQuantity <= 0) {
        removeFromCart(id);
        return;
    }

    item.quantity = newQuantity;

    saveCart();
    updateCart();
}

function cleanCart(){
    cart = [];
    localStorage.removeItem(STORAGE_KEY);
    updateCart();
}

function updateCart() {
    const cartBadge = document.getElementById('cartBadge');
    const totalItems = cart.reduce((total, item) => total + item.quantity, 0);
    cartBadge.textContent = totalItems;

    const cartItems = document.getElementById('cartItems');
    const cartTotal = document.getElementById('cartTotal');
    
    if (cart.length === 0) {
        cartItems.innerHTML = `
            <div class="carrinho-vazio">
                <p>Seu carrinho está vazio</p>
                <p>Adicione alguns cookies deliciosos!</p>
            </div>
        `;
        cartTotal.textContent = '0,00';
        return;
    }

    let htmlItems = '';
    let totalValue = 0;

    cart.forEach(item => {
        const subtotal = item.price * item.quantity;
        totalValue += subtotal;
        
        htmlItems += `
            <div class="item-carrinho">
                <div class="item-info">
                    <h4>${item.name}</h4>
                    <div class="item-preco">R$ ${item.price.toFixed(2).replace('.', ',')}</div>
                    <div class="controles-quantidade">
                        <button class="btn-quantidade" onclick="changeQuantity('${item.id}', ${item.quantity - 1})">-</button>
                        <span class="quantidade">${item.quantity}</span>
                        <button class="btn-quantidade" onclick="changeQuantity(${item.id}, ${item.quantity + 1})">+</button>
                        <button class="btn-quantidade" onclick="removeFromCart(${item.id})" style="background: #e53e3e; margin-left: 10px;">🗑️</button>
                    </div>
                </div>
                <div class="item-subtotal">
                    <strong>R$ ${subtotal.toFixed(2).replace('.', ',')}</strong>
                </div>
            </div>
        `;
    });

    cartItems.innerHTML = htmlItems;
    cartTotal.textContent = totalValue.toFixed(2).replace('.', ',');
}

function showFeedback(id) {
    const button = document.querySelector(
        `[data-item-id="${id}"]`
    );

    if (!button) return;

    button.classList.add('sucesso-animacao');

    const originalText = button.textContent;
    button.textContent = '✅ Adicionado!';

    setTimeout(() => {
        button.textContent = originalText;
        button.classList.remove('sucesso-animacao');
    }, 1000);
}

function buildOrderPayload() {
    return {
        items: cart.map(item => ({
            menu_item_id: item.id,
            quantity: item.quantity
        }))
    };
}


const checkoutButton = document.getElementById("checkout-btn");

if (cart.length === 0) {
    checkoutButton.disabled = true;
}

checkoutButton.addEventListener("click", async function() {
    const payload = buildOrderPayload();

    const response = await fetch("/api/orders/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
            // must have access token. if the customer is not logged in, they mustn't place an order
        },
        body: JSON.stringify(payload)
    })

    cleanCart() // to reset the cart after purchase. TO-DO: update with a message like "your order is being processed"
});


function openCart() {
    document.getElementById('modalCarrinho').style.display = 'block';
}

function closeCart() {
    document.getElementById('modalCarrinho').style.display = 'none';
}

window.onclick = function(event) {
    const modal = document.getElementById('modalCarrinho');
    if (event.target === modal) {
        closeCart();
    }
}

updateCart();