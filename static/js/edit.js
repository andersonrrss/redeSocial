// Editar foto de perfil
const profile_pic = document.querySelector("#profile_pic");
const pencil_icon = document.querySelector("#pencil_icon");

document.querySelector("#profile_pic_div").addEventListener("mouseover", () => {
  pencil_icon.style.visibility = "visible";
  profile_pic.style.filter = "blur(2px)";
});

document.querySelector("#profile_pic_div").addEventListener("mouseout", () => {
  pencil_icon.style.visibility = "hidden";
  profile_pic.style.filter = "none";
});

// Editar nome

const editName = document.querySelector("#edit_name");
const name = document.querySelector("#username");
const message = document.querySelector("#message");
const nameForm = document.querySelector("#nameForm");

nameForm.disabled = true;

editName.addEventListener("click", function () {
  editName.innerHTML = `<i class="fa-solid fa-check"></i>`;
  editName.classList = `bg-green-600 text-white ml-3 rounded-md px-4 hover:bg-green-700`;
  name.disabled = false;
  name.focus();
});

name.addEventListener("input", function () {
  let username = name.value;
  //Impede que o form seja submetido antes da hora
  nameForm.addEventListener("submit", preventSubmit);

  fetch(`/checkname?name=${username}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`ERRO => ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      editName.onclick = "none";
      // Checa se o nome de usuário é válido
      if (!data.isValid || data.exists) {
        name.style.borderColor = "red";
        message.style.visibility = "visible";
        editName.disabled = true;
        return false;
      }

      editName.disabled = false;
      // Remove o event listener para que o formulário possa ser submetido normalmente
      nameForm.removeEventListener("submit", preventSubmit);
      editName.addEventListener("click", function () {
        editName.disabled = true;
        nameForm.submit();
      });
      // Muda o estilo se o nome de usuário for válido
      name.style.borderColor = "green";
      message.style.visibility = "hidden";
    })
    .catch((err) => {
      console.warn("OCORREU UM ERRO " + err);
    });
});

// EDITAR A BIOGRAFIA

const bio = document.querySelector("#bio");
const biobtn = document.querySelector("#editbio");
const countBioChar = document.querySelector("#count");
const bioForm = document.querySelector("#bio_form");

countBioChar.innerHTML = `${bio.value.length}/150`;

biobtn.addEventListener("click", function () {
  bio.focus();
  bio.disabled = false;
  biobtn.classList = `bg-green-600 text-white my-3 rounded-md py-2 px-4 hover:bg-green-700`;
  biobtn.innerHTML = '<i class="fa-solid fa-check"></i>';
  biobtn.addEventListener("click", function () {
    bioForm.submit();
  });
});

bio.addEventListener("input", function () {
  const bio_length = bio.value.length;
  // Checa se a biografia é válida
  if (bio_length > 150) {
    bio.disabled = true;
    // Estilização para a quantidade de caracteres
  } else if (bio_length == 150) {
    countBioChar.style.color = "red";
  } else if (bio_length >= 125) {
    countBioChar.style.color = "#9e0000";
  } else {
    countBioChar.style.color = "black";
  }
  // Mostra a contagem de caracteres para o usuário
  countBioChar.innerHTML = `${bio_length}/150`;
  bio.value = bio.value.replace(/\n/g, "\r\n");
});

const preventSubmit = function (event) {
  event.preventDefault();
};
