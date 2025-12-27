document.addEventListener("DOMContentLoaded", function () {
        let mobile_top_bar = document.querySelector(".mobile_top_bar");
        let home_left_panel = document.querySelector(".home-left-panel");
        let mobile_top_bar_content = mobile_top_bar.innerHTML;
        let home_left_panel_content = home_left_panel.innerHTML;
        if (window.innerWidth >= 576) {
                mobile_top_bar.innerHTML = ``;
                home_left_panel.innerHTML = home_left_panel_content;
        }
        if (window.innerWidth < 576) {
                home_left_panel.innerHTML = ``;
                mobile_top_bar.innerHTML = mobile_top_bar_content;
        }
});
