
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
    showPass.innerHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 28 28">
      <path fill="#581c87" d="M25.257 16h.005h-.01zm-.705-.52c.1.318.387.518.704.52c.07 0 .148-.02.226-.04c.39-.12.61-.55.48-.94C25.932 14.93 22.932 6 14 6S2.067 14.93 2.037 15.02c-.13.39.09.81.48.94c.4.13.82-.09.95-.48l.003-.005c.133-.39 2.737-7.975 10.54-7.975c7.842 0 10.432 7.65 10.542 7.98M10.5 16a3.5 3.5 0 1 1 7 0a3.5 3.5 0 0 1-7 0m3.5-5a5 5 0 1 0 0 10a5 5 0 0 0 0-10"/>
    </svg>
    `;
  } else {
    showPass.innerHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 15 15">
      <path fill="#581c87" d="M7.5 9C5.186 9 3.561 7.848 2.497 6.666a9.4 9.4 0 0 1-1.449-2.164l-.08-.18l-.004-.007v-.001L.5 4.5l-.464.186v.002l.003.004l.026.063l.078.173a10.4 10.4 0 0 0 1.61 2.406C2.94 8.652 4.814 10 7.5 10zm7-4.5l-.464-.186l-.003.008l-.015.035l-.066.145a9.4 9.4 0 0 1-1.449 2.164C11.44 7.848 9.814 9 7.5 9v1c2.686 0 4.561-1.348 5.747-2.666a10.4 10.4 0 0 0 1.61-2.406a6 6 0 0 0 .104-.236l.002-.004v-.001h.001zM8 12V9.5H7V12zm-6.646-1.646l2-2l-.708-.708l-2 2zm10.292-2l2 2l.708-.708l-2-2z"/>
    </svg>
    ` 
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
