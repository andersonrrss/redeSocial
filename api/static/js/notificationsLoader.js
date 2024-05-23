fetch("/notifications", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({}), // Adicione o corpo da requisição se necessário
})
  .then((response) => response.json())
  .then((data) => {
    const notifications = document.querySelector("#notifications");

    if (!!data.length) {
      let html = "";
      data.forEach((item) => {
        let tempo = new Date(item.timestamp);
        // Converter para o fuso horário local do navegador
        tempo = new Date(tempo.getTime() - tempo.getTimezoneOffset() * 60000);
        html += `
        <div class="notificacao ${
          (!item.viewed && "nova_notification") || ""
        }">      
            <div>
                ${
                  !item.viewed
                    ? `
                <span class="text-purple-600 font-bold ">novo!!</span>
                `
                    : ""
                }
                <span class="text-gray-600">${item.content}</span>
            </div>
            <span class="text-gray-600">${tempo.toLocaleTimeString()}</span>
        </div>
        `;
      });

      notifications.innerHTML = html;
    } else {
      notifications.innerHTML = "<p class='text-center mt-44'>Nenhuma notificação..</p>";
    }
  })
  .catch((err) => {
    console.warn(`http error => ${err.message}`);
  });
