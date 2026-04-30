async function login(username, password){
    try{
        const response = await fetch("http://127.0.0.1:8000/api/token/", {
            method : "POST",
            headers: {
                "content-type" : "application/json"
            },
            body: JSON.stringify({
                username : username,
                password : password,
            })
        });

        const data = await response.json();
        return data.access;

    }
    catch(error){
        console.error(error)
    }
}


async function apiFetch(){
    try{
        const token = await login("username", "password"); //to-do: replace with real user input

        const response = await fetch("http://127.0.0.1:8000/api/item-by-category/", {
            method : "GET",
            headers : {
                "Authorization" : `Bearer ${token}`,
                "Content-Type" : "application/json"
            }
        });

        if (!response.ok){
            throw new Error("Could not fetch resource");
        }

        const data = await response.json();
        console.log(data);
    }
    catch(error){
        console.error(error);
    }
}