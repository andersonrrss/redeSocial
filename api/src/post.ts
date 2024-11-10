// Variáveis para armazenar os elementos
let container : any = null;
let img : any = null;
let exitBtn : any = null;
// Função do evento de clique adicionado via html
document.querySelectorAll(".fullScreenBtn").forEach(fullScreenBtn => {
    fullScreenBtn.addEventListener("click", () => {
        fullScreen(fullScreenBtn)
    })
});
document.querySelectorAll('.like-button').forEach(button => {
    button.addEventListener('click', () => {
        likePost(button)
    });
});

function fullScreen(btn : any) {
    btn = btn as HTMLButtonElement
    const image = btn.parentElement.querySelector("img") as HTMLImageElement;

    // Verifica se o container já foi criado
    if (!container) {
        // Se não foi criado, cria os elementos e os armazena nas variáveis globais
        container = document.createElement("div");
        img = document.createElement("img");
        exitBtn = document.createElement("button");

        container.classList = "fixed w-[100%] h-[100%] flex justify-center items-center";
        container.style.backdropFilter = "blur(5px)";
        container.style.backgroundColor = "rgba(0, 0, 0, 0.5)";

        img.classList = "max-w-[100%] max-h-[95%] transition-all duration-150 cursor-zoom-in";
        container.appendChild(img);

        exitBtn.innerHTML = `
        <button class="w-2 h-2 bg-transparent " style='filter: invert(1);'>
            <svg xmlns="http://www.w3.org/2000/svg" width="2em" height="2em" viewBox="0 0 24 24" class="text-black">
                <path fill="currentColor" d="m10 15.4l-5.9 5.9q-.275.275-.7.275t-.7-.275t-.275-.7t.275-.7L8.6 14H5q-.425 0-.712-.288T4 13t.288-.712T5 12h6q.425 0 .713.288T12 13v6q0 .425-.288.713T11 20t-.712-.288T10 19zm5.4-5.4H19q.425 0 .713.288T20 11t-.288.713T19 12h-6q-.425 0-.712-.288T12 11V5q0-.425.288-.712T13 4t.713.288T14 5v3.6l5.9-5.9q.275-.275.7-.275t.7.275t.275.7t-.275.7z"/>
            </svg>
        </button>
        `;
        exitBtn.classList = "absolute top-2 left-2";
        exitBtn.addEventListener("click", function () {
            btn.disabled = false;
            container.style.display = "none"; // Esconde o container
        });

        container.appendChild(exitBtn);
        document.body.appendChild(container);
    }

    // Atualiza o src da imagem e exibe o container
    img.src = image.src;
    container.style.display = "flex"; // Mostra o container

    let zoomin = false;
    container.addEventListener("dblclick", function (event:any) {
        if (zoomin) {
            img.style.transform = "scale(1) translate(0, 0)";
            img.classList.remove("cursor-zoom-out")
            img.classList.add("cursor-zoom-in")
            zoomin = false;
        } else {
            const mouseX = event.clientX;
            const mouseY = event.clientY;
            const imgRect = img.getBoundingClientRect();
            const centerX = imgRect.left + imgRect.width / 2;
            const centerY = imgRect.top + imgRect.height / 2;
            const offsetX = -(mouseX - centerX);
            const offsetY = -(mouseY - centerY);

            img.style.transform = `scale(2.0) translate(${offsetX}px, ${offsetY}px)`;
            img.classList.remove("cursor-zoom-in")
            img.classList.add("cursor-zoom-out")
            zoomin = true;
        }
    });
}


// Ver mais e Ver menos
const postsTexts = document.querySelectorAll('.imagePostContent'); // Seleciona todos os elementos de texto das postagens
const readMoreBtns = document.querySelectorAll('.readMoreBtn'); // Seleciona todos os botões de "Ler Mais"

if (postsTexts.length > 0) { // Verifica se existem postagens
    postsTexts.forEach((text, index) => { // Para cada texto de postagem
        const lineHeight = parseInt(window.getComputedStyle(text).lineHeight); // Obtém a altura da linha do texto
        const maxHeight = lineHeight * 5; // Define a altura máxima para 5 linhas

        if (text.scrollHeight > maxHeight) { // Se a altura do conteúdo for maior que 5 linhas
            if (readMoreBtns[index]) { // Verifica se o botão "Ler Mais" existe
                const btn = readMoreBtns[index] as HTMLButtonElement; // Obtém o botão correspondente
                btn.classList.remove('hidden'); // Remove a classe "hidden" para exibir o botão

                btn.addEventListener("click", function () { // Adiciona um evento de clique ao botão
                    const postContent = postsTexts[index] as HTMLParagraphElement; // Obtém o conteúdo da postagem
                    const isExpanded = postContent.style.webkitLineClamp === 'unset'; // Verifica se o texto está expandido
                    
                    if (isExpanded) { // Se o conteúdo estiver expandido
                        postContent.style.webkitLineClamp = '5'; // Limita o texto a 5 linhas
                        postContent.style.overflow = 'hidden'; // Oculta o conteúdo excedente
                        btn.textContent = 'Ler Mais'; // Altera o texto do botão para "Ler Mais"
                    } else { // Se o conteúdo estiver colapsado
                        postContent.style.webkitLineClamp = 'unset'; // Remove o limite de linhas
                        postContent.style.overflow = 'visible'; // Exibe o conteúdo completo
                        btn.textContent = 'Ver menos'; // Altera o texto do botão para "Ver Menos"
                    }
                });
            }
        }
    });
}


function likePost(button : any){
    const postId = (button as HTMLElement).getAttribute('post-id');
        try {
            fetch(`/like?post_id=${postId}`)
            .then(response => response.json())
            .then((data) => {
                const post = document.querySelector(`#id_${data.postId}`) as HTMLDivElement
                const likeCounter = post.querySelector(".like-counter") as HTMLSpanElement
                likeCounter.innerText = `${data.likeCount} curtidas`
                
                const likeButton = button as HTMLButtonElement
                if(data.action == "like"){
                    likeButton.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" viewBox="0 0 48 48">
                        <path fill="#ff3838" stroke="#ff3838" stroke-linecap="round" stroke-linejoin="round" stroke-width="4" d="M15 8C8.925 8 4 12.925 4 19c0 11 13 21 20 23.326C31 40 44 30 44 19c0-6.075-4.925-11-11-11c-3.72 0-7.01 1.847-9 4.674A10.99 10.99 0 0 0 15 8"/>
                    </svg>
                `
                } else {
                    likeButton.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" viewBox="0 0 48 48" >
                        <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="4" d="M15 8C8.925 8 4 12.925 4 19c0 11 13 21 20 23.326C31 40 44 30 44 19c0-6.075-4.925-11-11-11c-3.72 0-7.01 1.847-9 4.674A10.99 10.99 0 0 0 15 8"/>
                    </svg>
                    `
                }
            })
        } catch {
            alert("Algo deu errado")
        }
}