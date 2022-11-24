window.addEventListener("load", () => { 

  // comment
  const commentBox = document.querySelector("#comment");
  const toggleCommentBtn = document.querySelector(".comment-btn");

  toggleCommentBtn.addEventListener("click", () => {
    commentBox.classList.toggle("active");
    if (commentBox.classList.contains("active")) {
      toggleCommentBtn.textContent = "close";
    } else {
      toggleCommentBtn.textContent = "Open";
    }
  });

  // comment alert
  const commentAlert = document.querySelector(".comment-msg")

  setTimeout(() => {
    commentAlert.classList.add("go")
  }, 4000);

  // fetching api to the comment section and display every comment

    let comPage = 1;
    let post_id = $("#like-btn").attr("data-catid")

    //   the next and prev buttons in comment
    const prevComBtn = document.querySelector(".com-prev");
    const nextComBtn = document.querySelector(".com-next");

    // function to check if the commment can be paginated or not
    // function paginateCheck(){}

    nextComBtn.addEventListener("click", () => {
      comPage++;
      fetchData(comPage);
    });
    prevComBtn.addEventListener("click", () => {
      if(comPage > 0){comPage--}
        fetchData(comPage);

    });

    function fetchData(page=1) {
      fetch(`http://localhost:8000/comment/?page=${page}&&post_id=${post_id}`)
        .then((response) => {
          // check if there is no error in the response and return it
          if (!response.ok) {
            throw Error("ERROR! There was an error opening URL.");
          }
          return response.json();
        })
        .then((data) => {

          // if the comment page doesn't have previous page or next page, disable the navigation buttons
          const pageInfo = data[data.length - 1].pagination_info
          if(pageInfo.has_next === false) {
             $("#next").prop("disabled", true)
             nextComBtn.classList.add("disable")
          }else if (pageInfo.has_next === true) {
              $("#next").prop("disabled", false)
             nextComBtn.classList.remove("disable")
          }
          if(pageInfo.has_prev === false) {
              $("#prev").prop("disabled", true)
             prevComBtn.classList.add("disable")
          }else if (pageInfo.has_prev === true) {
              $("#prev").prop("disabled", false)
             prevComBtn.classList.remove("disable")
          }
          const commentContCont = document.querySelector(".com-con-cont");

          // loop through the comments array and return each user and details on the webpage
          const commentArr = data
          .map((user) => {
              if (user.content == undefined) {
                return;
              }
              const userDate = new Date(user.date).toDateString();
              return `
              <div class="comment-user" tabindex="0">
                  <div class="name-date-wrapper">
                      <p>${user.name}</p>
                      <p>
                        <time class="timeago" datetime="${userDate}">${userDate}</time>
                      </p>
                  </div>
                  <div class="message-box">
                      <p>${user.content}</p>
                  </div>
              </div>
              `;
            })
            .join("");
          commentContCont.innerHTML = commentArr;
        })
        .catch((error) => {
          alert("Error!", error.message);
        });
    }
    fetchData();
  // // end of fetch data

  
});
