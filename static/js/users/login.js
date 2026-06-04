export const urlToken = "http://127.0.0.1:8000/api/token/";

export async function login(url, username, password){
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
        return;

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