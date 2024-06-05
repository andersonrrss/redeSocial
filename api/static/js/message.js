const message_form = document.querySelector("#message_form");
const message_input = document.querySelector("#message_input");
const message_area = document.querySelector("#message_area");

const chat_id = message_form.getAttribute("data-chat-id");
const receiver_id = message_form.getAttribute("data-receiver-id");

function scrollToBottom() {
  message_area.scrollTop = message_area.scrollHeight;
}
scrollToBottom();

message_form.addEventListener("submit", function (event) {
  event.preventDefault();
  const message = message_input.value;
  if (!!message && !!message.trim()) {
    // Checa se alguma mensagem foi digitada
    message_input.value = "";
    fetch(
      `/sendmessage?message=${message.trim()}&receiver_id=${receiver_id}&chat_id=${chat_id}` // Informações necessárias para o envio da mensagem via servidor
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error(response.statusText);
        }
        return response.json();
      })
      .then((data) => {
        const message_element = document.createElement("p"); // Adicionar uma forma de ver o horário de envio da mensagem
        message_element.textContent = data.message;
        message_element.classList.add("message", "sent");
        message_area.appendChild(message_element);
        scrollToBottom(); // Rola para o final após adicionar a nova mensagem
        document.getElementById("separator").style.display = "none"; // Esconde o elemento que separa as mensagens velhas das novas
      })
      .catch((err) => {
        let status = err.status ?? "Status não disponível";
        let message = err.message ?? "Erro desconhecido";
        console.warn(`ERRO: ${message}(${status})`);
      });
  }
});

var socket = io();

socket.on("new-message", function (message) {

  const message_element = document.createElement("p");
  message_element.textContent = message.content;
  message_element.classList.add("message", "received");
  message_area.appendChild(message_element);
  scrollToBottom(); // Rola para o final após adicionar a nova mensagem
  console.log("New message received:"); // Log para depuração
  // Informa ao servidor que a mensagem foi lida
  fetch(`/messageviewed?message_id=${message.id}`).catch((err) => {
    let status = err.status ?? "Status não disponível";
    let message = err.message ?? "Erro desconhecido";
    console.warn(`ERRO: ${message}(${status})`);
  });
  document.getElementById("separator").style.display = "none"; // Esconde o elemento que separa as mensagens velhas das novas
});
