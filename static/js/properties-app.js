$(function() {
    // #TODO: Mögulega finna betri leið? brennur upp ram
    $(window).on('resize', function() {
        const x = $(this).width();
        if (x < 769 && x > 600) {
            $('#square-meters').html('M<sup>2</sup>');
        }
        else {
            $('#square-meters').html('Square meters');
        }
    });
});




// Creates the slider
$(document).ready(function () {
    $(".price").ionRangeSlider({
        onFinish: function (e) {
            const minValue = e.from;
            const upperValue = e.to;
            console.log(minValue); //TODO: TENGJA RETT
            console.log(upperValue);
            $.ajax({
                url: '/properties/search/?price-filter=' + minValue + ',' + upperValue,
                type: 'GET',
                success: function (resp) {
                    var newHTML = resp.data.map(d => {
                        return `
                        <div class="col-md-3 well castles">
                            <a href="/properties/${d.id}">
                            <div class="card mb-4 box-shadow">
                                <img class="card-img-top"  alt="Thumbnail [100%x225]" src='${d.image}'data-holder-rendered="true">
                                <div class="card-body">
                                    <h1 class="card-text" id="castle-name"> ${d.name}</h1>
                                    <p class="card-text" id="castle-info ">${d.info}</p>
                                    <p class="card-text">Price: ${d.price}</p>
                                    <p class="card-text">Size: ${ d.size }</p>
                                </div>
                            </div>
                            </a>
                        </div>`;
                    });
                    $('.castles').html(newHTML.join(''));
                },
                error: function (xhr, status, error) {
                    //Todo: gæti þurft eitthvað annað error handling
                    console.error(error);
                },
            })
        },

        type: "double",
        skin: "flat",
        min: 0,
        max: 100000,
})

});

$(document).ready(function () {
    $(".square-meters").ionRangeSlider({
        onFinish: function (e) {
            var minValue = e.from;
            var upperValue = e.to;
            let slider = $("#square-slider").val()
            console.log(minValue); //TODO: TENGJA RETT
            console.log(upperValue);
            $.ajax({
                url: '/properties/search/?square-filter=' + slider,
                type: 'GET',
                success: function (resp) {
                    var newHTML = resp.data.map(d => {
                        return `
                        <div class="col-md-3 well castles">
                            <a href="/properties/${d.id}">
                            <div class="card mb-4 box-shadow">
                                <img class="card-img-top"  alt="Thumbnail [100%x225]" src='${d.image}'data-holder-rendered="true">
                                <div class="card-body">
                                    <h1 class="card-text" id="castle-name"> ${d.name}</h1>
                                    <p class="card-text" id="castle-info ">${d.info}</p>
                                    <p class="card-text">Price: ${ d.price }</p>
                                    <p class="card-text">Size: ${ d.size }</p>
                                </div>
                            </div>
                            </a>
                        </div>`;
                    });
                    $('.castles').html(newHTML.join(''));
                },
                error: function (xhr, status, error) {
                    //Todo: gæti þurft eitthvað annað error handling
                    console.error(error);
                },
            })
        },

        type: "double",
        skin: "flat",
        min: 0,
        max: 15000,
})

});

$(document).ready(function () {
    $(".rooms").ionRangeSlider({
        onFinish: function (e) {
            var minValue = e.from;
            var upperValue = e.to;
            let slider = $("#room-slider").val()
            console.log(minValue); //TODO: TENGJA RETT
            console.log(upperValue);
            $.ajax({
                url: '/properties/search/?room-filter=' + slider,
                type: 'GET',
                success: function (resp) {
                    var newHTML = resp.data.map(d => {
                        return `
                        <div class="col-md-3 well castles">
                            <a href="/properties/${d.id}">
                            <div class="card mb-4 box-shadow">
                                <img class="card-img-top"  alt="Thumbnail [100%x225]" src='${d.image}'data-holder-rendered="true">
                                <div class="card-body">
                                    <h1 class="card-text" id="castle-name"> ${d.name}</h1>
                                    <p class="card-text" id="castle-info ">${d.info}</p>
                                    <p class="card-text">Price: ${d.price}</p>
                                    <p class="card-text">Size: ${ d.size }</p>
                                </div>
                            </div>
                            </a>
                        </div>`;
                    });
                    $('.castles').html(newHTML.join(''));
                },
                error: function (xhr, status, error) {
                    //Todo: gæti þurft eitthvað annað error handling
                    console.error(error);
                },
            })
        },

        type: "double",
        skin: "flat",
        min: 0,
        max: 50,
})

});




