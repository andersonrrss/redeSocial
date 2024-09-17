"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
const loginForm = document.querySelector("#login-form");
const name_or_email = document.querySelector("#name-or-email");
const name_email_MSG = document.querySelector("#emailNameMSG");
function validarEmail(email) {
    // Expressão regular para validar o formato do email
    var regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}
name_or_email.addEventListener("input", function () {
    return __awaiter(this, void 0, void 0, function* () {
        if (name_or_email.value.length >= 6) {
            let passed = true;
            if (validarEmail(name_or_email.value)) {
                yield fetch(`checkemail?email=${name_or_email.value}`)
                    .then(response => response.json())
                    .then(data => {
                    if (!data.exists) {
                        passed = false;
                        input_error(name_or_email, name_email_MSG, "Email não encontrado");
                    }
                });
            }
            else {
                yield fetch(`checkname?name=${name_or_email.value}`)
                    .then(response => response.json())
                    .then(data => {
                    if (!data.exists) {
                        passed = false;
                        input_error(name_or_email, name_email_MSG, "Nome de usuário não encontrado");
                    }
                });
            }
            passed && reset(name_or_email, name_email_MSG);
        }
    });
});
loginForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const email_name = name_or_email;
    const sing_btn = document.querySelector("#sing_button");
    const senha_input = document.querySelector("#password");
    const senha_div = document.querySelector("#divSenha");
    const senha_MSG = document.querySelector("#senhaMSG");
    senha_input.addEventListener("input", function () {
        senha_div.classList.remove("invalid-input");
        senha_MSG.classList.add("hidden");
    });
    let empty_input = false;
    if (email_name.value.length < 2) {
        email_name.classList.add("invalid-input");
        empty_input = true;
    }
    if (senha_input.value.length < 2) {
        senha_div.classList.add("invalid-input");
        empty_input = true;
    }
    if (empty_input) {
        alert("Preencha os campos necessários");
        return;
    }
    fetch(`checkPassword?identifier=${email_name.value}&senha=${senha_input.value}`)
        .then(response => response.json())
        .then(data => {
        if (!data.isRight) {
            senha_MSG.innerHTML = "Senha incorreta";
            senha_MSG.classList.remove("hidden");
            senha_div.classList.add("invalid-input");
        }
        else {
            this.submit();
        }
    });
});
