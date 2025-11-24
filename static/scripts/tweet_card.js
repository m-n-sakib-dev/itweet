console.log(current_user);
function likefunction(link_url, reaction) {
        csrftoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        fetch(link_url, {
                method: "POST",
                headers: {
                        "X-Requested-With": "XMLHttpRequest",
                        "X-CSRFToken": csrftoken,
                },
        })
                .then((response) => response.json())
                .then((data) => {
                        console.log(reaction);
                        document.getElementById("_" + data.tweet_id + "_like").textContent = data.like_count;
                        document.getElementById("_" + data.tweet_id + "_unlike").textContent = data.unlike_count;
                });
}
function toggleSeeMore(button) {
        const tweetText = button.previousElementSibling;
        // const tweetText = button.parentElement;
        if (tweetText.classList.contains("expanded")) {
                // Collapse
                tweetText.classList.remove("expanded");
                button.textContent = "See more";
        } else {
                // Expand
                tweetText.classList.add("expanded");
                button.textContent = "See less";
        }
}
// Automatically show "See more" only for long content
function initSeeMoreButtons() {
        document.querySelectorAll(".tweet-text").forEach((tweetText) => {
                // Check if text exceeds 3 lines
                if (tweetText.scrollHeight > tweetText.clientHeight) {
                        // Show the button
                        tweetText.nextElementSibling.style.display = "block";
                } else {
                        // Hide the button
                        tweetText.nextElementSibling.style.display = "none";
                }
        });
}

// Call on page load
document.addEventListener("DOMContentLoaded", initSeeMoreButtons);

function tempcommentList() {
        console.log("funtion called");
        return;
}

//funtion to fill the tweet card template
// function fillTweetTemplate(tweetData) {
//         // Get the template
//         const template = document.getElementById("tweet-card-template");
//         const clone = template.content.cloneNode(true);

//         // Fill basic data
//         clone.querySelector(".tweet_card h6").textContent = tweetData.user.username;
//         clone.querySelector(".tweet-card-upload-time").textContent = tweetData.created_at;
//         clone.querySelector(".tweet-card-text").textContent = tweetData.text;

//         // Profile image
//         const profileImg = clone.querySelector(".tweet_profile_img_cls");
//         // profileImg.src = tweetData.profile_image;

//         // Tweet image
//         if (tweetData.photo) {
//                 const tweetImg = clone.querySelector(".tweet_card_image");
//                 tweetImg.src = tweetData.photo.url;
//         } else {
//                 clone.querySelector(".tweet_card_image_container").style.display = "none";
//         }

//         // Reaction counts
//         clone.querySelector(".like_count").textContent = tweetData.like_count;
//         clone.querySelector(".unlike_count").textContent = tweetData.unlike_count;
//         clone.querySelector(".comment_count").textContent = tweetData.comment_count;

//         // Set up reaction buttons with original function names
//         const likeBtn = clone.querySelector('.reaction_btn[onclick*="like"]');
//         const unlikeBtn = clone.querySelector('.reaction_btn[onclick*="unlike"]');
//         const commentBtn = clone.querySelector('.icon-btn[onclick*="tempcommentList"]');

//         // Update like function call
//         likeBtn.setAttribute("onclick", `likefunction('/interaction/${tweetData.id}/reaction/like','like')`);
//         likeBtn.querySelector("i").id = `like_${tweetData.id}`;
//         likeBtn.nextElementSibling.id = `_${tweetData.id}`;

//         // Update unlike function call
//         unlikeBtn.setAttribute("onclick", `likefunction('/interaction/${tweetData.id}/reaction/unlike', 'unlike')`);
//         unlikeBtn.querySelector("i").id = `unlike_${tweetData.id}`;
//         unlikeBtn.nextElementSibling.id = `_${tweetData.id}`;

//         // Update comment function call
//         commentBtn.setAttribute("data-bs-target", `#exampleModal${tweetData.id}`);
//         commentBtn.nextElementSibling.id = `_${tweetData.id}`;

