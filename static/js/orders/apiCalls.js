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

        if (response.status === 401) {
            localStorage.removeItem("access");
            localStorage.removeItem("refresh");
            window.location.href = "/login/";
            return null;
        }

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
            const error = await response.json();
            const addressWarning = document.getElementById("address-warning");
            addressWarning.hidden = false;

            if (error["cep"]){
                addressWarning.textContent = error["cep"][0];
            }
            else if (error["street"]){
                addressWarning.textContent = error["street"][0];
            }
            else if (error["number"]){
                addressWarning.textContent = error["number"][0];
            }
            else if (error["neighborhood"]){
                addressWarning.textContent = error["neighborhood"][0];
            }
            else if (error["city"]){
                addressWarning.textContent = error["city"][0];
            }
            else {
                addressWarning.textContent = "Não foi possível cadastrar o endereço. Tente novamente";
            }

            return;
        }

        const address = await response.json();
        return address;

    } catch (error) {
        console.error(error);

        const addressWarning = document.getElementById("address-warning");
        addressWarning.hidden = false;
        addressWarning.textContent = "Não foi possível cadastrar o endereço. Verifique sua conexão e tente novamente.";
    }
}

window.loadAddresses = loadAddresses;
window.createAddress = createAddress;