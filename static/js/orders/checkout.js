function getCart() {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
}


function getSelectedAddressId() {
    const selected = document.querySelector('input[name="selected-address"]:checked');
    return selected ? Number(selected.value) : null;
}


async function confirmOrder() {
    const addressId = getSelectedAddressId();
    const warning = document.getElementById("order-warning");

    if (addressId === null) {
        warning.hidden = false;
        warning.textContent = "Selecione um endereço de entrega.";
        return;
    }

    const payload = {
        address_id: addressId,
        items: getCart().map(item => ({
            menu_item_id: item.id,
            quantity: item.quantity
        }))
    };

    const accessToken = localStorage.getItem("access");
    if (!accessToken) {
        window.location.href = "/login/";
        return;
    }

    confirmOrderButton.disabled = true;

    try {
        const response = await fetch("/api/orders/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${accessToken}`
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
            let error = null;

            try {
                error = await response.json();
            } catch (e) {
                console.error("Non-JSON response:", e);
            }

            warning.hidden = false;

            if (!error) {
                warning.textContent = "Erro no servidor. Tente novamente em instantes.";
            }
            else if (error.code === "minimum_order") {
                warning.textContent = "O pedido precisa ultrapassar o limite de R$30,00.";
            }
            else if (error.items?.code === "empty_cart") {
                warning.textContent = "O carrinho não pode ser concluído sem itens.";
            }
            else if (error.items?.code === "item_unavailable") {
                warning.textContent = `O item ${error.items.menu_item} não está disponível no momento.`;
            }
            else if (error.items?.code === "item_does_not_exist") {
                warning.textContent = "Esse item não existe.";
            }
            else if (error.items?.code === "stock_unavailable") {
                warning.textContent = `O item ${error.items.menu_item} não tem estoque o suficiente. Disponíveis: ${error.items.remaining}`;
            }
            else if (error.address_id) {
                warning.textContent = "Endereço inválido. Selecione outro endereço.";
            }
            else {
                warning.textContent = "Não foi possível concluir o pedido. Tente novamente.";
            }

            return;
        }

        const data = await response.json();
        cleanCart();
        window.location.href = `/orders/success/?order=${data.order_id}`;

    } catch (error) {
        console.error(error);
        warning.hidden = false;
        warning.textContent = "Erro ao conectar com o servidor.";

    } finally {
        confirmOrderButton.disabled = false;
    }
}