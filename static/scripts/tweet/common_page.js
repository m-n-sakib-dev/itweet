let page_number = 1;
let loading = false;
let hasMore = true;
let loading_spinner;
let following_loading;
let page_name;

document.addEventListener("DOMContentLoaded", () => {
        // setting fixed postioned nav-bar width matching with parent
        const homeFeedContainer = document.querySelector(".home_feed_conainer");
        const homeNavContainer = document.querySelector(".home-nav-container");
        homeNavContainer.style.width = homeFeedContainer.offsetWidth + "px";
        page_name = document.querySelector(".home-nav-item").querySelector(".page_name").dataset.pageName;
        loading_spinner = document.getElementById("loading_spinner");
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

function loadSavedTweets() {
        tweet_container = document.getElementById("tweets_list");
        fetch(`/user/saved-tweets?page=${page_number}`)
                .then((response) => response.json())
                .then((data) => {
                        if (data.success) {
                                data.tweets.forEach((tweet) => {
                                        clone = newTweetCard(tweet);
                                        tweet_container.appendChild(clone);
                                });
                                page_number++;
                                hasMore = data.is_more;
                                if (!hasMore) {
                                        loading_spinner.textContent = "No more Tweets. End of the page";
                                }
                        }
                })
                .then(() => {
                        initSeeMoreButtons();
                });
}
function loadHashtagTweets() {
        tweet_container = document.getElementById("tweets_list");
        hashtag_name = document.querySelector(".hashtag_name").textContent.slice(1);
        console.log(hashtag_name);

        fetch(`/hastags/${hashtag_name}/tweets?page=${page_number}`)
                .then((response) => response.json())
                .then((data) => {
                        if (data.success) {
                                data.tweets.forEach((tweet) => {
                                        clone = newTweetCard(tweet);
                                        tweet_container.appendChild(clone);
                                });
                                page_number++;
                                hasMore = data.is_more;
                                if (!hasMore) {
                                        loading_spinner.textContent = "No more Tweets. End of the page";
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
                                        if (container.id === "loading_spinner" && hasMore && !loading) {
                                                if (page_name == "saved_tweets") {
                                                        loadSavedTweets();
                                                } else if (page_name == "hashtag") {
                                                        loadHashtagTweets();
                                                }
                                        }
                                }
                        });
                },
                { threshold: 0.1 }
        ); // Trigger when 10% of container is visible

        observer.observe(loading_spinner);
}

function showLoading(loadingId) {
        document.getElementById(loadingId).style.display = "block";
}

function hideLoading(loadingId) {
        document.getElementById(loadingId).style.display = "none";
}
