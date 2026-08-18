const URL = "/api/orders";


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
                        <button class="btn-quantidade" onclick="changeQuantity(${item.id}, ${item.quantity - 1})">-</button>
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


const checkoutButton = document.getElementById("checkout-btn");

if (checkoutButton) {
    checkoutButton.addEventListener("click", checkout);
}

function renderOrderSummary() {
    const cart = JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];

    const orderSummary = document.getElementById("order-summary");
    const cartTotal = document.getElementById("cart-total");

    orderSummary.innerHTML = "";

    let total = 0;

    cart.forEach(item => {

        const subtotal = item.price * item.quantity;
        total += subtotal;

        orderSummary.innerHTML += `
            <div class="order-item">

                <strong>${item.name}</strong>

                <p>
                    ${item.quantity} × R$ ${item.price.toFixed(2)}
                </p>

                <p>
                    Subtotal:
                    <strong>R$ ${subtotal.toFixed(2)}</strong>
                </p>

            </div>

            <hr>
        `;
    });

    cartTotal.textContent = `R$ ${total.toFixed(2)}`;
}



function renderAdresses(addresses) {
    const addressList = document.getElementById("address-list");
    addressList.innerHTML = "";

    if (!addresses || addresses.length === 0) { 
        addressList.innerHTML = `<p>Você ainda não possui endereços cadastrados.</p>`;
        
        document.getElementById("address-form").hidden = false;
        return;
    }

    addresses.forEach(address => {
        addressList.innerHTML += `
            <label class="address-card">

                <input
                    type="radio"
                    name="selected-address"
                    value="${address.id}"
                    ${addresses.indexOf(address) === (addresses.length - 1) ? "checked='true'" : "checked='false'"}
                >

                <strong>${address.label}</strong><br>

                ${address.street}, ${address.number}<br>

                ${address.neighborhood} - ${address.city}/${address.state}<br>

                CEP: ${address.cep}

            </label>

            <hr>

        `;
    });
};

document.addEventListener("DOMContentLoaded", async () => {
    renderOrderSummary();
    
    const addresses = await loadAddresses();
    renderAdresses(addresses);

});


const addressForm = document.getElementById("address-form");
const newAddressButton = document.getElementById("new-address-button");

if (newAddressButton && addressForm) {
    newAddressButton.addEventListener("click", () => {
        addressForm.hidden = false;
    });
}

if (addressForm) {
    addressForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        await createAddress();

        const addresses = await loadAddresses();
        renderAdresses(addresses);

        addressForm.reset();
        addressForm.hidden = true;
    });
}

function openCart() {
    document.getElementById('modalCarrinho').style.display = 'block';
}

function closeCart() {
    document.getElementById('modalCarrinho').style.display = 'none';
}

window.updateCart = updateCart;
window.showFeedback = showFeedback;
window.openCart = openCart;
window.closeCart = closeCart;
window.renderOrderSummary = renderOrderSummary;
window.renderAdresses = renderAdresses;

window.onclick = function(event) {
    const modal = document.getElementById('modalCarrinho');
    if (event.target === modal) {
        closeCart();
    }
}

updateCart();