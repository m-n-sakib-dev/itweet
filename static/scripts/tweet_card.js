function likefunction(link_url, csrftoken) {
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
                        console.log(data.like_count);
                        console.log(data.unlike_count);
                });
}
