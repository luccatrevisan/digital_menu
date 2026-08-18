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
    // helpers for rendering errors in the form
    function clearAddressErrors() {
        document.querySelectorAll('#address-form .field-error').forEach(e => e.remove());
        const g = document.getElementById('address-form-warning');
        if (g) g.remove();
    }

    function showGlobalError(msg) {
        let w = document.getElementById('address-form-warning');
        if (!w) {
            w = document.createElement('div');
            w.id = 'address-form-warning';
            w.style.color = 'orangered';
            const form = document.getElementById('address-form');
            if (form) form.prepend(w);
        }
        w.textContent = msg;
    }

    function showFieldError(field, msg) {
        const input = document.getElementById(field);
        if (!input) return showGlobalError(msg);
        // remove previous
        const existing = input.parentNode.querySelector('.field-error');
        if (existing) existing.remove();
        const div = document.createElement('div');
        div.className = 'field-error';
        div.style.color = 'orangered';
        div.textContent = msg;
        input.insertAdjacentElement('afterend', div);
    }

    function parseApiError(err) {
        // returns { global?: string, errors?: [{field, message, code}] }
        if (Array.isArray(err) && typeof err[0] === 'string') return { global: err[0] };
        if (err && err.message && err.code) return { global: err.message, code: err.code };

        const result = { errors: [] };
        if (err && typeof err === 'object') {
            for (const key of Object.keys(err)) {
                const val = err[key];
                if (Array.isArray(val)) {
                    const first = val[0];
                    if (first && typeof first === 'object') {
                        result.errors.push({ field: key, message: first.message || JSON.stringify(first), code: first.code });
                    } else if (typeof first === 'string') {
                        result.errors.push({ field: key, message: first });
                    }
                }
            }
        }

        // if nothing collected, fallback to global string
        if (result.errors.length === 0) return { global: JSON.stringify(err) };
        return result;
    }

    // normalize inputs and build payload
    const stateInput = document.getElementById("state");
    const normalizedState = stateInput ? stateInput.value.trim().toUpperCase() : "";
    if (stateInput) stateInput.value = normalizedState;

    const payload = {
        street: document.getElementById("street").value,
        number: document.getElementById("number").value,
        neighborhood: document.getElementById("neighborhood").value,
        city: document.getElementById("city").value,
        state: normalizedState,
        cep: document.getElementById("cep").value,
        complement: document.getElementById("complement").value,
        label: document.getElementById("label").value
    };

    console.log("CREATING ADDRESS", payload);

    clearAddressErrors();

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
            const err = await response.json().catch(() => null);
            const parsed = parseApiError(err || { message: 'Erro ao criar endereço.' });

            if (parsed.global) {
                showGlobalError(parsed.global);
            }

            if (parsed.errors && parsed.errors.length) {
                parsed.errors.forEach(e => showFieldError(e.field, e.message));
            }

            return null;
        }

        const address = await response.json();
        return address;

    } catch (error) {
        console.error(error);
        showGlobalError('Erro ao conectar com o servidor.');
    }
}

window.checkout = checkout;
window.loadAddresses = loadAddresses;
window.createAddress = createAddress;