const inputSenha = document.querySelector("#password");
const showPass = document.querySelector("#olho");
const divSenha = document.querySelector("#divSenha");

inputSenha.addEventListener("focus", function () {
  showPass.style.display = "block";
  showPass.addEventListener("click", showPassword);
});
inputSenha.addEventListener("click", function () {
  divSenha.classList.add("focado");
});

inputSenha.addEventListener("blur", function () {
  divSenha.classList.remove("focado");
});

function showPassword() {
  if (inputSenha.type == "password") {
    inputSenha.type = "text";
    showPass.classList.remove("fa-eye");
    showPass.classList.add("fa-eye-slash");
  } else {
    showPass.classList.remove("fa-eye-slash");
    showPass.classList.add("fa-eye");
    inputSenha.type = "password";
  }
}

// Checagem do nome

const sing_button = document.querySelector("#sing_button")

const username_input = document.querySelector("#name");
const name_message = document.querySelector("#nameMSG");

username_input.addEventListener("input", function () {
  const username = username_input.value;
  if (username.length > 0) {
    fetch(`checkname?name=${username}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Erro -> ${response.statusText}`);
        }
        return response.json();
      })
      .then((data) => {
        sing_button.disabled = false
        username_input.classList.remove("invalid-input");
        name_message.classList.add("hidden");
        sing_button.classList.remove("disabled")

        if (!data.isValid) {
          input_error(username_input, name_message, "Nome inválido")
        }
        if (data.exists) {    
          input_error(username_input, name_message, "Nome já cadastrado")
        }
      });
  }
});


// Checagem do email

const email_input = document.querySelector("#email")
const email_msg = document.querySelector("#emailMSG")

email_input.addEventListener("input", function(){
  const email = email_input.value
  if(email.length > 0){
    fetch(`checkemail?email=${email}`)
    .then((response)=> {
      if(!response.ok){
        throw new Error(`ERRO -> ${response.statusText}`)
      }
      return response.json()
    })
    .then((data) => {
      sing_button.disabled = false
      sing_button.classList.remove("disabled")
      email_input.classList.remove("invalid-input");
      email_msg.classList.add("hidden");

      if(email.length > 0){
        if(!data.isValid){
          input_error(email_input, email_msg, "Email inválido")
        }
        if(data.exists){
          input_error(email_input, email_msg, "Email já cadastrado")
        }
      }
    })
  }
})

// Checa a senha e a confirmação

const senha_msg = document.querySelector("#senhaMSG")

inputSenha.addEventListener('input', function(){
  sing_button.disabled = false
  sing_button.classList.remove("disabled")
  divSenha.classList.remove("invalid-input");
  senha_msg.classList.add("hidden");

  if(inputSenha.value.length < 8){
    input_error(divSenha, senha_msg, "Sua senha deve conter pelo menso 8 caracteres")
  }
})

const confirmation = document.querySelector("#confirmation")
const confirmation_msg = document.querySelector("#confirmationMSG")

confirmation.addEventListener("input", function(){
  sing_button.disabled = false
  sing_button.classList.remove("disabled")
  confirmation.classList.remove("invalid-input");
  confirmation_msg.classList.add("hidden");
  if(inputSenha.value != confirmation.value){
    input_error(confirmation, confirmation_msg, "As senhas não coincidem")
  }
})

document.querySelector("#sing-form").addEventListener("submit", function(event) {
  event.preventDefault();

  // Defina uma variável para rastrear se algum campo é inválido
  let algumCampoInvalido = false;

  // Itera sobre todos os inputs dentro do formulário
  document.querySelectorAll("#sing-form input").forEach(input => {
    // Verifica se o valor do input é menor que 5 caracteres
    if (input.value.length < 5) {
      // Define o campo como inválido
      algumCampoInvalido = true;
      // Adiciona a classe 'invalid-input' para destacar o campo inválido
      input.classList.add('invalid-input');
    } else {
      // Remove a classe 'invalid-input' caso o campo seja válido
      input.classList.remove('invalid-input');
    }
  });
  if(document.querySelector("#password").value.length < 5){
    // Define o campo como inválido
      algumCampoInvalido = true;
      // Adiciona a classe 'invalid-input' para destacar o campo inválido
      document.querySelector("#divSenha").classList.add('invalid-input');
  }

  // Se algum campo for inválido, exibe um alerta e interrompe o envio do formulário
  if (algumCampoInvalido) {
    alert("Preencha os campos necessários");
  } else {
    // Caso contrário, envia o formulário
    this.submit();
  }
});

// Formatação dos erros dos inputs
function input_error(input, message_camp, message){
  message_camp.innerHTML = message
  message_camp.classList.remove("hidden")// Mostra a mensagem
  input.classList.add("invalid-input") // Adiciona a estilização de um input inválido
  sing_button.disabled = true // Desabilita o botão
  sing_button.classList.add("disabled") // Adicona o estilo de botão desabilitado
}