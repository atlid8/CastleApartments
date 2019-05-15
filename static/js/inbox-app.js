jQuery(document).ready(function($) {
    $(".clickable-message").click(function() {
        window.location = $(this).data("href");
    });
});