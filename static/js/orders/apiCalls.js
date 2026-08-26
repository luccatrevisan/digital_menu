async function checkout(){
    const payload = buildOrderPayload();
    const accessToken = localStorage.getItem("access");

    try{
        const response = await fetch("/api/orders/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization" : `Bearer ${accessToken}`
            },
            body: JSON.stringify(payload)
        });

        if (response.status === 401) {
            localStorage.removeItem("access");
            localStorage.removeItem("refresh");

            window.location.href = "/login/";
            return;
        }

        if (!response.ok) {
            const error = await response.json();
            const orderWarning = document.getElementById("order-warning");
            orderWarning.hidden = false;

            if (error[0] === "The total price should be R$30,00 or more.") {
                orderWarning.textContent = "O pedido precisa ultrapassar o limite de R$30,00.";
                return;
            }
            
            if (error.items.code === "empty_cart") {
                orderWarning.textContent = "O carrinho não pode ser concluído sem itens.";
            }
            else if (error.items.code === "item_unavailable") {
                orderWarning.textContent = `O item ${error.items.menu_item} não está disponível no momento.`;
            }
            else if (error.items.code === "item_does_not_exist") {
                orderWarning.textContent = "Esse item não existe.";
            }
            else if (error.items.code === "stock_unavailable") {
                orderWarning.textContent = `O item ${error.items.menu_item} não tem estoque o suficiente. Disponíveis: ${error.items.remaining}`;
            }
        
            return;
        }

        const data = await response.json();
        document.getElementById("order-warning").hidden = true;
        window.location.href = `/orders/checkout/?order=${data.order_id}`;
    
    } catch(error) {
        console.error(error);
        alert("Erro ao conectar com o servidor.");
    }
};


async function loadAddresses(){
    const accessToken = localStorage.getItem("access");

    try {
        const response = await fetch("/api/address/", {
            method: "GET",
            headers: {
                "Content-Type" : "application/json",
                "Authorization" : `Bearer ${accessToken}`
            }
        });

        if (!response.ok) {
            throw new Error("Could not load addresses.");
        }

        const addresses = await response.json();

        return addresses;
    } catch (error) {
        console.error(error);
    }
};


async function createAddress() {
    const accessToken = localStorage.getItem("access");

    const payload = {
        street: document.getElementById("street").value,
        number: document.getElementById("number").value,
        neighborhood: document.getElementById("neighborhood").value,
        city: document.getElementById("city").value,
        state: document.getElementById("state").value,
        cep: document.getElementById("cep").value,
        complement: document.getElementById("complement").value,
        label: document.getElementById("label").value
    };

    try {
        const response = await fetch("/api/address/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${accessToken}`
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error("Could not create address.");
        }

        const address = await response.json();
        return address;

    } catch (error) {
        console.error(error);
    }
}

window.checkout = checkout;
window.loadAddresses = loadAddresses;
window.createAddress = createAddress;