const urlToken = "http://127.0.0.1:8000/api/token/";

const loginForm = document.getElementById("login-form");

loginForm.addEventListener("submit", async function(event){
    event.preventDefault();

    const username = document.getElementById("iuser").value;
    const password = document.getElementById("ipassword").value;

    try {
        await login(urlToken, username, password);
        window.location.href = "/";
    } 
    catch(error) {
        const errorContainer = document.getElementById("login-error");

        if (error.message == "invalid_credentials") {
            errorContainer.textContent = "Usuário ou senha inválidos";
        } else {
            errorContainer.textContent = "Erro ao fazer login. Tente novamente.";
        }
    }
});


async function login(url, username, password){
    try{
        const response = await fetch(url, {
            method : "POST",
            headers : {
                "Content-Type" : "application/json",
                "X-CSRFToken": getCSRFToken()
            },
            body: JSON.stringify({
                username: username,
                password: password,
            })
        });

        if (!response.ok){
            if (response.status === 401){
                throw new Error("invalid_credentials");
            }
            throw new Error("server_error");
        }

        const data = await response.json();
        localStorage.setItem("access", data.access);
        return true;

    } catch(error){
        console.error(error);
        throw error;
    }
}


function getCSRFToken() {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken'))
        ?.split('=')[1];
}