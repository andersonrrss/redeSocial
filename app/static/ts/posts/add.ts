import { alertError } from "../main.js"

const postForm = document.querySelector("#postForm") as HTMLFormElement

const emojiSelector = document.getElementById("emojiSelector") as HTMLLIElement
const emojiSelectorBtn = document.getElementById("emojiSelectorBtn") as HTMLButtonElement
const emojiList = document.getElementById("emojiList") as HTMLUListElement
const emojiSearch = document.getElementById("emojiSearch") as HTMLInputElement

const imageUploadInput = document.getElementById("imageUpload") as HTMLInputElement
const textArea = document.querySelector("#textArea") as HTMLTextAreaElement
const deleteImage = document.querySelector("#deleteImage") as HTMLButtonElement

postForm.addEventListener("submit", function(e){
    e.preventDefault()
    const imageValue = imageUploadInput.value;
    const textAreaValue = textArea.value

    // Verifica se os campos de texto ou imagem estão vazios
    if(!imageValue && !textAreaValue){
        alertError("Nenhuma foto ou texto foram adicionados", 400)
        return;
    }

    // Envia o formulário usando fetch
    postForm.submit()
})

/* interface Emoji {
    slug: string;
    character: string
}

emojiSelectorBtn.addEventListener("click", function(){
    emojiSelector.classList.toggle("active")
})
fetch("https://emoji-api.com/emojis?access_key=")
.then(response => {
    if (!response.ok){
        throw new Error(`ERRO ${response.status}`)
    }
    return response.json();
})
.then((data) => {
    loadEmojis(data)
})
    
function loadEmojis(emojis: Emoji[]){
    emojis.forEach((emoji : Emoji) => {
        const li = document.createElement("li")
        li.setAttribute("emoji-name", emoji.slug)
        li.textContent = emoji.character
        li.classList.add("emojiChar")
        li.addEventListener("click", function(){
            textArea.value += emoji.character
        })
        emojiList.appendChild(li)        
    });
}

emojiSearch.addEventListener("input", function(e){
    const target = e.target as HTMLInputElement | null
    if(target){
        const value = target.value
        const emojis = document.querySelectorAll<HTMLLIElement>("#emojiList li")
        emojis.forEach(emoji => {
            const emojiName = emoji.getAttribute("emoji-name");
            if(emojiName && emojiName.toLowerCase().includes(value.toLowerCase())){
                emoji.style.display = "flex"
            } else {
                emoji.style.display = "none"
            }
        })
    }
}) */

imageUploadInput.addEventListener("change", function (event) {
    const target = event.target as HTMLInputElement
    const files = target.files;
    if (files){
        const fileArray = Array.from(files); // Converte os files para um array
        for (const file of fileArray) {
            const fileReader = new FileReader();
            const preview = document.querySelector("#preview") as HTMLDivElement;
            
            preview.innerHTML = "";
    
            fileReader.addEventListener('load', function() {
                const mediaElement = document.createElement('img');
                mediaElement.src = `${fileReader.result}`;

                preview.appendChild(mediaElement);
                deleteImage.classList.remove("hidden")
            });
            fileReader.readAsDataURL(file);
        }
    }
});

deleteImage.addEventListener("click", function(){
    const preview = document.querySelector("#preview") as HTMLDivElement;
    // Limpa o valor do input
    imageUploadInput.value = ""
    // Volta a vizualização para o padrão
    preview.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="70%" height="70%" viewBox="0 0 24 24">
            <path fill="#858585" d="M19 10a1 1 0 0 0-1 1v3.38l-1.48-1.48a2.79 2.79 0 0 0-3.93 0l-.7.71l-2.48-2.49a2.79 2.79 0 0 0-3.93 0L4 12.61V7a1 1 0 0 1 1-1h8a1 1 0 0 0 0-2H5a3 3 0 0 0-3 3v12.22A2.79 2.79 0 0 0 4.78 22h12.44a2.88 2.88 0 0 0 .8-.12a2.74 2.74 0 0 0 2-2.65V11A1 1 0 0 0 19 10M5 20a1 1 0 0 1-1-1v-3.57l2.89-2.89a.78.78 0 0 1 1.1 0L15.46 20Zm13-1a1 1 0 0 1-.18.54L13.3 15l.71-.7a.77.77 0 0 1 1.1 0L18 17.21Zm3-15h-1V3a1 1 0 0 0-2 0v1h-1a1 1 0 0 0 0 2h1v1a1 1 0 0 0 2 0V6h1a1 1 0 0 0 0-2"/>
        </svg>
    `
    this.classList.add("hidden")
})


const maxChars: number = 1500
const charCounter = document.querySelector("#charCounter") as HTMLSpanElement

if (textArea.value.length > 0){
    charCounter.innerHTML = `${textArea.value.length}/${maxChars}`
}

textArea.addEventListener("input" , function () {
    if (textArea.value.length > maxChars){
        textArea.value = textArea.value.substring(0, maxChars);
    }
    charCounter.innerHTML = `${textArea.value.length}/${maxChars}`
})