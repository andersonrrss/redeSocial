declare var io: any;

const message_form = document.querySelector("#message_form") as HTMLFormElement;
const message_input = document.querySelector("#message_input") as HTMLInputElement;
const message_area = document.querySelector("#message_area") as Element;
const repliesButtons = document.querySelectorAll(".reply") as NodeListOf<HTMLButtonElement>
const replyDiv = document.getElementById("reply") as HTMLDivElement
const messageSeparator: HTMLElement | null = document.getElementById("separator")

const chat_id = message_form.getAttribute("data-chat-id");
const receiver_id = message_form.getAttribute("data-receiver-id");
const replying = false

let reply_id = 0

interface Message{
  message_id: number
  content: string
  chat_id: number
  sender_id: number
  sender_name: string
  timestamp: number
  parent_message: string
  parent_id: number
}

function scrollToBottom() {
  setTimeout(() => {
    message_area.scrollTop = message_area.scrollHeight;
  }, 0);
}
scrollToBottom();

function loadmessage(message: Message, send : boolean){
  const message_element = document.createElement("div") as HTMLDivElement;
  if (send){
    // Mensagens enviadas
    message_element.innerHTML = `
      <button class="reply hidden" message_id="${message.message_id}" onclick="replymessage(this)">
          <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="black" d="m6.825 12l2.9 2.9q.3.3.288.7t-.313.7q-.3.275-.7.288t-.7-.288l-4.6-4.6q-.3-.3-.3-.7t.3-.7l4.6-4.6q.275-.275.688-.275T9.7 5.7q.3.3.3.713t-.3.712L6.825 10H16q2.075 0 3.538 1.463T21 15v3q0 .425-.288.713T20 19t-.712-.288T19 18v-3q0-1.25-.875-2.125T16 12z"/></svg>
      </button>

      <div class="flex flex-col message sent">
        ${message.parent_id > 0 ? `
          <div class="reply_sent" parent_id="${message.parent_id}">
            <span class="max-w-[80%] truncate inline-block">
              ${message.parent_message}
            </span>
            <span><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="black" d="m6.825 12l2.9 2.9q.3.3.288.7t-.313.7q-.3.275-.7.288t-.7-.288l-4.6-4.6q-.3-.3-.3-.7t.3-.7l4.6-4.6q.275-.275.688-.275T9.7 5.7q.3.3.3.713t-.3.712L6.825 10H16q2.075 0 3.538 1.463T21 15v3q0 .425-.288.713T20 19t-.712-.288T19 18v-3q0-1.25-.875-2.125T16 12z"/></svg></span>
        </div>` : ""
        }
        <p id="content"> ${message.content} </p>
      </div>
    </div>
    `;
    message_element.classList.add("flex", "w-full", "items-center", "justify-end")
  } else {
    // Mensagens recebidas
    message_element.innerHTML = `
      <div class="flex flex-col message received">
        ${!!message.parent_id?
          `<div class="reply_received" parent_id="${message.parent_id}">
              <span><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" transform="scale(-1,1)" viewBox="0 0 24 24"><path fill="black" d="m6.825 12l2.9 2.9q.3.3.288.7t-.313.7q-.3.275-.7.288t-.7-.288l-4.6-4.6q-.3-.3-.3-.7t.3-.7l4.6-4.6q.275-.275.688-.275T9.7 5.7q.3.3.3.713t-.3.712L6.825 10H16q2.075 0 3.538 1.463T21 15v3q0 .425-.288.713T20 19t-.712-.288T19 18v-3q0-1.25-.875-2.125T16 12z"/></svg></span>
              <span class="max-w-[80%] truncate inline-block">
                ${message.parent_message}
              </span>
          </div>`
          : ""
        }
        <p id="content">${message.content}</p>
      </div>
      <button class="reply hidden" message_id="${message.message_id}" onclick="replymessage(this)">
          <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" transform="scale(-1,1)" viewBox="0 0 24 24"><path fill="black" d="m6.825 12l2.9 2.9q.3.3.288.7t-.313.7q-.3.275-.7.288t-.7-.288l-4.6-4.6q-.3-.3-.3-.7t.3-.7l4.6-4.6q.275-.275.688-.275T9.7 5.7q.3.3.3.713t-.3.712L6.825 10H16q2.075 0 3.538 1.463T21 15v3q0 .425-.288.713T20 19t-.712-.288T19 18v-3q0-1.25-.875-2.125T16 12z"/></svg>
      </button>
      `;
      message_element.classList.add("flex", "w-full" ,"items-center", "justify-start") 
  }
  message_element.addEventListener("mouseover", () => showreply(message_element));
  message_element.addEventListener("mouseout", () => hidereply(message_element));
  message_element.setAttribute("id", `${message.message_id}`)
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
        
        replyDiv.classList.add("hidden")
        replyDiv.classList.remove("flex")

        reply_id = 0

        if (messageSeparator){
          messageSeparator.style.display = "none"; // Esconde o elemento que separa as mensagens velhas das novas
        }
      })
      .catch((err) => {
        let status = err.status ?? "Status não disponível";
        let message = err.message ?? "Erro desconhecido";
        console.warn(`ERRO: ${message}(${status})`);
      });
  }
});

var socket = io();

socket.on("new-message", function (message: Message) {
  loadmessage(message, false)
  scrollToBottom(); // Rola para o final após adicionar a nova mensagem

  // Informa ao servidor que a mensagem foi lida
  fetch(`/messageviewed?message_id=${message.message_id}`).catch((err) => {
    let status = err.status ?? "Status não disponível";
    let message = err.message ?? "Erro desconhecido";
    console.warn(`ERRO: ${message}(${status})`);
  });
  if (messageSeparator){
    messageSeparator.style.display = "none"; // Esconde o elemento que separa as mensagens velhas das novas
  }
});

repliesButtons.forEach(reply => {
  reply.addEventListener("click", () => {replymessage(reply)})
})
const deleteReply = document.querySelector("#deleteReply") as HTMLButtonElement
deleteReply.addEventListener("click", function(){
  replyDiv.classList.add("hidden")
})

function replymessage(reply: any){
  reply = reply as HTMLButtonElement

  reply_id = reply.parentElement.getAttribute("id")
  console.log(reply_id)
  message_input.focus()
  const reply_content = reply.parentElement.querySelector("#content").innerHTML
  const input_reply = replyDiv
  const replyText = input_reply.querySelector("#text") as HTMLSpanElement
  replyText.innerHTML = reply_content
  input_reply.classList.remove("hidden")
  input_reply.classList.add("flex")
}

function showreply(div: any) {
  div = div as HTMLDivElement
  let reply_incon = div.querySelector(".reply");
  reply_incon.classList.toggle("hidden");
}

function hidereply(div: any) {
  div = div as HTMLDivElement
  let reply_incon = div.querySelector(".reply");
  reply_incon.classList.add("hidden");
} 