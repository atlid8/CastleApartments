
function get_date() {
    let date = new Date();
    let year = date.getFullYear();
    let month = date.getMonth()+1;
    let day = date.getDate();

    if (month < 10) {
        month = "0" + month
    }

     if (day < 10) {
        day = "0" + day
    }

    return day + "/" + month + "/" + year
}

function get_tax() {
    let price = parseInt(document.getElementById("subtotal").value);
    return Math.round(Number(price) * 0.029).toString()
}

function get_total() {
    let price = parseInt(document.getElementById("subtotal").value);
    let tax = Math.round(Number(price) * 0.029).toString();
    return Math.round(tax + price).toString()
}

