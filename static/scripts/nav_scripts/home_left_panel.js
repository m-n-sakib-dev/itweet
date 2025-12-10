document.addEventListener("DOMContentLoaded", function () {
        const searchBtn = document.getElementById("left_panel_search_btn");
        const searchInput = document.getElementById("left_panel_searchInput");
        const clearSearch = document.getElementById("left_panel_clearSearch");
        const searchResult = document.getElementById("left_panel_search_result");
        const noResult = searchResult.innerHTML;

        searchBtn.addEventListener("click", function () {
                // Auto-focus search input
                setTimeout(() => {
                        searchInput.focus();
                }, 400);
        });

        clearSearch.addEventListener("click", function () {
                searchInput.value = ""; // Clear text
                searchInput.focus(); // Keep focus in search
                searchResult.innerHTML = noResult;
        });

        searchInput.addEventListener("input", function (e) {
                const query = e.target.value.trim();

                // Only search if query has enough characters
                if (query.length > 3) {
                        searchResult.textContent = "Searching.....";
                        if (query[0] == "#") {
                                input = query.slice(1);
                                fetch(`/search/?input_str=${input}&type=hashtag`)
                                        .then((r) => r.json())
                                        .then((data) => {
                                                if (data.success) {
                                                        console.log(data.result);
                                                        if (data.result.length == 0) {
                                                                searchResult.textContent = "No Result Found";
                                                        } else {
                                                                searchResult.textContent = data.result;
                                                        }
                                                }
                                        });
                        } else if (query[0] == "@") {
                                input = query;
                                fetch(`/search/?input_str=${input}&type=username`)
                                        .then((r) => r.json())
                                        .then((data) => {
                                                if (data.success) {
                                                        console.log(data.result);
                                                        if (data.result.length == 0) {
                                                                searchResult.textContent = "No Result Found";
                                                        } else {
                                                                searchResult.textContent = data.result;
                                                        }
                                                }
                                        });
                        } else {
                                input = query;
                                fetch(`/search/?input_str=${input}&type=name`)
                                        .then((r) => r.json())
                                        .then((data) => {
                                                if (data.success) {
                                                        console.log(data.result);
                                                        if (data.result.length == 0) {
                                                                searchResult.textContent = "No Result Found";
                                                        } else {
                                                                searchResult.textContent = data.result;
                                                        }
                                                }
                                        });
                        }
                } else {
                        searchResult.innerHTML = noResult;
                }
        });
});
