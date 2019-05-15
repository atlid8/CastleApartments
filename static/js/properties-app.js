window.searchInput = ""

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
//$(document).ready(function () {
//    $(".price").ionRangeSlider({
//        onFinish: function (e) {
//            const minValue = e.from;
//            const upperValue = e.to;
//            console.log(minValue); //TODO: TENGJA RETT
//            console.log(upperValue);
//            $.ajax({
//                url: '/properties/search/?price-filter=' + minValue + ',' + upperValue,
//                type: 'GET',
//                success: function (resp) {
//                    var newHTML = resp.data.map(d => {
//                        return `
//                        <div class="col-md-3 well castles">
//                            <a href="/properties/${d.id}">
//                            <div class="card mb-4 box-shadow">
//                                <img class="card-img-top"  alt="Thumbnail [100%x225]" src='${d.image}'data-holder-rendered="true">
//                                <div class="card-body">
//                                    <h1 class="card-text" id="castle-name"> ${d.name}</h1>
//                                    <p class="card-text" id="castle-info ">${d.info}</p>
//                                    <p class="card-text">Price: ${d.price}</p>
//                                    <p class="card-text">Size: ${ d.size }</p>
//                                </div>
//                            </div>
//                            </a>
//                        </div>`;
//                    });
//                    $('.castles').html(newHTML.join(''));
//                },
//                error: function (xhr, status, error) {
//                    //Todo: gæti þurft eitthvað annað error handling
//                    console.error(error);
//                },
//            })
//        },
//
//        type: "double",
//        skin: "flat",
//        min: 0,
//        max: 100000,
//})
//
//});

// $(document).ready(function () {
//     $(".square-meters").ionRangeSlider({
//         onFinish: function (e) {
//             var minValue = e.from;
//             var upperValue = e.to;
//             let slider = $("#square-slider").val()
//             console.log(minValue); //TODO: TENGJA RETT
//             console.log(upperValue);
//             $.ajax({
//                 url: '/properties/search/?square-filter=' + minValue + ',' + upperValue,
//                 type: 'GET',
//                 success: function (resp) {
//                     var newHTML = resp.data.map(d => {
//                         return `
//                         <div class="col-md-3 well castles">
//                             <a href="/properties/${d.id}">
//                             <div class="card mb-4 box-shadow">
//                                 <img class="card-img-top"  alt="Thumbnail [100%x225]" src='${d.image}'data-holder-rendered="true">
//                                 <div class="card-body">
//                                     <h1 class="card-text" id="castle-name"> ${d.name}</h1>
//                                     <p class="card-text" id="castle-info ">${d.info}</p>
//                                     <p class="card-text">Price: ${ d.price }</p>
//                                     <p class="card-text">Size: ${ d.size }</p>
//                                 </div>
//                             </div>
//                             </a>
//                         </div>`;
//                     });
//                     $('.castles').html(newHTML.join(''));
//                 },
//                 error: function (xhr, status, error) {
//                     //Todo: gæti þurft eitthvað annað error handling
//                     console.error(error);
//                 },
//             })
//         },
//
//         type: "double",
//         skin: "flat",
//         min: 0,
//         max: 15000,
// })
//
// });

$(document).ready(function () {
    $(".js-range-slider").ionRangeSlider({
        onFinish: function (e) {
            let room_range = $('#room-slider').val().split(';');
            let searchText = searchInput;
            let price_range = $('#price-slider').val().split(';');
            let square_range = $('#square-slider').val().split(';');
            let order_by = $('#orderdropdown').val();
            let zip_code = $('#zip-dropdown').val();
            let zip_filter = '&postcode='
            let search_check = '&search-filter='
            if (order_by !== null) {
                order_by = $('#orderdropdown').val();
            } else {
                order_by = 'name'
            }
            if (zip_code !== "") {
                zip_code = $('#zip-dropdown').val();
            } else {
                zip_filter = ""
            }
            if (searchInput !== "") {
                searchInput = searchInput
            } else {
                search_check = ""
            }
            $.ajax({
                url: '/properties/search/?price-filter=' + price_range[0] + ',' + price_range[1] + search_check +  searchInput + '&room-filter=' + room_range[0] + ',' + room_range[1] + '&square-filter=' + square_range[0] + ',' + square_range[1] + '&order=' + order_by + zip_filter + zip_code,
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
        let price_range = $('#price-slider').val().split(';');
        let room_range = $('#room-slider').val().split(';');
        let square_range = $('#square-slider').val().split(';');
        let order_by = $('#orderdropdown').val();
        let zip_code = $('#zip-dropdown').val();
        let zip_filter = '&postcode='
        if (order_by !== null) {
            order_by = $('#orderdropdown').val();
        } else {
            order_by = 'name'
        }
        if (zip_code !== "") {
            zip_code = $('#zip-dropdown').val();
        } else {
            zip_filter = ""
        }
        $.ajax({
            url: '/properties/search/?search-filter=' + searchText + '&price-filter=' + price_range[0] + ',' + price_range[1] + '&room-filter=' + room_range[0] + ',' + room_range[1] + '&square-filter=' + square_range[0] + ',' + square_range[1] + '&order=' + order_by + zip_filter + zip_code,
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
                window.searchInput = searchText
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
    $('.dropdown_search').on('change', function (e) {
        e.preventDefault();
        let room_range = $('#room-slider').val().split(';');
        let searchText = searchInput;
        let price_range = $('#price-slider').val().split(';');
        let square_range = $('#square-slider').val().split(';');
        let order_by = $('#orderdropdown').val();
        let order_filter = '&order='
        let zip_code = $('#zip-dropdown').val();
        let zip_filter = '&postcode='
        let search_check = '&search-filter='
        console.log()
        if (order_by !== null) {
            order_by = $('#orderdropdown').val();
        } else {
            order_filter = ""
            order_by= ""
        }
        if (zip_code !== "") {
            zip_code = $('#zip-dropdown').val();
        } else {
            zip_filter = ""
        }
        if (searchInput !== "") {
            searchInput = searchInput
        } else {
            search_check = ""
        }
        $.ajax({
            url: '/properties/search/?price-filter=' + price_range[0] + ',' + price_range[1] + search_check +  searchInput + '&room-filter=' + room_range[0] + ',' + room_range[1] + '&square-filter=' + square_range[0] + ',' + square_range[1] + order_filter + order_by + zip_filter + zip_code,
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
//
//
// $(document).ready(function () {
//     $('#zip-dropdown').on('change', function (e) {
//         e.preventDefault();
//         var zip = $('#zip-dropdown').val();
//         $.ajax({
//             url: '/properties/search/?postcode=' + zip,
//             type: 'GET',
//             success: function (resp) {
//                 var newHTML = resp.data.map(d => {
//                     return `
//                     <div class="col-md-3 well castles">
//                             <a href="/properties/${d.id}">
//                             <div class="card mb-4 box-shadow">
//                                 <img class="card-img-top"  alt="Thumbnail [100%x225]" src='${d.image}'data-holder-rendered="true">
//                                 <div class="card-body">
//                                     <h1 class="card-text" id="castle-name"> ${d.name}</h1>
//                                     <p class="card-text" id="castle-info ">${d.info}</p>
//                                     <p class="card-text">Price: ${d.price}</p>
//                                     <p class="card-text">Size: ${ d.size }</p>
//                             </div>
//                         </div>
//                         </a>
//                     </div>`
//                 });
//                 $('.castles').html(newHTML.join(''))
//             },
//             error: function (xhr, status, error) {
//                 //Todo: gæti þurft eitthvað annað error handling
//                 console.error(error);
//             }
//         })
//     })
//
// });
//