const urlToken = "http://127.0.0.1:8000/api/token/";

const registerForm = document.getElementById("register-form");

registerForm.addEventListener("submit", async function(event){
    event.preventDefault();

    const username = document.getElementById("iusername").value
    const email = document.getElementById("iemail").value
    const password = document.getElementById("ipassword").value
    const confirmPassword = document.getElementById("iconfirm_password").value

})


async function register(){
    
}