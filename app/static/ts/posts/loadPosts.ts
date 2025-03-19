import { checkTextLength, fullScreen, likePost, showComments } from "./post.js";

let currentPage = 1;
let loading = false;

type Context = "user_posts" | "feed"

document.addEventListener("DOMContentLoaded", function(){
    let postContainer = document.getElementById("posts-container")
    if (!postContainer){
        return
    }
    loadPosts(postContainer)
    // Adiciona o listener para o scroll
    window.addEventListener("scroll", () => {
        // Checa se o usuário chegou perto do final da página
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 500 && !loading) {
            loadPosts(postContainer);
        }
    });
})

function renderizePosts(data: any, postContainer: any){
    postContainer = postContainer as HTMLElement
    if (data.posts.length < 1) {
        postContainer.classList.add("flex", "justify-center", "items-center", "mt-20")
        postContainer.innerHTML = "<span>Nenhum post aqui ainda...</span>"
        return;
    }
    data.posts.forEach((postHtml : any) => {
        postContainer.insertAdjacentHTML("beforeend", postHtml);
    });
    const posts = document.querySelectorAll(".post") as NodeListOf<HTMLDivElement>
    posts.forEach(post => {
        checkTextLength(post)

        const likeButton = post.querySelector(".likeButton") as HTMLButtonElement
        if(likeButton){
            likeButton.addEventListener("click", function(){
                likePost(likeButton)
            })
        }

        const fullScreenButton = post.querySelector(".fullScreenBtn") as HTMLButtonElement
        if(fullScreenButton){
            fullScreenButton.addEventListener("click", function(){
                fullScreen(fullScreenButton)
            })
        }

        const commentButton = post.querySelector(".commentButton") as HTMLButtonElement
        if(commentButton){
            commentButton.addEventListener("click", function(){
                showComments(commentButton)
            })
        }
    })
    // Se houver mais posts, incrementa a página
    if (data.has_next) {
        currentPage++;
        loading = false;
    } else {
        // Não há mais posts para carregar
        loading = true;
    }
}

function loadPosts(postContainer : any) {
    if (loading) return;
    loading = true;
    postContainer = postContainer as HTMLElement
    const username = postContainer.getAttribute("username") as string
    const context : Context = postContainer.getAttribute("context")

    fetch(`/loadPosts?page=${currentPage}&username=${username}&context=${context}`)
    .then(response => response.json())
    .then(data => {
        if(data.error){
            alert(data.error)
            return;
        }
        renderizePosts(data, postContainer)
    })
    .catch(error => {
        console.error("Erro ao carregar posts:", error);
        loading = false;
    });
}



