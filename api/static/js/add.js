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
const textArea = document.querySelector("#text")

if (textArea.value.length > 0){
    document.querySelector("#charCounter").innerHTML = `${textArea.value.length}/${maxChars}`
}

textArea.addEventListener("input" , function () {
    if (textArea.value.length > maxChars){
        textarea.value = textarea.value.substring(0, maxChars);
    }
    document.querySelector("#charCounter").innerHTML = `${textArea.value.length}/${maxChars}`
})