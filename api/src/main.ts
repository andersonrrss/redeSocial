declare var io: any;

const socket = io();
socket.on("connect", function () {
  console.log("Server connected");
});

export function alertError(alertMessage: string, alertCode: number){
    const alertDiv = document.querySelector("#alertDiv") as HTMLDivElement
    const alertMessageSpan = document.querySelector("#alertMessage") as HTMLSpanElement
    const alertCodeSpan = document.querySelector("#alertCode") as HTMLSpanElement
    const hideAlertButton = document.querySelector("#closeAlert") as HTMLButtonElement
    
    alertMessageSpan.innerHTML = `${alertMessage}`
    alertCodeSpan.innerHTML = `[${alertCode}]`

    alertDiv.classList.remove("hidden")

    hideAlertButton.addEventListener("click", function(){
      alertDiv.classList.add("hidden")
    })
}

interface NewFollower{
    follower_id: number
    follower_name: string
}

socket.on("new_follower", function (data : NewFollower) {
  if ("Notification" in window) {
    Notification.requestPermission().then(function (permission) {
      if (permission === "granted") {
        // Criar a notificação com a URL de dados do ícone
        let notification = new Notification("Novo seguidor", {
          body: `@${data.follower_name} começou a seguir você!`, // Corpo da notificação
          icon: "./static/icons/new_follower.svg", // Ícone da notificação
          badge: "./static/icons/hugeicons--atom-01.svg", // Ícone do app
        });
        notification.onclick = function () {
          window.location.pathname = data.follower_name;
        };
      }
    });
  }
});

interface NewMessage{
    message_id: number,
    content: string
    chat_id: number
    sender_id: number,
    sender_name: string,
    timestamp: Date,
    parent_message: string,
    parent_id: number,
}

socket.on("new-message", function (data: NewMessage) {
  if ("Notification" in window) {
    Notification.requestPermission().then(function (permission) {
      if (permission === "granted") {
        // Criar a notificação com a URL de dados do ícone
        let notification = new Notification("Nova mensagem!", {
          body: `${data.sender_name} te enviou uma mensagem!!`, // Corpo da notificação
          icon: "../static/icons/hugeicons--message-download-01.svg", // Ícone da notificação
          badge: "../static/icons/hugeicons--atom-01.svg", // Ícone do app
        });
        notification.onclick = function(){
          window.location.pathname = `/chat/${data.chat_id}`;
        }
      }
    });
  }
});

const navBarButtons = document.querySelectorAll(".navbar-btn") as NodeListOf<HTMLAnchorElement>
navBarButtons.forEach((btn: HTMLAnchorElement) => {
  let btnPath = new URL(btn.href).pathname;
  if (btnPath == window.location.pathname) {
    let paths = btn.querySelectorAll("path")
    paths.forEach((path) => {
      path.setAttribute("stroke", "#7101d3")
    })
  }
});