const name_or_email = document.querySelector("#name-or-email")
const name_email_MSG = document.querySelector("#emailNameMSG")

function validarEmail(email) {
    // Expressão regular para validar o formato do email
    var regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

name_or_email.addEventListener("input", async function(){
    if(name_or_email.value.length >= 6){
        let passed = true
        if(validarEmail(name_or_email.value)){
            await fetch(`checkemail?email=${name_or_email.value}`)
            .then(response => response.json())
            .then(data => {
                if(!data.exists){
                    passed = false
                    input_error(name_or_email, name_email_MSG, "Email não encontrado")
                }
            })
        } else {
            await fetch(`checkname?name=${name_or_email.value}`)
            .then(response => response.json())
            .then(data => {
                if(!data.exists){
                    passed = false
                    input_error(name_or_email, name_email_MSG, "Nome de usuário não encontrado")
                }
            })
        }
        passed && reset(name_or_email, name_email_MSG)
    }
})

document.querySelector("#login-form").addEventListener("submit", function(event){
    event.preventDefault()

    const email_name = name_or_email
    const sing_btn = document.querySelector("#sing_button")
    const senha_input = document.querySelector("#password")
    const senha_div = document.querySelector("#divSenha")
    const senha_MSG = document.querySelector("#senhaMSG")

    senha_input.addEventListener("input", function(){
        senha_div.classList.remove("invalid-input")
        senha_MSG.classList.add("hidden")
    })

    let empty_input = false
    if(email_name.value.length < 2){
        email_name.classList.add("invalid-input")
        empty_input = true
    }
    if(senha_input.value.length < 2){
        senha_div.classList.add("invalid-input")
        empty_input = true
    }
    if(empty_input){
        alert("Preencha os campos necessários")
        return 
    }

    fetch(`checkPassword?identifier=${email_name.value}&senha=${senha_input.value}`)
    .then(response => response.json())
    .then(data => {
        if(!data.isRight){
            senha_MSG.innerHTML = "Senha incorreta"
            senha_MSG.classList.remove("hidden")
            senha_div.classList.add("invalid-input")
        } else {
            this.submit()
        }
    })


})