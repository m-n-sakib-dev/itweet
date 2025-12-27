document.addEventListener("DOMContentLoaded", function () {
        const textInput = document.getElementById("id_text");
        const charCount = document.getElementById("charCount");
        const uploadArea = document.getElementById("uploadArea");
        const fileInput = document.getElementById("id_photo");
        const imagePreview = document.getElementById("imagePreview");
        const submitBtn = document.getElementById("submitBtn");
        const suggestionTags = document.querySelectorAll(".suggestion-tag");
        const page_name = document.querySelector(".create-title").textContent;

        function fncharCount(text) {
                const lineBreaks = (text.match(/\n/g) || []).length;
                return text.length + lineBreaks;
        }
        let length = fncharCount(textInput.value);
        charCount.textContent = `${length}/1000`;
        // Character count and validation
        textInput.addEventListener("input", function () {
                length = fncharCount(textInput.value);
                charCount.textContent = `${length}/1000`;
                // Update color based on character count
                if (length > 999) {
                        charCount.classList.add("error");
                        charCount.classList.remove("warning");
                } else if (length > 900) {
                        charCount.classList.add("warning");
                        charCount.classList.remove("error");
                } else {
                        charCount.classList.remove("warning", "error");
                }

                // Disable submit if over limit
                submitBtn.disabled = length > 1000;
        });

        // Drag and drop functionality
        uploadArea.addEventListener("dragover", function (e) {
                e.preventDefault();
                this.classList.add("dragover");
        });

        uploadArea.addEventListener("dragleave", function () {
                this.classList.remove("dragover");
        });

        uploadArea.addEventListener("drop", function (e) {
                e.preventDefault();
                this.classList.remove("dragover");
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                        fileInput.files = files;
                        handleFileSelect(files[0]);
                }
        });

        // File input change
        fileInput.addEventListener("change", function () {
                if (this.files.length > 0) {
                        handleFileSelect(this.files[0]);
                }
        });

        // Handle file selection and preview
        function handleFileSelect(file) {
                if (file && file.type.startsWith("image/")) {
                        const reader = new FileReader();
                        reader.onload = function (e) {
                                imagePreview.innerHTML = `
                    <div style="position: relative; display: inline-block;">
                        <img src="${e.target.result}" class="preview-image" alt="Preview">
                        <button type="button" class="remove-image" onclick="removeImage()">
                            <i class="bi bi-x"></i>
                        </button>
                    </div>
                `;
                                imagePreview.style.display = "block";
                        };
                        reader.readAsDataURL(file);
                }
        }

        // Remove image
        window.removeImage = function () {
                fileInput.value = "";
                imagePreview.style.display = "none";
                imagePreview.innerHTML = "";
        };

        // Suggestion tags
        suggestionTags.forEach((tag) => {
                tag.addEventListener("click", function () {
                        const currentText = textInput.value;
                        const tagText = this.textContent;

                        if (currentText.length + tagText.length + 1 <= 1000) {
                                textInput.value = currentText + (currentText ? " " : "") + tagText;
                                textInput.dispatchEvent(new Event("input"));
                                textInput.focus();
                        }
                });
        });

        // Form submission animation
        const form = document.querySelector(".tweet-form");
        form.addEventListener("submit", function (e) {
                length = fncharCount(textInput.value);
                if (length > 1000) {
                        e.preventDefault();
                        return;
                } else if (fileInput.value == "" && length == 0) {
                        e.preventDefault();
                        return;
                }
                this.submitBtn.innerHTML = '<i class="bi bi-arrow-repeat spinner"></i> Posting...';
                submitBtn.disabled = true;
        });
        if (page_name.split(/\s/).join("") == "EditMyTweet") {
                document.querySelector(".image_upload_area").classList.add("d-none");
        }
});

// Add spinner animation
const style = document.createElement("style");
style.textContent = `
    .spinner {
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);
