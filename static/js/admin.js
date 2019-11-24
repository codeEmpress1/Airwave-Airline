var user_table = document.getElementById('allUsers');
var price_table = document.getElementById('pricelist');
var bookings_table = document.getElementById('bookings');
var historys = document.getElementById('bookingHistory');
var profile = document.getElementById('profile');
var prices = document.getElementById('prices');
// console.log(prices.value)
var user = document.querySelector('.userlanding');
var admin = document.querySelector('.adminlanding');
/*desc = document.querySelector('#desc');*/
function show(element) {
    element.style.display = "block";
}
function hide(element){
    element.style.display = "none";
}
// to displAY USER BLOCK
function display_user() {
    show(user);
    hide(admin);
}
// to display admin block
function display_admin() {
    show(admin);
    hide(user);
}
// for admin only
function show_users() {
    hide(price_table);
    hide(bookings_table);
    show(user_table);
}
function show_pricelist() {
    show(price_table);
    hide(bookings_table);
    hide(user_table);
 }
 function show_bookings() {
    hide(price_table);
    show(bookings_table);
    hide(user_table);
 }
//  for users only
function show_history() {
    show(historys);
    hide(prices);
    hide(profile);
}
function show_prices() {
    show(prices);
    hide(historys);
    hide(profile);
}
function show_profile() {
    show(profile);
    hide(historys);
    hide(prices);
}