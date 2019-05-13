

$(document).ready(function(){
    $('#kingdom-select').on("change", function(){
            $('#id_postcode').val($(this).val());
    });
});