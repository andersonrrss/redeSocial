const search_input = document.querySelector("#search_input");
const search_btn = document.querySelector("#search_btn");
const reset_btn = document.querySelector("#reset");
const results = document.querySelector("#results");

search_input.addEventListener("blur", function () {
  results.classList.remove("opacity-100");
  results.classList.add("opacity-0");
  setTimeout(() => {
    results.classList.add("hidden");
  }, 175)
});

search_input.addEventListener("input", function () {
  const query = search_input.value;
  if (!!query.length) {
    reset_btn.style.display = "block";
    fetch(`/getUsers?query=${query}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`erro ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        let html = "";
        data.forEach((element, index) => {
          if (index == 0) {
            html += `<a href="${element[1]}" class="w-full p-2 hover:bg-purple-50 transition-all duration-200"><span class="font-semibold">@</span> ${element[1]}</a> `;
          } else {
            html += `<a href="${element[1]}" class=" hover:bg-purple-50 w-full p-2 transition-all duration-200"><span class="font-semibold">@</span> ${element[1]}</a>`;
          }
        });
        results.classList.remove("hidden");
        results.classList.remove("opacity-0");
        results.classList.add("opacity-100");
        results.innerHTML = html;
      });
  } else {
    reset_btn.style.display = "none";
    showHistory()
  }

});

search_input.addEventListener("focus", showHistory);
function showHistory() {
  let history = JSON.parse(window.localStorage.getItem("searchHistory")) || [];
  let html = "";
  history.forEach((query, index) => {
    if(index == 0){
      html += `<a href="/search" class=" w-full p-2 hover:bg-purple-50 flex justify-between">
            <span>${query}</span> 
            <span place-self-end><i class="fa-solid fa-clock-rotate-left"></i></span>
        </a>`;
    } else{
      html += `<a href="/search" class=" w-full p-2 hover:bg-purple-50 flex justify-between ">
            <span>${query}</span> 
            <span place-self-end><i class="fa-solid fa-clock-rotate-left"></i></span>
        </a>`;
    }
  });
  results.classList.remove("hidden");
  results.classList.remove("opacity-0");
  results.classList.add("opacity-100");
  results.innerHTML = html;
}

search_btn.addEventListener("click", function () {
  if (search_input.value.length !== 0) {
    let history =
      JSON.parse(window.localStorage.getItem("searchHistory")) || [];

    if (!history.includes(search_input.value)) {
      history.push(search_input.value);
      if (history.length > 10) {
        history.shift();
      }
      localStorage.setItem("searchHistory", JSON.stringify(history));
    }
  }
});
