// Changes title to 'blah'
$(document).ready(function() {
    document.title = 'blah';
});

// Creates the slider
$(document).ready(function () {
    $(".js-range-slider").ionRangeSlider({
        onChange: function (data) {
            console.log(data.from);
            console.log(data.to);
            },
        type: "double",
        skin: "flat",
        min: 0,
        max: 1000,
    });
});