//         // Set up modal
//         const modal = clone.querySelector(".modal");
//         modal.id = `exampleModal${tweetData.id}`;
//         const modal_content = modal.querySelector(".modal-content");
//         modal_content.appendChild(fillPostDetailsTemplate(tweetData));
//         commentBtn.setAttribute("onclick", `commentList(${tweetData.id})`);
//         return clone;
// }

function loadTweets(user_id) {
        tweet_container = document.getElementById("tweet_feed_container");
        fetch(`/user/profile/tweets?user_id=${user_id}`)
                .then((response) => response.json())
                .then((data) => {
                        if (data.success) {
                                data.tweets.forEach((tweet) => {
                                        clone = fillTweetTemplate(tweet);
                                        tweet_container.appendChild(clone);
                                });
                        }
                })
                .then(() => {
                        initSeeMoreButtons();
                });
}

function fillPostDetailsTemplate(postData) {
        // Get the template
        const template = document.getElementById("post-details-template");
        const clone = template.content.cloneNode(true);

        // Fill basic data
        clone.querySelector(".post-username").textContent = postData.user.username + "'s Post";
        clone.querySelector(".post-text").textContent = postData.text;

        // Tweet image
        if (postData.photo && postData.photo.url) {
                const tweetImg = clone.querySelector(".tweet_card_image");
                tweetImg.src = postData.photo.url;
        } else {
                clone.querySelector(".tweet_card_image_container").style.display = "none";
        }

        // Reaction counts
        clone.querySelector(".like_count").textContent = postData.like_count || 0;
        clone.querySelector(".unlike_count").textContent = postData.unlike_count || 0;
        clone.querySelector(".comment_count_post-details").textContent = postData.comment_count || 0;

        // Set IDs for dynamic targeting
        const likeCount = clone.querySelector(".like_count");
        const unlikeCount = clone.querySelector(".unlike_count");
        const commentCount = clone.querySelector(".comment_count_post-details");
        const commentList = clone.querySelector(".comment_list");

        likeCount.id = `_${postData.id}`;
        unlikeCount.id = `_${postData.id}`;
        commentCount.id = `_${postData.id}`;
        commentList.id = `comment_list_${postData.id}`;

        return clone;
}

