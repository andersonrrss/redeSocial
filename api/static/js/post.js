"use strict";
// Variáveis para armazenar os elementos
let container = null;
let img = null;
let exitBtn = null;
function fullScreen(btn) {
    btn = btn;
    const image = btn.parentElement.querySelector("img");
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
    container.addEventListener("dblclick", function (event) {
        if (zoomin) {
            img.style.transform = "scale(1) translate(0, 0)";
            img.classList.remove("cursor-zoom-out");
            img.classList.add("cursor-zoom-in");
            zoomin = false;
        }
        else {
            const mouseX = event.clientX;
            const mouseY = event.clientY;
            const imgRect = img.getBoundingClientRect();
            const centerX = imgRect.left + imgRect.width / 2;
            const centerY = imgRect.top + imgRect.height / 2;
            const offsetX = -(mouseX - centerX);
            const offsetY = -(mouseY - centerY);
            img.style.transform = `scale(2.0) translate(${offsetX}px, ${offsetY}px)`;
            img.classList.remove("cursor-zoom-in");
            img.classList.add("cursor-zoom-out");
            zoomin = true;
        }
    });
}