$(document).ready(function () {
    $('#search-btn').on('click', function (e) {
        e.preventDefault();
        let searchText = $('#search-box').val();
        let price_range = $('#price-slider').val().split(';')
        let room_range = $('#room-slider').val().split(';')
        let square_range = $('#square-slider').val().split(';')
        console.log(price_range)
        $.ajax({
            url: '/properties/search/?search-filter=' + searchText + '&price-filter=' + price_range[0] + ',' + price_range[1] + '&room-filter=' + room_range[0] + ',' + room_range[1] + '&square-filter=' + square_range[0] + ',' + square_range[1],
            type: 'GET',
            success: function (resp) {
                var newHTML = resp.data.map(d => {
                    return `
                    <div class="col-md-3 well castles">
                            <a href="/properties/${d.id}">
                            <div class="card mb-4 box-shadow">
                                <img class="card-img-top"  alt="Thumbnail [100%x225]" src='${d.image}'data-holder-rendered="true">
                                <div class="card-body">
                                    <h1 class="card-text" id="castle-name"> ${d.name}</h1>
                                    <p class="card-text" id="castle-info ">${d.info}</p>
                                    <p class="card-text">Price: ${d.price}</p>
                                    <p class="card-text">Size: ${ d.size }</p>
                            </div>
                        </div>
                        </a>
                    </div>`
                });
                console.log(searchText);
                $('.castles').html(newHTML.join(''));
                $('#search-box').val('');
            },
            error: function (xhr, status, error) {
                //Todo: gæti þurft eitthvað annað error handling
                console.error(error);
            }
        })
    })

});

//<img class="card-img-top"  alt="Thumbnail [100%x225]" src='${d.image_set.first()}'data-holder-rendered="true">

$(document).ready(function () {
    $('#orderdropdown').on('change', function (e) {
        e.preventDefault();
        var order = $('#orderdropdown').val();
        $.ajax({
            url: '/properties/search/?order=' + order,
            type: 'GET',
            success: function (resp) {
                var newHTML = resp.data.map(d => {
                    return `
                    <div class="col-md-3 well castles">
                            <a href="/properties/${d.id}">
                            <div class="card mb-4 box-shadow">
                                <img class="card-img-top"  alt="Thumbnail [100%x225]" src='${d.image}'data-holder-rendered="true">
                                <div class="card-body">
                                    <h1 class="card-text" id="castle-name"> ${d.name}</h1>
                                    <p class="card-text" id="castle-info ">${d.info}</p>
                                    <p class="card-text">Price: ${d.price}</p>
                                    <p class="card-text">Size: ${ d.size }</p>
                            </div>
                        </div>
                        </a>
                    </div>`
                });
                $('.castles').html(newHTML.join(''))
            },
            error: function (xhr, status, error) {
                //Todo: gæti þurft eitthvað annað error handling
                console.error(error);
            }
        })
    })

});


$(document).ready(function () {
    $('#zip-dropdown').on('change', function (e) {
        e.preventDefault();
        var zip = $('#zip-dropdown').val();
        console.log("slider: ", slider);

        $.ajax({
            url: '/properties/search/?postcode=' + zip,
            type: 'GET',
            success: function (resp) {
                var newHTML = resp.data.map(d => {
                    return `
                    <div class="col-md-3 well castles">
                            <a href="/properties/${d.id}">
                            <div class="card mb-4 box-shadow">
                                <img class="card-img-top"  alt="Thumbnail [100%x225]" src='${d.image}'data-holder-rendered="true">
                                <div class="card-body">
                                    <h1 class="card-text" id="castle-name"> ${d.name}</h1>
                                    <p class="card-text" id="castle-info ">${d.info}</p>
                                    <p class="card-text">Price: ${d.price}</p>
                                    <p class="card-text">Size: ${ d.size }</p>
                            </div>
                        </div>
                        </a>
                    </div>`
                });
                $('.castles').html(newHTML.join(''))
            },
            error: function (xhr, status, error) {
                //Todo: gæti þurft eitthvað annað error handling
                console.error(error);
            }
        })
    })

});
