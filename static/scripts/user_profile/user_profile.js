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
                        }
                });
}
