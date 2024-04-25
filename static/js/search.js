const user_search = document.querySelector("#user_search")
const search_btn = document.querySelector("#search_btn")
const results = document.querySelector("#results")

user_search.addEventListener("input", function(){
    const query = user_search.value
    results.innerHTML = ""
    fetch(`/getUsers?query=${query}`)
        .then((response) => {
            if (!response.ok){
                throw new Error(`erro ${response.status}`)
            }
            return response.json()
        })
        .then((data) => {
            let html = ""
            data.forEach(element => {
                html += `<a href="${element[1]}" class="border-t border-gray-100 w-full p-1 hover:bg-gray-200">@${element[1]}</a>`        
            });
            console.log(data)
            results.innerHTML = html
        })
})