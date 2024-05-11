const inputSenha = document.querySelector("#password");
const showPass = document.querySelector("#olho");
const divSenha = document.querySelector("#divSenha")


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
