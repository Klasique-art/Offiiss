 // making the navbar sticky
 const navbar = document.querySelector(".nav-wrapper");
 window.addEventListener("scroll", () => {
   navbar.classList.toggle("sticky", scrollY > 70);
   if (window.scrollY > 0) {
     mobileNavItems.classList.remove("open");
     searchForm.classList.remove("open");
   }
 });
 
 // mobile nav
 const mobileNavBtn = document.querySelector(".mobile-nav .menu-btn");
 const mobileNavItems = document.querySelector(".mobile-nav .nav-items");

 mobileNavBtn.addEventListener("click", () => {
     mobileNavItems.classList.toggle("open")
 });

 //   search btn to reaveal search input
 const searchOpenBtn = document.querySelector(".search-open-btn");
 const searchForm = document.querySelector(".search-form");

 searchOpenBtn.addEventListener("click", () => {
   searchForm.classList.toggle("open");
 });

