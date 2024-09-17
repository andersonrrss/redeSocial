const chat_section = document.querySelector("#chat_section") as HTMLElement;
// Garante que o código continue mesmo se não houver chats ativos
try {
  const dropdowns = document.querySelectorAll(".dropdown-menu") as NodeListOf<HTMLUListElement>;
  const show_more = document.querySelectorAll(".show-more") as NodeListOf<HTMLUListElement>;

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
      setTimeout(() => {
        // Para que a animação funcione
        dropdowns[index].classList.toggle("show");
      }, 1);
    });
  });

  dropdowns.forEach((element) => {
    const closeBtn = element.querySelector("#closedropdown") as HTMLButtonElement;
    // Fechar dropdown
    closeBtn.addEventListener("click", function () {
      element.classList.remove("show");
      element.classList.toggle("hidden");
    });

    // Não acionar o hover do elemento da mensagem
    const parentElement = element.parentElement as HTMLDivElement
    element.addEventListener("mouseover", function () {
      parentElement.classList.toggle("no-hover");
    });
    element.addEventListener("mouseout", function () {
      parentElement.classList.remove("no-hover");
    });
  });

  const delete_chat = document.querySelectorAll(".delete_chat_btn") as NodeListOf<HTMLButtonElement>;
  delete_chat.forEach((button, index) => {
    const deleteChatForm = document.querySelectorAll(".deleteChatForm")[index] as HTMLFormElement
    button.addEventListener("click", function () {
      deleteChatForm.submit()
    });
  });
} catch {
  console.log("sem conversas");
}
