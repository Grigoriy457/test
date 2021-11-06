function add_item() {
     document.querySelector(".computer .stop_word_section").appendChild(document.querySelector(".computer .pass_word_subtitle").cloneNode(true));
     document.querySelector(".mobile .stop_word_section").appendChild(document.querySelector(".mobile .pass_word_subtitle").cloneNode(true));
     spun_plus = document.getElementsByClassName("active_span")
     console.log(spun_plus)
     // spun_plus[0].classList.toggle("active_span");
     // spun_plus[0].classList.toggle("disactive_span");
}