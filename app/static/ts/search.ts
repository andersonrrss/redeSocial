const search_input = document.querySelector("#search_input") as HTMLInputElement;
const search_btn = document.querySelector("#search_btn") as HTMLButtonElement;
const reset_btn = document.querySelector("#reset") as HTMLButtonElement;
const results = document.querySelector("#results") as Element;

function fetchQuery(query : string){
  fetch(`/search_users?query=${query}`)
  .then((response) => {
    if (!response.ok) {
      throw new Error(`erro ${response.status}`);
    }
    return response.json();
  })
  .then((data) => {
    let html = "";
    if (data.length == 0){
      html = `<span class=" hover:bg-purple-50 w-full p-2 transition-all duration-200">
                <span class="font-semibold">Nenhum resultado encontrado :/</span> 
              </span>`;
    } else{
      html = data.map((element: string) => `
        <a href="/${element}" class="hover:bg-purple-50 w-full p-2 transition-all duration-200">
          <span class="font-semibold">@</span> ${element}
        </a>
      `).join('');
    }
    
    results.classList.remove("hidden");
    results.classList.remove("opacity-0");
    results.classList.add("opacity-100");
    results.innerHTML = html;
  })
  .catch((error) => {
    console.error("Erro ao carregar usuários:", error);
    results.innerHTML = "<span>Erro ao carregar resultados.</span>";
  });
}

search_input.addEventListener("blur", function () {
  results.classList.remove("opacity-100");
  results.classList.add("opacity-0");
  setTimeout(() => {
    results.classList.add("hidden");
  }, 175);
})

search_input.addEventListener("input", () => {
  const query = search_input.value;
  reset_btn.style.display = query.length ? "block" : "none";

  if (query.length) {
    fetchQuery(query);
  } else {
    showHistory();
  }
});

search_input.addEventListener("focus", showHistory);

function showHistory() {
  const history = JSON.parse(window.localStorage.getItem("searchHistory") || "[]");
  const html = history.map((query: string) => `
    <a href="/search" class="w-full p-2 hover:bg-purple-50 flex justify-between">
      <span>${query}</span>
      <span place-self-end><i class="fa-solid fa-clock-rotate-left"></i></span>
    </a>
  `).join('');

  results.classList.remove("hidden", "opacity-0");
  results.classList.add("opacity-100");
  results.innerHTML = html;
}

search_btn.addEventListener("click", function () {
  if (search_input.value.length !== 0) {
    let history = JSON.parse(
      window.localStorage.getItem("searchHistory") || "[]"
    );

    if (!history.includes(search_input.value)) {
      history.push(search_input.value);
      if (history.length > 10) {
        history.shift();
      }
      localStorage.setItem("searchHistory", JSON.stringify(history));
    }
  }
});

search_btn.addEventListener("mouseover", function () {
  const paths = search_btn.querySelector("path") as SVGPathElement;
  paths.setAttribute("stroke", "#7101d3");
});

search_btn.addEventListener("mouseout", function () {
  const paths = search_btn.querySelector("path") as SVGPathElement;
  paths.setAttribute("stroke", "black");
});
