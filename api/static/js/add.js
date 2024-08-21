const emojiSelector = document.getElementById("emojiSelector")
const emojiSelectorBtn = document.getElementById("emojiSelectorBtn")
const emojiList = document.getElementById("emojiList")
const emojiSearch = document.getElementById("emojiSearch")

const textArea = document.querySelector("#textArea")
const deleteImage = document.querySelector("#deleteImage")

emojiSelectorBtn.addEventListener("click", function(){
    emojiSelector.classList.toggle("active")
})
fetch("https://emoji-api.com/emojis?access_key=c1e15a17580c2958b4ec9610ea9e636870b8e4a4")
.then(response => {
    if (!response.ok){
        throw new Error(response.status)
    }
    return response.json();
})
.then((data) => {
    loadEmojis(data)
})
    
function loadEmojis(emojis){
    emojis.forEach(emoji => {
        const li = document.createElement("li")
        li.setAttribute("emoji-name", emoji.slug)
        li.textContent = emoji.character
        li.classList = "emojiChar"
        li.addEventListener("click", function(){
            textArea.value += emoji.character
        })
        emojiList.appendChild(li)        
    });
}

emojiSearch.addEventListener("input", function(e){
    const value = e.target.value
    const emojis = document.querySelectorAll("#emojiList li")
    emojis.forEach(emoji => {
        if(emoji.getAttribute("emoji-name").toLowerCase().includes(value.toLowerCase())){
            emoji.style.display = "flex"
        } else {
            emoji.style.display = "none"
        }
    })
})

document.getElementById("imageUpload").addEventListener("change", function (event) {
    const files = event.target.files;
    for (const file of files) {
        const fileReader = new FileReader();
        const preview = document.querySelector("#preview");
        preview.innerHTML = "";

        fileReader.addEventListener('load', function() {
            const mediaElement = document.createElement('img');
            mediaElement.src = fileReader.result;
            if (mediaElement.tagName === 'VIDEO') {
                mediaElement.controls = true;
            }
            preview.appendChild(mediaElement);
            deleteImage.classList.remove("hidden")
        });
        fileReader.readAsDataURL(file);
    }
});

deleteImage.addEventListener("click", function(){
    const preview = document.querySelector("#preview");
    // Limpa o valor do input
    document.querySelector("#imageUpload").value = null
    // Volta a vizualização para o padrão
    preview.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="70%" height="70%" viewBox="0 0 24 24">
            <path fill="#858585" d="M19 10a1 1 0 0 0-1 1v3.38l-1.48-1.48a2.79 2.79 0 0 0-3.93 0l-.7.71l-2.48-2.49a2.79 2.79 0 0 0-3.93 0L4 12.61V7a1 1 0 0 1 1-1h8a1 1 0 0 0 0-2H5a3 3 0 0 0-3 3v12.22A2.79 2.79 0 0 0 4.78 22h12.44a2.88 2.88 0 0 0 .8-.12a2.74 2.74 0 0 0 2-2.65V11A1 1 0 0 0 19 10M5 20a1 1 0 0 1-1-1v-3.57l2.89-2.89a.78.78 0 0 1 1.1 0L15.46 20Zm13-1a1 1 0 0 1-.18.54L13.3 15l.71-.7a.77.77 0 0 1 1.1 0L18 17.21Zm3-15h-1V3a1 1 0 0 0-2 0v1h-1a1 1 0 0 0 0 2h1v1a1 1 0 0 0 2 0V6h1a1 1 0 0 0 0-2"/>
        </svg>
    `
    this.classList.add("hidden")
})


const maxChars = 1500

if (textArea.value.length > 0){
    document.querySelector("#charCounter").innerHTML = `${textArea.value.length}/${maxChars}`
}

textArea.addEventListener("input" , function () {
    if (textArea.value.length > maxChars){
        textarea.value = textarea.value.substring(0, maxChars);
    }
    document.querySelector("#charCounter").innerHTML = `${textArea.value.length}/${maxChars}`
})