function fillTweetTemplate(tweetData) {
        const template = document.getElementById("tweet-card-template");
        const clone = template.content.cloneNode(true);

        const tweetCard = clone.querySelector(".tweet-card");
        tweetCard.id = "tweet-card-" + tweetData.id;
        tweetCard.setAttribute("data-tweet-id", tweetData.id);
        tweetCard.setAttribute("data-full-text", tweetData.text);

        // Fill user data
        clone.querySelector(".username").textContent = tweetData.author.name;
        clone.querySelector(".user-handle").textContent = `@${tweetData.user.username}`;
        clone.querySelector(".timestamp").textContent = tweetData.created_at;

        //menu button feature
        const dropdown_menu = clone.querySelector(".dropdown-menu");
        if (tweetData.user.username == current_user.username) {
                //adding edit button
                menu_btn = document.createElement("li");
                menu_btn.innerHTML = `
                        <a class="dropdown-item tweet-menu-edit"  href="/tweet_edit/${tweetData.id}"><i class="bi bi-pencil-square me-1"></i>Edit</a>
                `;
                dropdown_menu.appendChild(menu_btn);
                //adding delete button and its confirmation modal

                menu_btn = document.createElement("li");
                menu_btn.innerHTML = `
                        <a class="dropdown-item tweet-menu-delete" data-tweet-id="${tweetData.id}"><i class="bi bi-trash me-1"></i>Delete</a>
                `;
                dropdown_menu.appendChild(menu_btn);
        }
        if (current_user.username) {
                menu_btn = document.createElement("li");
                menu_btn.innerHTML = `
                <a class="dropdown-item tweet-menu-save" data-tweet-id="${tweetData.id}" ><i class="bi bi-bookmark${
                        tweetData.is_saved ? "-x" : ""
                } me-1"></i><span class="text">${tweetData.is_saved ? "Unsave" : "Save"}</span></a>
                `;
                dropdown_menu.appendChild(menu_btn);
        }
        menu_btn = document.createElement("li");
        menu_btn.innerHTML = `
                <a class="dropdown-item tweet-menu-copylink" data-tweet-id="${tweetData.id}" ><i class="bi bi-clipboard me-1"></i>Copy Link</a>
        `;
        dropdown_menu.appendChild(menu_btn);

        // Fill tweet content
        if (tweetData.text) {
                const tweetText = clone.querySelector(".tweet-text");
                tweetText.textContent = tweetData.text;
        }

        // Profile image
        const profileImg = clone.querySelector(".user-avatar");
        profileImg.src = tweetData.author.profile_picture_url;

        // Tweet image - Fixed height
        if (tweetData.photo) {
                const tweetMedia = clone.querySelector(".tweet-media");
                const tweetImg = clone.querySelector(".media-image");
                tweetImg.src = tweetData.photo.url;
                tweetMedia.style.display = "block";

                // Set fixed height
                tweetMedia.style.height = "65vh";
                tweetMedia.style.maxHeight = "65vh";
        }

        // Reaction counts
        clone.querySelector(".likes-count").textContent = tweetData.like_count;
        clone.querySelector(".dislikes-count").textContent = tweetData.unlike_count;
        clone.querySelector(".comments-count").textContent = tweetData.comment_count;

        // Set up action buttons with proper event listeners
        const likeBtn = clone.querySelector(".like-btn");
        const dislikeBtn = clone.querySelector(".dislike-btn");
        const commentBtn = clone.querySelector(".comment-btn");

        //Set up users reaction on the tweet
        switch (tweetData.reaction) {
                case "like":
                        likeBtn.classList.add("active");
                        break;
                case "unlike":
                        dislikeBtn.classList.add("active");
        }

        // Set IDs for reaction tracking
        likeBtn.id = `like_btn_${tweetData.id}`;
        dislikeBtn.id = `dislike_btn_${tweetData.id}`;
        clone.querySelector(".likes-count").id = `_${tweetData.id}_like`;
        clone.querySelector(".dislikes-count").id = `_${tweetData.id}_unlike`;
        clone.querySelector(".comments-count").id = `_${tweetData.id}_comment`;

        // Set up modal for comments
        const modal = clone.querySelector(".tweet-modal");
        // modal.id = `tweetModal${tweetData.id}`;
        // commentBtn.setAttribute("data-bs-target", `#tweetModal${tweetData.id}`);
        modal.id = `exampleModal${tweetData.id}`;
        commentBtn.setAttribute("data-bs-target", `#exampleModal${tweetData.id}`);
        const modal_content = modal.querySelector(".modal-content");
        modal_content.appendChild(fillPostDetailsTemplate(tweetData));
        commentBtn.setAttribute("onclick", `commentList(${tweetData.id})`);

        // Return the clone - event listeners will be attached globally
        return clone;
}

