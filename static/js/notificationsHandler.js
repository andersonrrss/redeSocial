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
            body: `@${data.follower_name} começou a seguir você!`, // Corpo da notificação
            icon: "./static/icons/new_follower.svg",           // Ícone da notificação
            badge: "./static/icons/hugeicons--atom-01.svg",    // Ícone do app
            timestamp: Date.now(),                             // Timestamp da notificação
            vibrate: [200, 100, 200],                          // Padrão de vibração (vibra, pausa, vibra)
          });
          notification.onclick = function () {
            window.location.pathname = data.follower_name;
          };
        }
        
      })
    }
});