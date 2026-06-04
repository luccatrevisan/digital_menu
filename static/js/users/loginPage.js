import { login, urlToken } from "./login.js";


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