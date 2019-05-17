$(document).ready(function(){
    $('#id_postcode').on("change", function(){
        if($(this).val()==101){
            $('#kingdom-div').val("King's Landing");
        }
        else if($(this).val()==201){
            $('#kingdom-div').val("The Stormlands");
        }
        else if($(this).val()==210){
            $('#kingdom-div').val("Westerlands");
        }
       else if($(this).val()==301){
            $('#kingdom-div').val("The Riverlands");
        }
        else if($(this).val()==401){
            $('#kingdom-div').val("Dorne");
        }
        else if($(this).val()==501){
            $('#kingdom-div').val("The North");
        }
    });
});