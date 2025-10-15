function likefunction(link_url, csrftoken) {
        console.log(csrftoken);
        fetch(link_url, {
                method: "POST",
                headers: {
                        "X-Requested-With": "XMLHttpRequest",
                        "X-CSRFToken": csrftoken,
                },
        })
                .then((response) => response.json())
                .then((data) => {
                        document.querySelector(".like_count").textContent = data.like_count;
                        document.querySelector(".unlike_count").textContent = data.unlike_count;
                });
}
