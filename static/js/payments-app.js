// function get_date() {
//     let date = new Date();
//     let year = date.getFullYear();
//     let month = date.getMonth()+1;
//     let day = date.getDate();
//
//     if (month < 10) {
//         month = "0" + month
//     }
//
//      if (day < 10) {
//         day = "0" + day
//     }
//
//     return day + "/" + month + "/" + year
// }

function get_tax() {
    let price = document.getElementById("subtotal").innerHTML;
    return Math.round(Number(price) * 0.029).toString()
}

function get_total() {
    let price = document.getElementById("subtotal").innerHTML;
    let tax = Math.round(Number(price) * 0.029);
    return Math.round(tax + Number(price)).toString()
}

