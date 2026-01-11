console.log(current_user);
function likefunction(link_url, reaction) {
        csrftoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        return fetch(link_url, {
                method: "POST",
                headers: {
                        "X-Requested-With": "XMLHttpRequest",
                        "X-CSRFToken": csrftoken,
                },
        })
                .then((response) => response.json())
                .then((data) => {
                        document.getElementById("_" + data.tweet_id + "_like").textContent = data.like_count;
                        document.getElementById("_" + data.tweet_id + "_unlike").textContent = data.unlike_count;
                        return {
                                like_count: data.like_count,
                                unlike_count: data.unlike_count,
                        };
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

//new post details modal, its using currently
function loadPostDetail(tweetData) {
        const template = document.getElementById("post-details-template");
        const clone = template.content.cloneNode(true);

        const tweetCard = clone.querySelector(".tweet-card");
        tweetCard.id = "tweet-card-" + tweetData.id;
        tweetCard.setAttribute("data-tweet-id", tweetData.id);
        tweetCard.setAttribute("data-full-text", tweetData.text);

        // Profile image
        const profileImg = clone.querySelector(".user-avatar");
        profileImg.src = tweetData.user.profile.profile_picture;

        // Fill user data
        clone.querySelector(".username").textContent = tweetData.user.profile.name;
        clone.querySelector(".user-handle").textContent = `${tweetData.user.username}`;
        clone.querySelector(".timestamp").textContent = tweetData.created_at;

        //setting url on username, user profile pic and name
        clone.querySelectorAll(".user_profile_link").forEach((profile_link) => {
                profile_link.setAttribute("href", `/user/profile/${tweetData.user.id}`);
        });

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
                tweetText.innerHTML = `${tweetData.text}`;
        }

        // Tweet image - Fixed height
        if (tweetData.photo) {
                const tweetMedia = clone.querySelector(".tweet-media");
                const tweetImg = clone.querySelector(".media-image");
                tweetImg.src = tweetData.photo.url;
                tweetMedia.style.display = "block";
        }
        // In retweets aading the parent tweets content in a tweet-card
        if (tweetData.parent != null) {
                parent_tweet_container = clone.querySelector(".parent_tweet");
                parent_tweet_container.appendChild(parentTweet(tweetData.parent));
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
                        break;
        }

        // Set IDs for reaction tracking
        likeBtn.id = `like_btn_${tweetData.id}`;
        dislikeBtn.id = `dislike_btn_${tweetData.id}`;

        // Return the clone - event listeners will be attached globally
        return clone;
}

// Parent tweet showing tweet card in retweets
function parentTweet(tweetData) {
        const template = document.getElementById("tweet-card-template");
        const clone = template.content.querySelector(".tweet_info").cloneNode(true);

        clone.classList.add("tweet-card");
        const tweetCard = clone;
        tweetCard.setAttribute("data-tweet-id", tweetData.id);
        tweetCard.setAttribute("data-full-text", tweetData.text);

        // Profile image
        const profileImg = clone.querySelector(".user-avatar");
        profileImg.src = tweetData.user.profile.profile_picture;

        // Fill user data
        clone.querySelector(".username").textContent = tweetData.user.profile.name;
        clone.querySelector(".user-handle").textContent = `${tweetData.user.username}`;
        clone.querySelector(".timestamp").textContent = tweetData.created_at;

        //setting url on username, user profile pic and name
        clone.querySelectorAll(".user_profile_link").forEach((profile_link) => {
                profile_link.setAttribute("href", `/user/profile/${tweetData.user.id}`);
        });

        //menu button feature
        const dropdown_menu = clone.querySelector(".tweet-card-menu-dropdown");
        dropdown_menu.classList.add("d-none");

        // Fill tweet content
        if (tweetData.text) {
                const tweetText = clone.querySelector(".tweet-text");
                tweetText.innerHTML = `${tweetData.text}`;
        }

        // Tweet image - Fixed height
        if (tweetData.photo) {
                const tweetMedia = clone.querySelector(".tweet-media");
                const tweetImg = clone.querySelector(".media-image");
                tweetImg.src = tweetData.photo.url;
                tweetMedia.style.display = "block";
        }
        return clone;
}

// this tweet card is currently using
function newTweetCard(tweetData) {
        const template = document.getElementById("tweet-card-template");
        const clone = template.content.cloneNode(true);

        const tweetCard = clone.querySelector(".tweet-card");
        tweetCard.id = "tweet-card-" + tweetData.id;
        tweetCard.setAttribute("data-tweet-id", tweetData.id);
        tweetCard.setAttribute("data-full-text", tweetData.text);

        // Profile image
        const profileImg = clone.querySelector(".user-avatar");
        profileImg.src = tweetData.user.profile.profile_picture;

        // Fill user data
        clone.querySelector(".username").textContent = tweetData.user.profile.name;
        clone.querySelector(".user-handle").textContent = `${tweetData.user.username}`;
        clone.querySelector(".timestamp").textContent = tweetData.created_at;

        //setting url on username, user profile pic and name
        clone.querySelectorAll(".user_profile_link").forEach((profile_link) => {
                profile_link.setAttribute("href", `/user/profile/${tweetData.user.id}`);
        });

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
                tweetText.innerHTML = `${tweetData.text}`;
        }
        // In retweets aading the parent tweets content in a tweet-card
        if (tweetData.parent != null) {
                parent_tweet_container = clone.querySelector(".parent_tweet");
                parent_tweet_container.appendChild(parentTweet(tweetData.parent));
        }

        // Tweet image - Fixed height
        if (tweetData.photo) {
                const tweetMedia = clone.querySelector(".tweet-media");
                const tweetImg = clone.querySelector(".media-image");
                tweetImg.src = tweetData.photo.url;
                tweetMedia.style.display = "block";
        }

        // Reaction counts
        clone.querySelector(".likes-count").textContent = tweetData.like_count;
        clone.querySelector(".dislikes-count").textContent = tweetData.unlike_count;
        clone.querySelector(".comments-count").textContent = tweetData.comment_count;

        // Set up action buttons with proper event listeners
        const likeBtn = clone.querySelector(".like-btn");
        const dislikeBtn = clone.querySelector(".dislike-btn");
        const commentBtn = clone.querySelector(".comment-btn");
        const shareBtn = clone.querySelector(".share-btn");

        // calling sharemodalfunction to open a tweet share from
        shareBtn.setAttribute("onclick", `createShareModal(${tweetData.id})`);

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
        modal.querySelector(".modal-title").textContent = `${tweetData.user.profile.name}'s Tweet`;
        const modal_tweet_data = modal.querySelector(".modal_tweet_data");
        modal_tweet_data.appendChild(loadPostDetail(tweetData));
        modal.querySelector(".comment_list").id = `comment_list_${tweetData.id}`;
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
                likefunction(`/interaction/${tweetId}/reaction/like`, "like").then((data) => {
                        likeCount.innerHTML = data.like_count;
                        dislikeCount.innerHTML = data.unlike_count;
                });

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
                likefunction(`/interaction/${tweetId}/reaction/unlike`, "unlike").then((data) => {
                        likeCount.innerHTML = data.like_count;
                        dislikeCount.innerHTML = data.unlike_count;
                });

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
                const tweetId = e.target.dataset.tweetId;
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

function loadTweets(user_id) {
        tweet_container = document.getElementById("tweet_feed_container");
        fetch(`/user/profile/tweets?user_id=${user_id}`)
                .then((response) => response.json())
                .then((data) => {
                        if (data.success) {
                                data.tweets.forEach((tweet) => {
                                        clone = newTweetCard(tweet);
                                        tweet_container.appendChild(clone);
                                });
                        }
                })
                .then(() => {
                        initSeeMoreButtons();
                });
}

// function homeTweets(user_id) {
//
//         tweet_container = document.getElementById("tweet_feed_container");
//         fetch(`/user/profile/tweets?user_id=${user_id}`)
//                 .then((response) => response.json())
//                 .then((data) => {
//                         if (data.success) {
//                                 data.tweets.forEach((tweet) => {
//                                         clone = fillTweetTemplate(tweet);
//                                         tweet_container.appendChild(clone);
//                                 });
//                         }
//                 })
//                 .then(() => {
//                         initSeeMoreButtons();
//                 });
// }

// fuction for share modal
function createShareModal(tweet_id, title = "Share") {
        // Create modal HTML
        const modalHTML = `
    <div class="modal fade" id="dynamicShareModal" tabindex="-1">
        <div class="modal-dialog">
        <form>
            <div class="modal-content">
                <div class="modal-header px-3 py-2">
                    <h5 class="modal-title fs-5 flex-grow-1 text-center mb-0">${title}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body px-0">
                        <textarea name="input_text" class="share_tweet_input_filed" placeholder="Say something about the tweet...."></textarea>
                </div>
                <div class="modal-footer d-flex justify-content-between">
                <div class="text-muted" id="character_count">0</div>
                <button type="button" class="btn btn-primary px-5 submit-btn" data-bs-dismiss="modal" onclick="shareTweet(this, ${tweet_id})">Share</button>
                </div>
            </div>
            </form>
        </div>
    </div>
    `;

        // Add to DOM
        const modalContainer = document.createElement("div");
        modalContainer.innerHTML = modalHTML;
        document.body.appendChild(modalContainer.firstElementChild);

        // Initialize and show
        const modal = new bootstrap.Modal(document.getElementById("dynamicShareModal"));
        modal.show();

        // Clean up on hide
        modal._element.addEventListener("hidden.bs.modal", function () {
                modal.dispose();
                document.getElementById("dynamicShareModal").remove();
        });

        // Count the character of the input text
        const charCount = document.getElementById("character_count");
        const submitBtn = document.querySelector(".submit-btn");
        const textInput = document.querySelector(".share_tweet_input_filed");
        function fncharCount(text) {
                const lineBreaks = (text.match(/\n/g) || []).length;
                return text.length + lineBreaks;
        }
        let length = fncharCount(textInput.value);
        charCount.textContent = `${length}/1000`;
        // Character count and validation
        textInput.addEventListener("input", function () {
                length = fncharCount(textInput.value);
                charCount.textContent = `${length}/1000`;

                // Disable submit if over limit
                submitBtn.disabled = length > 1000;
        });

        return modal;
}

function shareTweet(btn, tweet_id) {
        inputText = btn.closest("form").querySelector('[name="input_text"]').value;
        formData = new FormData(btn.closest("form"));
        csrftoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        fetch(`/share_tweet/${tweet_id}`, {
                method: "POST",
                body: formData,
                headers: {
                        "X-Requested-With": "XMLHttpRequest",
                        "X-CSRFToken": csrftoken,
                },
        })
                .then((r) => r.json())
                .then((data) => {
                        if (data.success) {
                                alert("Tweet Shared Successfully");
                        }
                });
}
