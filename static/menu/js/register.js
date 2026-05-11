import { login, urlToken } from "./login.js";


const urlRegister = "http://127.0.0.1:8000/api/register/";

const registerForm = document.getElementById("register-form");

registerForm.addEventListener("submit", async function(event){
    event.preventDefault();

    const username = document.getElementById("iusername").value;
    const email = document.getElementById("iemail").value;
    const phoneNumber = document.getElementById("iphone_number").value;
    const password = document.getElementById("ipassword").value;
    const confirmPassword = document.getElementById("iconfirm_password").value;

    if (password !== confirmPassword){
        const errorContainer = document.getElementById("register-error");
        errorContainer.textContent = "As senhas não coincidem.";
        return;
    }

    try{
        await register(urlRegister, username, email, phoneNumber, password);
        await login(urlToken, username, password);
        window.location.href = "/";

    } catch(error){
        const errorContainer = document.getElementById("register-error");
        errorContainer.textContent = error.message;
    }

})


async function register(url, username, email, phoneNumber, password){
    try{
        const response = await fetch(url, {
            method : "POST",
            headers : {
                "Content-Type" : "application/json",
                "X-CSRFToken" : getCSRFToken(),
            },
            body : JSON.stringify({
                username : username,
                email : email,
                phone_number : phoneNumber,
                password : password
            })
        });

        if (!response.ok){
            const errorData = await response.json();
            if (errorData.username){
                throw new Error(errorData.username[0]);
            } else if (errorData.email){
                throw new Error(errorData.email[0]);
            } else if (errorData.password){
                throw new Error(errorData.password[0]);
            } else if (errorData.phone_number) {
                throw new Error("Usuário com este número de celular já existe.")
            } else {
                throw new Error("Erro ao cadastrar usuário");
            }
        }

    } catch(error){
        throw error;
    }
}


function getCSRFToken() {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken'))
        ?.split('=')[1];
}