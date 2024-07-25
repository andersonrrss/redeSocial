const message_form = document.querySelector("#message_form");
const message_input = document.querySelector("#message_input");
const message_area = document.querySelector("#message_area");

const chat_id = message_form.getAttribute("data-chat-id");
const receiver_id = message_form.getAttribute("data-receiver-id");
const replying = false

let reply_id = 0

function scrollToBottom() {
  setTimeout(() => {
    message_area.scrollTop = message_area.scrollHeight;
  }, 0);
}
scrollToBottom();

function loadmessage(data, send ){
  const message_element = document.createElement("div");
  if (send){
    // Mensagens enviadas
    message_element.innerHTML = `
      <button class="reply hidden" message_id="${data.message_id}" onclick="replymessage(this)">
          <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="black" d="m6.825 12l2.9 2.9q.3.3.288.7t-.313.7q-.3.275-.7.288t-.7-.288l-4.6-4.6q-.3-.3-.3-.7t.3-.7l4.6-4.6q.275-.275.688-.275T9.7 5.7q.3.3.3.713t-.3.712L6.825 10H16q2.075 0 3.538 1.463T21 15v3q0 .425-.288.713T20 19t-.712-.288T19 18v-3q0-1.25-.875-2.125T16 12z"/></svg>
      </button>

      <div class="flex flex-col message sent">
        ${data.parent_id > 0 ? `
          <div class="reply_sent" parent_id="${data.parent_id}">
            <span class="max-w-[80%] truncate inline-block">
              ${data.parent_message}
            </span>
            <span><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="black" d="m6.825 12l2.9 2.9q.3.3.288.7t-.313.7q-.3.275-.7.288t-.7-.288l-4.6-4.6q-.3-.3-.3-.7t.3-.7l4.6-4.6q.275-.275.688-.275T9.7 5.7q.3.3.3.713t-.3.712L6.825 10H16q2.075 0 3.538 1.463T21 15v3q0 .425-.288.713T20 19t-.712-.288T19 18v-3q0-1.25-.875-2.125T16 12z"/></svg></span>
        </div>` : ""
        }
        <p id="content"> ${data.content} </p>
      </div>
    </div>
    `;
    message_element.classList = "flex w-full items-center justify-end"
  } else {
    // Mensagens recebidas
    message_element.innerHTML = `
      <div class="flex flex-col message received">
        ${!!data.parent_id > 0?
          `<div class="reply_received" parent_id="${data.parent_id}">
              <span><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" transform="scale(-1,1)" viewBox="0 0 24 24"><path fill="black" d="m6.825 12l2.9 2.9q.3.3.288.7t-.313.7q-.3.275-.7.288t-.7-.288l-4.6-4.6q-.3-.3-.3-.7t.3-.7l4.6-4.6q.275-.275.688-.275T9.7 5.7q.3.3.3.713t-.3.712L6.825 10H16q2.075 0 3.538 1.463T21 15v3q0 .425-.288.713T20 19t-.712-.288T19 18v-3q0-1.25-.875-2.125T16 12z"/></svg></span>
              <span class="max-w-[80%] truncate inline-block">
                ${data.parent_message}
              </span>
          </div>`
          : ""
        }
        <p id="content">${data.content}</p>
      </div>
      <button class="reply hidden" message_id="${data.message_id}" onclick="replymessage(this)">
          <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" transform="scale(-1,1)" viewBox="0 0 24 24"><path fill="black" d="m6.825 12l2.9 2.9q.3.3.288.7t-.313.7q-.3.275-.7.288t-.7-.288l-4.6-4.6q-.3-.3-.3-.7t.3-.7l4.6-4.6q.275-.275.688-.275T9.7 5.7q.3.3.3.713t-.3.712L6.825 10H16q2.075 0 3.538 1.463T21 15v3q0 .425-.288.713T20 19t-.712-.288T19 18v-3q0-1.25-.875-2.125T16 12z"/></svg>
      </button>
      `;
      message_element.classList = "flex w-full items-center justify-start"
  }
  message_element.addEventListener("mouseover", () => showreply(message_element));
  message_element.addEventListener("mouseout", () => hidereply(message_element));
  message_element.setAttribute("id", data.message_id)
  message_area.appendChild(message_element);
}

message_form.addEventListener("submit", function (event) {
  event.preventDefault();
  const message = message_input.value;
  if (!!message && !!message.trim()) {
    // Checa se alguma mensagem foi digitada
    message_input.value = "";
    fetch(
      `/sendmessage?message=${message.trim()}&receiver_id=${receiver_id}&chat_id=${chat_id}&parent_id=${reply_id}` // Informações necessárias para o envio da mensagem via servidor
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error(response.statusText);
        }
        return response.json();
      })
      .then((data) => {
        loadmessage(data, true)
        scrollToBottom(); // Rola para o final após adicionar a nova mensagem
        document.getElementById("reply").classList.add("hidden")
        document.getElementById("reply").classList.remove("flex")

        reply_id = 0

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
  loadmessage(message, false)
  console.log(message.parent_content)
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
  reply_id = reply.parentElement.getAttribute("id")
  console.log(reply_id)
  message_input.focus()
  const reply_content = reply.parentElement.querySelector("#content").innerHTML
  const input_reply = document.querySelector("#reply")
  input_reply.querySelector("#text").innerHTML = reply_content
  input_reply.classList.remove("hidden")
  input_reply.classList.add("flex")
}

function showreply(div) {
  let reply_incon = div.querySelector(".reply");
  reply_incon.classList.toggle("hidden");
}

function hidereply(div) {
  let reply_incon = div.querySelector(".reply");
  reply_incon.classList.add("hidden");
} 