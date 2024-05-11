const search_input = document.querySelector("#search_input");
const search_btn = document.querySelector("#search_btn");
const reset_btn = document.querySelector("#reset")
const results = document.querySelector("#results");

search_input.addEventListener("input", function () {
  const query = search_input.value;
  if(!!query.length){
    reset_btn.style.display = "block"
    fetch(`/getUsers?query=${query}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`erro ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      let html = "";
      data.forEach((element) => {
        html += `<a href="${element[1]}" class="border-t border-gray-100 w-full p-1 hover:bg-gray-200">@${element[1]}</a>`;
      });
      results.innerHTML = html;
    });
  } else {
    reset_btn.style.display = "none"
  }
  results.innerHTML = "";
});

search_input.addEventListener("focus", function () {
  let history = JSON.parse(window.localStorage.getItem("searchHistory")) || [];
  let html = "";
  history.forEach((query) => {
    html += `<a href="/search" class=" w-full p-1 hover:bg-gray-200 flex justify-between">
            <span>${query}</span>
            <span place-self-end><i class="fa-solid fa-clock-rotate-left"></i></span>
        </a>`;
  });
  results.innerHTML = html;
});

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