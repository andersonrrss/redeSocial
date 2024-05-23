
const sing_button = document.querySelector("#sing_button");

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

function reset(input, message_camp){
  message_camp.classList.add("hidden")
  input.classList.remove("invalid-input")
  sing_button.disabled = false; // Desabilita o botão
  sing_button.classList.remove("disabled"); // Adicona o estilo de botão desabilitado
}

// Formatação dos erros dos inputs
function input_error(input, message_camp, message) {
  message_camp.innerHTML = message;
  message_camp.classList.remove("hidden"); // Mostra a mensagem
  input.classList.add("invalid-input"); // Adiciona a estilização de um input inválido
  sing_button.disabled = true; // Desabilita o botão
  sing_button.classList.add("disabled"); // Adicona o estilo de botão desabilitado
}
