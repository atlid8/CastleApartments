function get_tax() {
    let price = document.getElementById("subtotal").innerHTML;
    return Math.round(Number(price) * 0.029).toString()
}

function get_total() {
    let price = document.getElementById("subtotal").innerHTML;
    let tax = Math.round(Number(price) * 0.029);
    return Math.round(tax + Number(price)).toString()
}
