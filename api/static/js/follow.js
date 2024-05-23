const followbtn = document.querySelector("#followbtn");
const user_id = document.querySelector("#user_id").value;
const form = document.querySelector("#followbtnForm");

// Checa se o usuário já segue o perfil
fetch(`/isFollowed?user=${user_id}`)
  .then((response) => {
    if (!response.ok) {
      throw new Error(`http error -> ${response.status}`);
    }
    // Retorna a resposta
    return response.json();
  })
  .then((data) => {
    // Se o usuário for seguido
    if (data.is_followed) {
      followbtn.innerHTML = "Seguindo"; // Muda o conteúdo do botão
      followbtn.classList =
        "text-black text-center font-semibold p-2 rounded-md w-full bg-gray-300 hover:bg-gray-400"; // Muda o estilo do botão
      // Muda o método do form para POST
      form.method = "post";
    }
  })
  .catch((error) => {
    console.error("Erro:", error);
  });
