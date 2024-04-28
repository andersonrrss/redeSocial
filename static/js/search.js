const user_search = document.querySelector("#user_search");
const search_btn = document.querySelector("#search_btn");
const results = document.querySelector("#results");

user_search.addEventListener("input", function () {
  const query = user_search.value;
  results.innerHTML = "";
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
});

user_search.addEventListener("focus", function () {
  let history = JSON.parse(window.localStorage.getItem("searchHistory")) || [];
  let html = "";
  history.forEach((query) => {
    html += `<a href="/search" class="border-t border-gray-100 w-full p-1 hover:bg-gray-200 flex justify-between">
            <span>${query}</span>
            <span place-self-end><i class="fa-solid fa-clock-rotate-left"></i></span>
        </a>`;
  });
  results.innerHTML = html;
});

search_btn.addEventListener("click", function () {
  if (user_search.value.length !== 0) {
    let history =
      JSON.parse(window.localStorage.getItem("searchHistory")) || [];

    if (!history.includes(user_search.value)) {
      history.push(user_search.value);
      if (history.length > 10) {
        history.shift();
      }
      localStorage.setItem("searchHistory", JSON.stringify(history));
    }
  }
});
