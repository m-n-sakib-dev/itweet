// here all the comment feature handling js functions are written
// this function adds new comment on a tweet
function handleCommentSubmission(button, tweet_id) {
        const form = button.closest("form");
        csrf_token = document.getElementsByName("csrfmiddlewaretoken");

        fetch(`/interaction/${tweet_id}/comment/`, {
                method: "POST",
                headers: {
                        "X-Requested-With": "XMLHttpRequest",
                        "X-CSRFToken": csrf_token,
                },
                body: new FormData(form),
        })
                .then((response) => response.json())
                .then((data) => {
                        if (data.success) {
                                document.querySelector(`#_${tweet_id}.comment_count`).textContent = data.comment_count;
                                document.querySelector(`#_${tweet_id}.comment_count_post-details`).textContent = data.comment_count;
                                const comments_list = document.getElementById(`comment_list_${tweet_id}`);
                                clone = addcomment(data.comment_data, `comment_list_${tweet_id}`);
                                form.reset();
                                comments_list.prepend(clone);
                        } else {
                                alert("Error adding comment");
                        }
                });
}

// this function shows the main comments list(direct comment on the tweet)
function commentList(tweet_id) {
        csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        fetch(`/interaction/${tweet_id}/comments_list/`, {
                method: "POST",
                headers: {
                        "X-Requested-With": "XMLHttpRequest",
                        "X-CSRFToken": csrf_token,
                },
        })
                .then((response) => response.json())
                .then((data) => {
                        if (data.success) {
                                const comments_list = document.getElementById(`comment_list_${tweet_id}`);
                                comments_list.innerHTML = "";
                                // comments_list.innerHTML = data.html;
                                data.comments_list.forEach((commentData) => {
                                        clone = addcomment(commentData, `comment_list_${tweet_id}`);
                                        comments_list.appendChild(clone);
                                });
                        }
                });
}

// this function shows the reply comments list(replies on a comment)
function commentReplyList(comment_id) {
        csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        fetch(`/interaction/comments/${comment_id}/replies/`, {
                method: "POST",
                headers: {
                        "X-Requested-With": "XMLHttpRequest",
                        "X-CSRFToken": csrf_token,
                },
        })
                .then((response) => response.json())
                .then((data) => {
                        if (data.success) {
                                const comments_list = document.getElementById(`comment_reply_list_${comment_id}`);
                                // comments_list.innerHTML = data.html;
                                data.comments_list.forEach((commentData) => {
                                        clone = addcomment(commentData, `comment_reply_list_${comment_id}`);
                                        commentElement = clone.querySelector(".comment-actions");
                                        reply_btn = commentElement.querySelector(".reply-btn");
                                        commentElement.removeChild(reply_btn);
                                        comments_list.appendChild(clone);
                                });
                        }
                });
}

// this function handles reaction  on comments(like or unlike)
function commentlikefunction(buttonElement) {
        csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        comment_id = buttonElement.closest(".comment-item").dataset.commentId;
        reation_type = buttonElement.dataset.reationType;
        comment_action = buttonElement.closest(".comment-actions");
        fetch(`/interaction/comment/${comment_id}/reaction/${reation_type}`, {
                method: "POST",
                headers: {
                        "X-Requested-With": "XMLHttpRequest",
                        "X-CSRFToken": csrf_token,
                },
        })
                .then((response) => response.json())
                .then((data) => {
                        comment_action.querySelector(".comment_like_count").textContent = data.like_count;
                        comment_action.querySelector(".comment_unlike_count").textContent = data.unlike_count;
                        console.log(data.unlike_count);
                        // document.querySelector("#_" + data.tweet_id + ".unlike_count").textContent = data.unlike_count;
                });
}

// this function creates a comments body using the template and return a body which is used by other comment listing js function
function addcomment(commentData, parent_container) {
        const template = document.getElementById("comment_body_template");
        const clone = template.content.cloneNode(true);
        const commentElement = clone.querySelector(".comment-item");
        commentElement.dataset.commentId = commentData.id;
        commentElement.id = "containerOfcommentId" + commentData.id;
        commentElement.querySelector(".comment-username").textContent = commentData.user.user_name;
        commentElement.querySelector(".comment-content").textContent = commentData.content;
        commentElement.querySelector(".comment_like_count").textContent = commentData.like_count;
        commentElement.querySelector(".comment_unlike_count").textContent = commentData.unlike_count;
        commentElement.querySelector(".comment_reply_count").textContent = commentData.reply_count;
        commentElement.querySelector(".comment-reply-container").id = "comment_reply_list_" + commentData.id;
        comment_body = commentElement.querySelector(".comment-body");
        comment_menu = commentElement.querySelector(".comment-menu-dropdown-menu");
        comment_menu.innerHTML = `
                <li><button class="dropdown-item" onclick="editComment(${commentData.id},this)">Edit</button></li>
                <li><button class="dropdown-item" onclick="deletecomment(${commentData.id},${parent_container})">Delete</button></li>`;
        return clone;
}

