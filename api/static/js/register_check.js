// Checagem do nome na página de registro

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
        reset(username_input, name_message) 

        if (!data.isValid) {
          input_error(username_input, name_message, "Nome inválido");
        }
        if (data.exists) {
          input_error(username_input, name_message, "Nome já cadastrado");
        }
      });
  }
});

// Checagem do email na página de resgistro 

const email_input = document.querySelector("#email");
const email_msg = document.querySelector("#emailMSG");

email_input.addEventListener("input", function () {
  const email = email_input.value;
  if (email.length > 0) {
    fetch(`checkemail?email=${email}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`ERRO -> ${response.statusText}`);
        }
        return response.json();
      })
      .then((data) => {
        reset(email_input, email_msg )

        if (email.length > 0) {
          if (!data.isValid) {
            input_error(email_input, email_msg, "Email inválido");
          }
          if (data.exists) {
            input_error(email_input, email_msg, "Email já cadastrado");
          }
        }
      });
  }
});

// Checa a senha e a confirmação
const input_senha = document.querySelector("#password")
const div_senha = document.querySelector("#divSenha")
const senha_msg = document.querySelector("#senhaMSG");

input_senha.addEventListener("input", function () {
  reset(div_senha, senha_msg )

  if (input_senha.value.length < 8) {
    input_error(
      div_senha,
      senha_msg,
      "Sua senha deve conter pelo menos 8 caracteres"
    );
  }
});

const confirmation = document.querySelector("#confirmation");
const confirmation_msg = document.querySelector("#confirmationMSG");

confirmation.addEventListener("input", function () {
  reset(confirmation, confirmation_msg)
  if (input_senha.value != confirmation.value) {
    input_error(confirmation, confirmation_msg, "As senhas não coincidem");
  }
});

document
  .querySelector("#register-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    // Defina uma variável para rastrear se algum campo é inválido
    let algumCampoInvalido = false;

    // Itera sobre todos os inputs dentro do formulário
    document.querySelectorAll("#sing-form input").forEach((input) => {
      // Verifica se o valor do input é menor que 5 caracteres
      if (input.value.length < 5) {
        // Define o campo como inválido
        algumCampoInvalido = true;
        // Adiciona a classe 'invalid-input' para destacar o campo inválido
        input.classList.add("invalid-input");
      } else {
        // Remove a classe 'invalid-input' caso o campo seja válido
        input.classList.remove("invalid-input");
      }
    });
    // A senha é tratada de forma diferente devido ao seu formato no html
    if (document.querySelector("#password").value.length < 5) {
      // Define o campo como inválido
      algumCampoInvalido = true;
      // Adiciona a classe 'invalid-input' para destacar o campo inválido
      document.querySelector("#divSenha").classList.add("invalid-input");
    }

    // Se algum campo for inválido, exibe um alerta e interrompe o envio do formulário
    if (algumCampoInvalido) {
      alert("Preencha os campos necessários");
    } else {
      // Caso contrário, envia o formulário
      this.submit();
    }
  });