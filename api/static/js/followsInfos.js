document.addEventListener("DOMContentLoaded", () => {
  const username = document.querySelector("#username").value;
  const method = document.querySelector("#method").value;
  const show_follows = document.querySelector("#show_follows");

  // Faz requisição para pegar as informações
  fetch(`/follows?username=${username}`, {
    method: method.toUpperCase(), // POST é para os seguidos e GET para os seguidores
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Erro da requisição: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      // Checa se o usuário tem seguidores
      if (!data.has_follows) {
        show_follows.innerHTML = "Não tem nada aqui ainda..";
        return;
      }
      let html = "";
      // Itera sobre todos os seguidores para mostrá-los
      data.follows_infos.forEach((user) => {
        html += `
            <a href="/${user.nome}" class="flex justify-start items-center w-full p-3 hover:bg-gray-200">
                <img src="../static/${user.profile_pic}" class="w-5 rounded-full h-full mr-2"> 
                <span class="font-semibold">@${user.nome}</span>
            </a>
            `;
      });
      // Mostra o html
      show_follows.innerHTML = html;
    })
    .catch((err) => {
      console.error(`ERRO HTTP => ${err}`);
    });
});