// this function insert a comment reply form under a comment
function add_comment_reply_form(reply_button) {
        const parent_comment = reply_button.closest(".comment-item");
        const comment_id = parent_comment.dataset.commentId;
        const tweet_id = parent_comment.dataset.tweetId;
        const r_container = parent_comment.querySelector(".comment-reply-container");
        if (r_container.innerHTML == "") {
                commentReplyList(comment_id);
        }
        if (!r_container.querySelector(".reply-comment-form-container")) {
                const template = document.getElementById("comment_reply_form_template");
                const clone = template.content.cloneNode(true);
                const commentbtn = clone.querySelector(".submit_btn");
                commentbtn.dataset.commentId = comment_id;
                commentbtn.dataset.tweetId = tweet_id;
                r_container.prepend(clone);
        }
}

// this function handles reply on a comment
function fn_reply_comment(btn) {
        const comment_id = btn.dataset.commentId;
        const form = btn.closest(".comment-form");
        parent_comment = btn.closest(".comment-item");
        csrf_token = document.getElementsByName("csrfmiddlewaretoken");
        fetch(`/interaction/comments/${comment_id}/comment_reply/`, {
                method: "POST",
                headers: {
                        "X-Requested-With": "XMLHttpRequest",
                        "X-CSRFToken": csrf_token,
                },
                body: new FormData(form),
        })
                .then((response) => response.json())
                .then((data) => {
                        if (data.success) {
                                tweet_id = data.tweet_id;
                                document.querySelector(`#_${tweet_id}.comment_count`).textContent = data.comment_count;
                                document.querySelector(`#_${tweet_id}.comment_count_post-details`).textContent = data.comment_count;
                                const comments_list = document.getElementById(`comment_reply_list_${comment_id}`);
                                clone = addcomment(data.comment_data, `comment_reply_list_${comment_id}`);
                                commentElement = clone.querySelector(".comment-actions");
                                reply_btn = commentElement.querySelector(".reply-btn");
                                commentElement.removeChild(reply_btn);
                                form.reset();
                                comments_list.prepend(clone);
                                comments_list.removeChild(comments_list.querySelector(".reply-comment-form-container"));
                                parent_comment.querySelector(".comment_reply_count").textContent = data.reply_count;
                        } else {
                                alert("Error adding comment");
                        }
                });
}

//this function delete a comment
function deletecomment(comment_id, parent_container) {
        console.log(parent_container);
        csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        if (confirm("are you sure to delete this comment?")) {
                fetch(`/interaction/comments/${comment_id}/delete/`, {
                        method: "POST",
                        headers: {
                                "X-Requested-With": "XMLHttpRequest",
                                "X-CSRFToken": csrf_token,
                        },
                })
                        .then((response) => response.json())
                        .then((data) => {
                                if (data.success) {
                                        child = document.getElementById(`containerOfcommentId${comment_id}`);
                                        parent_container.removeChild(child);
                                        document.querySelector(`#_${data.tweet_id}.comment_count`).textContent = data.tweet_comment_count;
                                        document.querySelector(`#_${data.tweet_id}.comment_count_post-details`).textContent =
                                                data.tweet_comment_count;

                                        if (data.parent !== null) {
                                                parent_container = document.getElementById(`containerOfcommentId${data.parent.id}`);
                                                parent_container.querySelector(".comment_reply_count").textContent = data.parent.reply_count;
                                        }
                                        alert("message deleted sccessfully");
                                } else {
                                        console.log(data.error);
                                }
                        });
        }
}

// this function is for edit comment
function editComment(comment_id, btn) {
        const comment_body = btn.closest(".comment-item");
        csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        edit_form_container = comment_body;
        const template = document.getElementById("comment_reply_form_template");
        const clone = template.content.cloneNode(true);
        const form = clone.querySelector(".comment-form");
        const textarea = form.querySelector("textarea[name='content']");
        textarea.textContent = comment_body.querySelector(".comment-content").textContent;
        const copy_comment_body = edit_form_container.cloneNode(true);
        edit_form_container.innerHTML = clone.querySelector(".reply-comment-form-container").innerHTML;
        const submit_btn = edit_form_container.querySelector(".submit_btn");
        submit_btn.removeAttribute("onclick");
        submit_btn.addEventListener("click", () => {
                current_text = edit_form_container.querySelector("textarea[name='content']").value;
                form.content.value = current_text;
                fetch(`/interaction/comments/${comment_id}/edit/`, {
                        method: "POST",
                        headers: {
                                "X-Requested-With": "XMLHttpRequest",
                                "X-CSRFToken": csrf_token,
                        },
                        body: new FormData(form),
                })
                        .then((response) => response.json())
                        .then((data) => {
                                if (data.success) {
                                        copy_comment_body.querySelector(".comment-content").textContent = data.comment_data.content;
                                        edit_form_container.innerHTML = copy_comment_body.innerHTML;
                                        const dropdownElement = edit_form_container.querySelector(".dropdown");
                                        const dropdown = bootstrap.Dropdown.getInstance(dropdownElement);
                                        if (dropdown) {
                                                dropdown.toggle();
                                        } else {
                                                // If no instance exists, create one and toggle
                                                new bootstrap.Dropdown(dropdownElement).toggle();
                                        }
                                } else {
                                        alert("Error adding comment");
                                }
                        });
        });
}