// Global event listeners for buttons
document.addEventListener("click", function (e) {
        // Read more functionality
        if (e.target.classList.contains("read-more-btn")) {
                const tweetCard = e.target.closest(".tweet-card");
                const tweetText = tweetCard.querySelector(".tweet-text");
                const fullText = tweetCard.getAttribute("data-full-text");

                if (tweetText.textContent.length < fullText.length) {
                        tweetText.textContent = fullText;
                        e.target.textContent = "Show less";
                } else {
                        tweetText.textContent = fullText.substring(0, 120) + "...";
                        e.target.textContent = "Read more";
                }
        }

        // Like button functionality
        if (e.target.closest(".like-btn")) {
                const tweetCard = e.target.closest(".tweet-card");
                const tweetId = tweetCard.getAttribute("data-tweet-id");
                const likeBtn = tweetCard.querySelector(".like-btn");
                const dislikeBtn = tweetCard.querySelector(".dislike-btn");
                const likeCount = tweetCard.querySelector(".likes-count");
                const dislikeCount = tweetCard.querySelector(".dislikes-count");

                // Call your existing likefunction
                likefunction(`/interaction/${tweetId}/reaction/like`, "like");

                // Visual feedback
                if (likeBtn.classList.contains("active")) {
                        likeBtn.classList.remove("active");
                } else {
                        likeBtn.classList.add("active");
                }
                dislikeBtn.classList.remove("active");
        }

        // Dislike button functionality
        if (e.target.closest(".dislike-btn")) {
                const tweetCard = e.target.closest(".tweet-card");
                const tweetId = tweetCard.getAttribute("data-tweet-id");
                const likeBtn = tweetCard.querySelector(".like-btn");
                const dislikeBtn = tweetCard.querySelector(".dislike-btn");
                const likeCount = tweetCard.querySelector(".likes-count");
                const dislikeCount = tweetCard.querySelector(".dislikes-count");

                // Call your existing likefunction
                likefunction(`/interaction/${tweetId}/reaction/unlike`, "unlike");

                // Visual feedback
                if (dislikeBtn.classList.contains("active")) {
                        dislikeBtn.classList.remove("active");
                } else {
                        dislikeBtn.classList.add("active");
                }
                likeBtn.classList.remove("active");
        }

        //menu options functionality
        if (e.target.classList.contains("tweet-menu-delete")) {
                const tweetId = e.target.dataset.tweetId;
                const modalId = `delete-confirm-modal-${tweetId}`;

                let modal = document.getElementById(modalId);

                if (!modal) {
                        const modal_template = document.getElementById("confirm-modal-template");
                        const modal_clone = modal_template.content.cloneNode(true);
                        const modalElement = modal_clone.querySelector(".modal");
                        modalElement.id = modalId;
                        modalElement.querySelector(".confirm-tweet-delete-btn").dataset.tweetId = tweetId;
                        document.body.appendChild(modal_clone);
                        modal = document.getElementById(modalId);
                }

                const modalInstance = new bootstrap.Modal(modal);
                modalInstance.show();
        }
        if (e.target.classList.contains("tweet-menu-save")) {
                const tweetId = e.target.dataset.tweetId;
                console.log(tweetId);
                csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
                fetch(`/user/tweet/${tweetId}/save`, {
                        method: "POST",
                        headers: {
                                "X-Requested-With": "XMLHttpRequest",
                                "X-CSRFToken": csrf_token,
                        },
                })
                        .then((response) => response.json())
                        .then((data) => {
                                if (data.success) {
                                        console.log(data.message);
                                        icon = e.target.querySelector(".bi");
                                        text = e.target.querySelector(".text");
                                        if (data.message == "Tweet saved") {
                                                icon.classList.remove("bi-bookmark");
                                                icon.classList.add("bi-bookmark-x");
                                                text.textContent = "Unsave";
                                        } else {
                                                icon.classList.remove("bi-bookmark-x");
                                                icon.classList.add("bi-bookmark");
                                                text.textContent = "Save";
                                        }
                                } else {
                                        console.error(data.error);
                                }
                        });
        }
        if (e.target.classList.contains("confirm-tweet-delete-btn")) {
                console.log("confirm-tweet-delete-btn clicked");
                const tweetId = e.target.dataset.tweetId;
                console.log(tweetId);
                csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
                fetch(`/tweet_delete/${tweetId}`, {
                        method: "POST",
                        headers: {
                                "X-Requested-With": "XMLHttpRequest",
                                "X-CSRFToken": csrf_token,
                        },
                })
                        .then((response) => response.json())
                        .then((data) => {
                                if (data.success) {
                                        elementToRemove = document.getElementById("tweet-card-" + tweetId);
                                        if (elementToRemove) {
                                                elementToRemove.remove();
                                        }
                                        elementToRemove = document.getElementById(`delete-confirm-modal-${tweetId}`);
                                        if (elementToRemove) {
                                                elementToRemove.remove();
                                        }
                                }
                        });
        }
});
