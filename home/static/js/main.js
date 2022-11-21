// loader
const loader = document.querySelector(".loader");
window.addEventListener("load", () => {
  loader.style.display = "none";
  // swiper init
  var swiper = new Swiper(".slide-content", {
    slidesPerView: 3,
    spaceBetween: 20,
    loop: true,
    centerSlide: "true",
    fade: "true",
    grabCursor: "true",
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
      dynamicBullets: true,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    breakpoints: {
      0: {
        slidesPerView: 1,
      },
      768: {
        slidesPerView: 2,
      },
      991: {
        slidesPerView: 3,
      },
    },
  });

  // aos initialisation
  AOS.init({
    offset: 50,
    delay: 100,
    duration: 800,
    easing: "ease",
    once: false,
    mirror: false,
    anchorPlacement: "top-bottom",
  });

  // welcome notice
  const welNote = document.querySelector(".wel-notice");

  setTimeout(() => {
    welNote.classList.add("go");
  }, 1000);

  //the demo video functionality
  const videoBox = document.querySelector("#demo .video-box");
  const video = document.querySelector("#demo video");
  const playBtn = document.querySelector("#demo .play-btn");
  const overlay = document.querySelector("#demo .vid-overlay");


  playBtn.addEventListener("click", () => {
    const hasPlay = playBtn.classList.contains("play");
    if (hasPlay) {
      playVid();
      videoBox.addEventListener("mouseenter", ()=>{
        overlay.classList.remove("leave")
      })
      videoBox.addEventListener("mouseleave", ()=>{
        overlay.classList.remove("show")
        overlay.classList.add("leave")

      })
    } else {
      pauseVid();
      videoBox.addEventListener("mouseleave", ()=>{
        overlay.classList.remove("leave")
        overlay.classList.add("show")
      })
    }
  });

  
  function playVid() {
    video.play();
    playBtn.innerHTML = `<i class="fas fa-pause"></i>`;
    playBtn.classList.remove("play");
    overlay.style.backgroundColor = "rgba(65, 105, 225,.1)";
  }
  function pauseVid() {
    video.pause();
    playBtn.innerHTML = `<i class="fas fa-play"></i>`;
    playBtn.classList.add("play");
    overlay.style.backgroundColor = "rgba(65, 105, 225,.5)";
  }

});