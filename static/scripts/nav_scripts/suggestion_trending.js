// suggestion_trending.js
document.addEventListener("DOMContentLoaded", function () {
        // Load follow suggestions
        loadFollowSuggestions();
        refreshTrending();

        // Follow button handler
        document.addEventListener("click", function (e) {
                if (e.target.closest(".follow-btn")) {
                        const btn = e.target.closest(".follow-btn");
                        toggleFollow(btn, e.target.closest(".follow-item").dataset.userId);
                }

                // Refresh trending
                if (e.target.closest(".refresh-btn")) {
                        e.preventDefault();
                        refreshTrending();
                }
                if (e.target.closest(".refresh-follow")) {
                        loadFollowSuggestions();
                }
        });

        // Auto-refresh trending every 30 minutes
        setInterval(refreshTrending, 30 * 60 * 1000);
});

// Load follow suggestions
function loadFollowSuggestions() {
        const followList = document.getElementById("followList");
        if (!followList) return;
        fetch(`/follower/suggestions`) //url in project url.py file
                .then((response) => response.json())
                .then((data) => {
                        if (data.success) {
                                renderFollowSuggestions(data.suggested_users);
                        }
                });
}

// Render follow suggestions
function renderFollowSuggestions(users) {
        const followList = document.getElementById("followList");
        if (!followList) return;

        if (!users || users.length === 0) {
                followList.innerHTML = `
      <div class="loading-follow">
        <i class="bi bi-person-circle"></i>
        <p>No Suggestion Available</p>
      </div>
    </div>
        `;
                return;
        }

        followList.innerHTML = users
                .map(
                        (user) => `
        <a href="/user/profile/${user.id}" class="follow-item" data-user-id="${user.id}">
            <img src="${user.profile_picture || "/static/default-avatar.png"}" 
                 alt="${user.username}" 
                 class="follow-avatar"
                 onerror="this.src='/static/default-avatar.png'">
            <div class="follow-info">
                <div class="follow-name">${user.name}  </div>
		<span class="follow-handle">${user.username}</span>
		<span class="follow-handle">-- ${user.follower_count} Follower</span>
            </div>
            <button class="follow-btn ${user.is_following ? "following" : ""}" >
                ${user.is_following ? "Following" : "Follow"}
            </button>
        </a>
    `
                )
                .join("");
}

// Toggle follow
function toggleFollow(button, profile_id) {
        const isFollowing = button.classList.contains("following");

        // button.disabled = true;
        csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

        fetch(`user/profile/${profile_id}/togglefollow`, {
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
                        }
                        // Check if redirect is required
                        if (data.redirect && data.redirect_url) {
                                // Redirect to login page
                                window.location.href = data.redirect_url;
                                return;
                        }
                });
}

// Refresh trending
function refreshTrending() {
        const refreshBtn = document.querySelector(".refresh-btn");
        const icon = refreshBtn.querySelector("i");

        // Add spinning animation
        icon.classList.add("refresh_spin");
        refreshBtn.style.pointerEvents = "none";

        fetch(`/hastags/trending-hashtags`)
                .then((response) => response.json())
                .then((data) => {
                        if (data.success) {
                                trendingListContainer = document.getElementById("trendingList");
                                trendingListContainer.innerHTML = ``;
                                data.trending_hastags.forEach((hashtag) => {
                                        trend_item = document.createElement("div");
                                        trend_item.innerHTML = `
					<div class="trending-item">
                                                <a href="/hastags/${hashtag.data.name}/hashtag_page">
						<div class="trending-content">
						<div class="trending-name">#${hashtag.data.name}</div>
						<div class="trending-stats ps-2">${hashtag.data.tweet_count} tweets (${hashtag.recent_tweets} in 24hrs)</div>
						</div>
                                                </a>
					</div>
					`;
                                        trendingListContainer.appendChild(trend_item);
                                });
                        }
                })
                .then(() => {
                        icon.classList.remove("refresh_spin");
                        refreshBtn.style.pointerEvents = "auto";

                        // Update timestamp
                        const updateEl = document.querySelector(".update-time");
                        if (updateEl) {
                                updateEl.innerHTML = '<i class="bi bi-clock"></i> Just now';

                                // Revert after 2 seconds
                                setTimeout(() => {
                                        updateEl.innerHTML = '<i class="bi bi-clock"></i> Updated recently';
                                }, 2000);
                        }
                });
}
