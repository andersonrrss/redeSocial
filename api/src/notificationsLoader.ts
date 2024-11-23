interface Notification{
  senderName: string
  postId: number
  type: string
  viewed: boolean
  timestamp: Date
}

fetch("/notifications", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({}), // Adicione o corpo da requisição se necessário
})
  .then((response) => response.json())
  .then((data) => {
    const oldNotificationsDiv = document.querySelector("#notifications") as HTMLDivElement;
    const newNotificationsDiv = document.querySelector("#newNotifications") as HTMLDivElement

    if (data.length > 0) {
      let oldNotifications = "";
      let newNotifications = "";
      data.forEach((notification : Notification) => {
        if(notification.viewed){
          oldNotifications += renderNotification(notification)
        } else{
          newNotifications += renderNotification(notification)
        }
      });
      
      
      if(newNotifications){
        newNotificationsDiv.innerHTML = newNotifications
        const newNotificationsTittle = document.querySelector("#newNotificationsTitle") as HTMLTitleElement
        newNotificationsTittle.classList.remove("hidden")
      }
      
      oldNotificationsDiv.innerHTML = oldNotifications;
      if(!oldNotifications){
        const oldNotificationsTitle = document.querySelector("#notificationsTitle") as HTMLTitleElement
        oldNotificationsTitle.classList.add("hidden")
      }
    } else {
      const main = document.querySelector("#main") as HTMLElement
      main.innerHTML = `
        <h1 class="text-center m-2 text-2xl font-semibold text-purple-800">Notificações</h1>
        <div class="text-lg font-semibold text-gray-800 h-[80%] w-full flex justify-center items-center">Você não tem nenhuma notificação ainda...</div>
      `
    }
  })
  .catch((err) => {
    console.warn(`http error => ${err.message}`);
  });

  function renderNotification(notification: Notification){

    let tempo = new Date(notification.timestamp);

    switch (notification.type){
      // Notificação de novo seguidor
      case "new_follower":
        return `<a href="/${notification.senderName}" class="notificacao">
              <div class="flex justify-center items-center">
                <svg class="mr-2" xmlns="http://www.w3.org/2000/svg" width="1.2em" height="1.2em" viewBox="0 0 24 24">
                  <g fill="none" stroke="#7e22ce" stroke-linecap="round" stroke-width="1.8"><path stroke-linejoin="round" d="M12.125 14.719c-3.6 0-7.62 2.928-7.62 6.526m7.62-9.785a4.36 4.36 0 0 0 4.035-2.683a4.355 4.355 0 0 0-3.17-5.948a4.362 4.362 0 0 0-5.215 4.274a4.356 4.356 0 0 0 4.35 4.357"/>
                      <path stroke-miterlimit="10" d="M16.488 14.983v5.997m-2.993-2.992h6"/>
                  </g>
                </svg>
                <span class="font-semibold mr-2 ">@${notification.senderName}</span> começou a seguir você!
              </div>
              <div class="text-sm">${tempo.getHours()}:${tempo.getMinutes()} 
              - ${tempo.getDay()< 10? `0${tempo.getDay()}`: tempo.getDay()}/${tempo.getMonth()}</div>
            </a>`;
    }
  }