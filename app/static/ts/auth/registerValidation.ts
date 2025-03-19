import {checkInput, validateConfirmation} from './validationHelper.js'

const registerForm = document.querySelector("#register-form") as HTMLFormElement

const usernameInputElement = document.querySelector("#name") as HTMLInputElement;
const usernameMessageElement = document.querySelector("#nameMSG") as HTMLSpanElement;

const emailInputElement = document.querySelector("#email") as HTMLInputElement;
const emailMessageElement = document.querySelector("#emailMSG") as HTMLSpanElement;

const passwordInputElement = document.querySelector("#password") as HTMLInputElement
const passwordContainer = document.querySelector("#divSenha") as HTMLDivElement;
const passwordMessageElement = document.querySelector("#senhaMSG") as HTMLSpanElement;

const confirmationInputElement = document.querySelector("#confirmation") as HTMLInputElement;
const confirmationMessageElement = document.querySelector("#confirmationMSG") as HTMLSpanElement;

usernameInputElement.addEventListener("input", function () {
  let value = usernameInputElement.value
  checkInput(value, usernameInputElement, usernameMessageElement, "checkUsername", "username")
});

emailInputElement.addEventListener("input", function () {
  let value = emailInputElement.value
  checkInput(value, emailInputElement, emailMessageElement, "checkEmail", "email")
});

passwordInputElement.addEventListener("input", function () {
  let value = passwordInputElement.value
  checkInput(value, passwordContainer, passwordMessageElement, "checkPassword", "password")
});

confirmationInputElement.addEventListener("input", function () {
  validateConfirmation(confirmationInputElement, confirmationMessageElement, passwordInputElement.value)
});

// Faz uma ultima checagem em caso de envio do formulário 
// pressionando enter ou reabilitando o botão pelas ferramentas de desenvolvimento
// A função vai verificar cada input da página
registerForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const usernameResult = await checkInput(usernameInputElement.value, usernameInputElement, usernameMessageElement, "checkUsername", "username")
    const emailResult = await checkInput(emailInputElement.value, emailInputElement, emailMessageElement, "checkEmail", "email")
    const passwordResult = await checkInput(passwordInputElement.value, passwordContainer, passwordMessageElement, "checkPassword", "password")
    const confirmationResult = await validateConfirmation(confirmationInputElement, confirmationMessageElement, passwordInputElement.value)

    console.log(usernameResult)
    console.log(emailResult)
    console.log(passwordResult)
    console.log(confirmationResult)
    

    // O formulário vai ser enviado apenas se todos os campos forem válidos
    if (usernameResult && emailResult && passwordResult && confirmationResult) {
      console.log("enviado")
      registerForm.submit();
    }
});