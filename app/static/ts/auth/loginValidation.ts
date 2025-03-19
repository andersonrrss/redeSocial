import {checkInput, validatePassword} from './validationHelper.js'

const loginForm = document.querySelector("#login-form") as HTMLFormElement

const nameOrEmailInputElement = document.querySelector("#name-or-email") as HTMLInputElement
const nameOrEmailMessageElement = document.querySelector("#emailNameMSG") as HTMLSpanElement

nameOrEmailInputElement.addEventListener("input", async function(){
    const value = nameOrEmailInputElement.value
    await checkInput(value, nameOrEmailInputElement, nameOrEmailMessageElement, "validateNameOrEmail", "nameOrEmail")
})

loginForm.addEventListener("submit", async function(event){
    event.preventDefault()

    const passwordInputElement = document.querySelector("#password") as HTMLInputElement
    const passwordContainer = document.querySelector("#divSenha") as HTMLDivElement
    const passwordMessageElement = document.querySelector("#senhaMSG") as HTMLSpanElement

    const nameOrEmailResult = await checkInput(nameOrEmailInputElement.value, nameOrEmailInputElement, nameOrEmailMessageElement, "validateNameOrEmail", "nameOrEmail")
    const passwordResult = await validatePassword(passwordInputElement.value, nameOrEmailInputElement.value, passwordContainer, passwordMessageElement)

    if(nameOrEmailResult && passwordResult){
        loginForm.submit()
    }
})