function likefunction(link_url, csrftoken, reaction) {
        fetch(link_url, {
                method: "POST",
                headers: {
                        "X-Requested-With": "XMLHttpRequest",
                        "X-CSRFToken": csrftoken,
                },
        })
                .then((response) => response.json())
                .then((data) => {
                        document.querySelector("#_" + data.tweet_id + ".like_count").textContent = data.like_count;
                        document.querySelector("#_" + data.tweet_id + ".unlike_count").textContent = data.unlike_count;
                        icon = document.querySelector("#like_" + data.tweet_id);
                        icon_2 = document.querySelector("#unlike_" + data.tweet_id);
                        if (reaction == "like") {
                                if (icon.classList.contains("bi-hand-thumbs-up")) {
                                        icon.classList.remove("bi-hand-thumbs-up");
                                        icon.classList.add("bi-hand-thumbs-up-fill");
                                        if (icon_2.classList.contains("bi-hand-thumbs-down-fill")) {
                                                icon_2.classList.remove("bi-hand-thumbs-down-fill");
                                                icon_2.classList.add("bi-hand-thumbs-down");
                                        }
                                } else {
                                        icon.classList.remove("bi-hand-thumbs-up-fill");
                                        icon.classList.add("bi-hand-thumbs-up");
                                }
                        } else {
                                if (icon_2.classList.contains("bi-hand-thumbs-down")) {
                                        icon_2.classList.remove("bi-hand-thumbs-down");
                                        icon_2.classList.add("bi-hand-thumbs-down-fill");
                                        if (icon.classList.contains("bi-hand-thumbs-up-fill")) {
                                                icon.classList.remove("bi-hand-thumbs-up-fill");
                                                icon.classList.add("bi-hand-thumbs-up");
                                        }
                                } else {
                                        icon_2.classList.remove("bi-hand-thumbs-down-fill");
                                        icon_2.classList.add("bi-hand-thumbs-down");
                                }
                        }
                });
}
function toggleSeeMore(button) {
        const tweetText = button.previousElementSibling;
        // const tweetText = button.parentElement;
        console.log(tweetText.textContent);
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
        document.querySelectorAll(".tweet-card-text").forEach((tweetText) => {
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
