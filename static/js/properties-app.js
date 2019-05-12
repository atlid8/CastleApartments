// Changes title to 'blah'
// $(document).ready(function() {
//     document.title = 'blah';
// });

// Creates the slider
$(document).ready(function () {
    $(".js-range-slider").ionRangeSlider({
        onChange: function (data) {
            // console.log(data.from); #TODO: TENGJA RETT
            // console.log(data.to);
            },
        type: "double",
        skin: "flat",
        min: 0,
        max: 1000,
    });
});
$(document).ready(function () {
    $('#search-btn').on('click', function (e) {
        e.preventDefault();
        var searchText = $('#search-box').val();
        $.ajax({
            url: '/properties/search/?search-filter=' + searchText,
            type: 'GET',
            success: function (resp) {
                var newHTML = resp.data.map(d => {
                    return `
                    <div class="well castles">
                        <a href="/properties/${d.id}">
                            <img src='${d.firstimage}'>
                            <h4> ${d.name}</h4>
                            <p> ${d.info}</p>
                        </a>
                    </div>`
                });
                $('.castles').html(newHTML.join(''))
                $('#search-box').val('')
            },
            error: function (xhr, status, error) {
                //Todo: gæti þurft eitthvað annað errorr handling
                console.error(error);
            }
        })
    })

})