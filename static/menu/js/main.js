const url = "http://127.0.0.1:8000/api/item-by-category/"

async function apiFetch(url){
    try{
        const response = await fetch(url, {
            method : "GET",
            headers : {
                "Content-Type" : "application/json"
            }
        });

        if (!response.ok){
            throw new Error("Could not fetch resource");
        }

        const data = await response.json();
        return data;
    }
    catch(error){
        console.error(error);
        throw error
    }
}


function renderMenu(data){
    const container = document.getElementById("menu-container");

    container.innerHTML = "";

    data.forEach(category => {

        if (!category.menu_items || category.menu_items.length === 0) return;

        const categorySection = document.createElement("section");
        categorySection.classList.add("category");

        const categoryTitle = document.createElement("h2");
        categoryTitle.classList.add("category-title");
        categoryTitle.textContent = category.name;

        const itemsContainer = document.createElement("div");
        itemsContainer.classList.add("items-container");


        category.menu_items.forEach(item => {

            const itemDiv = document.createElement("div");
            itemDiv.classList.add("item");

            if (!item.is_available) {
                itemDiv.classList.add("unavailable");
            }

            itemDiv.innerHTML = `
                <img src="${item.image}" alt="${item.name}">
                <h3>${item.name}</h3>
                <p>${item.description}</p>

                <div class="price">
                    ${item.old_price ? `<span class="old-price">R$${item.old_price}</span>` : ""}
                    <span class="current-price">R$${item.price}</span>
                </div>

                <button 
                    class="botao-carrinho"
                    ${!item.is_available ? "disabled" : ""}
                    onclick="adicionarAoCarrinho('${item.name}', ${item.price})"
                >
                    ${item.is_available ? "Adicionar ao carrinho" : "Indisponível"}
                </button>
            `;

            itemsContainer.appendChild(itemDiv);
        });

        categorySection.appendChild(categoryTitle);
        categorySection.appendChild(itemsContainer);
        container.appendChild(categorySection);
    });
}


async function init(){
    try{
        const data = await apiFetch(url);
        renderMenu(data);
    } catch(error){
        console.error(error);
    }
}

init();