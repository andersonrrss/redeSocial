var socket = io()
      socket.on("connect", function(){
        console.log("Servidor conectado")
      })
      socket.on("new_follower", function(data){
        if("Notification" in window){
            Notification.requestPermission().then(function(permission){
                if(permission === "granted"){
                    let notification = new Notification("Novo seguidor", {
                        body: `@${data.follower_name} começou a seguir você!`,
                        icon: '../icons/mdi--account-plus.svg'
                    })
                    notification.onclick = function(){
                        window.location.pathname = data.follower_name
                    }
                }
            })
        }
      })