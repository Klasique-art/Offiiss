window.addEventListener("load", ()=>{
    // welcome notice
    const welNote = document.querySelector(".wel-notice")

    setTimeout(() => {
        welNote.classList.add("go")
    }, 2000);
})