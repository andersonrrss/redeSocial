var socket = io();
socket.on("connect", function () {
  console.log("Server connected");
});
socket.on("new_follower", function (data) {
  if ("Notification" in window) {
    Notification.requestPermission().then(function (permission) {
      if (permission === "granted") {
          // Criar a notificação com a URL de dados do ícone
          let notification = new Notification("Novo seguidor", {
            body: `@${data.follower_name} começou a seguir você!`,
            icon: "./static/icons/new_follower.svg",
          });
        }
        notification.onclick = function () {
          window.location.pathname = data.follower_name;
        };
      })
    }
});