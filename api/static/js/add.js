const emojiSelector = document.getElementById("emojiSelector")
const emojiSelectorBtn = document.getElementById("emojiSelectorBtn")
const emojiList = document.getElementById("emojiList")
const emojiSearch = document.getElementById("emojiSearch")

const textArea = document.querySelector("#textArea")

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
        });
        fileReader.readAsDataURL(file);
    }
});


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