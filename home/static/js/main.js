window.addEventListener("load", () => {

  // welcome notice
  const welNote = document.querySelector(".wel-notice");

  setTimeout(() => {
    welNote.classList.add("go");
  }, 1000);

  // making the navbar sticky
  const navbar = document.querySelector(".nav-wrapper");
  window.addEventListener("scroll", () => {
    navbar.classList.toggle("sticky", scrollY > 70);
  });
});
