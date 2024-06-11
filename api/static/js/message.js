const message_form = document.querySelector("#message_form");
const message_input = document.querySelector("#message_input");
const message_area = document.querySelector("#message_area");

const chat_id = message_form.getAttribute("data-chat-id");
const receiver_id = message_form.getAttribute("data-receiver-id");

function scrollToBottom() {
  setTimeout(() => {
    message_area.scrollTop = message_area.scrollHeight;
  }, 0);
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
        const message_element = document.createElement("div");
        message_element.innerHTML = `
          <button class="reply hidden" message_id="${ data.message_id }" onclick="replymessage(this)">
              <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24">
                  <g fill="none" stroke="black" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">
                    <path d="m7 17l-5-5l5-5m5 10l-5-5l5-5"/><path d="M22 18v-2a4 4 0 0 0-4-4H7"/>
                  </g>
              </svg>
          </button>
          <p class="message sent"> ${data.message} </p>
          `;
        message_element.addEventListener("mouseover", () => showreply(message_element));
        message_element.addEventListener("mouseout", () => hidereply(message_element));
        message_element.setAttribute("message_id", data.message_id)
        message_element.classList = "flex w-full items-center justify-end"
        message_area.appendChild(message_element);
        scrollToBottom(); // Rola para o final após adicionar a nova mensagem
        document.getElementById("reply").classList.add("hidden")
        document.getElementById("reply").classList.remove("flex") // Esconde o elemento que separa as mensagens velhas das novas
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
  const message_element = document.createElement("div");
  message_element.innerHTML = `
  <button class="reply hidden" message_id="${message.message_id}">
      <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24">
          <g fill="none" stroke="black" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">
            <path d="m7 17l-5-5l5-5m5 10l-5-5l5-5"/><path d="M22 18v-2a4 4 0 0 0-4-4H7"/>
          </g>
      </svg>
  </button>
  <p class="message sent"> ${message.content} </p>
  `;
  message_element.setAttribute("message_id", message.message_id)
  message_element.addEventListener("mouseover", showreply(this));
  message_element.addEventListener("mouseout", hidereply(this));
  message_area.appendChild(message_element);
  scrollToBottom(); // Rola para o final após adicionar a nova mensagem

  // Informa ao servidor que a mensagem foi lida
  fetch(`/messageviewed?message_id=${message.message_id}`).catch((err) => {
    let status = err.status ?? "Status não disponível";
    let message = err.message ?? "Erro desconhecido";
    console.warn(`ERRO: ${message}(${status})`);
  });
  document.getElementById("separator").style.display = "none"; // Esconde o elemento que separa as mensagens velhas das novas
});

document.querySelectorAll(".reply").forEach(reply => {
  reply.addEventListener("click", () => {replymessage(reply)})
})
document.querySelector("#deleteReply").addEventListener("click", function(){
  document.querySelector("#reply").classList.add("hidden")
})

function replymessage(reply){
  const message_id = reply.getAttribute("message_id")
  const message_content = reply.parentElement.querySelector(".message").innerHTML
  const input_reply = document.querySelector("#reply")
  input_reply.querySelector("#text").innerHTML = message_content
  input_reply.classList.remove("hidden")
  input_reply.classList.add("flex")
  scrollToBottom()
}

function showreply(div) {
  let reply_incon = div.querySelector(".reply");
  reply_incon.classList.toggle("hidden");
}

function hidereply(div) {
  let reply_incon = div.querySelector(".reply");
  reply_incon.classList.add("hidden");
}
