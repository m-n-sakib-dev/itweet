let tweetHasMore = true;
let profile_tweet_loading;
let tweetPage = 1;
document.addEventListener("DOMContentLoaded", () => {
        profile_tweet_loading = document.getElementById("profile_tweet_loading");
        infiniteScroll();
});
//function that will toggle the follow. if followed then unfollow. if not then follow
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
                                        console.log(entry.target.id);
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
