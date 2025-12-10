let tweetHasMore = true;
let profile_tweet_loading;
let tweetPage = 1;
document.addEventListener("DOMContentLoaded", () => {
        profile_tweet_loading = document.getElementById("profile_tweet_loading");
        loadAbout();
        activateUserProfileNav();
        infiniteScroll();
        document.querySelector(".user_profile_follower_count_container").addEventListener("click", loadFollowerList);
        document.querySelector(".user_profile_following_count_container").addEventListener("click", loadFollowingList);
});
//function that will toggle the follow. if followed then unfollow. if not then follow
function loadAbout() {
        fetch(`${profile_id}/about`)
                .then((r) => r.json())
                .then((data) => {
                        if (window.innerWidth > 992) document.querySelector(".user_profile_detail").innerHTML = data.about_content;
                        else document.querySelector("#aboutTab").innerHTML = data.about_content;
                });
}
function activateUserProfileNav() {
        tabs = document.querySelectorAll(".profile-nav-item");
        contents = document.querySelectorAll(".tab-content");
        tabs.forEach((tab) => {
                tab.addEventListener("click", () => {
                        tabData = tab.dataset.tab;
                        tabs.forEach((t) => t.classList.toggle("active"));
                        contents.forEach((c) => c.classList.toggle("active"));
                });
        });
        autohideNavbar("user_profile_center_container", "user-profile-navbar-id");
}

function fn_toggle_follow(profile_id) {
        follow_btn = document.querySelector(".follow-btn");
        csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        fetch(`/user/profile/${profile_id}/togglefollow`, {
                method: "POST",
                headers: {
                        "X-Requested-With": "XMLHttpRequest",
                        "X-CSRFToken": csrf_token,
                },
        })
                .then((response) => response.json())
                .then((data) => {
                        if (data.success) {
                                console.log(data);
                                if (data.action == "followed") {
                                        follow_btn.innerHTML = `<i class="bi bi-bookmark-dash"></i> Unfollow`;
                                } else {
                                        follow_btn.innerHTML = `<i class="bi bi-bookmark-plus"></i> Follow`;
                                }
                                document.querySelector(".profile_followers_count").textContent = data.followers_count;
                                document.querySelector(".profile_following_count").textContent = data.following_count;
                        }
                });
}

function loadUserTweets(user_id) {
        tweet_container = document.getElementById("user_tweet_feed_container");
        fetch(`/user/profile/tweets?user_id=${user_id}&page=${tweetPage}`)
                .then((response) => response.json())
                .then((data) => {
                        if (data.success) {
                                data.tweets.forEach((tweet) => {
                                        clone = newTweetCard(tweet);
                                        tweet_container.appendChild(clone);
                                });
                                tweetPage++;
                                tweetHasMore = data.is_more;
                                if (!data.is_more) {
                                        profile_tweet_loading.textContent = "No more Tweets. End of the page";
                                }
                        }
                })
                .then(() => {
                        initSeeMoreButtons();
                });
}

function infiniteScroll() {
        const observer = new IntersectionObserver(
                (entries) => {
                        entries.forEach((entry) => {
                                if (entry.isIntersecting) {
                                        // When container becomes visible in viewport
                                        const container = entry.target;
                                        if (container.id === "profile_tweet_loading" && tweetHasMore) {
                                                loadUserTweets(profile_id); // Load more "For You" tweets
                                        }
                                }
                        });
                },
                { threshold: 0.1 }
        ); // Trigger when 10% of container is visible

        observer.observe(profile_tweet_loading);
}

function loadFollowerList() {
        console.log("loading Follower");
        document.querySelector(".user_profile_follow_list_modal-title").textContent = "Followers";
        display_container = document.querySelector(".user_profile_follow_list_modal-body");
        display_container.innerHTML = ``;
        fetch(`${profile_id}/followers`)
                .then((r) => r.json())
                .then((data) => {
                        if (data.success) {
                                data.list.forEach((user) => {
                                        follow_item = document.createElement("div");
                                        follow_item.innerHTML = followListItemCard(user);
                                        display_container.appendChild(follow_item);
                                });
                        }
                });
}

function loadFollowingList() {
        console.log("loading Following");
        document.querySelector(".user_profile_follow_list_modal-title").textContent = "Following";
        display_container = document.querySelector(".user_profile_follow_list_modal-body");
        display_container.innerHTML = ``;
        fetch(`${profile_id}/following`)
                .then((r) => r.json())
                .then((data) => {
                        if (data.success) {
                                console.log(data.list);
                                data.list.forEach((user) => {
                                        follow_item = document.createElement("div");
                                        follow_item.innerHTML = followListItemCard(user);
                                        display_container.appendChild(follow_item);
                                });
                        }
                });
}

function followListItemCard(user) {
        return `
<div class="follow-item" data-user-id="${user.id}">
        <img src="${user.profile_picture || " /static/default-avatar.png"}" alt="${user.username}" class="follow-avatar"
                onerror="this.src='/static/default-avatar.png'">
        <div class="follow-info">
                <div class="follow-name">${user.name} </div>
                <span class="follow-handle">${user.username}</span>
                <span class="follow-handle">-- ${user.follower_count} Follower</span>
        </div>
        <button class="follow-btn ${user.is_following ? " following" : ""} ${
                user.id == current_user.id ? "d-none" : ""
        }" onclick="modalToggleFollow(this, ${user.id})">
                ${user.is_following ? "Following" : "Follow"}
        </button>
</div>
`;
}

function modalToggleFollow(button, user_id) {
        const isFollowing = button.classList.contains("following");

        // button.disabled = true;
        csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

        fetch(`/user/profile/${user_id}/togglefollow`, {
                method: "POST",
                headers: {
                        "X-Requested-With": "XMLHttpRequest",
                        "X-CSRFToken": csrf_token,
                },
        })
                .then((response) => response.json())
                .then((data) => {
                        if (data.success) {
                                button.classList.toggle("following");
                                button.textContent = isFollowing ? "Follow" : "Following";
                                console.log(profile_id + "  " + current_user.id);

                                if (profile_id == current_user.id) {
                                        document.querySelector(".profile_following_count").textContent = data.user_following_count;
                                }
                        }
                        // Check if redirect is required
                        if (data.redirect && data.redirect_url) {
                                // Redirect to login page
                                window.location.href = data.redirect_url;
                                return;
                        }
                });
}
