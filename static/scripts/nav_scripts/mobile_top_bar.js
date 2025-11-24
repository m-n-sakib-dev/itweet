document.addEventListener("DOMContentLoaded", function () {
        // ===========================================
        // ELEMENT REFERENCES
        // ===========================================
        const searchBtn = document.getElementById("searchBtn");
        const searchOverlay = document.getElementById("searchOverlay");
        const closeSearch = document.getElementById("closeSearch");
        const searchInput = document.getElementById("searchInput");
        const clearSearch = document.getElementById("clearSearch");
        const topbarContent = document.querySelector(".topbar-content");
        const searchResult = document.getElementById("topbar_search_result");
        const noResult = searchResult.innerHTML;

        // ===========================================
        // SEARCH OVERLAY TOGGLE FUNCTIONALITY
        // ===========================================

        /*
    SEARCH BUTTON CLICK HANDLER
    - Shows search overlay
    - Hides main topbar content
    - Focuses search input for immediate typing
    */
        searchBtn.addEventListener("click", function () {
                // Activate search overlay with CSS class
                searchOverlay.classList.add("active");

                // Auto-focus search input for better UX
                setTimeout(() => {
                        searchInput.focus();
                }, 50);
        });

        /*
    CLOSE SEARCH HANDLER
    - Hides search overlay  
    - Restores main topbar content
    - Clears search input
    */
        closeSearch.addEventListener("click", function () {
                // Deactivate search overlay
                searchOverlay.classList.remove("active");

                // Clear any search text
                searchInput.value = "";
        });
        /*
    CLEAR SEARCH INPUT HANDLER
    - Clears input field
    - Maintains focus for new search
    */
        clearSearch.addEventListener("click", function () {
                searchInput.value = ""; // Clear text
                searchInput.focus(); // Keep focus in search
                searchResult.innerHTML = noResult;
        });

        // ===========================================
        // KEYBOARD SHORTCUTS
        // ===========================================

        /*
    ESC KEY HANDLER
    - Closes search overlay when ESC pressed
    - Better UX for keyboard users
    */
        document.addEventListener("keydown", function (e) {
                // Check if ESC key pressed AND search is active
                if (e.key === "Escape" && searchOverlay.classList.contains("active")) {
                        // Trigger same close behavior as back button
                        searchOverlay.classList.remove("active");
                }
        });

        // ===========================================
        // SEARCH FUNCTIONALITY
        // ===========================================

        /*
    SEARCH INPUT HANDLER
    - Listens for typing
    - Triggers search after minimum characters
    - Debounce would be needed for production
    */
        searchInput.addEventListener("input", function (e) {
                const query = e.target.value.trim();

                // Only search if query has enough characters
                if (query.length > 0) {
                        // In production: Make API call here
                        console.log("Searching for:", query);
                        searchResult.textContent = query;

                        // You would typically:
                        // 1. Show loading state
                        // 2. Make fetch() request to search API
                        // 3. Update search-results with response
                        // 4. Handle errors
                } else {
                        searchResult.innerHTML = noResult;
                }
        });

        const tweetContainer = document.querySelector(".tweet-container");
        let prevScrollpos = 0;
        if (tweetContainer != null) {
                tweetContainer.addEventListener("scroll", function () {
                        var currentScrollPos = this.scrollTop;
                        if (prevScrollpos > currentScrollPos || currentScrollPos < 10) {
                                document.getElementById("home-nav-container").style.top = "0";
                        } else {
                                document.getElementById("home-nav-container").style.top = "-50px";
                        }
                        prevScrollpos = currentScrollPos;
                });
        }

        // the home-navbar hiding on scroll and showin on backscroll
});
