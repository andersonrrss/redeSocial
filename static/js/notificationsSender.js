const socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on("new_follower", data => {
    const notifications = document.querySelector("#notifications")
    const notification = document.createElement("div")
    notification.classList.add("notification")
})