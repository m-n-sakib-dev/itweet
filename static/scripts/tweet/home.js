let forYouPage = 1;
let followingPage = 1;
let forYouLoading = false;
let followingLoading = false;
let forYouHasMore = true;
let followingHasMore = true;
let foryou_loading;
let following_loading;

document.addEventListener("DOMContentLoaded", () => {
        // setting fixed postioned nav-bar width matching with parent
        const homeFeedContainer = document.querySelector(".home_feed_conainer");
        const homeNavContainer = document.querySelector(".home-nav-container");
        homeNavContainer.style.width = homeFeedContainer.offsetWidth + "px";

        foryou_loading = document.getElementById("foryou_loading");
        following_loading = document.getElementById("following_loading");
        initializeTabs();
        initializeInfiniteScroll();
});

function initializeTabs() {
        const forYouTab = document.querySelector(".nav-foryou");
        const followingTab = document.querySelector(".nav-following");
        const forYouContainer = document.getElementById("home_foryou_tweets_container");
        const followingContainer = document.getElementById("home_following_tweets_container");

        forYouTab.addEventListener("click", () => {
                forYouTab.classList.add("active");
                followingTab.classList.remove("active");

                forYouContainer.classList.remove("hidden");
                forYouContainer.classList.add("visible");
                followingContainer.classList.remove("visible");
                followingContainer.classList.add("hidden");
        });

        followingTab.addEventListener("click", () => {
                followingTab.classList.add("active");
                forYouTab.classList.remove("active");

                followingContainer.classList.remove("hidden");
                followingContainer.classList.add("visible");
                forYouContainer.classList.remove("visible");
                forYouContainer.classList.add("hidden");
        });
}

function homeTweets() {
        tweet_container = document.getElementById("foryou_tweets_list");
        fetch(`/tweets/home/all?page=${forYouPage}`)
                .then((response) => response.json())
                .then((data) => {
                        if (data.success) {
                                data.tweets.forEach((tweet) => {
                                        clone = newTweetCard(tweet);
                                        tweet_container.appendChild(clone);
                                });
                                forYouPage++;
                                forYouHasMore = data.is_more;
                                if (!forYouHasMore) {
                                        foryou_loading.textContent = "No more Tweets. End of the page";
                                }
                        }
                })
                .then(() => {
                        initSeeMoreButtons();
                });
}
function followingTweets() {
        tweet_container = document.getElementById("following_tweets_list");
        fetch(`/tweets/home/following_tweets?page=${followingPage}`)
                .then((response) => response.json())
                .then((data) => {
                        if (data.success) {
                                data.tweets.forEach((tweet) => {
                                        clone = newTweetCard(tweet);
                                        tweet_container.appendChild(clone);
                                });
                                followingPage++;
                                followingHasMore = data.is_more;
                                if (!followingHasMore) {
                                        following_loading.textContent = "No more Tweets. End of the page";
                                }
                        }
                })
                .then(() => {
                        initSeeMoreButtons();
                });
}
function initializeInfiniteScroll() {
        const observer = new IntersectionObserver(
                (entries) => {
                        entries.forEach((entry) => {
                                if (entry.isIntersecting) {
                                        // When container becomes visible in viewport
                                        const container = entry.target;
                                        if (container.id === "foryou_loading" && forYouHasMore && !forYouLoading) {
                                                homeTweets(); // Load more "For You" tweets
                                        } else if (container.id === "following_loading" && followingHasMore && !followingLoading) {
                                                followingTweets(); // Load more "Following" tweets
                                        }
                                }
                        });
                },
                { threshold: 0.1 }
        ); // Trigger when 10% of container is visible

        observer.observe(foryou_loading);
        observer.observe(following_loading);
}

function showLoading(loadingId) {
        document.getElementById(loadingId).style.display = "block";
}

function hideLoading(loadingId) {
        document.getElementById(loadingId).style.display = "none";
}
