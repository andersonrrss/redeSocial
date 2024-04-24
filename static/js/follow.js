const followbtn = document.querySelector("#followbtn")
const user_id = document.querySelector("#user_id").value
const form = document.querySelector("#followbtnForm")

// Checa se o usuário já segue o perfil
fetch(`/isFollowed?user=${user_id}`)
.then((response) => {
    if (!response.ok){
        throw new Error(`http error -> ${response.status}`)
    }
    return response.json()
})
.then(data => {
    // Muda a classe do botão para que o estilo seja aplicado
    if (data.is_followed) {
        followbtn.innerHTML = "Seguindo"
        followbtn.classList = "text-black text-center font-semibold p-2 rounded-md w-full bg-gray-300 hover:bg-gray-400";
        form.method = "post"
    // Se o usuário não segue o perfil então
    }else{
        form.method = "get"
    }
})
.catch(error => {
    console.error('Erro:', error);
});
