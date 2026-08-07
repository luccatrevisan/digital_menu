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


function addToCart(id, name, price, image){
    const existingItem = cart.find(item => item.id === id);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id,
            name,
            price,
            image,
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


function buildOrderPayload() {
    return {
        items: cart.map(item => ({
            menu_item_id: item.id,
            quantity: item.quantity
        }))
    };
}

window.addToCart = addToCart;
window.removeFromCart = removeFromCart;
window.changeQuantity = changeQuantity;
window.cleanCart = cleanCart;
window.buildOrderPayload = buildOrderPayload;