

$(document).ready(function(){
    $('#zip-select').on("change", function(){
            $('#id_postcode').val($(this).val());
    });
});