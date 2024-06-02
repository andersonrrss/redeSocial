const chat_section = document.querySelector("#chat_section");
// Garante que o código continue mesmo se não houver chats ativos
try {
  const dropdowns = document.querySelectorAll(".dropdown-menu");
  const show_more = document.querySelectorAll(".show-more");

  show_more.forEach((element, index) => {
    element.addEventListener("click", function () {
      // Fecha todos os dropdowns, exceto o que foi clicado
      dropdowns.forEach((dropdown, i) => {
        if (i !== index) {
          dropdown.classList.add("hidden");
          dropdown.classList.remove("show");
        }
      });

      // Mostra apenas o dropdown correspondente
      dropdowns[index].classList.toggle("hidden");
      setTimeout(() => { // Para que a animação funcione
        dropdowns[index].classList.toggle("show");
      }, 1);
    });
  });

  dropdowns.forEach((element) => {
    const closeBtn = element.querySelector("#closedropdown");
    // Fechar dropdown
    closeBtn.addEventListener("click", function () {
      element.classList.remove("show");
      element.classList.toggle("hidden");
    });

    // Não acionar o hover do elemento da mensagem
    element.addEventListener("mouseover", function () {
      element.parentElement.classList.toggle("no-hover");
    });
    element.addEventListener("mouseout", function () {
      element.parentElement.classList.remove("no-hover");
    });
  });
} catch {
  console.log("sem conversas");
}
