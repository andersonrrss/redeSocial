const socket = io();
socket.on("connect", function () {
    console.log("Server connected");
});
export function alertError(alertMessage, alertCode) {
    const alertDiv = document.querySelector("#alertDiv");
    const alertMessageSpan = document.querySelector("#alertMessage");
    const alertCodeSpan = document.querySelector("#alertCode");
    const hideAlertButton = document.querySelector("#closeAlert");
    alertMessageSpan.innerHTML = `${alertMessage}`;
    alertCodeSpan.innerHTML = `[${alertCode}]`;
    alertDiv.classList.remove("hidden");
    hideAlertButton.addEventListener("click", function () {
        alertDiv.classList.add("hidden");
    });
}
socket.on("new_follower", function (data) {
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
socket.on("new-message", function (data) {
    if ("Notification" in window) {
        Notification.requestPermission().then(function (permission) {
            if (permission === "granted") {
                // Criar a notificação com a URL de dados do ícone
                let notification = new Notification("Nova mensagem!", {
                    body: `${data.sender_name} te enviou uma mensagem!!`, // Corpo da notificação
                    icon: "../static/icons/hugeicons--message-download-01.svg", // Ícone da notificação
                    badge: "../static/icons/hugeicons--atom-01.svg", // Ícone do app
                });
                notification.onclick = function () {
                    window.location.pathname = `/chat/${data.chat_id}`;
                };
            }
        });
    }
});
const navBarButtons = document.querySelectorAll(".navbar-btn");
navBarButtons.forEach((btn) => {
    let btnPath = new URL(btn.href).pathname;
    if (btnPath == window.location.pathname) {
        let paths = btn.querySelectorAll("path");
        paths.forEach((path) => {
            path.setAttribute("stroke", "#7101d3");
        });
    }
});
