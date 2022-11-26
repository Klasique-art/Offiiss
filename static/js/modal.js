window.addEventListener("load", () => {
  // footer links modals
  const faq = document.querySelector("#faq");
  const terms = document.querySelector("#terms");
  const privacy = document.querySelector("#privacy");
  const faqContainer = document.querySelector(".faq-container");
  const termsContainer = document.querySelector(".terms-container");
  const privacyContainer = document.querySelector(".privacy-container");
  const faqCloseBtn = document.querySelector(".faq-container .close-btn");
  const termsCloseBtn = document.querySelector(".terms-container .close-btn");
  const privacyCloseBtn = document.querySelector(".privacy-container .close-btn");

  faq.addEventListener("click", showFaq);
  terms.addEventListener("click", showTerms);
  privacy.addEventListener("click", showPrivacy);

  faqCloseBtn.addEventListener("click", closeFaq)
  termsCloseBtn.addEventListener("click", closeTerms)
  privacyCloseBtn.addEventListener("click", closePrivacy)

  function showFaq() {
    faqContainer.classList.add("show")
  }
  function showTerms() {
    termsContainer.classList.add("show")
  }
  function showPrivacy() {
    privacyContainer.classList.add("show")
  }

  function closeFaq() {
    faqContainer.classList.remove("show")
  }
  function closeTerms() {
    termsContainer.classList.remove("show")
  }
  function closePrivacy() {
    privacyContainer.classList.remove("show")
  }

  // faq accordion

  const title = document.querySelectorAll(".accordion-box")

  title.forEach((heading)=>{
      const accordBtn = heading.querySelector(".acc-btn")
      accordBtn.addEventListener("click", ()=>{
          title.forEach((item)=>{
              item.classList.toggle("show-text")
              if(item !== heading){
                  item.classList.remove("show-text")
              }
          })
      })

})

});
